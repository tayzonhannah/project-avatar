# Project Avatar: End-to-End System Architecture, Decoupled Pipelines & Data Flow Specifications

**Lead Systems Architect**, Project Avatar  
**Philippine Junior Data Science Challenge (PJDSC) 2026**  
**Document Identifier:** `docs/ARCHITECTURE.md`  
**Execution Context:** Production Deployment & Reproducibility  
**Date of Ratification:** October 2026  
**Statutory Compliance:** Republic Act 10173 (Data Privacy Act of 2012) & PJDSC Competition Rubric (Sections 3.1, 4.1, 4.2)

---

## 1. Executive Summary & Core Architectural Tenets

Project Avatar is a high-resolution, multi-hazard epidemiological early warning and clinical decision support system designed specifically for the National Capital Region (NCR) of the Philippines. Operating over an empirically calibrated **$1.0\ \text{km} \times 1.0\ \text{km}$ spatial grid** ($30\ \text{columns} \times 45\ \text{rows} = 1,350\ \text{cells}$), the system bridges the institutional and methodological gap between environmental telemetry (atmospheric particulate matter, urban heat island anomalies, and monsoonal inundation) and municipal public health response (leptospirosis outbreaks, acute kidney injury surges, and hemodialysis bed saturation).

```
+----------------------------------------------------------------------------------------------------+
|                                 CORE ARCHITECTURAL TENETS                                          |
+--------------------------+---------------------------------+---------------------------------------+
| Architectural Principle  | Empirical Rationale (From EDA)  | System Engineering Realization        |
+--------------------------+---------------------------------+---------------------------------------+
| 1. Strict Component      | Heavy geospatial rasters (30m   | Zero raster processing in the online  |
|    Decoupling            | DEM, Landsat LST) choke live UI | serving path; all rasters reduced to  |
|                          | and LLM inference runtimes.     | pre-computed grid Parquet tables.     |
+--------------------------+---------------------------------+---------------------------------------+
| 2. Anticipatory Warning  | Official DOH surveillance linelist| Environmental telemetry triggers   |
|    Decoupling            | exhibits a median 15.0-day delay| forward-looking warnings 14-21 days   |
|                          | (IQR: 11-20d; p90: 25.0d).      | ahead of retrospective central registries|
+--------------------------+---------------------------------+---------------------------------------+
| 3. Contract-Driven       | Loose dictionaries cause schema | Subsystems communicate exclusively via|
|    Type Safety           | drift and serialization crashes.| strict Pydantic v2 schemas and JSON.  |
+--------------------------+---------------------------------+---------------------------------------+
| 4. Empirical Hyperparam- | Class imbalance (7.67:1),       | LightGBM scale_pos_weight = 7.67;     |
|    eter Calibration      | skewness (+7.54), 37.8% zeros,  | Tweedie compound Poisson loss (p=1.45)|
|                          | cloud-mask occlusion (68.0%).   | static dry-season SUHI prior mapping. |
+--------------------------+---------------------------------+---------------------------------------+
| 5. Statutory Privacy     | 45.76% of municipal reporting   | Automated k-anonymity (k >= 5) cell   |
|    Enforcement           | cells have 1 to 4 cases.        | suppression; 4-tier categorical bands.|
+--------------------------+---------------------------------+---------------------------------------+
```

---

## 2. High-Level Subsystem Decoupling & Component Boundaries

