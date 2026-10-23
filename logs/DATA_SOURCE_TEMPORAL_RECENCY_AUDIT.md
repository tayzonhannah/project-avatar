# Project Avatar: Data Source Temporal Recency & Real-Time Feasibility Audit

**Document Classification:** Engineering & Epidemiological Technical Audit  
**Author:** Lead Data & Epidemiological Researcher, Project Avatar  
**Competition:** Philippine Junior Data Science Challenge (PJDSC) 2026  
**Date:** October 2026  
**Cross-References:** [`docs/RESEARCH_SYNTHESIS.md`](../docs/RESEARCH_SYNTHESIS.md) | [`data/README.md`](../data/README.md) | [PJDSC Rubric Section 1.2 & 2.2](../.agents/skills/pjdsc-rubric/SKILL.md)

---

## 1. Executive Summary & Problem Context

In developing an environmental health early warning system for Metro Manila—addressing compounding risks of monsoonal flooding, urban heat islands (UHI), fine particulate pollution ($\text{PM}_{2.5}$), and waterborne leptospirosis—a fundamental question arises:

> **Core Inquiry**: *Do all proposed data sources have real-time and recent data? Can a mobile health application legitimately issue "real-time" alerts based on these streams?*

### The Verdict: Absolute Transparency
**No, the data sources do not all have real-time or recent data.** 

In reality, the assets documented in Project Avatar span a wide temporal spectrum:
- **Static Baselines**: Ranging from **26-year-old topographic models** (SRTM DEM, 2000) to **4-to-6-year-old population censuses** (PSA 2020 CPH).
- **Retrospective / Delayed Series**: Datasets with **2 to 3 months of processing latency** (Copernicus ERA5-Land reanalysis) or **1 to 4 weeks of administrative and laboratory delay** (DOH PIDSR disease bulletins).
- **Periodic Remote Sensing**: Satellites with **8-to-16-day revisit frequencies** (Landsat 8/9 TIRS) or daily afternoon orbits (MODIS, Sentinel-5P) that suffer from **severe cloud and precipitation occlusion during the exact tropical cyclones being tracked**.
- **Near-Real-Time (NRT) Streams**: Only weather observations (DOST-PAGASA synoptic stations and radar alerts) and live numerical weather prediction APIs provide true operational real-time feeds.

Rather than being a conceptual defect, **this temporal reality is an epidemiological strength**. Leptospirosis is biologically, clinically, and institutionally **not** a real-time event. Attempting to build an early warning system reliant on real-time confirmed infection registries would result in failure: by the time clinical cases are logged into official surveillance systems, hemodialysis centers at tertiary hospitals (NKTI, San Lazaro Hospital) are already operating past $150\%$ capacity.

Project Avatar circumvents this bottleneck by engineering a **Decoupled Anticipatory Architecture**: historical, high-latency data trains non-linear distributed lag models ($\tau \in [1, 8]$ weeks), while live operational weather feeds trigger forward-looking risk alerts 2 to 4 weeks before clinical surges materialize.

---

## 2. Comprehensive Temporal Audit Matrix

