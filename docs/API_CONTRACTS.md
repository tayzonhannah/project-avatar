# Project Avatar: Concrete API Contracts, Pydantic Schemas & Data Payload Specifications

**Lead Systems Architect**, Project Avatar  
**Philippine Junior Data Science Challenge (PJDSC) 2026**  
**Document Identifier:** `docs/API_CONTRACTS.md`  
**Associated Source Code Module:** [`src/api_contracts.py`](../src/api_contracts.py)  
**Pydantic Engine:** Pydantic v2 (Python 3.13)  
**Date of Ratification:** October 2026  
**Statutory Adherence:** Republic Act 10173 (Data Privacy Act of 2012) & PJDSC Competition Rubric (Section 3.1)

---

## 1. Architectural Context & Design Philosophy

In modern health informatics and machine learning engineering, loose dictionaries and unstructured JSON payloads represent a primary failure mode, creating silent schema drift, type coersion bugs, and serialization exceptions. Project Avatar enforces **contract-driven, type-safe decoupling** across all architectural boundaries.

```
       PROJECT AVATAR CONTRACT TOPOLOGY & DATA FLOW
+----------------------------------------------------------------------------------------------------+
| 1. FEATURE STORE (Offline Batch Parquet)                                                           |
|    - Schema: GridCellFeatures (1km downscaling predictors)                                         |
|    - Schema: MunicipalLaggedFeatures (Verified lag features: Lags 1-4, dropping Lag 0)             |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| 2. TABULAR ML INFERENCE SERVICE                                                                    |
|    - Consumes: MunicipalLaggedFeatures & GridCellFeatures                                          |
|    - Emits: PM25GridPrediction (Continuous 1km surface)                                            |
|    - Emits: LeptospirosisLguPrediction (Surge prob + Tweedie count + k>=5 small cell suppression)   |
|    - Bundles: CompositeRiskPayload (Complete 17-LGU NCR inference state)                           |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| 3. RAG KNOWLEDGE ENGINE                                                                            |
|    - Ingests: RAGAdvisoryRequest (Consumes structured JSON; zero raster dependencies)               |
|    - Performs: Vector semantic search over DOH CPGs, WHO guidelines, and NKTI surge protocols       |
|    - Emits: RAGAdvisoryResponse (Prioritized directives, clinical prescriptions, exact citations)  |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| 4. STREAMLIT DECISION SUPPORT FRONTEND                                                             |
|    - Consumes: CompositeRiskPayload (for choropleth rendering & SHAP waterfall plots)              |
|    - Consumes: RAGAdvisoryResponse (for frontline actionable directives and PDF export)            |
+----------------------------------------------------------------------------------------------------+
```

### Core Design Rules
1. **Pydantic v2 Enforcement**: All runtime payloads are strictly validated against Pydantic models with field constraints (`ge`, `le`, regex patterns). Invalid values fail immediately with descriptive error responses (`HTTP 422`).
2. **Empirical Parameter Lock-in**: Feature vectors explicitly require the empirical lag variables confirmed in exploratory data analysis (`rainfall_lag_1w` through `rainfall_lag_4w`, `soil_moisture_lag_2w`, `cumulative_rainfall_2w_to_4w`), while instantaneous `rainfall_lag_0w` is completely eliminated from the model contract.
3. **Statutory Small Cell Suppression (RA 10173)**: Models incorporate a mandatory Pydantic validator that automatically suppresses case counts where $1 \le n_{\text{cases}} < 5$, rendering them as `"<5"` and setting `is_suppressed = True` to prevent re-identification linkage attacks.

---

## 2. Standard Domain Enumerations