The architecture strictly decouples the platform into four independent, horizontally scalable subsystems:

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       PROJECT AVATAR TOPOLOGY                                     │
├──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────────────┤
│ 1. FEATURE PIPELINE  │ 2. TABULAR ML ENGINES│ 3. RAG ADVISORY      │ 4. STREAMLIT WEB APP         │
│ (Offline / Batch)    │ (Inference Microserv)│ (Knowledge Engine)   │ (Frontline Decision UI)      │
├──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────────────┤
│ • Multi-Sensor ETL   │ • Spatial XGBoost    │ • Vector Database    │ • Interactive Choropleths    │
│ • 1km Grid Alignment │   (PM2.5 Downscaler) │   (ChromaDB / FAISS) │   (17 NCR LGUs)              │
│ • Imputation Engine  │ • LightGBM Surge Clf │ • Curated Corpus     │ • 1km PM2.5 Raster Overlay   │
│ • Lag Extraction     │   (scale_pos_wt=7.67)│   (WHO, DOH, CPGs)   │ • Local SHAP Waterfall Plots │
│ • Parquet Feature    │ • Tweedie Regressor  │ • Gemini Prompting   │ • Action Protocol Triggers   │
│   Store Generation   │   (Count p = 1.45)   │   (Role-Specific)    │ • PDF / JSON Export          │
└──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────────────┘
```

### Decoupled Subsystem Boundary Matrix
1. **Feature Pipeline $\rightarrow$ Tabular ML Engines**: Transmits strictly validated tabular Parquet feature matrices (`data/processed/analysis_matrix_ncr_eda.parquet`) or memory-mapped DataFrames. Tabular ML engines have **zero dependency on GDAL, Rasterio, or Google Earth Engine**.
2. **Tabular ML Engines $\rightarrow$ RAG Knowledge Engine**: Transmits a strongly typed `CompositeRiskPayload` JSON document. The RAG engine has **zero dependency on XGBoost, LightGBM, or Scikit-Learn**.
3. **Tabular ML Engines & RAG Engine $\rightarrow$ Streamlit Web App**: The web frontend consumes model predictions, SHAP attribution dictionaries, and synthesized markdown advisory payloads via standard REST/JSON APIs, ensuring complete UI responsiveness.

---

## 3. Subsystem 1: Feature Engineering & Geospatial Pipeline

The Feature Pipeline ingests, harmonizes, aligns, and persists multi-source environmental and epidemiological telemetry.

```
       SUBSYSTEM 1: FEATURE PIPELINE ARCHITECTURE & GRID TRANSFORMATIONS