```
+---------------------------------------------------------------------------------------------------------------------------------------------+
|                                              PROJECT AVATAR COMPREHENSIVE DATA TEMPORAL AUDIT                                               |
+--------------------------+---------------------+-------------------+---------------------+-------------------------+------------------------+
| Dataset / Platform       | Source Agency       | Nominal Cadence   | True Latency / Age  | Cloud / Weather Gaps    | Real-Time Feasibility  |
+--------------------------+---------------------+-------------------+---------------------+-------------------------+------------------------+
| SRTM 1-Arc-Second DEM    | NASA JPL / USGS     | Static            | 26 Years Old (2000) | None (Radar surface)    | ❌ Static Topography   |
| PSA Census 2020 CPH      | PSA                 | 5-to-10 Year Base | 6 Years Old (2020)  | None (Demographic)      | ❌ Static Denominator  |
| WorldPop Projections     | Univ. Southampton   | Annual Projection | 1-to-2 Years Old    | None (Model surface)    | ❌ Static Grid         |
| ERA5-Land Reanalysis     | ECMWF / Copernicus  | Hourly Gridded    | 2 to 3 Months Lag   | None (Model assimilation)| ❌ Retrospective Only  |
| Landsat 8/9 TIRS LST     | USGS / NASA         | 16-day repeat     | 8-to-16 Days        | Critical (Cloud mask)   | ❌ Periodic Only       |
| DOH PIDSR Weekly Registry| DOH Epidemiology Bur| Weekly (EpiWeek)  | 1 to 4 Weeks Lag    | None (Clinical reports) | ❌ Retrospective Only  |
| DENR-EMB Fixed AQI       | DENR-EMB            | Hourly / Daily    | Real-time to Weeks  | High hardware downtime  | ⚠️ Partial / Fragmented|
| MODIS MAIAC AOD / LST    | NASA LP DAAC        | Daily (Terra/Aqua)| NRT: ~3 to 5 Hours  | Severe during typhoons  | ⚠️ Weather-Permitting  |
| Sentinel-5P TROPOMI      | ESA / Copernicus    | Daily (~13:30 PHT)| NRT: ~3 Hours       | Severe during monsoons  | ⚠️ Weather-Permitting  |
| DOST-PAGASA Bulletins    | DOST-PAGASA         | Hourly / 3-Hourly | Minutes to 1 Hour   | Radar rain attenuation  | ✅ Operational NRT     |
| Live Weather APIs        | Open-Meteo / GFS    | Hourly / 15-Min   | Real-Time & 7d Fwd  | None (Numerical model)  | ✅ Operational Live    |
+--------------------------+---------------------+-------------------+---------------------+-------------------------+------------------------+
```

---

## 3. Deep-Dive Analysis of Data Constraints

### 3.1 Static & Decadal Baselines

#### 1. Shuttle Radar Topography Mission (SRTM) 1-Arc-Second Global DEM
- **Data Origin**: Flown aboard Space Shuttle Endeavour in **February 2000**.
- **Temporal Reality**: The data is over a quarter-century old.
- **Physical Implications**: While regional tectonic elevation changes slowly, Metro Manila's micro-topography has undergone drastic artificial modifications:
  - Land reclamation projects along Manila Bay (Pasay, Parañaque, Manila City).
  - Rapid coastal and estuarine land subsidence in the CAMANAVA district (*Caloocan, Malabon, Navotas, Valenzuela*) exceeding $2\text{--}5\ \text{cm/year}$ due to groundwater over-extraction.
  - Engineering of the Manggahan Floodway, elevated river dikes, and pumped drainage channels.
- **Project Mitigation**: SRTM provides the base regional slope and macro-drainage gradient ($\overline{\text{Slope}} < 1.0\%$), but must not be misinterpreted as a dynamic, real-time puddle or street-level flood depth sensor.

#### 2. PSA 2020 Census of Population and Housing (2020 CPH) & WorldPop
- **Data Origin**: May 2020 mid-pandemic enumeration by the Philippine Statistics Authority.
- **Temporal Reality**: 6-year-old population counts.
- **Demographic Implications**: Informal settlements in river easements and esteros experience dynamic post-typhoon relocation, seasonal labor migration, and urban densification.
- **Project Mitigation**: Used as the normalized population denominator ($N_s$) for calculating municipal incidence rates per 100,000 population; adjusted via official PSA inter-censal annual growth projections.

---

### 3.2 High-Latency Retrospective Data

#### 3. ECMWF ERA5-Land Climate Reanalysis
- **Nominal Resolution**: Hourly climate variables at $0.1^\circ \times 0.1^\circ$ (~$9\ \text{km}$).
- **Temporal Reality**: Standard ERA5-Land products have a release latency of **2 to 3 months** behind real time. Even the preliminary `ERA5T` stream maintains a 5-day lag and is not optimized for instant real-time query pipelines.
- **Operational Reality**: ERA5-Land cannot be queried inside a live mobile alert pipeline for "today's weather". Its true utility is serving as the gold-standard historical training matrix (2018–2024) to establish climatological baselines.

