"""
Project Avatar: Leptospirosis Risk Prediction Engine.
Dual-head gradient boosted decision tree implementation using LightGBM:
1. Surge Classifier: LightGBM Binary Classifier with empirical scale_pos_weight = 7.67.
2. Case Volume Regressor: LightGBM Tweedie Regressor (variance power p = 1.45) for zero-inflated skewness.
3. TreeSHAP Explainer: Computes local feature attribution watermarks.
4. RA 10173 Statutory Compliance: Enforces k-anonymity (k >= 5) small cell suppression.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Any
import numpy as np
import pandas as pd
import lightgbm as lgb
import shap

from src.utils.seed import GLOBAL_SEED, set_seed
from src.api_contracts import (
    LGUName,
    RiskTier,
    LeptospirosisLguPrediction,
)

set_seed(GLOBAL_SEED)

DEFAULT_LEPTO_FEATURES: List[str] = [
    "rainfall_lag_1w",
    "rainfall_lag_2w",
    "rainfall_lag_3w",
    "rainfall_lag_4w",
    "soil_moisture_lag_2w",
    "cumulative_rainfall_2w_to_4w",
    "pm25_rolling_4w",
    "uhi_anomaly",
    "elev_m",
    "slope_pct",
    "twi",
    "population",
]


class LeptospirosisRiskEngine:
    """
    Anticipatory Leptospirosis Risk Engine for Metro Manila LGUs.
    Integrates LightGBM Dual-Head model with TreeSHAP local interpretability.
    """

    def __init__(
        self,
        features: Optional[List[str]] = None,
        scale_pos_weight: float = 7.67,
        tweedie_variance_power: float = 1.45,
        random_state: int = GLOBAL_SEED,
    ):
        """
        Initializes the dual-head risk engine.

        Args:
            features: List of predictor feature column names.
            scale_pos_weight: LightGBM weight for positive surge class (EDA ratio: 7.67).
            tweedie_variance_power: Compound Poisson-Gamma power parameter (default: 1.45).
            random_state: Universal random seed for deterministic tree generation.
        """
        self.features = features or list(DEFAULT_LEPTO_FEATURES)
        self.scale_pos_weight = scale_pos_weight
        self.tweedie_variance_power = tweedie_variance_power
        self.random_state = random_state

        self.classifier: Optional[lgb.LGBMClassifier] = None
        self.regressor: Optional[lgb.LGBMRegressor] = None
        self.explainer: Optional[shap.TreeExplainer] = None
        self.is_fitted: bool = False

    def train(
        self,
        df: pd.DataFrame,
        target_classifier_col: str = "outbreak_surge_target",
        target_regressor_col: str = "reported_cases",
    ) -> Dict[str, float]:
        """
        Trains both classifier and regressor heads on historical epidemiological data.

        Args:
            df: Historical analysis matrix DataFrame.
            target_classifier_col: Binary outbreak surge column name.
            target_regressor_col: Weekly reported count column name.

        Returns:
            Dictionary of training summary metrics.
        """
        data = df.copy()

        # Ensure cumulative rainfall column is computed
        if "cumulative_rainfall_2w_to_4w" not in data.columns:
            data["cumulative_rainfall_2w_to_4w"] = (
                data["rainfall_lag_2w"] + data["rainfall_lag_3w"] + data["rainfall_lag_4w"]
            )

        X = data[self.features].copy()
        y_clf = data[target_classifier_col].astype(int)
        y_reg = data[target_regressor_col].astype(float)

        # 1. Surge Classification Head
        self.classifier = lgb.LGBMClassifier(
            objective="binary",
            scale_pos_weight=self.scale_pos_weight,
            learning_rate=0.05,
            n_estimators=120,
            max_depth=5,
            num_leaves=24,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=self.random_state,
            verbosity=-1,
        )
        self.classifier.fit(X, y_clf)

        # 2. Tweedie Count Regression Head
        self.regressor = lgb.LGBMRegressor(
            objective="tweedie",
            tweedie_variance_power=self.tweedie_variance_power,
            learning_rate=0.04,
            n_estimators=100,
            max_depth=4,
            num_leaves=16,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=self.random_state,
            verbosity=-1,
        )
        self.regressor.fit(X, y_reg)

        # 3. Initialize TreeSHAP Explainer over classifier head
        self.explainer = shap.TreeExplainer(self.classifier.booster_)
        self.is_fitted = True

        clf_preds = self.classifier.predict_proba(X)[:, 1]
        reg_preds = self.regressor.predict(X)

        return {
            "n_samples": float(len(X)),
            "mean_surge_probability": float(np.mean(clf_preds)),
            "mean_predicted_cases": float(np.mean(reg_preds)),
            "scale_pos_weight": float(self.scale_pos_weight),
        }

    def predict_lgu(
        self,
        lgu_feature_row: Dict[str, Any],
        lgu_id: str = "PH130000000",
        epi_week: int = 40,
        year: int = 2024,
    ) -> LeptospirosisLguPrediction:
        """
        Executes dual-head prediction and TreeSHAP attribution for a single municipal observation.
        Enforces RA 10173 statutory small cell suppression.

        Args:
            lgu_feature_row: Dictionary of feature key-values.
            lgu_id: PSGC municipal identifier.
            epi_week: Target Epidemiological Week number.
            year: Target surveillance year.

        Returns:
            Validated LeptospirosisLguPrediction Pydantic instance.
        """
        if not self.is_fitted or self.classifier is None or self.regressor is None:
            raise RuntimeError("LeptospirosisRiskEngine must be trained before inference.")

        # Ensure cumulative rainfall is present
        if "cumulative_rainfall_2w_to_4w" not in lgu_feature_row:
            lgu_feature_row["cumulative_rainfall_2w_to_4w"] = (
                float(lgu_feature_row.get("rainfall_lag_2w", 0.0))
                + float(lgu_feature_row.get("rainfall_lag_3w", 0.0))
                + float(lgu_feature_row.get("rainfall_lag_4w", 0.0))
            )

        # Build single-row DataFrame with aligned features
        x_vec = pd.DataFrame([{f: float(lgu_feature_row.get(f, 0.0)) for f in self.features}])

        # Probability and Tweedie point estimate
        surge_prob = float(self.classifier.predict_proba(x_vec)[0, 1])
        predicted_cases = float(np.maximum(0.0, self.regressor.predict(x_vec)[0]))

        # Categorical Risk Tier mapping
        if surge_prob < 0.25:
            risk_tier = RiskTier.LOW
        elif surge_prob < 0.50:
            risk_tier = RiskTier.MODERATE
        elif surge_prob < 0.75:
            risk_tier = RiskTier.HIGH
        else:
            risk_tier = RiskTier.CRITICAL

        # RA 10173 Small Cell Suppression
        if 1.0 <= predicted_cases < 5.0:
            suppressed_display = "<5"
            is_suppressed = True
        else:
            suppressed_display = f"{predicted_cases:.1f}"
            is_suppressed = False

        # TreeSHAP feature attributions
        raw_shap = self.explainer.shap_values(x_vec)
        # Handle SHAP output format (binary clf may return array of shape (1, n_features) or list of 2 arrays)
        if isinstance(raw_shap, list):
            sample_shap = np.abs(raw_shap[1][0])
        elif raw_shap.ndim == 3:
            sample_shap = np.abs(raw_shap[0, :, 1])
        else:
            sample_shap = np.abs(raw_shap[0])

        shap_total = float(np.sum(sample_shap))
        if shap_total > 1e-6:
            shap_norm = {self.features[i]: float(sample_shap[i] / shap_total) for i in range(len(self.features))}
        else:
            shap_norm = {f: 1.0 / len(self.features) for f in self.features}

        # Select top 5 drivers sorted by magnitude
        sorted_drivers = dict(sorted(shap_norm.items(), key=lambda kv: kv[1], reverse=True)[:5])

        # Validate LGU Name enum
        raw_lgu_name = str(lgu_feature_row.get("lgu_name", "City of Manila"))
        try:
            valid_lgu_name = LGUName(raw_lgu_name)
        except ValueError:
            # Fallback matching
            matches = [
                m for m in LGUName
                if m.value.lower() in raw_lgu_name.lower() or raw_lgu_name.lower() in m.value.lower()
            ]
            valid_lgu_name = matches[0] if matches else LGUName.MANILA

        return LeptospirosisLguPrediction(
            lgu_id=lgu_id,
            lgu_name=valid_lgu_name,
            epi_week=epi_week,
            year=year,
            outbreak_surge_probability=round(surge_prob, 4),
            risk_tier=risk_tier,
            predicted_cases_tweedie=round(predicted_cases, 2),
            suppressed_case_display=suppressed_display,
            is_suppressed=is_suppressed,
            top_shap_drivers=sorted_drivers,
        )

    def predict_ncr_all(
        self,
        muni_df: pd.DataFrame,
        epi_week: int,
        year: int,
    ) -> List[LeptospirosisLguPrediction]:
        """
        Generates predictions for all 17 Metro Manila LGUs for a specific epidemiological week.
        """
        subset = muni_df[(muni_df["epi_week"] == epi_week) & (muni_df["year"] == year)]
        if subset.empty:
            # If specific week not found, use latest week
            subset = muni_df.sort_values(by=["year", "epi_week"]).groupby("lgu_name").last().reset_index()

        predictions: List[LeptospirosisLguPrediction] = []
        for _, row in subset.iterrows():
            row_dict = row.to_dict()
            pred = self.predict_lgu(
                lgu_feature_row=row_dict,
                lgu_id=str(row_dict.get("lgu_id", "PH130000000")),
                epi_week=epi_week,
                year=year,
            )
            predictions.append(pred)

        return predictions