+----------------------------------------------------------------------------------------------------+
| DATA INGESTION SOURCES                                                                             |
| 1. SRTM 1-Arc-Second DEM (NASA JPL / USGS): Static topographic elevation baseline (~30m)           |
| 2. Landsat 8/9 TIRS & MODIS LST (USGS / NASA): Thermal infrared surface temperatures                |
| 3. ERA5-Land Reanalysis (ECMWF Copernicus): 0.1° (~9 km) hourly meteorological & soil grids        |
| 4. DENR-EMB Ambient Stations (DENR): Continuous PM2.5 telemetry from 7 fixed NCR stations         |
| 5. DOST-PAGASA Synoptic Logs: Hourly precipitation, heat index, and cyclone rainfall warnings      |
| 6. DOH PIDSR Weekly Registries: Municipal weekly reported leptospirosis cases and linelists        |
| 7. PSA 2020 CPH & WorldPop: 100m gridded population density surfaces and municipal census          |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| GEOSPATIAL RESAMPLING & UNIFIED GRID CONVERSION                                                    |
| - Standard Analysis Extent (Metro Manila Bounding Box):                                            |
|   [Min Lon: 120.85°E, Min Lat: 14.35°N, Max Lon: 121.15°E, Max Lat: 14.80°N]                     |
| - Grid Dimensions: 30 columns x 45 rows = 1,350 uniform cells at 1.0 km x 1.0 km resolution       |
| - Storage CRS: EPSG:4326 (WGS 84); Metric Projected Analysis CRS: EPSG:32651 (UTM Zone 51N)       |
| - Spatial Resampling Protocol:                                                                     |
|   * SRTM DEM & Landsat: Area-weighted downscaling to 1km grid centroids                            |
|   * ERA5-Land Reanalysis: 2D Bicubic spline interpolation from 0.1° down to 1.0 km                 |
|   * DENR-EMB Stations: Inverse Distance Weighting (IDW) & Spatial Nearest Centroid mapping         |
|   * LGU Administrative Polygons: Zonal intersection linking each 1km cell to its parent LGU        |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| MISSINGNESS IMPUTATION & CLOUD-MASK DECOUPLING                                                     |
| - Cloud-Mask Occlusion Mitigation:                                                                 |
|   * EDA Finding: 68.0% monsoon cloud masking makes real-time satellite LST unusable during storms.  |
|   * Architecture: Decouple into a static dry-season (March-May; 12.67% null) Surface Urban Heat     |
|     Island anomaly prior (Phi_thermal_prior) + real-time all-weather synoptic heat index telemetry.|
| - Sensor Telemetry Imputation: Trailing 7-day rolling median filter (MAE 5.63 µg/m³, r = 0.8278)   |
|   with Akima cubic spline interpolation for brief telemetry drops (<= 3 hours).                    |
| - Linelist Surveillance Imputation: Missing onset dates imputed via Admission Date - 4.0 days      |
|   (empirical median clinical presentation lag), eliminating Missing at Random (MAR) selection bias.|
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| EMPIRICALLY CONFIRMED LAG GENERATION & TOPOGRAPHIC DERIVATION                                      |
| - Topographic Wetness Index (TWI): TWI = ln(a / tan(beta)), isolating sluggish lowlands (< 0.8%)   |
| - Lag Feature Selection:                                                                           |
|   * rainfall_lag_1w (incubation onset)                                                             |
|   * rainfall_lag_2w (PRIMARY OUTBREAK PEAK: r = 0.6267, p = 1.83e-12)                              |
|   * rainfall_lag_3w (SECONDARY CLINICAL PEAK: r = 0.5477, p = 3.07e-09; AKI / ICU surge)           |
|   * rainfall_lag_4w (surveillance reporting lag: r = 0.2927, p = 0.0031)                           |
|   * soil_moisture_lag_2w (ground saturation & puddle persistence: r = 0.4041, p = 2.53e-05)        |
|   * cumulative_rainfall_2w_to_4w (multi-week cumulative flood exposure)                           |
|   * [DROPPED] rainfall_lag_0w (Instantaneous Paradox: r = 0.1480, p = 0.134, non-significant)      |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| FEATURE STORE ARTIFACT EXPORT                                                                      |
| Output: data/processed/analysis_matrix_ncr_eda.parquet (Zstandard compressed, partitioned by week)|
+----------------------------------------------------------------------------------------------------+
```

---

## 4. Subsystem 2: Tabular Machine Learning Engines

The Tabular ML subsystem comprises two distinct, specialized gradient boosted decision tree (GBDT) engines tailored to solve the spatial downscaling and compound epidemic surge prediction problems.

```
+----------------------------------------------------------------------------------------------------+
|                         SUBSYSTEM 2: TABULAR MACHINE LEARNING ENGINES                              |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|   ┌──────────────────────────────────────────────┐  ┌──────────────────────────────────────────┐   |
|   │ ENGINE 2A: SPATIAL XGBOOST                   │  │ ENGINE 2B: LAGGED LIGHTGBM RISK ENGINE   │   |
|   │ (PM2.5 Downscaling Regressor)                │  │ (Surge Classifier & Tweedie Regressor)   │   |
|   ├──────────────────────────────────────────────┤  ├──────────────────────────────────────────┤   |
|   │ • Task: Continuous downscaling from 7 EMB    │  │ • Task: Dual-Head municipal-level        │   |
|   │   stations to 1,350 1-km grid cells.         │  │   anticipatory outbreak surge prediction.│   |
|   │ • Objective: reg:squarederror                │  │ • Head 1: Binary Classification          │   |
|   │ • Input Features:                            │  │   - Objective: binary                    │   |
|   │   - ERA5 boundary layer height               │  │   - scale_pos_weight = 7.67 (11.5% pos)  │   |
|   │   - 10m wind vector components (u, v)        │  │   - Evaluation Metric: PR-AUC (auc_pr)   │   |
|   │   - 2m air temp, surface pressure, RH        │  │ • Head 2: Count Regression               │   |
|   │   - Road network density (OpenStreetMap)     │  │   - Objective: tweedie (p = 1.45)        │   |
|   │   - Distance to major arteries (EDSA/C5)     │  │   - Resolves +7.54 skewness & 37.8% zeros│   |
|   │   - Static NDBI urban built-up index         │  │ • Input Features:                        │   |
|   │   - SRTM elevation & topographic roughness   │  │   - rainfall_lag_1w to rainfall_lag_4w   │   |
|   │ • Validation Strategy:                       │  │   - soil_moisture_lag_2w                 │   |
|   │   - Spatial Leave-One-Station-Out CV         │  │   - cumulative_rainfall_2w_to_4w         │   |
|   │     (Spatial LOSO-CV) to prevent spatial     │  │   - pm25_rolling_4w                      │   |
|   │     autocorrelation leakage.                 │  │   - uhi_seasonal_anomaly                 │   |
|   │ • Output: Gridded continuous PM2.5 surface   │  │   - mean_elev_m, pct_lowland, twi        │   |
|   │   with WHO 2021 guideline exceedance ratios. │  │ • Validation Strategy:                   │   |
|   │                                              │  │   - Walk-forward TimeSeriesSplit (k = 5) │   |
|   │                                              │  │ • Explainability Engine:                 │   |
|   │                                              │  │   - TreeSHAP computes local feature      │   |
|   │                                              │  │     attributions per municipal prediction│   |
|   └──────────────────────────────────────────────┘  └──────────────────────────────────────────┘   |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