```python
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
    LOW = "LOW"               # Surge probability < 0.25
    MODERATE = "MODERATE"     # 0.25 <= Surge probability < 0.50
    HIGH = "HIGH"             # 0.50 <= Surge probability < 0.75
    CRITICAL = "CRITICAL"     # Surge probability >= 0.75

class AQICategory(str, Enum):
    """Ambient Air Quality Index Categories based on DENR / WHO standards."""
    GOOD = "Good (0-12 µg/m³)"
    FAIR = "Fair (12.1-35.4 µg/m³)"
    UNHEALTHY_SENSITIVE = "Unhealthy for Sensitive Groups (35.5-55.4 µg/m³)"
    VERY_UNHEALTHY = "Very Unhealthy (55.5-150.4 µg/m³)"
    HAZARDOUS = "Hazardous (>= 150.5 µg/m³)"

class StakeholderRole(str, Enum):
    """Recipient stakeholder role for RAG-synthesized action advisories."""
    MUNICIPAL_HEALTH_OFFICER = "MHO_EPIDEMIOLOGIST"
    DISASTER_RISK_REDUCTION_OFFICER = "LDRRMO_PLANNER"
    BARANGAY_HEALTH_WORKER = "BHW_COMMUNITY"
    GENERAL_PUBLIC = "PUBLIC_CITIZEN"

class ActionPriority(str, Enum):
    """Priority urgency for operational directives."""
    P1_IMMEDIATE = "P1_IMMEDIATE (Within 24 Hours)"
    P2_URGENT = "P2_URGENT (Within 48-72 Hours)"
    P3_ROUTINE = "P3_ROUTINE (Within 1-2 Weeks)"
```

---

## 3. Input Feature Schemas

### 3.1 `GridCellFeatures` (1.0 km $\times$ 1.0 km Downscaling Input)
Represents a single cell within the $30 \times 45 = 1,350$ cell grid covering Metro Manila (`[120.85°E, 14.35°N, 121.15°E, 14.80°N]`).

| Field Name | Type | Constraints | Description & Empirical Source |
| :--- | :--- | :--- | :--- |
| `cell_id` | `str` | Format `GRID_R{row}_C{col}` | Unique cell identifier across the 1,350 grid units. |
| `latitude` | `float` | `14.35 <= lat <= 14.80` | WGS 84 latitude centroid of the grid cell. |
| `longitude` | `float` | `120.85 <= lon <= 121.15` | WGS 84 longitude centroid of the grid cell. |
| `lgu_name` | `LGUName` | Valid NCR LGU | Parent administrative LGU containing cell centroid. |
| `elev_m` | `float` | `-5.0 <= elev <= 500.0` | SRTM 1-arc-second (~30m) mean surface elevation (m ASL). |
| `slope_pct` | `float` | `0.0 <= slope <= 100.0` | SRTM derived surface slope gradient percentage. |
| `twi` | `float` | `0.0 <= twi <= 30.0` | Topographic Wetness Index ($\ln(a / \tan \beta)$). |
| `ndbi` | `float` | `-1.0 <= ndbi <= 1.0` | Normalized Difference Built-up Index (impervious density). |
| `road_density_km_per_km2` | `float` | `0.0 <= density <= 50.0`| OpenStreetMap road density (vehicular proxy). |
| `distance_to_major_artery_m`| `float` | `>= 0.0` | Distance to primary transit artery (EDSA, C5, R10). |
| `uhi_seasonal_anomaly_c` | `float` | `-5.0 <= anomaly <= 15.0`| Static Landsat/MODIS dry-season SUHI prior (°C). |
| `boundary_layer_height_m` | `float` | `50.0 <= blh <= 5000.0` | ERA5 planetary boundary layer height (particulate dispersion). |
| `wind_u_10m_ms` | `float` | `-50.0 <= u <= 50.0` | ERA5 10m zonal (east-west) wind vector component. |
| `wind_v_10m_ms` | `float` | `-50.0 <= v <= 50.0` | ERA5 10m meridional (north-south) wind vector component. |
| `air_temp_2m_k` | `float` | `270.0 <= temp <= 320.0` | ERA5 2m dry-bulb temperature in Kelvin. |
| `relative_humidity_pct` | `float` | `10.0 <= rh <= 100.0` | ERA5 2m relative humidity percentage. |
| `surface_pressure_hpa` | `float` | `900.0 <= p <= 1100.0` | ERA5 surface atmospheric pressure in hPa. |

### 3.2 `MunicipalLaggedFeatures` (LightGBM Leptospirosis Input)
Represents the municipal-level feature vector incorporating verified empirical lags and compounding risk priors.