#### 4. DOH Philippine Integrated Disease Surveillance and Response (PIDSR)
- **Surveillance Cadence**: Weekly epidemiological bulletins (`EpiWeek`, Sunday to Saturday).
- **Temporal Reality**: Official consolidated case counts suffer an inherent **1 to 4 week administrative and diagnostic delay**:
  1. *Clinical Presentation*: Patients present to Rural Health Units (RHUs) or district emergency rooms 7 to 14 days after initial flood exposure.
  2. *Laboratory Confirmation*: Serological testing (Microscopic Agglutination Test [MAT] or IgM ELISA) requires batch transport to referral centers (San Lazaro Hospital or RITM), taking 5 to 10 days.
  3. *Surveillance Consolidation*: City Health Offices (CHOs) aggregate municipal line lists, transmit them to the Metro Manila Center for Health Development (MMCHD), which then submits to the DOH Epidemiology Bureau.
- **Operational Reality**: Real-time infection reporting does not exist in Philippine public health. Any system attempting to deliver "real-time infection alerts" is inherently disconnected from frontline clinical logistics.

---

### 3.3 Periodic & Cloud-Occluded Satellite Remote Sensing

#### 5. Landsat 8 and 9 Thermal Infrared Sensor (TIRS)
- **Constellation Cadence**: 16-day orbit per satellite; combined 8-day repeat frequency.
- **Temporal & Atmospheric Reality**: Thermal infrared sensors cannot penetrate atmospheric water vapor, cumulus cloud decks, or heavy overcast skies.
- **Monsoon Impact**: During the Southwest Monsoon (*Habagat*) and tropical cyclone season (June to November)—precisely when flood and disease hazards peak—cloud-free Landsat acquisitions drop to nearly zero for multiple consecutive weeks.
- **Project Mitigation**: Landsat-derived Land Surface Temperature (LST) and Normalized Difference Built-up Index (NDBI) are extracted during the antecedent dry season (March–May) to construct a **static/seasonal Urban Heat Island (UHI) vulnerability baseline**, rather than attempting real-time storm tracking.

#### 6. Sentinel-5P TROPOMI & MODIS MAIAC Aerosol Optical Depth (AOD)
- **Constellation Cadence**: Daily overpasses (MODIS Terra ~10:30, Aqua ~13:30; Sentinel-5P ~13:30 PHT).
- **Latency**: Near-Real-Time (NRT) data products are available within 3 to 5 hours of orbit.
- **Atmospheric Reality**: While latency is short, heavy rain and thick storm clouds contaminate optical aerosol retrievals (`qa_value < 0.50`), forcing mandatory masking of particulate data during typhoon landfalls.
- **Ground Sensor Reality (DENR-EMB)**: Surface air quality monitoring in NCR is constrained to only 7–10 operational reference stations across 17 LGUs, plagued by frequent hardware telemetry downtime and maintenance outages.

---

### 3.4 Genuine Real-Time & Operational Streams

#### 7. DOST-PAGASA Synoptic Weather Observations & Heavy Rainfall Warnings
- **Cadence**: Hourly and 3-hourly synoptic observations; real-time Doppler radar scans; urgent Color-Coded Heavy Rainfall Warnings (Yellow, Orange, Red).
- **Latency**: Issued within minutes of precipitation threshold exceedance.
- **Operational Reality**: Represents a verified, statutory real-time trigger for immediate municipal disaster risk reduction and community alerts.

#### 8. Operational Global Numerical Weather Prediction (NWP) APIs
- **Cadence**: Hourly updates, 15-minute nowcasts, and 7-day probabilistic forecasts (e.g., Open-Meteo, NOAA GFS, ECMWF IFS).
- **Latency**: Real-time programmatic API access ($<500\ \text{ms}$ response times).
- **Operational Reality**: High availability, zero cloud-occlusion missingness, and continuous forward-looking projection.