### 4.1 Engine 2A: Spatial XGBoost Regressor (PM2.5 Downscaling)
- **Problem**: Fixed DENR-EMB stations are spatially sparse ($N=7$), leaving large residential swaths unmonitored.
- **Formulation**: Learns the non-linear transfer function between regional atmospheric dynamics, urban geometry, and local ground particulate concentration:
  $$\widehat{\text{PM}}_{2.5}(x, y, t) = f_{\text{XGBoost}}\Big(\mathbf{X}_{\text{synoptic}}(t), \ \mathbf{X}_{\text{reanalysis}}(x, y, t), \ \mathbf{X}_{\text{surface}}(x, y)\Big)$$
- **Spatial Cross-Validation**: Evaluated using Spatial Leave-One-Station-Out Cross-Validation (Spatial LOSO-CV). In each fold, all data from one physical station is held out completely to verify spatial interpolation fidelity across unmonitored LGUs.

### 4.2 Engine 2B: Lagged LightGBM Leptospirosis Risk Engine
- **Dual-Head Architecture**:
  1. **Surge Classification Head**: Directly targets the binary outbreak surge indicator $\mathbb{I}_{\{\text{Incidence} \ge 1.0\ \text{per } 100\text{k}\}}$. With an empirical class imbalance ratio of **$7.67 : 1$**, standard cross-entropy generates unacceptable false negatives. Enforcing `scale_pos_weight = 7.67` and tuning hyperparameter cutoffs on Precision-Recall AUC (`auc_pr`) ensures early detection of high-consequence disease surges.
  2. **Tweedie Count Regression Head**: Directly models the zero-inflated, fat-tailed case volume ($37.84\%$ zeros, $+7.54$ skewness, $73.78$ kurtosis) using a compound Poisson-Gamma distribution with variance power parameter $p = 1.45$.
- **Temporal Leakage Prevention**: Enforces strict walk-forward temporal cross-validation (`TimeSeriesSplit`, $k = 5$). Models trained on weeks $1 \dots t$ predict strictly on week $t+1$, mimicking operational deployment.
- **Explainability**: Integrated TreeSHAP computes Shapley values for each municipal prediction, outputting the exact percentage contribution of antecedent rainfall lags, soil moisture, and thermal priors to clinical users.

---

## 5. Subsystem 3: Decoupled RAG Knowledge & Action Advisory Engine

The Retrieval-Augmented Generation (RAG) subsystem acts as an automated, clinically grounded epidemiological advisor. It converts quantitative risk probabilities into actionable, role-tailored public health directives.

```
       SUBSYSTEM 3: DECOUPLED RAG KNOWLEDGE & ACTION ADVISORY ENGINE
+----------------------------------------------------------------------------------------------------+
| TRIGGER: INCOMING VALIDATED JSON RISK PAYLOAD                                                      |
| {                                                                                                  |
|   "lgu_id": "PH137402000", "lgu_name": "City of Malabon",                                         |
|   "risk_tier": "CRITICAL", "outbreak_surge_probability": 0.842,                                    |
|   "predicted_cases_tweedie": 18.4, "top_shap_drivers": {                                           |
|     "rainfall_lag_2w": 0.38, "soil_moisture_lag_2w": 0.22, "elev_m": 0.15                         |
|   }                                                                                                |
| }                                                                                                  |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| VECTOR DATABASE RETRIEVAL (ChromaDB / FAISS)                                                       |
| Embeddings: text-embedding-004 / BGE-small-en-v1.5                                                 |
| Filtered Query: "Leptospirosis Post-Exposure Prophylaxis Doxycycline Dosing Malabon high flood"    |
| Retrieved Curated Corpus Chunks:                                                                   |
| 1. DOH AO 2010-0018: Post-Exposure Prophylaxis (PEP) Protocol (Doxycycline 200mg single dose       |
|    within 24-48 hours for casual exposure; 200mg weekly for continuous exposure).                  |
| 2. WHO AirQ+ Protocol: Particulate exposure respiratory pre-conditioning threshold (> 35 µg/m³).   |
| 3. NKTI Clinical Practice Guideline: Staging emergency hemodialysis gymnasiums when municipal      |
|    outbreak score > 0.75; oliguria screening (< 0.5 mL/kg/h).                                      |
| 4. Republic Act 10121 & NDRRMC Guidelines: Lowland CAMANAVA mandatory evacuation and boot provision|
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| ROLE-BASED PROMPT ORCHESTRATION & SYNTHESIS (Gemini 1.5 Pro / Flash)                              |
| Strict Grounding Prompt: Synthesize directives ONLY from retrieved regulatory documents.           |
| Role-Specific Formatting:                                                                          |
| • City Health Officer (CHO): Clinical triage, Doxycycline stockpiling, dialysis bed escalation.     |
| • DRRM Officer (LDRRMO): Drainage gate clearing, PPE rubber boot distribution, shelter cooling.     |
| • Barangay Health Worker (BHW): Tagalog/English door-to-door prophylaxis mobilization script.       |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| OUTPUT: STRICT RAG ADVISORY PAYLOAD (Pydantic Validated JSON)                                      |
| Contains executive summary, prioritized action directives, clinical dosages, and exact citations. |
+----------------------------------------------------------------------------------------------------+
```

