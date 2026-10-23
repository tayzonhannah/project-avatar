# Project Avatar: Empirical Ground Truth & Exploratory Data Analysis (EDA) Findings
**Lead Data Scientist**, Project Avatar  
**Philippine Junior Data Science Challenge (PJDSC) 2026**  
**Document Identifier:** `docs/EDA_FINDINGS.md`  
**Associated Executable Notebook:** [`notebooks/01_eda_and_cleaning.ipynb`](../notebooks/01_eda_and_cleaning.ipynb)  
**Execution Environment:** Python 3.13 (`random_state=42` globally enforced)  
**Date of Audit:** October 2026  
**Statutory & Ethical Compliance:** Republic Act 10173 (Data Privacy Act of 2012) & PJDSC Competition Rubric (Sections 1.2, 1.3, 2.1)

---

## 1. Executive Summary & Analytical Mandate

Before designing system architecture or deploying machine learning pipelines for Project Avatar, empirical ground truth must be derived directly from exploratory data analysis. This monograph synthesizes the empirical findings produced by executing `notebooks/01_eda_and_cleaning.ipynb` across multi-source epidemiological registries, atmospheric particulate monitors, synoptic weather logs, climate reanalysis grids, satellite thermal products, and digital elevation models over the National Capital Region (NCR) of the Philippines.

```
+----------------------------------------------------------------------------------------------------+
|                         PROJECT AVATAR: EMPIRICAL PARAMETER DISCOVERY DASHBOARD                     |
+--------------------------+---------------------------------+---------------------------------------+
| Domain Dimension         | Discovered Empirical Parameter  | Downstream System / ML Action         |
+--------------------------+---------------------------------+---------------------------------------+
| Spatial Bounding Box     | [120.85°E, 14.35°N,             | Unified 1.0 km x 1.0 km analysis grid |
| & Coordinate Systems     |  121.15°E, 14.80°N]             | 30 columns x 45 rows = 1,350 cells    |
|                          | EPSG:4326 (Store) / 32651 (UTM) | Bilinear & bicubic downscaling        |
+--------------------------+---------------------------------+---------------------------------------+
| Primary Lag Window       | Lag 2 Weeks: r = 0.6267         | Feed rainfall_lag_2w &                |
| (Peak Cross-Correlation) | Lag 3 Weeks: r = 0.5477         | rainfall_lag_3w as dominant features  |
|                          | (p < 10^-8; Bartlett ±0.192)    | Instantaneous Lag 0 dropped (p=0.134) |
+--------------------------+---------------------------------+---------------------------------------+
| Surveillance Latency     | Median: 15.0 days               | Decoupled anticipatory architecture:  |
| (Clinical & Admin Lag)   | IQR: 11 - 20 days; p90: 25.0 d  | Issue warnings 2-3 weeks before DOH   |
|                          | Severe right skew (tail > 35 d) | central registry reflects cases       |
+--------------------------+---------------------------------+---------------------------------------+
| Missingness Dynamics     | Baseline: 3.43% (MCAR)          | 7-day rolling median / Akima spline;  |
|                          | Crisis Surge: 22.50% (MAR)      | Landsat thermal used as dry baseline  |
|                          | Monsoon Clouds: 68.0% masked    | (never live optical during cyclones)  |
+--------------------------+---------------------------------+---------------------------------------+
| Target Skewness &        | Skewness: +7.54; Kurtosis: 73.78| LightGBM scale_pos_weight = 7.67;     |
| Class Imbalance          | Outbreak Surge Imbalance: 7.67:1| Tweedie count regression (p = 1.45)   |
|                          | Zero-inflation: 37.84%          | Mandatory RA 10173 cell suppression   |
+--------------------------+---------------------------------+---------------------------------------+
```

---

## 2. Spatial Profiling, Resolution & Alignment Specifications

### 2.1 Coordinate Reference Systems (CRS) & Grid Transformation
Public health registries and environmental sensors in the Philippines use disparate spatial frameworks that cannot be naively joined without spatial distortion.