---

## 4. The Biological & Epidemiological Paradigm: Why "Real-Time" Disease Surveillance is a Fallacy

A critical insight formalized in Project Avatar's epidemiological foundation is that **the biological incubation kinetics of waterborne zoonoses preclude instantaneous disease surges**:

```
+----------------------------------------------------------------------------------------------------+
|                      CHRONOLOGICAL TIMELINE OF A POST-FLOOD LEPTOSPIROSIS SURGE                    |
+----------------------------------------------------------------------------------------------------+
| Phase 0: Hydrologic Inundation (Day 0 - Day 3)                                                     |
| - Heavy monsoon downpours flood lowlands (SRTM DEM < 5m elevation, slope < 1%).                    |
| - Rattus norvegicus urinary colonies flush into open street canals.                                |
| - Citizens wade through septic floodwaters during emergency evacuations.                           |
| --> Data Streams: DOST-PAGASA Heavy Rainfall Warnings (Real-Time).                                |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| Phase 1: Silent Biological Incubation (Day 4 - Day 14 / Lag τ = 1 to 2 Weeks)                     |
| - Spirochetes (Leptospira interrogans) penetrate mucosal membranes or skin fissures.               |
| - Primary incubation period: 2 to 30 days (median 7 to 14 days).                                   |
| - ZERO clinical hospital surge detected by surveillance systems.                                   |
| --> Critical Window: Immediate Post-Exposure Prophylaxis (PEP: Doxycycline 200mg within 24-48h).   |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| Phase 2: Clinical Progression & Emergency Presentation (Days 15 - 28 / Lag τ = 2 to 4 Weeks)       |
| - Septicemic phase progresses to immune phase; acute tubular necrosis (ATN) and jaundice develop.  |
| - Massive patient influx to San Lazaro Hospital and NKTI for acute peritoneal / hemodialysis.      |
| - Hemodialysis gymnasiums activated; bed occupancy exceeds 150%.                                   |
| --> Clinical Crisis: Acute renal failure and Leptospiral Pulmonary Hemorrhage Syndrome (LPHS).    |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
| Phase 3: Surveillance Bulletin Consolidation (Days 28 - 56 / Lag τ = 4 to 8 Weeks)                 |
| - Laboratory confirmation tests (MAT/ELISA) completed.                                             |
| - Municipal line lists transmitted through CHOs to DOH MMCHD and Epidemiology Bureau.              |
| - Official DOH PIDSR Weekly Surveillance Bulletin published.                                       |
| --> Retrospective Reality: The published case counts describe exposures from 4 to 6 weeks earlier. |
+----------------------------------------------------------------------------------------------------+
```

### The Strategic Conclusion
If a mobile health application or early warning system relies on **real-time confirmed cases**, it will sound the alarm **only after the epidemic has already overwhelmed municipal hospitals**. 

True public health protection requires an **Anticipatory Early Warning System** that detects the environmental precursor shock today, models the non-linear distributed lag window ($\tau \in [1, 8]$ weeks), and dispatches interventions weeks before clinical admissions peak.

---

## 5. Architectural Decoupling: How Project Avatar Solves the Real-Time Challenge

To ensure both computational feasibility and scientific rigor, Project Avatar strictly separates its data pipelines into two independent layers:

