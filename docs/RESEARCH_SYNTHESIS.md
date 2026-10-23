# Project Avatar: Epidemiological Baseline, Compounding Environmental Hazards, and Problem Synthesis for Metro Manila

**Lead Epidemiological Researcher**, Project Avatar  
**Philippine Junior Data Science Challenge (PJDSC) 2026**  
**Document Classification:** Foundational Epidemiological Monograph  
**Publication Date:** October 2026  

---

## 1. Executive Summary & Problem Formulation

Megacity Metro Manila (the National Capital Region [NCR] of the Philippines)—encompassing 16 highly urbanized cities and one municipality across an area of $619.57\ \text{km}^2$—houses over $13.48\ \text{million}$ residents, yielding an average population density exceeding $21,700\ \text{people/km}^2$ (Philippine Statistics Authority [PSA], 2021). This dense urban fabric represents one of the most ecologically strained and climate-vulnerable metropolitan landscapes in Southeast Asia. 

Historically, public health surveillance in the Philippines has operated in institutional and methodological silos. Infectious disease registries maintained by the Department of Health (DOH) Epidemiology Bureau track waterborne and zoonotic surges as isolated clinical events. Concurrently, atmospheric particulate monitors operated by the Department of Environment and Natural Resources Environmental Management Bureau (DENR-EMB) and hydrometeorological stations managed by the Philippine Atmospheric, Geophysical and Astronomical Services Administration (PAGASA) log environmental extremes independently. Consequently, municipal Local Government Units (LGUs) and tertiary healthcare networks are continuously caught off-guard by **cascading, compound environmental health shocks**.

```
+----------------------------------------------------------------------------------------------------+
|                               THE COMPOUNDING MULTI-HAZARD PARADIGM                                |
+----------------------------------------------------------------------------------------------------+
|  Phase 1: Dry-to-Wet Thermal Transition (March - May)                                              |
|  - Extreme Heat Waves (PAGASA Heat Index > 42°C - 48°C)                                            |
|  - High Surface Urban Heat Island (UHI LST Anomalies: +3°C to +7°C)                                |
|  - Chronic Fine Particulate Exposure (PM2.5 > 3-7x WHO 2021 Guideline)                             |
|  --> Pathophysiological Impact: Chronic subclinical dehydration, microvascular dysfunction,        |
|      pulmonary mucosal inflammation, baseline renal tubular stress.                                |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
|  Phase 2: Acute Tropical Cyclogenesis & Monsoon Inundation (June - October)                        |
|  - Extreme Monsoonal Rainfall (Habagat) & Severe Cyclones (e.g., Carina, Kristine, Ondoy)          |
|  - Severe Flash Flooding in Flat Lowlands (SRTM DEM < 5m Elevation, Slope < 1%)                   |
|  - Rodent Reservoir Flush (Rattus norvegicus urinary shedding of Leptospira interrogans)          |
|  --> Environmental Exposure: Prolonged wading in septic, pathogen-dense urban standing waters.    |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
|  Phase 3: The 1 to 4-Week Distributed Lag Epidemiological Surge (July - December)                  |
|  - Pathogen Incubation Window (Empirical Peak at Lag 2: r = 0.627, p < 10^-11)                     |
|  - Clinical Deterioration & Hospitalization Peak (Lag 3: r = 0.548, p < 10^-8; Weil's syndrome/AKI)|
|  - Institutional Surveillance Reporting Lag (Empirical Median Total Latency: 15.0 days; MAR mechanism)|
|  --> Severe Outcome: Fulminant Leptospirosis, Acute Kidney Injury (AKI), Dialysis Bed Saturation  |
|      at NKTI & San Lazaro Hospital, Persistent Elevated Case Fatality Rate (CFR: 8% - 12%).       |
+----------------------------------------------------------------------------------------------------+
```

This research synthesis establishes an authoritative, empirically grounded baseline across three interconnected environmental health axes in Metro Manila:
1. **Waterborne Zoonoses**: Endemic and epidemic leptospirosis (*Leptospira interrogans*) characterized by persistent, elevated Case Fatality Rates (CFR: $8\%\text{--}12\%$) and severe acute kidney injury (AKI).
2. **Atmospheric Particulate Pollution**: Ambient fine particulate matter ($\text{PM}_{2.5}$) levels chronically breaching the World Health Organization (WHO) 2021 guidelines by $300\%\text{--}760\%$, driving underlying cardiopulmonary morbidity.
3. **Thermal Extremes & Urban Heat Islands (UHI)**: Unprecedented heat indices ($42^\circ\text{C}\text{--}48^\circ\text{C}$) exacerbating systemic cardiovascular and renal vulnerability in outdoor laborers and high-density informal settlements.

We formalize the **Compounding Hazard Hypothesis**, demonstrating that post-typhoon leptospirosis surges cannot be understood or mitigated through rainfall alone. Rather, they represent a non-linear, multi-week distributed lag cascade conditioned by prior thermal stress, drainage topography, and socioeconomic vulnerability.

---

## 2. Public Health Burden Synthesis: Metro Manila Environmental Health Baseline

### 2.1 Waterborne & Zoonotic Baseline: Leptospirosis Surveillance Profile

Leptospirosis, caused by pathogenic spirochetes of the genus *Leptospira* (predominantly *Leptospira interrogans*), is hyper-endemic across the low-lying, flood-prone alluvial plains of Metro Manila. The primary urban reservoir host is the brown rat (*Rattus norvegicus*), which chronically sheds spirochetes in its urine into standing surface water, muddy unpaved alleys, and choked open drainage canals.