```
       MULTI-SENSOR SPATIAL ALIGNMENT & RESAMPLING SPECIFICATIONS
+-----------------------+-------------+------------------+-----------------+-----------------------+
| Dataset               | Native CRS  | Native Res.      | Target Res.     | Resampling Protocol   |
+-----------------------+-------------+------------------+-----------------+-----------------------+
| SRTM DEM              | EPSG:4326   | 1 arc-sec (~30m) | 1.0 km x 1.0 km | Area-weighted average |
| Landsat 8/9 TIRS LST  | EPSG:32651  | 100m resamp. 30m | 1.0 km x 1.0 km | Area-weighted mean    |
| MODIS LST (MOD11A1)   | Sinusoidal  | 1.0 km x 1.0 km  | 1.0 km x 1.0 km | Nearest-neighbor/grid |
| ERA5-Land Reanalysis  | EPSG:4326   | 0.1° (~9.0 km)   | 1.0 km x 1.0 km | Bicubic spline interp |
| DENR-EMB PM2.5        | EPSG:4326   | Point (7 stns)   | 1.0 km x 1.0 km | IDW / Zonal centroid  |
| DOH PIDSR Weekly Reg. | EPSG:4326   | Vector (17 LGUs) | LGU Boundaries  | Zonal aggregation     |
+-----------------------+-------------+------------------+-----------------+-----------------------+
```

- **Standard Storage CRS**: `EPSG:4326` (WGS 84 geographic latitude/longitude).
- **Standard Metric Analysis CRS**: `EPSG:32651` (WGS 84 / UTM Zone 51N). Projected coordinates must be used for Euclidean buffer computations, hydrologic distance to river channels, and slope calculations to eliminate latitudinal distortion ($1^\circ\ \text{lat} \approx 110.6\ \text{km}$, $1^\circ\ \text{lon at } 14.6^\circ\text{N} \approx 107.5\ \text{km}$).
- **Exact Metro Manila Spatial Bounding Box**:
  $$\text{Bounding Box} = \left[ \text{Min Lon}: 120.85^\circ\text{E}, \ \text{Min Lat}: 14.35^\circ\text{N}, \ \text{Max Lon}: 121.15^\circ\text{E}, \ \text{Max Lat}: 14.80^\circ\text{N} \right]$$
  - Longitudinal span: $0.30^\circ \approx 32.25\ \text{km}$.
  - Latitudinal span: $0.45^\circ \approx 49.77\ \text{km}$.
  - Target Grid Geometry: $30\ \text{columns} \times 45\ \text{rows} = 1,350\ \text{cells}$ at $1.0\ \text{km} \times 1.0\ \text{km}$ resolution.

### 2.2 Topographic Vulnerability & Drainage Depressions
Topographic profiling from the 1-arc-second SRTM DEM reveals extreme vulnerability concentrated along specific hydrological basins:
- **Mean Elevation across NCR**: $14.8\ \text{meters}$ above mean sea level (ASL), but with extreme local variance:
  - **CAMANAVA Coastal Plain** (*Caloocan, Malabon, Navotas, Valenzuela*): Mean elevation $1.8\text{--}3.8\ \text{m}$ ASL.
  - **Historic Port & Estero Belt** (*City of Manila, Pasay*): Mean elevation $3.2\text{--}3.5\ \text{m}$ ASL.
  - **Marikina River Lowland Floodplain**: Mean elevation $7.4\ \text{m}$ ASL, flanked by the elevated Quezon City Plateau ($38.5\ \text{m}$ ASL).
- **Slope Gradients**: The CAMANAVA corridor, Manila bayfront, and Marikina valley exhibit mean slope gradients **$\overline{\text{Slope}} < 0.8\%$** (with Navotas at $0.2\%$ and Malabon at $0.3\%$). This sluggish gradient inhibits gravity drainage, driving the **Topographic Wetness Index (TWI)** above $13.5\text{--}14.8$, creating permanent standing water reservoirs for pathogenic *Leptospira interrogans*.

### 2.3 Remote Sensing Cloud Occlusion Failure Mode
A critical spatial-temporal insight discovered during EDA is the failure of optical and thermal satellite sensors during tropical cyclones:
- **Dry Season Cloud Masking (March–May)**: Pixel null rate of **$12.7\%$**. Thermal infrared retrieval from Landsat 8/9 and MODIS accurately captures Surface Urban Heat Island (SUHI) anomalies ($+3.2^\circ\text{C}\text{--}+7.1^\circ\text{C}$ in central Manila and Caloocan).
- **Monsoon Season Cloud Masking (June–November)**: Pixel null rate jumps to **$68.0\%$**, with heavy overcast skies blocking surface thermal emission during the exact weeks of cyclone landfall.
- **Architectural Directive**: **Never attempt real-time satellite LST or optical flood detection inside live disaster alerting pipelines.** Instead, static dry-season SUHI anomaly maps must be pre-computed as baseline seasonal vulnerability priors ($\Phi_{\text{thermal}}$).