```
+----------------------------------------------------------------------------------------------------+
|                         PROJECT AVATAR DECOUPLED PIPELINE ARCHITECTURE                             |
+----------------------------------------------------------------------------------------------------+

  [LAYER 1: OFFLINE HISTORICAL RESEARCH & TRAINING PIPELINE]
  ==================================================================================================
  • Multi-Year Historical Archives:
    - 2020-2024 DOH PIDSR Municipal Case Registries (Weekly aggregated counts)
    - 2018-2024 ERA5-Land Hourly Climate Reanalysis (Precipitation, soil moisture)
    - Landsat 8/9 Thermal Infrared Sensor Collections (Multi-year LST anomalies)
    - NASA SRTM 1-Arc-Second DEM (Static slope, topographic wetness index)
    - PSA 2020 Census of Population & WorldPop (Normalized population baselines)
                                                  │
                                                  ▼
  • Feature Engineering & Distributed Lag Modeling:
    - Construct non-linear distributed lag matrices: τ = 1, 2, ..., 8 weeks
    - Train Tabular ML Models (LightGBM / XGBoost) with TimeSeriesSplit & spatial blocks
    - Calibrate the Compounding Environmental Health Risk Function:
      H_compound(t, s) = g(Φ_thermal, Ψ_hydrologic, Ω_lag, Ξ_air_baseline)
                                                  │
                                                  ▼
  • Frozen Artifact Deployment:
    - Serialized model weights (`model_weights.joblib`, `risk_scalers.pkl`)
    - Static Precomputed Spatial GeoParquet (`ncr_spatial_vulnerability_100m.parquet`)
  
  ==================================================================================================
                                                  │
                                                  ▼
  [LAYER 2: ONLINE REAL-TIME INFERENCE & CITIZEN ALERT ENGINE]
  ==================================================================================================
  • Live Operational Telemetry Ingestion (< 1 second):
    - DOST-PAGASA Heavy Rainfall Warnings & Synoptic Station Bulletins (Scraped / Webhook)
    - Live Numerical Weather Prediction API (Open-Meteo / GFS live precipitation nowcast)
    - User GPS Geolocation Coordinates (Mobile App / Interactive Web UI)
                                                  │
                                                  ▼
  • Sub-Second Forward Inference:
    - Query static vulnerability for user coordinate (Elevation, Slope, UHI baseline)
    - Ingest current live rainfall intensity + antecedent 7-day weather
    - Execute pre-trained distributed lag forward pass (projecting risk for Weeks t+1 to t+4)
                                                  │
                                                  ▼
  • RAG Synthesis & Plain-Language Advisory Dispatch:
    - Retrieve context-specific clinical guidelines from indexed WHO AirQ+ & DOH protocols
    - Generate localized push notification:
      "ALERT: Extreme flooding detected in low-lying corridor. Outbreak probability 
       projected to peak in 14-21 days. Seek medical prophylaxis (Doxycycline) within 48h."
+----------------------------------------------------------------------------------------------------+
```

---

## 6. Strategic Recommendations & Alignment with the PJDSC Rubric

When presenting Project Avatar in the final competition deliverables—the **20-Slide Presentation Deck**, the **Demonstration Video**, and the **Code Repository**—the team should address this issue directly:

### 1. Refine the Terminology Across All Deliverables
- **Avoid Misleading Claims**: Do not state that the system operates on *"real-time disease surveillance"* or *"live satellite imagery during storms"*.
- **Use Precise Scientific Language**: Frame Project Avatar as:
  > *"A real-time environmental hazard monitoring framework driving predictive, lagged epidemiological early warnings."*

### 2. Turn the Limitation into a Winning Rubric Argument
Under **Section 2.2 of the PJDSC Rubric (Real-World Bottlenecks & Operational Mitigation)**:
- Explicitly present the **Surveillance Lag Bottleneck**: *"Traditional DOH surveillance operates with a 1-to-4 week institutional delay, meaning public health interventions are historically reactive."*
- Present Project Avatar’s **Anticipatory Solution**: *"By coupling live hydrometeorological nowcasts with an empirical 1-to-8 week distributed lag model trained on multi-year baselines, Project Avatar enables proactive prophylaxis dispatch within 24 to 48 hours of inundation—weeks before hospital dialysis wards reach capacity."*

### 3. Transparent Technical Disclosure in Repository Documentation
- In `data/README.md`, maintain the provenance and latency tables documented here.
- Document how missing satellite data during severe cloud cover is handled via **fallback to numerical weather reanalysis and rolling temporal medians**.
- Ensure code modules in `src/` explicitly separate offline training scripts from real-time API inference routines.

---

## 7. References (Strict APA 7th Edition)

