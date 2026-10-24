"""
Project Avatar: API Contracts and Pydantic Data Models.

Defines the concrete schemas for subsystem communication across:
1. Feature Pipeline -> Tabular ML Engines (Grid & Municipal Features)
2. Tabular ML Engines -> RAG Knowledge Engine & Web App (Risk Payloads)
3. RAG Knowledge Engine -> Streamlit Web App (Action Advisories)
4. Statutory Privacy Compliance (small cell suppression enforcement)
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


# =====================================================================
# 1. DOMAIN ENUMERATIONS
# =====================================================================

class LGUName(str, Enum):
    """The 17 Local Government Units of the National Capital Region (NCR)."""
    CALOOCAN = "City of Caloocan"
    LAS_PINAS = "City of Las Piñas"
    MAKATI = "City of Makati"
    MALABON = "City of Malabon"
    MANDALUYONG = "City of Mandaluyong"
    MANILA = "City of Manila"
    MARIKINA = "City of Marikina"
    MUNTINLUPA = "City of Muntinlupa"
    NAVOTAS = "City of Navotas"
    PARANAQUE = "City of Parañaque"
    PASAY = "City of Pasay"
    PASIG = "City of Pasig"
    PATEROS = "Municipality of Pateros"
    QUEZON_CITY = "Quezon City"
    SAN_JUAN = "City of San Juan"
    TAGUIG = "City of Taguig"
    VALENZUELA = "City of Valenzuela"


class RiskTier(str, Enum):
    """Standardized 4-tier public health risk categories."""
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AQICategory(str, Enum):
    """Ambient Air Quality Index Categories based on US EPA / DENR harmonized standards."""
    GOOD = "Good (0-12 µg/m³)"
    FAIR = "Fair (12.1-35.4 µg/m³)"
    UNHEALTHY_SENSITIVE = "Unhealthy for Sensitive Groups (35.5-55.4 µg/m³)"
    VERY_UNHEALTHY = "Very Unhealthy (55.5-150.4 µg/m³)"
    HAZARDOUS = "Hazardous (>= 150.5 µg/m³)"


class StakeholderRole(str, Enum):
    """Recipient stakeholder role for synthesized action advisories."""
    MUNICIPAL_HEALTH_OFFICER = "MHO_EPIDEMIOLOGIST"
    DISASTER_RISK_REDUCTION_OFFICER = "LDRRMO_PLANNER"
    BARANGAY_HEALTH_WORKER = "BHW_COMMUNITY"
    GENERAL_PUBLIC = "PUBLIC_CITIZEN"


class ActionPriority(str, Enum):
    """Priority urgency for action directives."""
    P1_IMMEDIATE = "P1_IMMEDIATE (Within 24 Hours)"
    P2_URGENT = "P2_URGENT (Within 48-72 Hours)"
    P3_ROUTINE = "P3_ROUTINE (Within 1-2 Weeks)"


class LanguageCode(str, Enum):
    """Supported output languages for community advisories."""
    ENGLISH = "EN"
    TAGALOG = "TL"


# =====================================================================
# 2. INPUT FEATURE SCHEMAS (FEATURE STORE -> ML ENGINES)
# =====================================================================

class GridCellFeatures(BaseModel):
    """
    Uniform 1.0 km x 1.0 km grid cell feature vector for Spatial XGBoost downscaling.
    Spatial bounding box: [120.85°E, 14.35°N, 121.15°E, 14.80°N].
    """
    cell_id: str = Field(..., description="Unique cell identifier formatted as 'GRID_R{row:02d}_C{col:02d}'")
    latitude: float = Field(..., ge=14.35, le=14.80, description="WGS84 Latitude centroid of the 1km grid cell")
    longitude: float = Field(..., ge=120.85, le=121.15, description="WGS84 Longitude centroid of the 1km grid cell")
    lgu_name: LGUName = Field(..., description="Parent LGU administrative boundary containing this cell centroid")

    # Topographic & Built Environment
    elev_m: float = Field(..., ge=-5.0, le=500.0, description="Mean surface elevation in meters ASL")
    slope_pct: float = Field(..., ge=0.0, le=100.0, description="Derived surface slope gradient percentage")
    twi: float = Field(..., ge=0.0, le=30.0, description="Topographic Wetness Index (water accumulation potential)")
    ndbi: float = Field(..., ge=-1.0, le=1.0, description="Normalized Difference Built-up Index (impervious surface)")
    road_density_km_per_km2: float = Field(..., ge=0.0, le=50.0, description="Road density in km/km²")
    distance_to_major_artery_m: float = Field(..., ge=0.0, le=50000.0, description="Distance to closest major artery (m)")

    # Atmospheric & Reanalysis Predictors
    uhi_seasonal_anomaly_c: float = Field(..., ge=-5.0, le=15.0, description="Dry-season SUHI thermal anomaly prior in °C")
    boundary_layer_height_m: float = Field(..., ge=50.0, le=5000.0, description="Planetary boundary layer height (m)")
    wind_u_10m_ms: float = Field(..., ge=-50.0, le=50.0, description="10m zonal wind vector component in m/s")
    wind_v_10m_ms: float = Field(..., ge=-50.0, le=50.0, description="10m meridional wind vector component in m/s")
    air_temp_2m_k: float = Field(..., ge=270.0, le=320.0, description="2-meter air temperature in Kelvin")
    relative_humidity_pct: float = Field(..., ge=10.0, le=100.0, description="2-meter relative humidity percentage")
    surface_pressure_hpa: float = Field(..., ge=900.0, le=1100.0, description="Surface atmospheric pressure in hPa")


class MunicipalLaggedFeatures(BaseModel):
    """
    Municipal-level lagged epidemiological feature vector for LightGBM Leptospirosis Engine.
    Fields directly match model inputs and empirical distributed lags (Lags 1-4).
    """
    lgu_id: str = Field(..., description="Philippine Standard Geographic Code (PSGC) identifier (e.g. 'PH137402000')")
    lgu_name: LGUName = Field(..., description="Municipal / City Local Government Unit name")
    epi_week: int = Field(..., ge=1, le=53, description="ISO 8601 Epidemiological Week number (1-53)")
    year: int = Field(..., ge=2020, le=2030, description="Calendar year of surveillance")

    # Distributed Lag Predictors
    rainfall_lag_1w: float = Field(..., ge=0.0, le=1000.0, description="Rainfall lagged 1w in mm")
    rainfall_lag_2w: float = Field(..., ge=0.0, le=1000.0, description="Rainfall lagged 2w in mm (Peak surge)")
    rainfall_lag_3w: float = Field(..., ge=0.0, le=1000.0, description="Rainfall lagged 3w in mm (Hospitalization surge)")
    rainfall_lag_4w: float = Field(..., ge=0.0, le=1000.0, description="Rainfall lagged 4w in mm (Surveillance lag)")
    soil_moisture_lag_2w: float = Field(..., ge=0.0, le=1.0, description="Soil moisture lagged 2w in m³/m³")
    cumulative_rainfall_2w_to_4w: float = Field(..., ge=0.0, le=2500.0, description="Cumulative rolling rainfall 2w-4w in mm")

    # Environmental & Demographic Stressors
    pm25_rolling_4w: float = Field(..., ge=0.0, le=300.0, description="Trailing 4w mean PM2.5 in µg/m³")
    uhi_anomaly: float = Field(..., ge=-5.0, le=15.0, description="Dry-season SUHI thermal anomaly in °C")
    elev_m: float = Field(..., ge=-5.0, le=200.0, description="Mean municipal elevation in meters ASL")
    slope_pct: float = Field(..., ge=0.0, le=100.0, description="Mean surface slope gradient percentage")
    twi: float = Field(..., ge=0.0, le=25.0, description="Mean municipal Topographic Wetness Index")
    population: float = Field(..., ge=10000.0, le=5000000.0, description="Municipal population")


# =====================================================================
# 3. MODEL PREDICTION SCHEMAS (TABULAR ML -> RAG & APP)
# =====================================================================

class PM25GridPrediction(BaseModel):
    """Downscaled continuous PM2.5 particulate prediction for a 1km grid cell."""
    cell_id: str = Field(..., description="Grid cell identifier")
    latitude: float = Field(..., description="Centroid Latitude")
    longitude: float = Field(..., description="Centroid Longitude")
    lgu_name: LGUName = Field(..., description="Associated LGU")
    predicted_pm25_ug_m3: float = Field(..., ge=0.0, le=500.0, description="Predicted ambient PM2.5 concentration in µg/m³")
    who_annual_exceedance_factor: float = Field(..., description="Ratio above WHO 2021 annual guideline (5.0 µg/m³)")
    who_24h_exceedance_factor: float = Field(..., description="Ratio above WHO 2021 24-hour guideline (15.0 µg/m³)")
    aqi_category: AQICategory = Field(..., description="Standardized Air Quality Index Category")
    spatial_uncertainty_std: float = Field(..., ge=0.0, description="Cross-validated prediction uncertainty standard error")


class LeptospirosisLguPrediction(BaseModel):
    """
    Municipal-level anticipatory leptospirosis risk prediction.
    Enforces small cell suppression (k >= 5) for privacy protection.
    """
    lgu_id: str = Field(..., description="PSGC municipal identifier")
    lgu_name: LGUName = Field(..., description="LGU name")
    epi_week: int = Field(..., ge=1, le=53, description="Target Epidemiological Week")
    year: int = Field(..., ge=2020, description="Target Year")

    # LightGBM Surge Classification Output
    outbreak_surge_probability: float = Field(..., ge=0.0, le=1.0, description="Calibrated probability of epidemic surge")
    risk_tier: RiskTier = Field(..., description="Standardized 4-tier risk classification band")

    # Tweedie Count Regression Output
    predicted_cases_tweedie: float = Field(..., ge=0.0, description="Raw expected weekly cases via Tweedie loss")
    suppressed_case_display: str = Field(..., description="Privacy-compliant case display string (e.g., '<5' or '18.4')")
    is_suppressed: bool = Field(..., description="True if raw case count is suppressed due to k-anonymity (1 <= n < 5)")

    # Model Interpretability
    top_shap_drivers: Dict[str, float] = Field(..., description="Top 5 signed feature attribution values derived via TreeSHAP")
    statutory_privacy_notice: str = Field(
        default="Adherence to RA 10173: Reporting cells with 1 to 4 cases are suppressed (<5) to eliminate re-identification.",
        description="Privacy disclosure notice"
    )

    @field_validator("suppressed_case_display")
    @classmethod
    def enforce_small_cell_suppression(cls, v: str, info) -> str:
        """Enforces that counts between 1 and 4 are rendered strictly as '<5'."""
        data = info.data
        if "predicted_cases_tweedie" in data:
            raw_cases = data["predicted_cases_tweedie"]
            if 1.0 <= raw_cases < 5.0 and v != "<5":
                return "<5"
        return v


class CompositeRiskPayload(BaseModel):
    """
    Aggregated contract bundle emitted by the Tabular ML service.
    Consolidated payload passed to the RAG Knowledge Engine and Web App.
    """
    payload_id: str = Field(..., description="Unique UUID for this inference batch")
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="UTC timestamp of generation")
    model_version_xgboost: str = Field(default="xgboost-pm25-v1.2.0", description="Version of the Spatial PM2.5 model")
    model_version_lightgbm: str = Field(default="lightgbm-lepto-v1.3.0", description="Version of the Leptospirosis model")
    target_epi_week: int = Field(..., ge=1, le=53, description="Target Epidemiological Week")
    target_year: int = Field(..., ge=2020, description="Target Year")

    # Payload Sub-Collections
    municipal_predictions: List[LeptospirosisLguPrediction] = Field(
        ..., min_length=17, max_length=17, description="Array of 17 NCR municipal predictions"
    )
    grid_summary_metrics: Dict[str, float] = Field(
        ..., description="Regional summary metrics (mean PM2.5, peak PM2.5, % cells exceeding WHO)"
    )


# =====================================================================
# 4. RAG KNOWLEDGE & ADVISORY SCHEMAS (RAG ENGINE -> APP)
# =====================================================================

class RAGAdvisoryRequest(BaseModel):
    """Request payload sent to the RAG Knowledge Engine to generate an advisory."""
    lgu_id: str = Field(..., description="PSGC municipal identifier")
    lgu_name: LGUName = Field(..., description="Target municipal LGU")
    risk_tier: RiskTier = Field(..., description="Current municipal risk tier")
    outbreak_surge_probability: float = Field(..., ge=0.0, le=1.0, description="Calibrated surge probability")
    suppressed_case_display: str = Field(..., description="Compliant case display string")
    dominant_shap_drivers: Dict[str, float] = Field(..., description="Top signed features driving the risk")
    target_role: StakeholderRole = Field(..., description="Target recipient role for directive specialization")
    language: LanguageCode = Field(default=LanguageCode.ENGLISH, description="Preferred advisory language")


class ActionDirective(BaseModel):
    """Individual actionable protocol directive generated by the RAG engine."""
    directive_id: str = Field(..., description="Unique directive identifier (e.g. 'DIR-MALABON-01')")
    priority: ActionPriority = Field(..., description="Operational urgency tier")
    action_title: str = Field(..., description="Short title of the recommended action")
    action_description: str = Field(..., description="Detailed instructions grounded in clinical guidelines and protocols")
    target_stakeholder: str = Field(..., description="Designated execution lead (e.g., City Health Officer, BHW Leader)")
    resource_requirement: str = Field(..., description="Estimated supplies needed")


class RetrievedCitation(BaseModel):
    """Grounding citation retrieved from the indexed regulatory corpus."""
    citation_id: str = Field(..., description="Unique citation index identifier")
    document_title: str = Field(..., description="Document or protocol title")
    issuing_authority: str = Field(..., description="Issuing body (e.g., 'Department of Health', 'WHO', 'NKTI')")
    statutory_or_cpg_reference: str = Field(..., description="Specific AO, Memorandum, or Section reference")
    exact_excerpt: str = Field(..., description="Relevant text excerpt providing grounding authority")
    url_or_doi: Optional[str] = Field(None, description="Online URL or DOI lookup link")


class ClinicalPrescription(BaseModel):
    """Formal clinical guidance for post-exposure prophylaxis or triage staging."""
    regimen_name: str = Field(..., description="Name of the therapeutic or prophylactic protocol")
    drug_and_dosage: str = Field(..., description="Pharmacology guidelines (e.g. 'Doxycycline 200 mg single dose')")
    timing_window: str = Field(..., description="Clinical administration window (e.g. 'Within 24-48h of exposure')")
    contraindications: str = Field(..., description="Strict clinical contraindications (e.g. 'Pregnancy, lactating, age < 8y')")
    alternative_drug: str = Field(..., description="Approved alternative (e.g. 'Amoxicillin 500mg TID for 7 days')")


class RAGAdvisoryResponse(BaseModel):
    """Complete synthesized advisory response delivered to the UI."""
    advisory_id: str = Field(..., description="Unique advisory tracking identifier")
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="UTC timestamp of generation")
    lgu_name: LGUName = Field(..., description="Target municipality")
    target_role: StakeholderRole = Field(..., description="Target stakeholder role")
    risk_tier: RiskTier = Field(..., description="Assigned public health risk tier")
    executive_summary: str = Field(..., description="Epidemiological and environmental risk synthesis")
    prioritized_directives: List[ActionDirective] = Field(..., min_length=1, description="List of operational actions")
    clinical_guidance: Optional[ClinicalPrescription] = Field(None, description="Clinical drug dosing guidelines")
    retrieved_citations: List[RetrievedCitation] = Field(
        ..., min_length=1, description="Citations grounding the advisory"
    )
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Retrieval relevance confidence score")
    statutory_privacy_statement: str = Field(
        default="Adherence to RA 10173: Confidential epidemiological advisory for public health coordination.",
        description="Privacy notice"
    )


# =====================================================================
# 5. ERROR AND STATUS SCHEMAS
# =====================================================================

class APIErrorDetail(BaseModel):
    """Detailed validation or processing error item."""
    field: Optional[str] = Field(None, description="Input field that triggered the error")
    message: str = Field(..., description="Descriptive error explanation")
    error_code: str = Field(..., description="Standard machine-readable error code")


class APIErrorResponse(BaseModel):
    """Standardized error wrapper for HTTP 4xx/5xx responses."""
    success: bool = Field(default=False, description="Always false for error responses")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Error timestamp")
    status_code: int = Field(..., ge=400, le=599, description="HTTP status code")
    error_type: str = Field(..., description="High-level category of error")
    errors: List[APIErrorDetail] = Field(default_factory=list, description="Array of specific error details")