### Knowledge Base Corpus Inventory
The vector database indices authoritative regulatory, clinical, and scientific documents:
1. **Department of Health (DOH)**:
   - *Administrative Order No. 2010-0018*: Revised Guidelines on the Prevention and Management of Leptospirosis in the Philippines.
   - *DOH Memorandum No. 2024-0288*: Urgent Advisory on Doxycycline Post-Exposure Prophylaxis for Flooded Communities.
   - *PIDSR Surveillance Manual (3rd Edition)*: Case definitions for suspected, probable, and confirmed leptospirosis.
2. **World Health Organization (WHO)**:
   - *WHO Air Quality Guidelines (2021)*: Health risk thresholds for particulate matter ($\text{PM}_{2.5}$) and heat exposure.
   - *WHO Human Leptospirosis: Guidance for Diagnosis, Surveillance, and Control (2003)*.
3. **Tertiary Hospital Clinical Protocols**:
   - *National Kidney and Transplant Institute (NKTI)*: Emergency Hemodialysis Gymnasium Staging and Acute Kidney Injury Rapid Referral Protocol (2024).
4. **Statutory & Legal Frameworks**:
   - *Republic Act 10121*: Philippine Disaster Risk Reduction and Management Act of 2010.
   - *Republic Act 10173*: Data Privacy Act of 2012 (statutory cell suppression and confidentiality).

---

## 6. Subsystem 4: Responsive Streamlit Web Application

The user-facing presentation tier is built using Streamlit, Plotly, PyDeck, and Folium, delivering sub-2-second response times for municipal health officers and disaster planners.