| Field Name | Type | Constraints | Description & Empirical Evidence |
| :--- | :--- | :--- | :--- |
| `lgu_id` | `str` | PSGC format (`PH13...`) | Philippine Standard Geographic Code. |
| `lgu_name` | `LGUName` | Valid NCR LGU | Official municipal / city name. |
| `epi_week` | `int` | `1 <= week <= 53` | Target ISO 8601 Epidemiological Week. |
| `year` | `int` | `2020 <= year <= 2030` | Target calendar year. |
| `rainfall_lag_1w_mm` | `float` | `>= 0.0` | Rainfall lagged 1 week (Incubation onset: $r=0.4048$). |
| `rainfall_lag_2w_mm` | `float` | `>= 0.0` | Rainfall lagged 2 weeks (**PEAK OUTBREAK TRIGGER: $r=0.6267$**). |
| `rainfall_lag_3w_mm` | `float` | `>= 0.0` | Rainfall lagged 3 weeks (**HOSPITALIZATION SURGE: $r=0.5477$**). |
| `rainfall_lag_4w_mm` | `float` | `>= 0.0` | Rainfall lagged 4 weeks (Surveillance delay: $r=0.2927$). |
| `soil_moisture_lag_2w_m3_m3`| `float` | `0.0 <= sm <= 1.0` | ERA5 Soil moisture lagged 2 weeks (Puddle saturation: $r=0.4041$). |
| `cumulative_rainfall_2w_to_4w_mm`| `float`| `>= 0.0` | Multi-week rolling precipitation accumulation pulse. |
| `pm25_rolling_4w_ug_m3` | `float` | `>= 0.0` | Trailing 4-week ambient PM2.5 (capillary fragility prior). |
| `uhi_seasonal_anomaly_c` | `float` | `-5.0 <= anomaly <= 15.0`| Static pre-monsoon SUHI thermal anomaly prior (°C). |
| `mean_heat_index_lag_4w_c`| `float` | `20.0 <= hi <= 60.0` | Trailing 4-week mean apparent Heat Index (°C). |
| `mean_elevation_m` | `float` | `-5.0 <= elev <= 200.0` | Mean municipal elevation in meters ASL. |
| `pct_area_lowland_under_5m`| `float` | `0.0 <= pct <= 100.0` | Percent of municipal area under 5m elevation. |
| `pct_area_sluggish_slope` | `float` | `0.0 <= pct <= 100.0` | Percent of municipal area with slope $< 0.8\%$. |
| `mean_twi` | `float` | `0.0 <= twi <= 25.0` | Mean Topographic Wetness Index. |
| `population_density_per_km2`| `float` | `>= 1000.0` | PSA 2020 municipal population density. |

---

## 4. Model Prediction Schemas

### 4.1 `PM25GridPrediction` (Spatial XGBoost Output)
Outputs high-resolution ambient particulate predictions per 1km grid cell.
```python
class PM25GridPrediction(BaseModel):
    cell_id: str
    latitude: float
    longitude: float
    lgu_name: LGUName
    predicted_pm25_ug_m3: float = Field(..., ge=0.0, le=500.0)
    who_annual_exceedance_factor: float
    who_24h_exceedance_factor: float
    aqi_category: AQICategory
    spatial_uncertainty_std: float
```

### 4.2 `LeptospirosisLguPrediction` (LightGBM Dual-Head Output)
Outputs municipal-level outbreak surge probabilities and Tweedie case counts, enforcing small cell suppression ($k \ge 5$).
```python
class LeptospirosisLguPrediction(BaseModel):
    lgu_id: str
    lgu_name: LGUName
    epi_week: int = Field(..., ge=1, le=53)
    year: int = Field(..., ge=2020)
    outbreak_surge_probability: float = Field(..., ge=0.0, le=1.0)
    risk_tier: RiskTier
    predicted_cases_tweedie: float = Field(..., ge=0.0)
    suppressed_case_display: str
    is_suppressed: bool
    top_shap_drivers: Dict[str, float]
    statutory_privacy_notice: str = (
        "Adherence to RA 10173: Reporting cells with 1 to 4 cases are suppressed (<5) "
        "to eliminate re-identification risk."
    )

    @field_validator("suppressed_case_display")
    @classmethod
    def enforce_small_cell_suppression(cls, v: str, info) -> str:
        data = info.data
        if "predicted_cases_tweedie" in data:
            raw_cases = data["predicted_cases_tweedie"]
            if 1.0 <= raw_cases < 5.0 and v != "<5":
                return "<5"
        return v
```

### 4.3 `CompositeRiskPayload` (Unified Batch Inference State)
Aggregates the entire inference run across the 17 NCR LGUs into a single immutable document for the RAG Engine and Web App.
```python
class CompositeRiskPayload(BaseModel):
    payload_id: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    model_version_xgboost: str = "xgboost-pm25-v1.0.4"
    model_version_lightgbm: str = "lightgbm-lepto-v1.2.0"
    target_epi_week: int
    target_year: int
    municipal_predictions: List[LeptospirosisLguPrediction]  # Exactly 17 items
    grid_summary_metrics: Dict[str, float]
```

