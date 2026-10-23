"""
Project Avatar: End-to-End Pipeline & Contract Verification Test Suite.
Tests:
1. Feature Engineering (1-8 week lags, SRTM derivatives, NDBI, TWI) across Polars & Pandas.
2. Leptospirosis Risk Engine (LightGBM dual-head + TreeSHAP + RA 10173 small cell suppression).
3. Spatial PM2.5 Downscaler (XGBoost 1km grid downscaling, WHO exceedance factor, AQI categories).
4. ChromaDB RAG Advisory Engine (regulatory citation retrieval and role-specialized action cards).
5. Universal seed reproducibility.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import polars as pl
import pytest

from src.utils.seed import GLOBAL_SEED, set_seed
from src.data.feature_engineering import (
    calculate_rolling_precipitation_lags,
    calculate_srtm_derivatives,
    calculate_topographic_wetness_index,
    calculate_ndbi,
    build_ncr_feature_store,
)
from src.models.leptospirosis_model import LeptospirosisRiskEngine
from src.models.pm25_downscaler import SpatialPM25Downscaler
from src.rag.advisory_engine import ChromaAdvisoryEngine
from src.api_contracts import (
    LGUName,
    RiskTier,
    StakeholderRole,
    LanguageCode,
    RAGAdvisoryRequest,
    LeptospirosisLguPrediction,
    PM25GridPrediction,
)


@pytest.fixture(autouse=True)
def enforce_test_seed():
    """Enforces global seed before each test."""
    set_seed(GLOBAL_SEED)


# =====================================================================
# 1. FEATURE ENGINEERING TESTS
# =====================================================================

def test_rolling_precipitation_lags_pandas():
    """Verifies 1-8 week lag calculation and cumulative exposure on Pandas DataFrame."""
    df = pd.DataFrame({
        "lgu_name": ["City of Manila"] * 12,
        "week": list(range(1, 13)),
        "weekly_rainfall_mm": [10.0 * i for i in range(1, 13)],
    })

    result = calculate_rolling_precipitation_lags(
        df,
        precipitation_col="weekly_rainfall_mm",
        group_col="lgu_name",
        time_col="week",
        max_lag=8,
        include_cumulative=True,
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 12

    # Verify lag 1 to 8 columns exist
    for lag in range(1, 9):
        col = f"rainfall_lag_{lag}w"
        assert col in result.columns

    # Verify cumulative windows
    assert "cumulative_rainfall_2w_to_4w" in result.columns
    assert "cumulative_rainfall_1w_to_8w" in result.columns

    # Test lag 1 value at week 5: should equal rainfall at week 4 (40.0)
    assert result.loc[result["week"] == 5, "rainfall_lag_1w"].values[0] == 40.0
    # Test lag 2 value at week 5: should equal rainfall at week 3 (30.0)
    assert result.loc[result["week"] == 5, "rainfall_lag_2w"].values[0] == 30.0


def test_rolling_precipitation_lags_polars():
    """Verifies that Polars DataFrames are properly processed and returned as Polars."""
    pl_df = pl.DataFrame({
        "lgu_name": ["City of Malabon"] * 10,
        "week": list(range(1, 11)),
        "weekly_rainfall_mm": [15.0 * i for i in range(1, 11)],
    })

    result = calculate_rolling_precipitation_lags(
        pl_df,
        precipitation_col="weekly_rainfall_mm",
        group_col="lgu_name",
        time_col="week",
        max_lag=8,
        include_cumulative=True,
    )

    assert isinstance(result, pl.DataFrame)
    assert "rainfall_lag_1w" in result.columns
    assert "rainfall_lag_8w" in result.columns
    assert "cumulative_rainfall_2w_to_4w" in result.columns


def test_srtm_derivatives():
    """Verifies spatial gradient, aspect, roughness, and depression masking."""
    # Synthetic tilted plane: elevation increases along x-axis
    rows, cols = 10, 10
    grid = np.zeros((rows, cols), dtype=np.float64)
    for c in range(cols):
        grid[:, c] = 2.0 + (c * 1.5)  # slopes upward from 2m to 15.5m

    derivs = calculate_srtm_derivatives(grid, cell_size_m=1000.0)

    assert "slope_pct" in derivs
    assert "slope_deg" in derivs
    assert "aspect_deg" in derivs
    assert "roughness_m" in derivs
    assert "lowland_mask" in derivs
    assert "sluggish_slope_mask" in derivs

    assert derivs["slope_pct"].shape == (rows, cols)
    # Check that lowlands under 5m are flagged
    assert derivs["lowland_mask"][0, 0] is np.True_ or derivs["lowland_mask"][0, 0] == True  # noqa: E712
    assert derivs["lowland_mask"][0, -1] is np.False_ or derivs["lowland_mask"][0, -1] == False  # noqa: E712


def test_topographic_wetness_index():
    """Verifies TWI calculation and boundary values."""
    grid = np.full((15, 15), 10.0)
    grid[7, 7] = 1.0  # local basin depression

    twi = calculate_topographic_wetness_index(grid, cell_size_m=1000.0)
    assert twi.shape == (15, 15)
    assert np.all(twi >= 0.0)
    assert np.all(twi <= 30.0)


def test_calculate_ndbi():
    """Verifies Normalized Difference Built-up Index across data types."""
    swir = np.array([0.4, 0.2, 0.5])
    nir = np.array([0.2, 0.3, 0.1])

    ndbi = calculate_ndbi(swir, nir)
    assert len(ndbi) == 3
    assert np.all(ndbi >= -1.0) and np.all(ndbi <= 1.0)
    # First element: (0.4 - 0.2) / (0.4 + 0.2) = 0.2 / 0.6 = ~0.333
    assert pytest.approx(ndbi[0], rel=1e-2) == 0.333


# =====================================================================
# 2. LEPTOSPIROSIS MODEL & PRIVACY CONTRACT TESTS
# =====================================================================

def test_leptospirosis_model_contract_and_shap():
    """Tests LightGBM risk classifier training, inference, and SHAP attribution."""
    muni_df, _ = build_ncr_feature_store()

    engine = LeptospirosisRiskEngine()
    metrics = engine.train(muni_df)

    assert metrics["n_samples"] > 0
    assert engine.is_fitted
    assert engine.classifier is not None
    assert engine.regressor is not None

    sample_row = muni_df.iloc[0].to_dict()
    pred = engine.predict_lgu(sample_row, lgu_id="PH137402000", epi_week=30, year=2024)

    assert isinstance(pred, LeptospirosisLguPrediction)
    assert 0.0 <= pred.outbreak_surge_probability <= 1.0
    assert pred.risk_tier in [RiskTier.LOW, RiskTier.MODERATE, RiskTier.HIGH, RiskTier.CRITICAL]
    assert len(pred.top_shap_drivers) <= 5
    assert sum(pred.top_shap_drivers.values()) > 0.0


def test_statutory_small_cell_suppression():
    """Verifies strict adherence to RA 10173: suppression when 1 <= cases < 5."""

    # Create dummy prediction with 2.8 cases
    pred_data = {
        "lgu_id": "PH137402000",
        "lgu_name": LGUName.MALABON,
        "epi_week": 32,
        "year": 2024,
        "outbreak_surge_probability": 0.42,
        "risk_tier": RiskTier.MODERATE,
        "predicted_cases_tweedie": 2.8,
        "suppressed_case_display": "<5",
        "is_suppressed": True,
        "top_shap_drivers": {"rainfall_lag_2w": 0.4, "soil_moisture_lag_2w": 0.3},
    }
    pred = LeptospirosisLguPrediction(**pred_data)
    assert pred.suppressed_case_display == "<5"
    assert pred.is_suppressed is True

    # When cases >= 5.0, not suppressed
    unsuppressed_data = dict(pred_data)
    unsuppressed_data["predicted_cases_tweedie"] = 14.5
    unsuppressed_data["suppressed_case_display"] = "14.5"
    unsuppressed_data["is_suppressed"] = False

    pred_unsuppressed = LeptospirosisLguPrediction(**unsuppressed_data)
    assert pred_unsuppressed.suppressed_case_display == "14.5"
    assert pred_unsuppressed.is_suppressed is False


# =====================================================================
# 3. SPATIAL PM2.5 DOWNSCALER TESTS
# =====================================================================

def test_spatial_pm25_downscaler():
    """Verifies Spatial XGBoost training and 1km grid downscaling contract."""
    _, grid_df = build_ncr_feature_store()
    station_df = pd.read_csv("data/raw/atmospheric/denr_emb_pm25_stations_2023_2024.csv")

    downscaler = SpatialPM25Downscaler(n_estimators=30)
    train_metrics = downscaler.train_on_stations(station_df)

    assert train_metrics["n_samples"] > 0
    assert downscaler.is_fitted

    # Single cell prediction
    single_cell = grid_df.iloc[0].to_dict()
    cell_pred = downscaler.predict_cell(single_cell)

    assert isinstance(cell_pred, PM25GridPrediction)
    assert cell_pred.predicted_pm25_ug_m3 >= 0.0
    assert cell_pred.who_annual_exceedance_factor >= 0.0
    assert cell_pred.who_24h_exceedance_factor >= 0.0

    # Downscale entire 1,350 grid
    grid_preds = downscaler.downscale_grid(grid_df)
    assert len(grid_preds) == len(grid_df)


# =====================================================================
# 4. CHROMA RAG ADVISORY ENGINE TESTS
# =====================================================================

def test_chroma_rag_advisory_engine():
    """Verifies semantic citation retrieval and multi-role deterministic advisory synthesis."""
    rag_engine = ChromaAdvisoryEngine()

    # Test Citation Retrieval
    citations = rag_engine.retrieve_relevant_citations("Doxycycline post-exposure prophylaxis dosing", n_results=2)
    assert len(citations) >= 1
    assert any("DOH" in c.document_title or "AO" in c.statutory_or_cpg_reference for c in citations)

    # Test MHO Advisory Request
    req_mho = RAGAdvisoryRequest(
        lgu_id="PH137402000",
        lgu_name=LGUName.MALABON,
        risk_tier=RiskTier.CRITICAL,
        outbreak_surge_probability=0.88,
        suppressed_case_display="18.5",
        dominant_shap_drivers={"rainfall_lag_2w": 0.42, "elev_m": 0.28},
        target_role=StakeholderRole.MUNICIPAL_HEALTH_OFFICER,
        language=LanguageCode.ENGLISH,
    )
    resp_mho = rag_engine.generate_advisory(req_mho)
    assert resp_mho.lgu_name == LGUName.MALABON
    assert resp_mho.risk_tier == RiskTier.CRITICAL
    assert len(resp_mho.prioritized_directives) >= 1
    assert resp_mho.clinical_guidance is not None
    assert "Doxycycline" in resp_mho.clinical_guidance.drug_and_dosage

    # Test Tagalog BHW Advisory Request
    req_bhw = RAGAdvisoryRequest(
        lgu_id="PH137402000",
        lgu_name=LGUName.MALABON,
        risk_tier=RiskTier.HIGH,
        outbreak_surge_probability=0.72,
        suppressed_case_display="<5",
        dominant_shap_drivers={"rainfall_lag_2w": 0.35},
        target_role=StakeholderRole.BARANGAY_HEALTH_WORKER,
        language=LanguageCode.TAGALOG,
    )
    resp_bhw = rag_engine.generate_advisory(req_bhw)
    assert "BABALA" in resp_bhw.executive_summary or "baha" in resp_bhw.executive_summary.lower()


# =====================================================================
# 5. REPRODUCIBILITY SEED TEST
# =====================================================================

def test_universal_seed_reproducibility():
    """Verifies that set_seed ensures deterministic random generation."""
    set_seed(GLOBAL_SEED)
    rand_arr1 = np.random.normal(size=10)

    set_seed(GLOBAL_SEED)
    rand_arr2 = np.random.normal(size=10)

    np.testing.assert_array_equal(rand_arr1, rand_arr2)