```
+----------------------------------------------------------------------------------------------------+
|                         SUBSYSTEM 4: STREAMLIT WEB APPLICATION ARCHITECTURE                        |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [ TOP APP HEADER ]: Project Avatar | Metro Manila Multi-Hazard Health Intelligence Platform       |
|  [ CONTROLS ]: Temporal Horizon Slider (Historic Lags 1-4 | Forward 2-Week Early Warning Window)    |
|                                                                                                    |
|  ┌──────────────────────────────────────────────┐  ┌──────────────────────────────────────────┐   |
|  │ INTERACTIVE NCR LGU CHOROPLETH               │  │ LGU DEEP DIVE & EXPLAINABILITY PANEL     │   |
|  │ • Basemap: CartoDB DarkMatter / Positron     │  │ Selected: City of Malabon (CAMANAVA)     │   |
|  │ • Choropleth Layer: 17 LGU Polygons colored  │  │ • Current Status: CRITICAL RISK (Tier 4) │   |
|  │   by Risk Tier (Low, Moderate, High, Critical)│ │ • Outbreak Surge Prob: 84.2%             │   |
|  │ • Raster Layer Toggle:                       │  │ • Expected Cases: "<5" (Suppressed)      │   |
|  │   - 1km Downscaled PM2.5 Surface Heatmap     │  │                                          │   |
|  │   - Lowland Flood Depressions (SRTM < 5m,    │  │ TreeSHAP Feature Attribution Waterfall:   │   |
|  │     Slope < 0.8%, TWI > 13.5)                │  │ [Rainfall Lag 2w]    ████████████ (+38%) │   |
|  │ • Hover Tooltip: LGU Name, Pop. Density,     │  │ [Soil Moisture 2w]  ███████      (+22%) │   |
|  │   Dominant Environmental Drivers             │  │ [Lowland Elevation]  ████         (+15%) │   |
|  └──────────────────────────────────────────────┘  │ [PM2.5 Rolling 4w]   ███          (+11%) │   |
|                                                    └──────────────────────────────────────────┘   |
|                                                                                                    |
|  ┌────────────────────────────────────────────────────────────────────────────────────────────┐   |
|  │ DECISION SUPPORT & ACTION TRIGGER CONSOLE                                                  │   |
|  │ • Tab 1: Municipal Health Officer (Clinical Triage & Doxycycline Stockpile Estimator)      │   |
|  │ • Tab 2: Disaster Risk Reduction Officer (Drainage & Evacuation Zone Tasking)             │   |
|  │ • Tab 3: Barangay Health Worker Script (Tagalog / English Community Advisory)             │   |
|  │ • Action Button: [Generate Official LGU Health Advisory PDF / Export JSON Contract]        │   |
|  └────────────────────────────────────────────────────────────────────────────────────────────┘   |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

### Key UI Features & Guardrails
1. **Interactive Choropleth Engine**: Uses Mapbox / PyDeck vector rendering to display NCR municipal boundaries shaded by categorical risk tier, with instant layer toggling for the $1.0\ \text{km} \times 1.0\ \text{km}$ downscaled $\text{PM}_{2.5}$ raster and SRTM alluvial flood contours.
2. **Local Explainability**: For any selected LGU, renders an interactive Plotly horizontal bar chart displaying local TreeSHAP values, explaining *why* the municipality is elevated.
3. **Statutory Cell Suppression**: If the Tweedie regressor predicts a point case estimate between $1$ and $4$, the UI automatically displays `"<5"` and flags the statutory citation (*RA 10173 & Section 4.2 of data/README.md*).
4. **Performance Caching**: Employs `@st.cache_data` for GeoJSON boundaries, pre-computed Parquet matrices, and model weights, ensuring the UI remains snappy even under heavy user exploration.

---

## 7. End-to-End System Diagrams

### 7.1 Offline Model Training & Knowledge Indexing Pipeline

```mermaid
flowchart TD
    subgraph S1["1. Raw Multi-Source Data Ingestion"]
        A1["DENR-EMB PM2.5 Station Logs<br/>(7 Fixed NCR Stations)"]
        A2["DOST-PAGASA Synoptic Weather<br/>(Science Garden, Port Area, NAIA)"]
        A3["ERA5-Land Reanalysis<br/>(0.1° Climate & Soil Moisture)"]
        A4["SRTM 1-Arc-Second DEM<br/>(30m Elevation Baseline)"]
        A5["Landsat 8/9 TIRS & MODIS LST<br/>(Dry-Season Thermal Infrared)"]
        A6["DOH PIDSR Weekly Linelists<br/>(17 Municipal LGUs, 2023-2024)"]
        A7["PSA 2020 CPH & WorldPop<br/>(Population Density Grids)"]
    end

    subgraph S2["2. Offline Geospatial & Cleaning Pipeline"]
        B1["Grid Resampling & Alignment<br/>(Unified 1.0 km x 1.0 km Grid; 1,350 Cells)"]
        B2["Cloud-Mask Decoupling<br/>(Static Dry-Season SUHI Prior Extracted)"]
        B3["Sensor Imputation Engine<br/>(7-Day Rolling Median + Akima Spline)"]
        B4["Surveillance Delay Imputation<br/>(Onset = Admission - 4.0 Days; MAR Correction)"]
        B5["Topographic Wetness & Slope Derivation<br/>(SRTM DEM Slope < 0.8%, TWI > 13.5)"]
        B6["Distributed Lag Engine<br/>(Compute Lags 1-4w; Drop Lag 0; Soil Saturation)"]
        B7["Feature Store Export<br/>(analysis_matrix_ncr_eda.parquet)"]
    end

    subgraph S3["3. Tabular Machine Learning Training"]
        C1["Spatial XGBoost Training<br/>(PM2.5 Downscaling Regressor)"]
        C2["Spatial LOSO-CV Validation<br/>(Leave-One-Station-Out CV)"]
        C3["LightGBM Surge Classifier Training<br/>(scale_pos_weight = 7.67, PR-AUC Objective)"]
        C4["Tweedie Count Regressor Training<br/>(Poisson-Gamma Deviance, p = 1.45)"]
        C5["Walk-Forward TimeSeriesSplit<br/>(k = 5 Folds over 104 Weeks)"]
        C6["Model Artifact Serialization<br/>(xgboost_pm25.json, lightgbm_lepto.ubj)"]
    end

    subgraph S4["4. Regulatory Knowledge Indexing"]
        D1["Corpus Ingestion<br/>(DOH CPGs, WHO AirQ+, NKTI Protocols, RA 10173)"]
        D2["Document Chunking & Cleaning<br/>(Recursive Character Splitting; 512 Tokens)"]
        D3["Dense Vector Embedding<br/>(text-embedding-004 / BGE-small-en)"]
        D4["Vector Database Indexing<br/>(ChromaDB / FAISS Persistent Store)"]
    end

    A1 & A2 & A3 & A4 & A5 & A6 & A7 --> B1
    B1 --> B2 & B3 & B4 & B5
    B2 & B3 & B4 & B5 --> B6 --> B7
    B7 --> C1 & C3 & C4
    C1 --> C2 --> C6
    C3 & C4 --> C5 --> C6
    D1 --> D2 --> D3 --> D4