---

## 3. Temporal Lag Dynamics & Epidemiological Cross-Correlations

### 3.1 Empirical Cross-Correlation Function (CCF) Analysis
To rigorously validate the **Compounding Hazard Hypothesis**, Cross-Correlation Functions (CCF) were computed across $104$ continuous epidemiological weeks (2023-W01 to 2024-W52) between hydrometeorological predictors and DOH-reported leptospirosis cases.

With sample size $N = 104$ weeks, Bartlett’s $95\%$ white-noise statistical significance bound is:
$$\text{Threshold}_{95\%} = \pm \frac{1.96}{\sqrt{N}} = \pm \frac{1.96}{\sqrt{104}} \approx \pm 0.1922$$

```
   CROSS-CORRELATION FUNCTION (CCF): ENVIRONMENTAL PREDICTORS VS LEPTOSPIROSIS CASES
+-----------+-------------------+--------------------+--------------------+-------------------+-----------------------+
| Lag (wks) | Pearson r (Rain)  | p-value (Rain)     | 95% CI (Rain)      | Pearson r (Soil)  | Statistical Status    |
+-----------+-------------------+--------------------+--------------------+-------------------+-----------------------+
| Lag 0     | 0.1480            | 1.34e-01           | [-0.046, +0.331]   | 0.2256            | Not Significant       |
| Lag 1     | 0.4048            | 2.22e-05           | [+0.231, +0.554]   | 0.3285            | Significant (p<0.001) |
| Lag 2     | 0.6267            | 1.83e-12           | [+0.493, +0.732]   | 0.4041            | Peak Outbreak Surge   |
| Lag 3     | 0.5477            | 3.07e-09           | [+0.395, +0.671]   | 0.3545            | Sustained Organ Damage|
| Lag 4     | 0.2927            | 3.12e-03           | [+0.103, +0.462]   | 0.2382            | Significant (p<0.01)  |
| Lag 5     | 0.1397            | 1.68e-01           | [-0.059, +0.327]   | 0.1890            | Not Significant       |
| Lag 6     | 0.1129            | 2.68e-01           | [-0.086, +0.303]   | 0.2078            | Not Significant       |
| Lag 7     | 0.1099            | 2.84e-01           | [-0.090, +0.301]   | 0.2177            | Not Significant       |
| Lag 8     | 0.0894            | 3.86e-01           | [-0.111, +0.282]   | 0.1890            | Not Significant       |
+-----------+-------------------+--------------------+--------------------+-------------------+-----------------------+
```

```
               CROSS-CORRELATION FUNCTION PROFILE (r vs. Lag Weeks)
   r
 +0.80 |
 +0.70 |                     * Peak (Lag 2: r=0.627)
 +0.60 |                           * (Lag 3: r=0.548)
 +0.50 |               * (Lag 1: r=0.405)
 +0.40 |                                       * (Lag 4: r=0.293)
 +0.30 |
 +0.20 | - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Bartlett Threshold (r=0.192)
 +0.10 |       * (Lag 0: r=0.148)                          *       *
  0.00 +-------+-------+-------+-------+-------+-------+-------+-------+--> Lag (Weeks)
           0       1       2       3       4       5       6       7       8
```

### 3.2 Epidemiological Interpretation & Downstream Feature Selection
1. **The Instantaneous Paradox (Lag 0)**:
   - Instantaneous correlation between rainfall and cases is **statistically non-significant** ($r = 0.1480, p = 0.134$). During typhoon week ($\tau = 0$), residents are actively displaced, roads are submerged, and bacteria are merely inoculating mucous membranes.
   - **Directive**: ML models that prioritize instantaneous precipitation will fail to predict outbreaks.
2. **The Biological Incubation Peak (Lag 2)**:
   - Correlation reaches its absolute peak at **Lag 2 weeks ($r = 0.6267, p = 1.83 \times 10^{-12}$)**.
   - Matches pathogen kinetics: median biological incubation is $7\text{--}14\ \text{days}$ (WHO, 2003), followed by Phase 1 leptospiremia and initial healthcare presentation.
3. **The Clinical Hospitalization Peak (Lag 3)**:
   - Correlation remains strongly elevated at **Lag 3 weeks ($r = 0.5477, p = 3.07 \times 10^{-9}$)**.
   - Aligns with the transition to Phase 2 immune-mediated organ destruction (Weil’s syndrome, oliguria, pulmonary hemorrhage) and tertiary emergency room admission (NKTI, San Lazaro Hospital).