```
       MUNICIPAL LEPTOSPIROSIS BURDEN IN METRO MANILA (NCR)
+-------------------------+----------------------------------+-----------------------------+
| Surveillance Period     | Epidemiological Metric           | Value / Clinical Impact     |
+-------------------------+----------------------------------+-----------------------------+
| 2023 Full-Year Baseline | NCR Case Fatality Rate (CFR)     | 11.24%                      |
|                         | National Cumulative Deaths (CFR) | 359 deaths (CFR 10.8%)      |
+-------------------------+----------------------------------+-----------------------------+
| 2024 Epidemic Surge     | NCR Total Cumulative Cases       | 2,734 cases (~90% YoY inc.) |
| (Post-Carina/Kristine)  | NCR Total Confirmed Deaths       | 216 deaths (CFR 7.90%)      |
|                         | Floodwater Exposure Prevalence   | > 72% of confirmed cases    |
+-------------------------+----------------------------------+-----------------------------+
| Primary Clinical Centers| National Kidney & Transplant     | Hemodialysis gymnasium      |
|                         | Institute (NKTI); San Lazaro     | conversion; dialysis bed    |
|                         | Hospital (SLH)                   | occupancy > 150% capacity   |
+-------------------------+----------------------------------+-----------------------------+
```

#### Documented Surveillance Metrics & Fatality Rates
Official weekly surveillance data from the Department of Health Epidemiology Bureau (DOH-EB) and the Metro Manila Center for Health Development (MMCHD) demonstrate a severe and recurrent mortality toll:
- **2023 Surveillance Window**: DOH surveillance logged a regional Case Fatality Rate (CFR) of **$11.24\%$** in Metro Manila during peak monsoon surveillance periods, tracking alongside a national CFR of **$10.8\%$** ($359$ fatalities; Department of Health [DOH], 2023; Inquirer, 2023).
- **2024 Epidemic Crisis**: Following consecutive compound hydrometeorological events—including the enhanced Southwest Monsoon (*Habagat*), Typhoon Carina (Gaemi), Severe Tropical Storm Kristine (Trami), and Super Typhoon Leon—Metro Manila crossed epidemic alert thresholds. By November 2024, DOH-MMCHD recorded **$2,734\ \text{cases}$** in NCR alone—a **$90\%$ surge** relative to the identical period in 2023—with **$216\ \text{deaths}$** ($\text{CFR} = 7.90\%$; GMA Network, 2024b). Over **$72\%$** of patients reported direct contact with contaminated floodwaters (DOH, 2024b).
- **Regional Epidemiological Transmission Dynamics**: As demonstrated by Tan et al. (2025) in their regional meta-synthesis of flood-associated disease outbreaks across Southeast Asia, urban inundation acts as an environmental catalyst, concentrating pathogenic spirochetes in standing residential floodwaters and dramatically accelerating cross-species zoonotic transmission during extreme weather disruptions.

#### Spatial Clustering & High-Risk Corridors
Leptospirosis cases in NCR do not distribute uniformly; they cluster heavily along specific hydrological basins and socio-topographic zones:
1. **The CAMANAVA Coastal Corridor** (*Caloocan, Malabon, Navotas, Valenzuela*): High-density coastal plain bordering Manila Bay characterized by subsidence, tidal backflow, and sluggish estuarine drainage.
2. **The Marikina River Basin & Manggahan Floodway** (*Marikina, Pasig, eastern Quezon City*): Subject to rapid riverine overflow from the Sierra Madre watershed, inundating sub-grade residential communities.
3. **The Core Historic Port & Estero Belt** (*Manila City - Tondo, San Nicolas, Sampaloc; Pasay City*): Characterized by informal settlements directly flanking esteros (urban creeks) with compromised sewage infrastructure.

#### Clinical Trajectory & Systemic Healthcare Strain
While mild leptospirosis manifests as an acute febrile syndrome, urban exposure in Metro Manila frequently leads to the severe, icteric form known as **Weil’s disease**, characterized by jaundice, coagulopathy, acute respiratory distress syndrome (ARDS) via diffuse alveolar hemorrhage, and rapid-onset **Acute Kidney Injury (AKI)** requiring continuous renal replacement therapy or intermittent hemodialysis. 

During the August–October 2024 post-flood peaks, tertiary referral centers—specifically the **National Kidney and Transplant Institute (NKTI)** in Quezon City and **San Lazaro Hospital (SLH)** in Manila—exhausted clinical bed capacity. NKTI was forced to convert its physical therapy gymnasium and waiting areas into emergency hemodialysis staging wards, operating dialysis machines on continuous 24-hour schedules to treat patients with fulminant uremia and fluid overload (GMA Network, 2024a; NKTI, 2024).

---

### 2.2 Atmospheric Baseline: Ambient $\text{PM}_{2.5}$ Pollution and WHO Exceedance

Metro Manila’s ambient airshed is severely degraded by vehicular, industrial, and secondary aerosol emissions, creating a chronic toxic respiratory baseline across all 17 LGUs.

```
+----------------------------------------------------------------------------------------------------+
|                      AIR QUALITY STANDARDS VS. METRO MANILA AMBIENT REALITY                         |
+--------------------------------+---------------------------------+---------------------------------+
| Guideline / Standard Body      | Annual Mean Limit               | 24-Hour Mean Limit              |
+--------------------------------+---------------------------------+---------------------------------+
| WHO 2021 Global AQ Guidelines  | 5.0 µg/m³                       | 15.0 µg/m³                      |
| Philippine DAO 2020-14 (EMB)   | 25.0 µg/m³                      | 35.0 µg/m³                      |
| Metro Manila EMB Fixed Stations| 25.0 - 38.5 µg/m³ (Observed)    | 45.0 - 82.0 µg/m³ (Peak Events) |
| Exceedance Above WHO Guideline | +400% to +670% Excess           | +200% to +446% Excess           |
+--------------------------------+---------------------------------+---------------------------------+
```

#### Regulatory Discrepancy: Philippine DAO 2020-14 vs. WHO 2021 Guidelines
A critical policy vulnerability stems from the gap between domestic statutory thresholds and international health-based guidelines:
- **Philippine Clean Air Act of 1999 (Republic Act 8749)** and **DENR Administrative Order (DAO) No. 2020-14** establish the National Ambient Air Quality Guideline Values (NAAQGV) for $\text{PM}_{2.5}$ at:
  - Long-term (Annual Average): **$25\ \mu\text{g/Ncm}$**
  - Short-term (24-Hour Average): **$35\ \mu\text{g/Ncm}$** (Department of Environment and Natural Resources [DENR], 2020).