```

---

### 7.2 Online Real-Time Inference, RAG Retrieval & Alerting Pipeline

```mermaid
flowchart TD
    subgraph Ingest["1. Real-Time Environmental Ingestion"]
        E1["PAGASA Synoptic Weather Feed<br/>(Current Rain, Heat Index, Cyclone Warnings)"]
        E2["Open-Meteo / ECMWF Live Forecast<br/>(7-Day Numerical Weather Predictions)"]
        E3["Static Spatial Feature Store<br/>(DEM Lowlands, SUHI Thermal Anomaly Priors)"]
        E4["Historical Lag Buffer<br/>(Trailing 1-4 Weeks Rainfall & Soil Saturation)"]
    end

    subgraph FeatureEngine["2. Real-Time Feature Ingestion Engine"]
        F1["Input Payload Assembly<br/>(Validate via Pydantic GridCell & Municipal Schemas)"]
        F2["Rolling Telemetry Imputation<br/>(7-Day Rolling Median Filter)"]
        F3["Lag Feature Assembler<br/>(rainfall_lag_1w to 4w, soil_moisture_lag_2w)"]
    end

    subgraph MLEngine["3. Tabular ML Inference Microservice"]
        G1["Spatial XGBoost Evaluator<br/>(Generate Continuous 1km PM2.5 Grid Surface)"]
        G2["LightGBM Outbreak Surge Evaluator<br/>(Predict Municipal Outbreak Probability)"]
        G3["Tweedie Count Regressor Evaluator<br/>(Predict Raw Case Numbers)"]
        G4["TreeSHAP Explainer<br/>(Compute Top Feature Attribution Drivers)"]
        G5["RA 10173 Guardrail Engine<br/>(Apply k >= 5 Small Cell Suppression & Risk Tiers)"]
        G6["Composite Risk Payload Assembly<br/>(Pydantic CompositeRiskPayload Output)"]
    end

    subgraph RAGEngine["4. Decoupled RAG Knowledge Engine"]
        H1["Risk Assessment Ingestion<br/>(Accepts Strictly Formatted JSON Payload)"]
        H2["Vector Store Query Formulation<br/>(Targeted Clinical / Action Retrieval)"]
        H3["ChromaDB Semantic Retrieval<br/>(Top-k Relevant DOH, WHO, NKTI Protocol Chunks)"]
        H4["LLM Prompt Synthesis<br/>(Gemini 1.5 Pro / Flash Grounded Reasoning)"]
        H5["Advisory Payload Generation<br/>(Pydantic RAGAdvisoryResponse)"]
    end

    subgraph UIApp["5. Streamlit Frontline Decision UI"]
        I1["Interactive NCR LGU Choropleth<br/>(17 LGUs Shaded by Risk Tier)"]
        I2["1km PM2.5 Heatmap & Flood Contours<br/>(SRTM < 5m, Slope < 0.8% Overlay)"]
        I3["LGU Drilldown & SHAP Waterfall Panel<br/>(Explainable Driver Decomposition)"]
        I4["Action Advisory & Directives Console<br/>(MHO, LDRRMO, BHW Action Protocols)"]
        I5["Export Engine<br/>(One-Click PDF Directives & REST API)"]
    end

    E1 & E2 & E3 & E4 --> F1
    F1 --> F2 --> F3
    F3 --> G1 & G2 & G3
    G1 & G2 & G3 --> G4 --> G5 --> G6
    G6 --> H1
    H1 --> H2 --> H3 --> H4 --> H5
    G6 --> UIApp
    H5 --> UIApp
    UIApp --> I1 & I2 & I3 & I4 & I5