---

## 5. RAG Knowledge Engine & Advisory Schemas

### 5.1 `RAGAdvisoryRequest` (Ingestion Payload)
Consumed by the RAG microservice to trigger vector retrieval and LLM prompt orchestration.
```python
class RAGAdvisoryRequest(BaseModel):
    lgu_id: str
    lgu_name: LGUName
    risk_tier: RiskTier
    outbreak_surge_probability: float = Field(..., ge=0.0, le=1.0)
    suppressed_case_display: str
    dominant_shap_drivers: Dict[str, float]
    target_role: StakeholderRole
    language: LanguageCode = LanguageCode.ENGLISH
```

### 5.2 `RAGAdvisoryResponse` (Synthesized Public Health Directives)
The primary contract powering the decision support console in the Streamlit UI.
```python
class ActionDirective(BaseModel):
    directive_id: str
    priority: ActionPriority
    action_title: str
    action_description: str
    target_stakeholder: str
    resource_requirement: str

class ClinicalPrescription(BaseModel):
    regimen_name: str
    drug_and_dosage: str
    timing_window: str
    contraindications: str
    alternative_drug: str

class RetrievedCitation(BaseModel):
    citation_id: str
    document_title: str
    issuing_authority: str
    statutory_or_cpg_reference: str
    exact_excerpt: str
    url_or_doi: Optional[str] = None

class RAGAdvisoryResponse(BaseModel):
    advisory_id: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    lgu_name: LGUName
    target_role: StakeholderRole
    risk_tier: RiskTier
    executive_summary: str
    prioritized_directives: List[ActionDirective]
    clinical_guidance: Optional[ClinicalPrescription] = None
    retrieved_citations: List[RetrievedCitation]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    statutory_privacy_statement: str = (
        "Adherence to RA 10173: Confidential epidemiological advisory "
        "for authorized public health personnel."
    )
```

---

## 6. Concrete JSON Payload Examples

### 6.1 Municipal Lagged Features (`MunicipalLaggedFeatures`)
**Scenario**: City of Malabon, Epidemiological Week 32, 2024 (Post-Typhoon Carina surge window).
```json
{
  "lgu_id": "PH137402000",
  "lgu_name": "City of Malabon",
  "epi_week": 32,
  "year": 2024,
  "rainfall_lag_1w_mm": 45.2,
  "rainfall_lag_2w_mm": 218.4,
  "rainfall_lag_3w_mm": 142.0,
  "rainfall_lag_4w_mm": 38.6,
  "soil_moisture_lag_2w_m3_m3": 0.482,
  "cumulative_rainfall_2w_to_4w_mm": 399.0,
  "pm25_rolling_4w_ug_m3": 34.8,
  "uhi_seasonal_anomaly_c": 4.5,
  "mean_heat_index_lag_4w_c": 43.2,
  "mean_elevation_m": 2.4,
  "pct_area_lowland_under_5m": 92.5,
  "pct_area_sluggish_slope": 88.4,
  "mean_twi": 14.12,
  "population_density_per_km2": 24150.0
}
```

### 6.2 1km Grid Cell Feature Vector (`GridCellFeatures`)
**Scenario**: Lowland alluvial cell `GRID_R22_C10` situated in CAMANAVA estuarine basin.
```json
{
  "cell_id": "GRID_R22_C10",
  "latitude": 14.65,
  "longitude": 120.95,
  "lgu_name": "City of Malabon",
  "elev_m": 2.1,
  "slope_pct": 0.3,
  "twi": 14.2,
  "ndbi": 0.48,
  "road_density_km_per_km2": 18.4,
  "distance_to_major_artery_m": 340.0,
  "uhi_seasonal_anomaly_c": 4.2,
  "boundary_layer_height_m": 620.0,
  "wind_u_10m_ms": -3.4,
  "wind_v_10m_ms": 2.1,
  "air_temp_2m_k": 304.5,
  "relative_humidity_pct": 88.0,
  "surface_pressure_hpa": 1008.2
}
```