4. **The Diagnostic & Reporting Residue (Lag 4)**:
   - Statistically significant correlation persists into **Lag 4 weeks ($r = 0.2927, p = 0.0031$)**, capturing batch laboratory confirmation delays (MAT/IgM) and institutional consolidation backlogs.
5. **Soil Moisture Saturation Dynamics**:
   - ERA5 volumetric soil moisture exhibits peak correlation at **Lag 2 weeks ($r = 0.4041, p = 2.53 \times 10^{-5}$)** and maintains positive correlation through Lag 4 ($r = 0.2382$). Saturated soil prevents floodwater infiltration, prolonging microbial viability in muddy residential alleys.
6. **Required Downstream Feature Specifications**:
   - `rainfall_lag_2w` (Primary trigger feature)
   - `rainfall_lag_3w` (Hospital admission surge feature)
   - `rainfall_lag_4w` (Surveillance consolidation feature)
   - `soil_moisture_lag_2w` (Ground saturation feature)
   - `cumulative_rainfall_2w_to_4w` (Integrated rolling surge feature)

---

## 4. Surveillance Hygiene, Reporting Latencies & Imputation Rules

### 4.1 Linelist Latency Decomposition
Analysis of $3,541$ case records in the DOH surveillance linelist sample reveals the anatomical breakdown of surveillance delay:

```
                  SURVEILLANCE LATENCY EMPIRICAL DISTRIBUTION
+---------------------------------------+-----------+----------+-----------+-----------+-----------+
| Surveillance Latency Phase            | Mean (d)  | Std (d)  | p50 (Med) | p90 (d)   | p95 (d)   |
+---------------------------------------+-----------+----------+-----------+-----------+-----------+
| 1. Clinical Presentation Lag (Onset)  | 5.03 d    | 3.22 d   | 4.0 d     | 9.0 d     | 11.0 d    |
| 2. Diagnostic & Administrative Lag    | 10.98 d   | 4.88 d   | 10.0 d    | 17.0 d    | 20.0 d    |
| 3. Total End-to-End Surveillance Lag  | 16.01 d   | 5.86 d   | 15.0 d    | 25.0 d    | 29.0 d    |
+---------------------------------------+-----------+----------+-----------+-----------+-----------+
```

- **Median Total Surveillance Lag**: **$15.0\ \text{days}$** (IQR: $11\text{--}20\ \text{days}$).
- **Extreme Right Tail**: $10\%$ of cases experience latency $\ge 25.0\ \text{days}$, and $5\%$ exceed $29.0\ \text{days}$.
- **Operational Reality**: In Philippine public health, central disease registries are permanently retrospective. By the time a municipal case surge is officially logged in DOH-EB bulletins, hemodialysis beds at NKTI are already saturated.
- **Architectural Directive**: Project Avatar must implement a **Decoupled Anticipatory Warning Engine**: live weather feeds (PAGASA, Open-Meteo) trigger forward-looking risk alerts $14\text{--}21\ \text{days}$ in advance of official registry updates.

### 4.2 Missingness Mechanism: MCAR vs. MAR
Surveillance data hygiene was audited across baseline conditions versus post-cyclone outbreak surges:
- **Baseline Routine Surveillance**:
  - Missing symptom onset dates: **$3.43\%$** (consistent with Missing Completely at Random [MCAR] due to transcription errors).
  - Mean reporting delay: $9.5\ \text{days}$.
- **Outbreak Surge Crisis (Typhoons Carina & Kristine)**:
  - Missing symptom onset dates surged to **$22.50\%$**.
  - Mean reporting delay expanded to $16.8\ \text{days}$.
- **Statistical Independence Test**:
  $$\chi^2 = 284.62, \quad \text{degrees of freedom} = 1, \quad p < 10^{-60}$$
- **Verdict**: Missingness in Philippine disease surveillance is **strictly Missing at Random (MAR)**, conditioned on outbreak intensity and clinical caseload saturation. Deleting rows with missing onset dates introduces severe survivorship and selection bias.

### 4.3 Imputation Strategy Benchmarking
Imputation rules were evaluated on continuous environmental telemetry (DENR-EMB $\text{PM}_{2.5}$ station series) by simulating $20\%$ artificial gaps:

```
               SLIDING-WINDOW IMPUTATION BENCHMARK RESULTS
+-------------------------------+---------------+---------------+-----------------------+
| Imputation Strategy           | MAE (µg/m³)   | RMSE (µg/m³)  | Pearson Corr. (r)     |
+-------------------------------+---------------+---------------+-----------------------+
| Trailing 14-Day Rolling Mean  | 5.547 µg/m³   | 6.796 µg/m³   | 0.8263                |
| Trailing 7-Day Rolling Median | 5.634 µg/m³   | 6.812 µg/m³   | 0.8278 (Optimal)      |
| Linear Spline Interpolation   | 6.201 µg/m³   | 7.685 µg/m³   | 0.7809                |
| Forward Fill (LOCF)           | 6.484 µg/m³   | 8.361 µg/m³   | 0.7546                |
+-------------------------------+---------------+---------------+-----------------------+
```

- **Recommended Imputation Protocols**:
  1. **Continuous Telemetry (PM2.5, Rainfall)**: Deploy a **Trailing 7-Day Rolling Median** for operational robustness against sensor spikes, with Akima cubic spline interpolation for short telemetry gaps ($\le 3\ \text{hours}$).
  2. **Surveillance Linelist (Onset Dates)**: Impute missing onset dates using **Admission Date minus Empirical Median Clinical Lag ($4.0\ \text{days}$)**, preserving epidemiological consistency.

---

## 5. Target Skewness, Class Imbalance & Machine Learning Directives

### 5.1 Target Distribution Profile & Zero-Inflation
Across all $1,768$ municipal-week observations ($17\ \text{LGUs} \times 104\ \text{weeks}$):
- **Mean Cases per Week**: $5.04$
- **Median Cases per Week**: $2.00$
- **Standard Deviation**: $8.68$
- **Skewness Coefficient**: **$+7.54$** (extreme positive right skew)
- **Kurtosis**: **$73.78$** (leptokurtic, fat-tailed distribution)
- **Zero-Inflation Rate**: **$37.84\%$** of municipal-weeks report zero cases.
- **Small Cell Count Rate ($1 \le n < 5$)**: **$45.76\%$** of municipal-weeks report fewer than 5 cases.

```
                    TARGET DISTRIBUTION: WEEKLY REPORTED CASES
   Density
    ^
    |  * (Zero count: 37.8%)
    |  *
    |  * * (1-4 cases: 45.8%)
    |  * * *
    |  * * * *
    |  * * * * *
    |  * * * * * *
    |  * * * * * * *   (Outbreak tail > 20 cases: 3.2%)
    +------------------------------------------------------------> Cases
       0   2   4   6   8  10  12  14  16  18  20  25  30  40  50+
```

### 5.2 Regulatory Disclosure Thresholds (Republic Act 10173)
Because **$45.76\%$** of municipal-week cells contain $1$ to $4$ cases, strict adherence to Section 4.2 of `data/README.md` and RA 10173 is mandatory:
- In any municipal-temporal reporting cell where $1 \le n_{\text{cases}} < 5$, the raw count must be **suppressed or pooled** to prevent re-identification attacks ($k \ge 5$).
- Downstream public dashboards and mobile endpoints must report categorical risk tiers (*Low*, *Moderate*, *High*, *Critical*) rather than disaggregated small integer counts.

### 5.3 Class Imbalance & LightGBM Parameterization
When formulating outbreak prediction as a binary early warning classification task (Outbreak Surge Target: Weekly Municipal Incidence $\ge 1.0$ per $100,000$ population):
- **Negative Class (Non-Surge Weeks)**: $1,564$ observations ($88.46\%$)
- **Positive Class (Outbreak Surge Weeks)**: $204$ observations ($11.54\%$)
- **Class Imbalance Ratio**:
  $$\text{Imbalance Ratio} = \frac{N_{\text{neg}}}{N_{\text{pos}}} = \frac{1564}{204} \approx 7.67 : 1$$

#### Downstream Hyperparameter Directives for LightGBM & XGBoost:
1. **Binary Classification (`objective: "binary"`)**:
   - `scale_pos_weight = 7.67` (strictly enforced to penalize false negatives during disease surges).
   - `metric = "auc_pr"` (Precision-Recall AUC / Average Precision) rather than ROC-AUC or accuracy.
2. **Count Regression (`objective: "tweedie"` or `"poisson"`)**:
   - Standard Mean Squared Error (MSE) will fail due to skewness $+7.54$ and $37.8\%$ zeros.
   - Use **Tweedie loss** with variance power $p \in [1.3, 1.6]$, or a **Zero-Inflated Negative Binomial (ZINB)** model to handle compound Poisson dispersion.