Copernicus Climate Change Service. (2020). *ERA5-Land hourly data from 1950 to present* [Data set]. European Centre for Medium-Range Weather Forecasts (ECMWF). https://doi.org/10.24381/cds.e2161bac

Department of Environment and Natural Resources. (2020). *Administrative Order No. 2020-14: Revised national ambient air quality guideline values for particulate matter 2.5 (PM2.5)*. DENR Environmental Management Bureau. https://air.emb.gov.ph/wp-content/uploads/2020/07/DAO-2020-14-PM2.5.pdf

Department of Health. (2023). *Philippine integrated disease surveillance and response: Annual surveillance bulletin 2023*. Epidemiology Bureau, Department of Health, Republic of the Philippines. https://doh.gov.ph/surveillance-reports/

European Space Agency. (2021). *Sentinel-5P TROPOMI science product user guide* (Doc. No. S5P-MPC-SRON-SPUG). European Space Agency. https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-5p-tropomi/

Lyapustin, A., Wang, Y., Korkin, S., & Huang, D. (2018). MODIS collection 6 MAIAC algorithm. *Atmospheric Measurement Techniques*, 11(10), 5741–5765. https://doi.org/10.5194/amt-11-5741-2018

Matsushita, N., Ng, C. F. S., Kim, Y., Suzuki, M., Saito, M., Ariyoshi, K., Salva, E. P., Dimaano, E. M., & Hashizume, M. (2018). The non-linear and lagged short-term relationship between rainfall and leptospirosis and the intermediate role of floods in the Philippines. *PLOS Neglected Tropical Diseases*, 12(4), Article e0006331. https://doi.org/10.1371/journal.pntd.0006331

NASA Jet Propulsion Laboratory. (2013). *NASA Shuttle Radar Topography Mission (SRTM) global 1 arc-second* [Data set]. NASA EOSDIS Land Processes DAAC. https://doi.org/10.5067/MEaSUREs/SRTM/SRTMGL1.003

Philippine Atmospheric, Geophysical and Astronomical Services Administration. (2024). *Manual of meteorological observation practices in the Philippines*. Department of Science and Technology. https://bagong.pagasa.dost.gov.ph/learning-tools/meteorological-instruments

Philippine Statistics Authority. (2021). *2020 census of population and housing (2020 CPH) population counts declared official by the President: National Capital Region*. Philippine Statistics Authority. https://psa.gov.ph/content/2020-census-population-and-housing-2020-cph-population-counts-declared-official-president

Republic of the Philippines. (2012). *Republic Act No. 10173: Data Privacy Act of 2012*. Official Gazette of the Republic of the Philippines. https://www.officialgazette.gov.ph/2012/08/15/republic-act-no-10173/

Republic of the Philippines. (2019). *Republic Act No. 11332: Mandatory Reporting of Notifiable Diseases and Health Events of Public Health Concern Act*. Official Gazette of the Republic of the Philippines. https://www.officialgazette.gov.ph/2019/04/26/republic-act-no-11332/

Tan, B., De Vera, P., Abrazaldo, J., & Ng, C. (2025). Flood-associated disease outbreaks and transmission in Southeast Asia. *Frontiers in Microbiology*, 16, Article 1694246. https://doi.org/10.3389/fmicb.2025.1694246

U.S. Geological Survey. (2021). *Landsat 8-9 Collection 2 Level 2 Science Product Guide* (LSDS-1619, Version 2.0). Earth Resources Observation and Science (EROS) Center, U.S. Geological Survey. https://www.usgs.gov/media/files/landsat-8-9-collection-2-level-2-science-product-guide

World Health Organization. (2021). *WHO global air quality guidelines: Particulate matter (PM2.5 and PM10), ozone, nitrogen dioxide, sulfur dioxide and carbon monoxide*. World Health Organization. https://apps.who.int/iris/handle/10665/345329

WorldPop. (2020). *Global high resolution population denominators project: Philippines 100m population counts* [Data set]. University of Southampton. https://doi.org/10.5258/SORD/13860