```

---

### 7.3 Decoupled Subsystem Interconnection & Contract Flow

```mermaid
flowchart LR
    subgraph DataPlane["Data & Feature Plane"]
        FP["Feature Pipeline<br/>(ETL, Resampling, Lagging)"]
        FS[("Feature Store<br/>(Parquet Files)")]
    end

    subgraph ComputePlane["Model & Knowledge Plane"]
        ML["Tabular ML Engines<br/>(XGBoost + LightGBM)"]
        RAG["RAG Advisory Engine<br/>(ChromaDB + Gemini)"]
    end

    subgraph ServingPlane["Presentation Plane"]
        UI["Streamlit Application<br/>(Choropleths, SHAP, Triggers)"]
    end

    FP -->|Batch Write| FS
    FS -->|Read Features| ML
    ML -->|"CompositeRiskPayload (JSON)"| RAG
    ML -->|"Inference & SHAP (JSON)"| UI
    RAG -->|"RAGAdvisoryResponse (JSON)"| UI
```

---

## 8. Operational Performance, Security & Regulatory Specifications

### 8.1 Performance & Latency Budgets
- **Feature Preprocessing**: Offline batch execution takes $< 4.5\ \text{minutes}$ for 104 weeks of data across 1,350 grid cells.
- **Online Tabular Inference**: XGBoost continuous 1km surface ($1,350$ cells) + LightGBM 17-LGU dual-head inference executes in **$< 180\ \text{milliseconds}$**.
- **Vector Retrieval**: ChromaDB similarity search (Top-$4$ chunks) completes in **$< 45\ \text{milliseconds}$**.
- **RAG Generation**: Gemini 1.5 Flash stream generation completes in **$< 1.8\ \text{seconds}$**.
- **Total End-to-End Latency**: Sub-2-second target strictly satisfied from UI trigger to render.

### 8.2 Security, Anonymization & Data Privacy Safeguards (RA 10173)
- **Air-Gapped Patient Records**: Individual patient records are never uploaded, committed to version control, or exposed over API endpoints.
- **Mandatory $k$-Anonymity Cell Suppression**: Any spatial-temporal cell reporting $1 \le n < 5$ cases is automatically suppressed and displayed as `"<5"`.
- **Cryptographic Provenance**: All raw environmental downloads are hashed upon receipt using SHA-256 (`data/raw/checksums.sha256`).

---

## 9. References (Strict APA 7th Edition)

Centers for Disease Control and Prevention. (2024). *Leptospirosis clinical guidance*. U.S. Department of Health and Human Services. https://www.cdc.gov/leptospirosis/

Department of Health. (2010). *Administrative Order No. 2010-0018: Revised guidelines on the prevention and management of leptospirosis in the Philippines*. Department of Health, Republic of the Philippines. https://doh.gov.ph/

Department of Health. (2023). *Philippine integrated disease surveillance and response: System overview and operational manual*. Epidemiology Bureau, Department of Health, Republic of the Philippines. https://doh.gov.ph/

Department of Health. (2024). *Memorandum No. 2024-0288: Urgent advisory on doxycycline post-exposure prophylaxis for flooded communities*. Department of Health, Republic of the Philippines. https://doh.gov.ph/

Matsushita, N., Ng, C. F. S., Kim, Y., Suzuki, M., Saito, M., Ariyoshi, K., Salva, E. P., Dimaano, E. M., & Hashizume, M. (2018). The non-linear and lagged short-term relationship between rainfall and leptospirosis and the intermediate role of floods in the Philippines. *PLOS Neglected Tropical Diseases*, 12(4), Article e0006331. https://doi.org/10.1371/journal.pntd.0006331

National Kidney and Transplant Institute. (2024). *Public advisory: Surge in post-typhoon leptospirosis admissions and emergency hemodialysis staging*. NKTI Information Office. https://nkti.gov.ph/

Philippine Atmospheric, Geophysical and Astronomical Services Administration. (2024). *Manual of meteorological observation practices in the Philippines*. Department of Science and Technology. https://bagong.pagasa.dost.gov.ph/

Republic of the Philippines. (2010). *Republic Act No. 10121: Philippine Disaster Risk Reduction and Management Act of 2010*. Official Gazette of the Republic of the Philippines. https://www.officialgazette.gov.ph/2010/05/27/republic-act-no-10121/

Republic of the Philippines. (2012). *Republic Act No. 10173: Data Privacy Act of 2012*. Official Gazette of the Republic of the Philippines. https://www.officialgazette.gov.ph/2012/08/15/republic-act-no-10173/

World Health Organization. (2003). *Human leptospirosis: Guidance for diagnosis, surveillance and control*. World Health Organization. https://apps.who.int/iris/handle/10665/42667

World Health Organization. (2021). *WHO global air quality guidelines: Particulate matter (PM2.5 and PM10), ozone, nitrogen dioxide, sulfur dioxide and carbon monoxide*. World Health Organization. https://apps.who.int/iris/handle/10665/345329