- **World Health Organization (WHO) 2021 Air Quality Guidelines** slashed health thresholds following definitive epidemiological evidence of cardiopulmonary damage at low exposure:
  - Long-term (Annual Average): **$5\ \mu\text{g/m}^3$**
  - Short-term (24-Hour Average): **$15\ \mu\text{g/m}^3$** (World Health Organization [WHO], 2021).

Consequently, an ambient concentration of $24\ \mu\text{g/m}^3$ is categorized by the DENR-EMB Air Quality Index (AQI) as "Fair" or legally compliant, despite being **nearly 5 times higher** than the WHO health threshold.

#### Station-Level Exceedance Rates
Continuous Ambient Air Quality Monitoring Stations operated by DENR-EMB across the National Capital Region—including stations at **North Caloocan, Commonwealth Avenue (Quezon City), Pasig City Hall, Malabon, Valenzuela, Bicutan (Parañaque), and Taft Avenue (Manila)**—routinely report ambient metrics demonstrating chronic public exposure:
- **Annual Mean Concentrations**: Ranging from **$25.0$ to $38.5\ \mu\text{g/m}^3$**, exceeding the WHO annual guideline by **$500\%\text{--}770\%$** (Clean Air Asia, 2022; Greenpeace Philippines, 2021).
- **Short-Term Episodic Inversions**: During the dry season (December–February) and post-harvest biomass transport periods, stagnant atmospheric conditions produce 24-hour spikes of **$45.0\text{--}82.0\ \mu\text{g/m}^3$**, breaching the WHO 24-hour threshold on more than $65\%$ of monitored days annually.
- **Source Partitioning**: Mobile transportation accounts for approximately **$80\%\text{--}88\%$** of total particulate emissions in the metropolis, driven by an aging fleet of diesel-powered public utility jeepneys (PUJs), commercial freight trucks, and severe traffic congestion (Clean Air Asia, 2022).

#### Morbidity and Mortality Endpoints
Epidemiological investigations in NCR confirm severe health consequences:
- **Occupational and High-Risk Group Exposure**: Collado et al. (2023) demonstrated through spatiotemporal monitoring in Metro Manila that mobile transit workers, open-air public utility vehicle (PUV) drivers, and roadside laborers endure extreme localized $\text{PM}_{2.5}$ concentration spikes far exceeding ambient station averages, compounding systemic respiratory degradation.
- **Chronic Obstructive Pulmonary Disease (COPD)**: MMDA traffic enforcers and open-air PUJ drivers exhibit high risks of chronic airway obstruction; occupational cohort studies demonstrate an adjusted Odds Ratio of **$1.24$** for high-risk COPD categories among traffic enforcers relative to age-matched non-exposed cohorts (Seposo et al., 2021).
- **Premature Mortality Burden**: Health impact assessments model that ambient fine particulate exposure in the Philippines causes over **$27,000$ premature deaths annually**, with the densest concentration of excess cardiovascular, stroke, and acute lower respiratory infection (ALRI) mortality concentrated within the Metro Manila conurbation (Centre for Research on Energy and Clean Air [CREA], 2023).

---

### 2.3 Thermal Extremes & Urban Heat Island (UHI) Dynamics

Metro Manila’s rapid, unplanned horizontal and vertical urbanization has converted natural agricultural wetlands and coastal vegetated zones into dense, impermeable surfaces of reinforced concrete, asphalt, and galvanized iron roofing.

#### Surface Urban Heat Island (SUHI) Characteristics
Remote sensing analyses leveraging thermal infrared sensors on **Landsat 8/9 TIRS** and **MODIS Land Surface Temperature (LST)** demonstrate severe Surface Urban Heat Island (SUHI) intensity across the capital:
- Research by Estoque, Murayama, and Myint (2017) and Estoque and Murayama (2017) demonstrated that impervious surface density (quantified by the Normalized Difference Built-up Index [NDBI]) correlates strongly and positively with LST ($r > 0.75$), while vegetated canopies (Normalized Difference Vegetation Index [NDVI]) exhibit steep negative correlations.
- Geospatial assessments by Vergara and Blanco (2023) utilizing MODIS thermal products across the Philippines confirmed that the high-density built environment of Metro Manila generates persistent, localized surface thermal hotspots that sharply increase community-level heat vulnerability and amplify cardiovascular risk among elderly populations.
- High-density urban cores—including Manila City, northern Pasay, Caloocan, and inner Quezon City—exhibit mean land surface temperature anomalies **$+3.2^\circ\text{C}$ to $+7.1^\circ\text{C}$ hotter** than surrounding peri-urban and coastal baseline environments (Estoque et al., 2017).

```
+----------------------------------------------------------------------------------------------------+
|                       PAGASA HEAT INDEX CATEGORIES & PHYSIOLOGICAL THRESHOLDS                      |
+-------------------+--------------------+-----------------------------------------------------------+
| Classification    | Heat Index Range   | Clinical / Physiological Endpoints                        |
+-------------------+--------------------+-----------------------------------------------------------+
| Caution           | 27°C - 32°C        | Fatigue possible with prolonged exposure & activity.       |
| Extreme Caution   | 33°C - 41°C        | Heat cramps and heat exhaustion possible; continued       |
|                   |                    | physical activity induces systemic stress.                |
| Danger            | 42°C - 51°C        | Heat cramps/exhaustion likely; heat stroke imminent with  |
|                   |                    | prolonged activity. Mandatory work limits recommended.    |
| Extreme Danger    | ≥ 52°C             | Heat stroke highly imminent; systemic multi-organ failure |
|                   |                    | risk without active cooling.                              |
+-------------------+--------------------+-----------------------------------------------------------+
```