### 6.3 Municipal Model Prediction (`LeptospirosisLguPrediction`)
**Scenario**: Model outputs a point count of $3.4$ cases. The Pydantic validator automatically enforces small cell suppression under Republic Act 10173, masking the display as `"<5"`.
```json
{
  "lgu_id": "PH137402000",
  "lgu_name": "City of Malabon",
  "epi_week": 32,
  "year": 2024,
  "outbreak_surge_probability": 0.842,
  "risk_tier": "CRITICAL",
  "predicted_cases_tweedie": 3.4,
  "suppressed_case_display": "<5",
  "is_suppressed": true,
  "top_shap_drivers": {
    "rainfall_lag_2w_mm": 0.384,
    "soil_moisture_lag_2w_m3_m3": 0.221,
    "pct_area_lowland_under_5m": 0.178,
    "pm25_rolling_4w_ug_m3": 0.115,
    "uhi_seasonal_anomaly_c": 0.102
  },
  "statutory_privacy_notice": "Adherence to RA 10173: Reporting cells with 1 to 4 cases are suppressed (<5) to eliminate re-identification risk."
}
```

### 6.4 Synthesized RAG Advisory Response (`RAGAdvisoryResponse`)
**Scenario**: Full role-specialized clinical advisory returned to the Malabon City Health Officer.
```json
{
  "advisory_id": "ADV-2024-W32-MALABON",
  "generated_at": "2024-08-12T01:30:00Z",
  "lgu_name": "City of Malabon",
  "target_role": "MHO_EPIDEMIOLOGIST",
  "risk_tier": "CRITICAL",
  "executive_summary": "CRITICAL ALERT: Malabon City faces an immediate epidemic leptospirosis surge driven by extreme Lag-2 rainfall (218.4 mm) and soil saturation (0.48 m³/m³) following Tropical Cyclone Carina. Chronic PM2.5 pre-conditioning (34.8 µg/m³) elevates systemic vulnerability to Leptospiral Pulmonary Hemorrhage Syndrome (LPHS) and Acute Kidney Injury (AKI).",
  "prioritized_directives": [
    {
      "directive_id": "DIR-MAL-01",
      "priority": "P1_IMMEDIATE (Within 24 Hours)",
      "action_title": "Enact Post-Exposure Prophylaxis (PEP) Campaign",
      "action_description": "Mobilize Barangay Health Workers (BHWs) to distribute Doxycycline 200mg single dose to all individuals with casual flood exposure within 24-48 hours. Issue weekly 200mg prophylaxis for individuals with ongoing water contact.",
      "target_stakeholder": "City Health Officer & Barangay Health Centers",
      "resource_requirement": "15,000 capsules Doxycycline 100mg (7,500 patient courses)"
    },
    {
      "directive_id": "DIR-MAL-02",
      "priority": "P1_IMMEDIATE (Within 24 Hours)",
      "action_title": "Establish Acute Febrile & AKI Triage Screening",
      "action_description": "Open specialized syndromic screening lanes at all 21 Malabon health centers. Mandate routine serum creatinine testing, urine output monitoring (<0.5 mL/kg/h), and screening for conjunctival suffusion and calf tenderness.",
      "target_stakeholder": "Rural Health Unit Physicians & Triage Nurses",
      "resource_requirement": "500 Point-of-Care Creatinine Test Cartridges"
    },
    {
      "directive_id": "DIR-MAL-03",
      "priority": "P2_URGENT (Within 48-72 Hours)",
      "action_title": "Alert Regional Tertiary Referral Hospital (NKTI)",
      "action_description": "Pre-coordinate clinical transfer pathways with the National Kidney and Transplant Institute (NKTI) and San Lazaro Hospital for patients presenting with oliguria, hyperkalemia, or hemoptysis before uremic shock develops.",
      "target_stakeholder": "Emergency Medical Services & Hospital Liaison Officer",
      "resource_requirement": "2 Dedicated Critical Care Patient Transport Ambulances"
    }
  ],
  "clinical_guidance": {
    "regimen_name": "DOH Leptospirosis Post-Exposure Prophylaxis (PEP)",
    "drug_and_dosage": "Doxycycline 200 mg orally once (two 100mg capsules)",
    "timing_window": "Single dose within 24 to 48 hours of floodwater exposure",
    "contraindications": "Contraindicated in pregnant women, nursing mothers, and children under 8 years of age.",
    "alternative_drug": "Amoxicillin 500 mg orally every 8 hours for 7 days (for pregnant/lactating patients and children)"
  },
  "retrieved_citations": [
    {
      "citation_id": "CIT-DOH-2010",
      "document_title": "Administrative Order No. 2010-0018: Revised Guidelines on Prevention and Management of Leptospirosis",
      "issuing_authority": "Department of Health (Philippines)",
      "statutory_or_cpg_reference": "Section V, Subsection B (Prophylaxis Regimens)",
      "exact_excerpt": "Post-exposure prophylaxis with oral doxycycline (200 mg single dose) should be administered within 24-48 hours after wading in floodwaters.",
      "url_or_doi": "https://doh.gov.ph/ao-2010-0018"
    },
    {
      "citation_id": "CIT-NKTI-2024",
      "document_title": "Public Advisory on Post-Typhoon Leptospirosis Surge and Hemodialysis Staging",
      "issuing_authority": "National Kidney and Transplant Institute (NKTI)",
      "statutory_or_cpg_reference": "Emergency Staging Protocol 2024-03",
      "exact_excerpt": "Due to 150% dialysis bed occupancy, peripheral health units must institute early volume resuscitation and avoid delayed referrals until frank anuria develops.",
      "url_or_doi": "https://nkti.gov.ph/public-advisories/leptospirosis-surge-2024"
    }
  ],
  "confidence_score": 0.962,
  "statutory_privacy_statement": "Adherence to RA 10173: Confidential epidemiological advisory for authorized public health personnel."
}
```