---

## 6. Downstream System Architecture & Feature Store Handoff

The features generated during this EDA have been validated and exported to:
- **Cleaned Parquet Feature Matrix**: `data/processed/analysis_matrix_ncr_eda.parquet` ($1,768\ \text{rows} \times 30\ \text{columns}$)
- **Machine-Readable Metadata**: `data/processed/eda_summary_metrics.json`
- **Visualization Artifacts**: `data/processed/*.png`

```
                                FEATURE STORE CONTRACT
+-----------------------------+-------------------+---------------------------------------------------+
| Feature Identifier          | Data Type         | Biological / Operational Role                     |
+-----------------------------+-------------------+---------------------------------------------------+
| rainfall_lag_2w             | float64 (mm)      | Peak biological incubation trigger (r = 0.627)    |
| rainfall_lag_3w             | float64 (mm)      | Peak hospitalization & organ failure (r = 0.548)  |
| rainfall_lag_4w             | float64 (mm)      | Sustained surveillance reporting lag (r = 0.293)  |
| soil_moisture_lag_2w        | float64 (m³/m³)   | Flood persistence & puddle saturation (r = 0.404) |
| pm25_rolling_4w             | float64 (µg/m³)   | Chronic baseline pulmonary vulnerability prior    |
| uhi_anomaly                 | float64 (°C)      | Pre-monsoon thermal dehydration stress index      |
| elev_m                      | float64 (m ASL)   | Lowland flooding vulnerability (< 5m indicator)   |
| slope_pct                   | float64 (%)       | Drainage sluggishness (< 1.0% indicator)          |
| twi                         | float64           | Topographic Wetness Index (water accumulation)    |
| outbreak_surge_target       | int64 (0 or 1)    | Ground truth binary early warning classification  |
+-----------------------------+-------------------+---------------------------------------------------+
```

---

## 7. References (Strict APA 7th Edition)

Centers for Disease Control and Prevention. (2024). *Leptospirosis clinical guidance*. U.S. Department of Health and Human Services. https://www.cdc.gov/leptospirosis/

Department of Environment and Natural Resources. (2020). *Administrative Order No. 2020-14: Revised national ambient air quality guideline values for particulate matter 2.5 (PM2.5)*. DENR Environmental Management Bureau. https://air.emb.gov.ph/wp-content/uploads/2020/07/DAO-2020-14-PM2.5.pdf

Department of Health. (2023). *Philippine integrated disease surveillance and response: Annual surveillance bulletin 2023*. Epidemiology Bureau, Department of Health, Republic of the Philippines. https://doh.gov.ph/

Department of Health. (2024). *Press release: DOH reports surge in leptospirosis admissions in NCR following tropical cyclone Carina and southwest monsoon*. Department of Health, Republic of the Philippines. https://doh.gov.ph/

Matsushita, N., Ng, C. F. S., Kim, Y., Suzuki, M., Saito, M., Ariyoshi, K., Salva, E. P., Dimaano, E. M., & Hashizume, M. (2018). The non-linear and lagged short-term relationship between rainfall and leptospirosis and the intermediate role of floods in the Philippines. *PLOS Neglected Tropical Diseases*, 12(4), Article e0006331. https://doi.org/10.1371/journal.pntd.0006331

Philippine Atmospheric, Geophysical and Astronomical Services Administration. (2024). *Climatological extremes and heat index monitoring summary for Metro Manila stations*. Department of Science and Technology. https://bagong.pagasa.dost.gov.ph/climate/heat-index

Philippine Statistics Authority. (2021). *2020 census of population and housing (2020 CPH) population counts declared official by the President: National Capital Region*. Philippine Statistics Authority. https://psa.gov.ph/

Republic of the Philippines. (2012). *Republic Act No. 10173: Data Privacy Act of 2012*. Official Gazette of the Republic of the Philippines. https://www.officialgazette.gov.ph/2012/08/15/republic-act-no-10173/

World Health Organization. (2003). *Human leptospirosis: Guidance for diagnosis, surveillance and control*. World Health Organization. https://apps.who.int/iris/handle/10665/42667

World Health Organization. (2021). *WHO global air quality guidelines: Particulate matter (PM2.5 and PM10), ozone, nitrogen dioxide, sulfur dioxide and carbon monoxide*. World Health Organization. https://apps.who.int/iris/handle/10665/345329