#### The 2024 Heat Index Crisis & Emergency Admissions
During the March–May 2024 hot dry season (exacerbated by a strong El Niño event), PAGASA synoptic stations at **Science Garden (Quezon City)** and **Ninoy Aquino International Airport (NAIA, Pasay)** repeatedly clocked apparent temperatures in the **Danger** category ($42^\circ\text{C}\text{--}51^\circ\text{C}$):
- Peak heat indices reached **$44^\circ\text{C}\text{--}48^\circ\text{C}$** for multiple consecutive weeks, prompting nationwide public school transitions to modular remote learning due to hazardous classroom heat (PAGASA, 2024; Inquirer, 2024).
- The DOH Event-Based Surveillance and Response (ESR) system logged **$77\ \text{severe, verified heat-related illnesses}$** and **$7\ \text{direct heat stroke mortalities}$** nationally by April 2024, with emergency rooms across NCR reporting hundreds of undocumented outpatient presentations for heat cramps, syncope, severe dehydration, and hypertensive crises (Department of Health [DOH], 2024a). Outdoor transport workers, street sweepers, construction laborers, and elderly residents of uninsulated informal settlements bore the heaviest burden.

---

## 3. The Compounding Hazard Hypothesis: Cascading & Lagged Dynamics

### 3.1 Formal Definition: The Empirically Calibrated Compounding Risk Function

Traditional epidemiological models evaluate environmental risks as independent, additive terms. In contrast, Project Avatar formalizes the **Compounding Multi-Hazard Hypothesis**, now rigorously refined and locked in via the empirical discoveries of our exploratory data analysis (EDA; see `docs/EDA_FINDINGS.md`):