---

## 7. Error Handling & HTTP Status Code Specifications

All microservices adhere to standard HTTP status codes and return standardized `APIErrorResponse` payloads upon failure:

```
+-------------+-----------------------+-------------------------------------------------------------+
| HTTP Status | Error Type            | Operational Scenario / Cause                                |
+-------------+-----------------------+-------------------------------------------------------------+
| 200 OK      | Success               | Successful feature extraction, inference, or RAG synthesis. |
| 400 Bad Req | MALFORMED_REQUEST     | JSON syntax error, missing required root payload keys.      |
| 404 Not Fnd | RESOURCE_NOT_FOUND    | Invalid LGU identifier or unsupported epidemiological week. |
| 422 Unproc  | VALIDATION_ERROR      | Pydantic validation failure (e.g., negative rainfall,       |
|             |                       | coordinates outside Metro Manila bounding box).             |
| 500 Server  | INFERENCE_FAILURE     | Tabular model exception or SHAP calculation failure.        |
| 503 Unavail | VECTOR_STORE_OFFLINE  | ChromaDB connection timeout or Gemini API rate limit.       |
+-------------+-----------------------+-------------------------------------------------------------+
```

### Standardized Error Payload Structure (`APIErrorResponse`)
```json
{
  "success": false,
  "timestamp": "2026-10-24T05:30:00Z",
  "status_code": 422,
  "error_type": "VALIDATION_ERROR",
  "errors": [
    {
      "field": "rainfall_lag_2w_mm",
      "message": "Input should be greater than or equal to 0.0",
      "error_code": "greater_than_equal"
    },
    {
      "field": "latitude",
      "message": "Centroid latitude 14.25 is outside NCR bounds [14.35, 14.80]",
      "error_code": "out_of_bounds"
    }
  ]
}
```

---

## 8. References (Strict APA 7th Edition)

Department of Health. (2010). *Administrative Order No. 2010-0018: Revised guidelines on the prevention and management of leptospirosis in the Philippines*. Department of Health, Republic of the Philippines. https://doh.gov.ph/

Department of Health. (2024). *Memorandum No. 2024-0288: Urgent advisory on doxycycline post-exposure prophylaxis for flooded communities*. Department of Health, Republic of the Philippines. https://doh.gov.ph/

National Kidney and Transplant Institute. (2024). *Public advisory: Surge in post-typhoon leptospirosis admissions and emergency hemodialysis staging*. NKTI Information Office. https://nkti.gov.ph/

Republic of the Philippines. (2012). *Republic Act No. 10173: Data Privacy Act of 2012*. Official Gazette of the Republic of the Philippines. https://www.officialgazette.gov.ph/2012/08/15/republic-act-no-10173/

World Health Organization. (2021). *WHO global air quality guidelines: Particulate matter (PM2.5 and PM10), ozone, nitrogen dioxide, sulfur dioxide and carbon monoxide*. World Health Organization. https://apps.who.int/iris/handle/10665/345329