> **Refined Hypothesis Statement**: *In Metro Manila, post-flood leptospirosis outbreaks do not scale linearly with instantaneous rainfall volume. Instead, outbreak magnitude and clinical fatality (Weil's syndrome/AKI) are governed by a multi-stage compounding cascade: severe pre-monsoon Urban Heat Island stress and fine particulate inhalation pre-condition the population with endothelial inflammation and subclinical renal/fluid deficits. These collide with low-elevation flood inundation and an empirical 1-to-4 week distributed lag pathogen incubation window—peaking at Lag 2 ($r = 0.6267, p = 1.83 \times 10^{-12}$) and Lag 3 ($r = 0.5477, p = 3.07 \times 10^{-9}$)—operating 14 to 21 days ahead of retrospective central surveillance registries.*

Formally, for municipal local government unit $s \in \{1, \dots, 17\}$ at epidemiological week $t$, the compounding environmental health risk $\mathcal{H}_{\text{compound}}(t, s)$ is formulated as:

$$\mathcal{H}_{\text{compound}}(t, s) = g\left( \Phi_{\text{thermal}}(t, s), \ \Psi_{\text{hydrologic}}(t, s), \ \Omega_{\text{lag}}(t, s), \ \Xi_{\text{air\_baseline}}(s) \right)$$

where each component is calibrated to empirical ground truth:

1. **$\Phi_{\text{thermal}}(t, s)$ — Decoupled Antecedent Thermal Stress**:
   EDA revealed that optical and thermal infrared satellite sensors experience **$68.0\%$ cloud masking during the monsoon season** (June–November), rendering real-time satellite LST retrieval unviable during active cyclone landfall. Consequently, $\Phi_{\text{thermal}}(t, s)$ is structurally decoupled into a high-resolution static dry-season surface prior and an all-weather synoptic atmospheric heat term:
   $$\Phi_{\text{thermal}}(t, s) = \alpha \cdot \text{LST}_{\text{SUHI\_prior}}(s) + (1 - \alpha) \cdot \sum_{k=4}^{12} w_k \cdot \max\Big(0, \ \text{HI}_{\text{synoptic}}(t-k, s) - 42^\circ\text{C}\Big)$$
   where:
   - $\text{LST}_{\text{SUHI\_prior}}(s)$ is the static, cloud-screened dry-season (March–May; $12.67\%$ clear-sky null rate) Surface Urban Heat Island anomaly derived from Landsat 8/9 TIRS (Band 10, $30\ \text{m}$) and MODIS (MOD11A1, $1\ \text{km}$).
   - $\text{HI}_{\text{synoptic}}(t-k, s)$ is all-weather daily heat index telemetry from PAGASA synoptic stations (Science Garden, Port Area, NAIA) and ERA5-Land reanalysis ($2\ \text{m}$ temperature and dewpoint), with continuous sensor gaps imputed using a **trailing 7-day rolling median filter** (benchmarked at $\text{MAE} = 5.634\ \mu\text{g/m}^3, r = 0.8278$) and short telemetry runs ($\le 3\ \text{hours}$) filled via Akima cubic spline interpolation.

2. **$\Psi_{\text{hydrologic}}(t, s)$ — Topographic Inundation & Soil Saturation Potential**:
   Combining cumulative precipitation with SRTM 1-arc-second (~$30\ \text{m}$) digital elevation and volumetric soil water dynamics:
   $$\Psi_{\text{hydrologic}}(t, s) = \left[ \frac{\int_{t-2}^{t} P(\tau, s) \, d\tau}{\max\left(\epsilon, \ \overline{\text{Slope}}_{\text{SRTM}}(s)\right)} \right] \cdot \text{SM}_{\text{ERA5}}(t-2, s) \cdot \mathbb{I}_{\left\{\overline{\text{Elev}}_{\text{SRTM}}(s) < 5\text{m}\right\}}$$
   where:
   - Empirical DEM profiling isolates the hyper-vulnerable low-elevation alluvial basins: the CAMANAVA corridor ($1.8\text{--}3.8\ \text{m}$ ASL; slope $0.2\%\text{--}0.3\%$) and Manila port/estero belt ($3.2\text{--}3.5\ \text{m}$ ASL), where Topographic Wetness Indices ($\text{TWI}$) exceed $13.5\text{--}14.8$.
   - $\text{SM}_{\text{ERA5}}(t-2, s)$ integrates volumetric soil water saturation ($0\text{--}7\ \text{cm}$ layer) at Lag 2 weeks ($r = 0.4041, p = 2.53 \times 10^{-5}$), capturing ground saturation that prevents drainage and sustains puddles.

3. **$\Omega_{\text{lag}}(t, s)$ — Empirically Locked Distributed Lag Response**:
   Cross-correlation analysis ($N = 104$ weeks; Bartlett $95\%$ significance bound $\pm 0.1922$) demonstrated that instantaneous rainfall ($\tau = 0$) has no statistically significant correlation with disease incidence ($r = 0.1480, p = 0.134$). The distributed lag function is therefore locked strictly to the significant temporal window $\tau \in \{1, 2, 3, 4\}$:
   $$\Omega_{\text{lag}}(t, s) = \sum_{\tau=1}^{4} \beta(\tau) \cdot P(t - \tau, s) + \delta \cdot P_{\text{cum\_2w\_4w}}(t, s)$$
   with empirical CCF weights reflecting:
   - **$\tau = 1$ (Week 1)**: $r = 0.4048, p = 2.22 \times 10^{-5}$ (primary mucosal/cutaneous incubation onset).
   - **$\tau = 2$ (Week 2)**: $r = 0.6267, p = 1.83 \times 10^{-12}$ (**absolute peak outbreak trigger**; Phase 1 leptospiremia).
   - **$\tau = 3$ (Week 3)**: $r = 0.5477, p = 3.07 \times 10^{-9}$ (**peak clinical hospitalization & organ failure**; Phase 2 Weil's syndrome/AKI).
   - **$\tau = 4$ (Week 4)**: $r = 0.2927, p = 0.0031$ (surveillance reporting and laboratory confirmation delay).
   - $P_{\text{cum\_2w\_4w}}(t, s) = \sum_{\tau=2}^{4} P(t-\tau, s)$ aggregates the sustained multi-week flood exposure. Lags $\tau \ge 5$ ($r \le 0.1397$, non-significant) are excluded from the primary feature store.

4. **$\Xi_{\text{air\_baseline}}(s)$ — Chronic Vascular & Pulmonary Baseline Vulnerability**:
   Captures chronic cardiopulmonary degradation parameterized by multi-year median $\text{PM}_{2.5}$ exceedances above the WHO 2021 annual guideline ($5.0\ \mu\text{g/m}^3$):
   $$\Xi_{\text{air\_baseline}}(s) = \ln\left( \frac{\text{PM}_{2.5}^{\text{median\_4w}}(s)}{\text{PM}_{2.5}^{\text{WHO}}(5.0\ \mu\text{g/m}^3)} \right)$$
   incorporating the $400\%\text{--}670\%$ chronic ambient exceedances documented across DENR-EMB continuous monitoring stations.

---

### 3.2 The 1-to-4 Week Distributed Lag Window & Surveillance Latency Decoupling

The empirical findings from `notebooks/01_eda_and_cleaning.ipynb` fundamentally redefine how early warning systems must interact with public health registries in Metro Manila.

```
       EMPIRICALLY CONFIRMED LAG STRUCTURE & SURVEILLANCE TIME HORIZON
+-----------+-----------------------+-------------------+--------------------+--------------------------------------------+
| Lag Phase | Temporal Window       | Pearson r (Rain)  | p-value (Rain)     | Pathophysiological & Operational Milestone  |
+-----------+-----------------------+-------------------+--------------------+--------------------------------------------+
| Lag τ = 0 | Day 0 - Day 3         | 0.1480            | 0.1340 (p > 0.05)  | Inundation occurs. Instantaneous Paradox:  |
|           |                       |                   | [NON-SIGNIFICANT]  | cases are NOT yet clinically detectable.   |
+-----------+-----------------------+-------------------+--------------------+--------------------------------------------+
| Lag τ = 1 | Week 1 (Days 4 - 7)   | 0.4048            | 2.22e-05           | Subclinical incubation; mucosal penetration|
|           |                       |                   | [SIGNIFICANT]      | by Leptospira interrogans spirochetes.    |
+-----------+-----------------------+-------------------+--------------------+--------------------------------------------+
| Lag τ = 2 | Week 2 (Days 8 - 14)  | 0.6267            | 1.83e-12           | PEAK OUTBREAK SURGE. Leptospiremia onset;  |
|           |                       |                   | [PRIMARY PEAK]     | high fever, myalgia; primary care visits.  |
+-----------+-----------------------+-------------------+--------------------+--------------------------------------------+
| Lag τ = 3 | Week 3 (Days 15 - 21) | 0.5477            | 3.07e-09           | SUSTAINED CLINICAL CRISIS. Immune phase;   |
|           |                       |                   | [SECONDARY PEAK]   | AKI, Weil's disease; NKTI ICU admissions.  |
+-----------+-----------------------+-------------------+--------------------+--------------------------------------------+
| Lag τ = 4 | Week 4 (Days 22 - 28) | 0.2927            | 3.12e-03           | SURVEILLANCE RESIDUE. Batch lab testing    |
|           |                       |                   | [SIGNIFICANT]      | (MAT/ELISA) and PIDSR weekly compilation.  |
+-----------+-----------------------+-------------------+--------------------+--------------------------------------------+
| Lag τ = 5 | Weeks 5 - 8           | 0.0894 - 0.1397   | 0.1680 - 0.3860    | Sub-threshold noise (r < Bartlett ±0.1922).|
| to τ = 8  | (Days 29 - 56)        |                   | [NON-SIGNIFICANT]  | Dropped from active trigger features.      |
+-----------+-----------------------+-------------------+--------------------+--------------------------------------------+
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

#### Surveillance Latency & The Missing at Random (MAR) Mechanism
Decomposition of $3,541$ DOH surveillance linelist records establishes that public health registries operate under severe structural latency:
- **Clinical Presentation Delay**: Median $4.0\ \text{days}$ (IQR: $3\text{--}6\ \text{days}$) from symptom onset to healthcare consultation.
- **Diagnostic & Administrative Delay**: Median $10.0\ \text{days}$ (IQR: $7\text{--}14\ \text{days}$) for serological batch verification (MAT/IgM) and hierarchical encoding into PIDSR.
- **Total Surveillance Latency**: Median **$15.0\ \text{days}$** (IQR: $11\text{--}20\ \text{days}$), with a long right tail where the $90\text{th}$ percentile reaches **$25.0\ \text{days}$** and the $95\text{th}$ percentile reaches **$29.0\ \text{days}$**.
- **Missingness Mechanism (MAR)**: Missing symptom onset dates surge from $3.43\%$ under baseline conditions to **$22.50\%$ during disaster surges** ($\chi^2 = 284.62, p < 10^{-60}$), confirming that data missingness is strictly **Missing at Random (MAR)** conditioned on hospital capacity saturation. Imputing onset dates as $\text{Onset Date} = \text{Admission Date} - 4.0\ \text{days}$ eliminates survivorship bias.

```
       THE 15-DAY SURVEILLANCE DEFICIT: RETROSPECTIVE VS. ANTICIPATORY WARNING
Day 0           Day 4           Day 14          Day 15          Day 25+
[Flood Event]   [Incubation]    [Clinical Peak] [Surveillance]  [Central DOH
  Rainfall        Bacterial       Severe AKI,     Median Lag:     Official Report]
  Lag 0           Penetration     Dialysis Sat.   Registry Logs   Dialysis wards
                                                  Earliest Case   ALREADY full
┌───────────────┬───────────────┬───────────────┐
│  Lag τ = 1    │  Lag τ = 2    │  Lag τ = 3    │
└───────────────┴───────────────┴───────────────┘
▲                                               ▲
│                                               │
Project Avatar Anticipatory Warning             Traditional Siloed Health Warning
Issued Here: 14 to 21 Days Ahead                Arrives Here: 2 to 3 Weeks Late!
```

---

### 3.3 Target Skewness, Zero-Inflation & Machine Learning Formulation

Empirical distribution profiling across all $1,768$ municipal-weeks reveals extreme statistical properties that preclude standard naive linear regressions:
- **Skewness**: **$+7.542$** (extreme positive skewness driven by post-typhoon epidemic peaks).
- **Kurtosis**: **$73.782$** (leptokurtic, fat-tailed distribution).
- **Zero-Inflation**: **$37.84\%$** of municipal-weeks log exactly zero cases.
- **Small Cell Count Rate ($1 \le n < 5$)**: **$45.76\%$** of observations report between 1 and 4 cases.

To ensure computational and statutory integrity, Project Avatar formulates a dual-engine machine learning strategy:

#### 1. Binary Outbreak Surge Classification (LightGBM)
- **Target Formulation**: $\mathbb{I}_{\{\text{Incidence} \ge 1.0\ \text{per } 100,000\ \text{population}\}}$, defining an actionable public health surge.
- **Class Imbalance**: Negative class $1,564$ weeks ($88.46\%$) vs. Positive class $204$ weeks ($11.54\%$), yielding an empirical imbalance ratio of **$7.67 : 1$**.
- **Hyperparameter Mandate**: Enforce `scale_pos_weight = 7.67` with objective `binary`, evaluating strictly on Precision-Recall AUC (`metric = "auc_pr"`).
- **Validation Scheme**: Walk-forward temporal block cross-validation (`TimeSeriesSplit`, $k = 5$) to strictly prevent temporal leakage.

#### 2. Count Regression with Compound Poisson-Gamma Deviance (Tweedie)
- Standard Mean Squared Error (MSE) assumes homoscedastic Gaussian residuals and produces massive errors on zero-inflated, highly skewed targets.
- The regression engine deploys a **Tweedie loss function** with variance power $p = 1.45$, naturally accommodating the mass at zero ($37.84\%$) and continuous positive fat tails ($+7.54$ skewness).

#### 3. Statutory Small Cell Suppression (RA 10173 Compliance)
Because $45.76\%$ of municipal-weeks report fewer than 5 cases, raw model point estimates could inadvertently enable re-identification linkage attacks if paired with emergency dispatch logs. Conforming to **Section 4.2 of `data/README.md` and Republic Act 10173**, all user-facing dashboards and APIs:
- Suppress raw predicted case counts when $1 \le n_{\text{cases}} < 5$, rendering them as `"<5"`.
- Map probabilities into standardized, actionable 4-tier categorical risk bands:
  - **Low** (Surge probability $< 0.25$)
  - **Moderate** ($0.25 \le \text{Pr} < 0.50$)
  - **High** ($0.50 \le \text{Pr} < 0.75$)
  - **Critical** ($\text{Pr} \ge 0.75$)

---

### 3.4 The Physiological Collision: Thermal Dehydration, $\text{PM}_{2.5}$, and Sepsis

The persistent $8\%\text{--}12\%$ Case Fatality Rate observed in Metro Manila cannot be explained solely by microbiological virulence. It represents a **multi-system physiological collapse** caused by compounding stressors:

```
                       THE PHYSIOLOGICAL COLLAPSE CASCADE
+----------------------------------------------------------------------------------------------------+
| CHRONIC PRE-CONDITIONING (Weeks -12 to 0)                                                          |
| - Chronic Ambient PM2.5 Inhalation: Inhaled ultrafine particles induce systemic oxidative stress,  |
|   alveolar-capillary barrier disruption, and persistent vascular endothelial activation.           |
| - Acute-on-Chronic UHI Thermal Load: High wet-bulb / heat index drives continuous profuse sweating, |
|   subclinical intravascular volume depletion, and elevated baseline serum creatinine.              |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| ACUTE ZOONOTIC INFECTION (Weeks 1 to 3)                                                            |
| - Leptospira interrogans entry via skin fissures into dehydrated, micro-inflamed vascular beds.     |
| - Spirochete outer membrane proteins (LipL32, Loa22) trigger toll-like receptor 2 (TLR2) signaling,|
|   inducing acute tubulointerstitial nephritis and direct proximal tubular injury.                  |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| FULMINANT CLINICAL ENDPOINT (Weeks 2 to 8)                                                         |
| - Volume-depleted renal tubules suffer acute tubular necrosis under bacterial endotoxemia.          |
| - Pre-existing pulmonary capillary fragility from PM2.5 renders patients hyper-susceptible to      |
|   Leptospiral Pulmonary Hemorrhage Syndrome (LPHS), carrying a case fatality rate > 50%.          |
| - Severe metabolic acidosis, hyperkalemia, and anuria outstrip available regional hemodialysis     |
|   infrastructure, cementing the regional CFR at 8% - 12%.                                          |
+----------------------------------------------------------------------------------------------------+
```

1. **Pre-Renal Dehydration via Urban Heat Islands**: Urban informal laborers exposed to recurrent $42^\circ\text{C}\text{--}48^\circ\text{C}$ heat indices suffer from chronic subclinical volume contraction. When *Leptospira* endotoxins invade renal tubules, the kidney—already operating under ischemic hemodynamic stress—rapidly progresses to irreversible acute tubular necrosis (ATN), eliminating the typical oliguric buffer phase.
2. **Capillary Fragility & Pulmonary Hemorrhage**: Chronic exposure to ambient fine particulates ($\text{PM}_{2.5}$) damages the alveolar-capillary basement membrane through sustained reactive oxygen species (ROS) generation. Subsequent immune-mediated cytokine cascades during the second phase of leptospirosis trigger catastrophic pulmonary hemorrhage syndrome (LPHS), where alveolar capillaries rupture, leading to rapid suffocation and mortality within hours of admission.

---

## 4. Translational Policy Framework & Operational Trigger Protocols

To translate the Compounding Hazard Hypothesis into frontline municipal action, Project Avatar establishes a **3-Tiered Anticipatory Action Protocol** for Metro Manila LGUs, City Health Offices (CHOs), the Metro Manila Disaster Risk Reduction and Management Council (MMDRRMC), and regional hospital networks:

```
                      MUNICIPAL OPERATIONAL DECISION MATRIX
+-------------------+-----------------------------------+--------------------------------------------+
| Operational Tier  | Environmental / Model Trigger     | Mandatory Municipal Health Directives      |
+-------------------+-----------------------------------+--------------------------------------------+
| TIER 1:           | - PAGASA Heat Index > 42°C for    | 1. Activate air-conditioned municipal      |
| PRE-SEASON        |   3+ consecutive days; OR         |    cooling hubs across public spaces.      |
| THERMAL &         | - DENR-EMB PM2.5 24h > 35 µg/m³;  | 2. Deploy Barangay Health Workers (BHWs)   |
| VULNERABILITY     | - Sentinel-5P / MODIS AOD         |    to register vulnerable elderly/chronic. |
| ALERT             |   anomaly > 2.0σ                  | 3. Pre-position Doxycycline stockpiles at  |
|                   |                                   |    all Barangay Health Centers (BHCs).     |
+-------------------+-----------------------------------+--------------------------------------------+
| TIER 2:           | - Severe Tropical Cyclone / Heavy | 1. Issue mandatory flood avoidance orders; |
| ACUTE HYDROLOGIC  |   Monsoon Rainfall Warning;       |    distribute protective rubber boots.     |
| IMPACT & PROPHY-  | - Inundation detected in low-     | 2. Enact Rapid Post-Exposure Prophylaxis   |
| LAXIS DISPATCH    |   elevation zones (SRTM < 5m);    |    (PEP): Doxycycline 200mg single dose    |
|                   | - Avatar Flood Risk Index > 0.70  |    within 24-48h of floodwater exposure.   |
|                   |                                   | 3. Initiate roving BHW prophylactic mobile |
|                   |                                   |    clinics in informal settlements.        |
+-------------------+-----------------------------------+--------------------------------------------+
| TIER 3:           | - Post-Inundation Lag Weeks 1 - 4 (Peak at Weeks 2 - 3);| 1. Place regional dialysis centers (NKTI,  |
| POST-FLOOD        | - Avatar Outbreak Probability     |    district hospitals) on Stage-3 surge.   |
| DISTRIBUTED SURGE |   Score > 0.65;                   | 2. Establish fever fast-lanes at all RHUs. |
| & CLINICAL STAGING| - Clustered syndromic fever alerts| 3. Mandatory screening for jaundice, calf  |
|                   |   in municipal PIDSR pipeline     |    tenderness, and oliguria (<0.5 mL/kg/h).|
|                   |                                   | 4. Direct rapid referral of suspected AKI  |
|                   |                                   |    cases before uremic crisis develops.    |
+-------------------+-----------------------------------+--------------------------------------------+
```

---

## 5. References (Strict APA 7th Edition)

Centre for Research on Energy and Clean Air. (2023). *Estimating the health and economic cost of air pollution in the Philippines*. CREA. https://energyandcleanair.org/?s=Philippines

Centers for Disease Control and Prevention. (2024). *Leptospirosis clinical guidance*. U.S. Department of Health and Human Services. https://www.cdc.gov/leptospirosis/

Clean Air Asia. (2022). *Clean Air Asia strengthens localized efforts towards healthier air in Manila City*. Clean Air Asia Publications. https://cleanairasia.org/our-news/clean-air-asia-strengthen-localized-efforts-towards-healthier-air-manila-city

Collado, J. T., Abalos, J. G., De Los Reyes, I., Cruz, M. T., Leung, G. F., Abenojar, K., Manalo, C. R., Go, B., Chan, C. L., Gonzales, C. K. G., Simpas, J. B. B., Porio, E. E., Wong, J. Q., Lung, S. C., & Cambaliza, M. O. L. (2023). Spatiotemporal assessment of PM2.5 exposure of a high-risk occupational group in a Southeast Asian megacity. *Aerosol and Air Quality Research*, 23(1), Article 220134. https://doi.org/10.4209/aaqr.220134

Department of Environment and Natural Resources. (2020). *Administrative Order No. 2020-14: Revised national ambient air quality guideline values for particulate matter 2.5 (PM2.5)*. DENR Environmental Management Bureau. https://air.emb.gov.ph/wp-content/uploads/2020/07/DAO-2020-14-PM2.5.pdf

Department of Health. (2023). *Philippine integrated disease surveillance and response: Annual surveillance bulletin 2023*. Epidemiology Bureau, Department of Health, Republic of the Philippines. https://doh.gov.ph/

Department of Health. (2024a). *Event-based surveillance and response report: National heat-related illness registry (March–May 2024)*. Epidemiology Bureau, Department of Health, Republic of the Philippines. https://doh.gov.ph/

Department of Health. (2024b). *Press release: DOH reports surge in leptospirosis admissions in NCR following tropical cyclone Carina and southwest monsoon*. Department of Health, Republic of the Philippines. https://doh.gov.ph/

Estoque, R. C., & Murayama, Y. (2017). Monitoring surface urban heat island formation in a tropical mountain city using Landsat data (1987–2015). *ISPRS Journal of Photogrammetry and Remote Sensing*, 133, 18–29. https://doi.org/10.1016/j.isprsjprs.2017.09.008

Estoque, R. C., Murayama, Y., & Myint, S. W. (2017). Effects of landscape composition and pattern on land surface temperature: An urban heat island study in the megacities of Southeast Asia. *Science of The Total Environment*, 577, 349–359. https://doi.org/10.1016/j.scitotenv.2016.10.195

GMA Network. (2024a, August 8). *NKTI gym turned into leptospirosis ward as cases climb*. GMA News Online. https://www.gmanetwork.com/news/topstories/metro/916431/nkti-gym-turned-into-leptospirosis-ward-as-cases-climb/story/

GMA Network. (2024b, November 14). *DOH-MMCHD: Metro Manila leptospirosis cases reach 2,734 with 216 deaths in 2024*. GMA News Online. https://www.gmanetwork.com/news/topstories/metro/927063/metro-manila-leptospirosis-cases-deaths-2024/story/

Greenpeace Philippines. (2021). *PH urged to comply with new WHO air quality guidelines as Manila nearly triples safe limits*. Greenpeace Southeast Asia. https://www.greenpeace.org/philippines/press/10943/ph-urged-to-comply-with-new-who-air-quality-guidelines-as-manila-nearly-triples-safe-limits/

Inquirer. (2023, September 6). *DOH: Lepto infections in regions, Metro spiking*. Philippine Daily Inquirer. https://newsinfo.inquirer.net/1827723/doh-lepto-infections-in-regions-metro-spiking

Inquirer. (2024, April 28). *Dangerous heat index logged across Metro Manila; schools shift to remote learning*. Philippine Daily Inquirer. https://newsinfo.inquirer.net/

Matsushita, N., Ng, C. F. S., Kim, Y., Suzuki, M., Saito, M., Ariyoshi, K., Salva, E. P., Dimaano, E. M., & Hashizume, M. (2018). The non-linear and lagged short-term relationship between rainfall and leptospirosis and the intermediate role of floods in the Philippines. *PLOS Neglected Tropical Diseases*, 12(4), Article e0006331. https://doi.org/10.1371/journal.pntd.0006331

National Kidney and Transplant Institute. (2024). *Public advisory: Surge in post-typhoon leptospirosis admissions and emergency hemodialysis staging*. NKTI Information Office. https://nkti.gov.ph/

Philippine Atmospheric, Geophysical and Astronomical Services Administration. (2024). *Climatological extremes and heat index monitoring summary for Metro Manila stations*. Department of Science and Technology. https://bagong.pagasa.dost.gov.ph/climate/heat-index

Philippine Statistics Authority. (2021). *2020 census of population and housing (2020 CPH) population counts declared official by the President: National Capital Region*. Philippine Statistics Authority. https://psa.gov.ph/

Republic of the Philippines. (1999). *Republic Act No. 8749: Philippine Clean Air Act of 1999*. Official Gazette of the Republic of the Philippines. https://www.officialgazette.gov.ph/1999/06/23/republic-act-no-8749/

Republic of the Philippines. (2012). *Republic Act No. 10173: Data Privacy Act of 2012*. Official Gazette of the Republic of the Philippines. https://www.officialgazette.gov.ph/2012/08/15/republic-act-no-10173/

Seposo, X., Arcilla, A. L. A., De Guzman, J. G. N., III, Dizon, E. M. S., Figuracion, A. N. R., Morales, C. M. M., Tugonon, P. K. A., & Apostol, G. L. C. (2021). Ambient air quality and the risk for Chronic Obstructive Pulmonary Disease among Metro Manila Development Authority traffic enforcers in Metro Manila: An exploratory study. *Chronic Diseases and Translational Medicine*, 7(4), 263–270. https://doi.org/10.1016/j.cdtm.2021.01.002

Tan, B., De Vera, P., Abrazaldo, J., & Ng, C. (2025). Flood-associated disease outbreaks and transmission in Southeast Asia. *Frontiers in Microbiology*, 16, Article 1694246. https://doi.org/10.3389/fmicb.2025.1694246

Vergara, D. C. D. M., & Blanco, A. C. (2023). Surface urban heat islands and related health risk in the Philippines: A geospatial assessment using MODIS data. *The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, XLVIII-4/W6-2022, 451–456. https://doi.org/10.5194/isprs-archives-xlviii-4-w6-2022-451-2023

World Health Organization. (2003). *Human leptospirosis: Guidance for diagnosis, surveillance and control*. World Health Organization. https://apps.who.int/iris/handle/10665/42667

World Health Organization. (2021). *WHO global air quality guidelines: Particulate matter (PM2.5 and PM10), ozone, nitrogen dioxide, sulfur dioxide and carbon monoxide*. World Health Organization. https://apps.who.int/iris/handle/10665/345329
