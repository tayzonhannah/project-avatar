# Project Avatar: Data Hygiene, Provenance & Ethical Audit Protocol

**Lead Epidemiological Researcher**, Project Avatar  
**Philippine Junior Data Science Challenge (PJDSC) 2026**  
**Classification:** Open Science Architecture & Statutory Privacy Audit  
**Adherence:** Republic Act 10173 (Data Privacy Act of 2012) & PJDSC Rubric (Section 1.2)  

---

## 1. Data Architecture & Directory Standards

To ensure computational reproducibility, auditability, and absolute privacy separation, all Project Avatar assets are organized under a strict three-tier layout. Raw input registries remain completely immutable; all transformations are versioned via deterministic, containerized pipelines.

```
data/
├── raw/                              # Immutable raw input assets (read-only)
│   ├── atmospheric/                  # Sentinel-5P, MODIS AOD, DENR-EMB station logs
│   ├── thermal/                      # Landsat 8/9 TIRS, MODIS LST
│   ├── hydrometeorological/          # PAGASA synoptic logs, ERA5-Land, SRTM DEM
│   └── epidemiological/              # DOH PIDSR municipal bulletins, PSA/WorldPop census
├── processed/                        # Intermediate & harmonized analysis matrices
│   ├── spatial_features/             # Topographic slope, urban heat island anomalies
│   ├── time_series_features/         # Distributed lag matrices (τ = 1 to 8 weeks)
│   └── analysis_matrix_ncr.parquet   # Final sanitized, k-anonymized tabular dataset
├── external/                         # Spatial boundaries (PSA PSGC, GADM Level 2)
└── README.md                         # This comprehensive protocol document
```

### Coordinate Reference Systems & Temporal Binning Standards
- **Standard Storage CRS**: `EPSG:4326` (WGS 84 geographic latitude/longitude).
- **Standard Analysis & Metric CRS**: `EPSG:32651` (WGS 84 / UTM Zone 51N) for area calculations, Euclidean buffer generation, and spatial convolution over Metro Manila.
- **Temporal Binning Standard**: ISO 8601 Epidemiological Weeks (**EpiWeeks**, Monday 00:00:00 to Sunday 23:59:59 PHT [UTC+8]), harmonized with the Department of Health (DOH) weekly surveillance reporting cadence.

---


---

## 1.1 Data Provenance & Simulation Disclosure

> **Transparency Disclosure**: To guarantee computational reproducibility without exposing proprietary patient-level medical records, the files populated in `data/raw/` are reproducible synthetic fixtures generated via `scripts/generate_raw_fixtures.py` under seed `random_state=42`. 
> - **Epidemiological Surveillance**: Calibrated to empirical totals and distributions from published DOH-EB annual reports and PIDSR bulletins. The synthetic generation incorporates known pathogen kinetics (peak biological incubation 2-3 weeks post-cyclone); consequently, cross-correlation function (CCF) analysis validates pipeline recovery rather than establishing novel etiologic discovery.
> - **Environmental & Atmospheric**: Gridded topography is resampled from SRTM DEM grids; air quality series are calibrated against DENR-EMB continuous station distributions.

## 2. Comprehensive Dataset Catalog & Download Pipelines

```
+-----------------------------------------------------------------------------------------------------------------------------------+
|                                                 PROJECT AVATAR DATASET MATRIX                                                     |
+--------------------------+---------------------+-------------------+---------------------+------------------+---------------------+
| Dataset Identity         | Primary Source      | Spatial Res.      | Temporal Res.       | License          | Access Mechanism    |
+--------------------------+---------------------+-------------------+---------------------+------------------+---------------------+
| Sentinel-5P TROPOMI      | ESA / Copernicus    | 3.5 km × 5.5 km   | Daily (13:30 orbit) | CC BY 4.0 Open   | GEE Python / CDSE   |
| MODIS MAIAC AOD          | NASA LP DAAC        | 1.0 km            | Daily (Terra/Aqua)  | Public / Open    | Earthdata API / GEE |
| Landsat 8/9 TIRS LST     | USGS / NASA         | 30 m (resampled)  | 16-day repeat       | Public Domain    | GEE / EarthExplorer |
| MODIS LST (MOD11A1)      | NASA LP DAAC        | 1.0 km            | Daily (Day/Night)   | Public / Open    | GEE / LP DAAC       |
| PAGASA Synoptic Rain     | DOST-PAGASA         | Synoptic Stations | Hourly / Daily      | PH Open Gov      | eFOI Portal / Scrape|
| ERA5-Land Reanalysis     | ECMWF / Copernicus  | 0.1° (~9 km)      | Hourly / Daily      | Copernicus Open  | ECMWF CDS API       |
| SRTM 1-Arc-Second DEM    | NASA JPL / USGS     | 30 m (1 arc-sec)  | Static Baseline     | Public Domain    | Earthdata / USGS    |
| DOH Weekly PIDSR Bulletins| DOH Epidemiology Bur| Municipal (17 LGU)| EpiWeek (Weekly)    | Official Health  | DOH EB / Digitized  |
| WorldPop & PSA 2020 CPH  | PSA / WorldPop      | 100 m / Barangay  | 2020 Base / Proj.   | CC BY 4.0 / Open | WorldPop FTP / PSA  |
+--------------------------+---------------------+-------------------+---------------------+------------------+---------------------+
```

---

### 2.1 Atmospheric & Particulate Pollution Datasets

#### 1. Sentinel-5P TROPOMI (TROPOspheric Monitoring Instrument)
- **Canonical Collections**:
  - Ultraviolet Aerosol Index: `COPERNICUS/S5P/OFFL/L3_AER_AI`
  - Nitrogen Dioxide Tropospheric Column: `COPERNICUS/S5P/OFFL/L3_NO2`
  - Carbon Monoxide Total Column: `COPERNICUS/S5P/OFFL/L3_CO`
- **Source / Custodian**: European Space Agency (ESA) & European Commission Copernicus Programme.
- **Spatial Resolution & Coverage**: $3.5\ \text{km} \times 5.5\ \text{km}$ nadir footprint; clipped to Metro Manila bounding box (`[120.85, 14.35, 121.15, 14.80]`).
- **Temporal Resolution**: Daily overpass (~13:30 local solar time); 2018–present.
- **License**: Creative Commons Attribution 4.0 International (CC BY 4.0) via Copernicus Open Access Policy.
- **Automated Ingestion Pipeline (Google Earth Engine Python API)**:
```python
import ee

ee.Initialize()
ncr_geom = ee.Geometry.Rectangle([120.85, 14.35, 121.15, 14.80])

def extract_sentinel5p_aer_ai(start_date: str, end_date: str):
    """Fetches QA-filtered Sentinel-5P Aerosol Index over Metro Manila."""
    collection = (
        ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_AER_AI")
        .filterBounds(ncr_geom)
        .filterDate(start_date, end_date)
        .select("absorbing_aerosol_index")
    )
    return collection
```

#### 2. MODIS MAIAC Aerosol Optical Depth (AOD)
- **Canonical Product**: `MCD19A2` Version 6.1 (Multi-Angle Implementation of Atmospheric Correction [MAIAC] Terrestrial AOD).
- **Source / Custodian**: NASA Land Processes Distributed Active Archive Center (LP DAAC) / Goddard Space Flight Center.
- **Spatial Resolution**: Gridded $1.0\ \text{km} \times 1.0\ \text{km}$.
- **Temporal Resolution**: Daily composite from Terra (~10:30) and Aqua (~13:30) satellite platforms; 2000–present.
- **License**: NASA Open Data Policy (unrestricted public use).
- **Download Pipeline**: Extracted via NASA Earthdata API using Python `earthaccess` client or Earth Engine Collection `MODIS/061/MCD19A2_GRANULES`.
```python
import earthaccess

def query_modis_maiac_aod(start_date: str, end_date: str):
    auth = earthaccess.login(strategy="netrc")
    granules = earthaccess.search_data(
        short_name="MCD19A2",
        bounding_box=(120.85, 14.35, 121.15, 14.80),
        temporal=(start_date, end_date),
    )
    # Filter for SDS: Optical_Depth_055 with QA flags == 0 (best quality)
    return earthaccess.download(granules, "data/raw/atmospheric/modis_aod/")
```

---

### 2.2 Thermal & Urban Heat Island (UHI) Datasets

#### 3. Landsat 8/9 Thermal Infrared Sensor (TIRS) Surface Temperature
- **Canonical Collection**: `LANDSAT/LC08/C02/T1_L2` and `LANDSAT/LC09/C02/T1_L2` (Collection 2, Level-2 Surface Temperature [ST] Band 10).
- **Source / Custodian**: U.S. Geological Survey (USGS) and NASA.
- **Spatial Resolution**: 30-meter pixels (instrument thermal resolution $100\ \text{m}$, resampled to $30\ \text{m}$ using cubic convolution).
- **Temporal Resolution**: 16-day repeat cycle (combined 8-day constellation frequency with Landsat 8 and 9); 2013–present.
- **License**: Public Domain (USGS Open Data Policy).
- **Ingestion & Calibration**: Pixel values converted to Land Surface Temperature in Kelvin using scale factor $0.00341802$ and offset $149.0$:
$$\text{LST}_{\text{Kelvin}} = (\text{DN} \times 0.00341802) + 149.0$$
$$\text{LST}_{\text{Celsius}} = \text{LST}_{\text{Kelvin}} - 273.15$$

#### 4. MODIS Land Surface Temperature (MOD11A1 / MYD11A1)
- **Canonical Product**: `MOD11A1` (Terra) and `MYD11A1` (Aqua) Version 6.1 Daily LST and Emissivity.
- **Source / Custodian**: NASA LP DAAC.
- **Spatial Resolution**: $1.0\ \text{km} \times 1.0\ \text{km}$.
- **Temporal Resolution**: Daily day/night observations; continuous coverage.
- **License**: Public Domain / NASA Open Data Policy.
- **Role**: Provides daily continuity for heatwave surveillance, bridging the 8–16 day cloud-gaps of Landsat.

---

### 2.3 Hydrometeorology & Drainage Topography Datasets

#### 5. DOST-PAGASA Synoptic Observations & Rainfall Advisories
- **Primary Source**: Philippine Atmospheric, Geophysical and Astronomical Services Administration (DOST-PAGASA).
- **Key Metro Manila Stations**:
  - Science Garden Synoptic Station (*Quezon City*; WMO ID: 98429; Lat: 14.65°N, Lon: 121.04°E)
  - Port Area Synoptic Station (*Manila City*; WMO ID: 98425; Lat: 14.59°N, Lon: 120.97°E)
  - Ninoy Aquino International Airport (NAIA) Station (*Pasay City*; WMO ID: 98430; Lat: 14.51°N, Lon: 121.01°E)
- **Variables**: Hourly rainfall (mm), 24-hour cumulative rainfall, dry-bulb temperature, relative humidity, calculated apparent heat index, tropical cyclone rainfall advisories (Yellow, Orange, Red Warning levels).
- **License**: Open Government Data (Philippines), accessed via Philippine Freedom of Information (`eFOI.gov.ph`) portal and official PAGASA Weather Bulletins.

#### 6. ERA5-Land Climate Reanalysis
- **Canonical Product**: `ECMWF/ERA5_LAND/HOURLY` (Copernicus Climate Change Service).
- **Source / Custodian**: European Centre for Medium-Range Weather Forecasts (ECMWF).
- **Spatial Resolution**: $0.1^\circ \times 0.1^\circ$ (approx. $9\ \text{km} \times 9\ \text{km}$).
- **Temporal Resolution**: Hourly reanalysis, aggregated to daily totals.
- **Key Parameters**: `total_precipitation_hourly`, `volumetric_soil_water_layer_1` ($0\text{--}7\ \text{cm}$ soil moisture saturation), `2m_temperature`, `2m_dewpoint_temperature`.
- **License**: Copernicus C3S License (CC BY 4.0 equivalent).
- **Pipeline**: Automated retrieval using the official ECMWF `cdsapi` library.

#### 7. Shuttle Radar Topography Mission (SRTM) Digital Elevation Model
- **Canonical Product**: NASA SRTM 1-Arc-Second Global DEM (`USGS/SRTMGL1_003`).
- **Source / Custodian**: NASA Jet Propulsion Laboratory (JPL) & USGS.
- **Spatial Resolution**: 1 arc-second (~$30\ \text{meters}$).
- **Temporal Resolution**: Static topographic baseline.
- **Derived Hydrologic Features**:
  1. Elevation above mean sea level ($z$, meters).
  2. Topographic slope gradient ($\theta = \arctan(\sqrt{(\partial z / \partial x)^2 + (\partial z / \partial y)^2})$ in degrees/percent).
  3. Topographic Wetness Index ($\text{TWI} = \ln(\alpha / \tan \beta)$), isolating low-lying urban depression zones with natural drainage slope $<1.0\%$.

---

### 2.4 Epidemiological Registries & Demographics

#### 8. DOH Weekly Disease Registries (PIDSR / FASSSTER)
- **Primary Source**: Epidemiology Bureau (EB), Department of Health, Republic of the Philippines.
- **Registry Framework**: Event-Based Surveillance and Response (ESR) and Philippine Integrated Disease Surveillance and Response (PIDSR).
- **Spatial Granularity**: **Municipal / City LGU level** across 17 administrative units in NCR.
- **Temporal Granularity**: Weekly aggregated counts keyed by Epidemiological Week (`EpiWeek_YYYY_WW`).
- **Parameters**: Total confirmed/suspected leptospirosis cases, validated deaths, hospital admissions, reported direct flood exposure flag.
- **License / Authorization**: Official Public Health Surveillance Release under statutory disease reporting mandate (Republic Act 11332; Mandatory Reporting of Notifiable Diseases). Strictly anonymized and aggregated.

#### 9. PSA Census of Population and Housing & WorldPop Demographics
- **Primary Sources**:
  - Philippine Statistics Authority (PSA): 2020 Census of Population and Housing (2020 CPH) municipal and barangay-level population aggregates.
  - WorldPop Project (University of Southampton): Gridded 100-meter population count and age/sex-structured density surfaces (constrained building footprint model).
- **Spatial Resolution**: 100-meter raster grid and vector LGU administrative polygons.
- **License**: PSA Open Data Policy / Creative Commons Attribution 4.0 International (CC BY 4.0).
- **Pipeline**: Direct download from the WorldPop FTP repository (`hub.worldpop.org`) and integration with PSA Philippine Standard Geographic Codes (PSGC).

---

## 3. Data Quality, Null-Handling & Harmonization Protocols

To ensure robust modeling free from spatial or temporal artifacts, the pipeline executes rigorous pre-processing standards:

```
Raw Multi-Sensor Ingestion
         │
         ├──> Satellite Optical/Thermal Quality Masking (QA Bitmasking)
         │    - Sentinel-5P: Filter `qa_value >= 0.50` (removes thick cloud & ice contamination)
         │    - Landsat 8/9: Decode `QA_PIXEL` bitmask (strip high aerosol & cloud shadow pixels)
         │    - MODIS MAIAC: Filter `AOD_QA == 0` (best cloud-free surface retrieval)
         │
         ├──> Spatiotemporal Null Imputation
         │    - Meteorological Gaps: Fill short missing runs (≤ 3 hours) via Akima cubic spline
         │    - Persistent Cloud Occlusion: Spatial interpolation via ordinary Kriging & MissForest
         │    - Rolling Temporal Median: 7-day trailing window imputation for satellite grids
         │
         └──> Spatial & Temporal Alignment
              - Resample all rasters to standard 100m grid using bilinear interpolation
              - Zonal aggregation across the 17 NCR Municipal Boundaries (GADM / PSA PSGC)
              - Harmonize all streams into unified ISO EpiWeek bins (Monday to Sunday)
```

---

## 4. Compliance Check: Strict Data Privacy Protocol (Republic Act 10173)

Project Avatar handles public health metrics within a strict legal and ethical framework governed by **Republic Act No. 10173**, known as the **Data Privacy Act of 2012 (DPA)**, its Implementing Rules and Regulations (IRR), and governing advisories issued by the **National Privacy Commission (NPC)** of the Philippines.

```
+----------------------------------------------------------------------------------------------------+
|                         DATA PRIVACY ACT OF 2012 (RA 10173) COMPLIANCE AUDIT                       |
+--------------------------+-------------------------------------------------------------------------+
| Regulatory Dimension     | Project Avatar Protocol Specification                                   |
+--------------------------+-------------------------------------------------------------------------+
| Statutory Classification | Health and disease outcome metrics are classified as                    |
|                          | Sensitive Personal Information under Section 3(l) of RA 10173.          |
+--------------------------+-------------------------------------------------------------------------+
| Legal Processing Basis   | Public health research exemption pursuant to Section 12(e) and          |
|                          | Section 13(f) of RA 10173; strictly non-commercial open research.      |
+--------------------------+-------------------------------------------------------------------------+
| Spatial De-Identification| Absolute restriction to Municipal / City LGU level (17 units in NCR).   |
|                          | Zero storage of street addresses, barangay micro-locators, or GPS cords.|
+--------------------------+-------------------------------------------------------------------------+
| Small Cell Suppression   | Statistical disclosure control (k ≥ 5 convention). Any cell with fewer    |
| (k-Anonymity Threshold)  | than 5 recorded cases is suppressed or pooled into sub-regional strata.  |
+--------------------------+-------------------------------------------------------------------------+
| Attribute Generalization | Age attributes collapsed into broad five-tier epidemiological brackets  |
|                          | (<5, 5-14, 15-24, 25-59, 60+); exact birthdates permanently purged.     |
+--------------------------+-------------------------------------------------------------------------+
| Technical Defense        | Cryptographic SHA-256 integrity verification; air-gapped processing     |
|                          | scripts; automated .gitignore blocking raw disaggregated tables.        |
+--------------------------+-------------------------------------------------------------------------+
```

### 4.1 Statutory Basis & Legal Classification
Under Section 3(l) of RA 10173, an individual's medical history, clinical diagnoses, physical condition, and disease infection status are classified as **Sensitive Personal Information**. Processing of sensitive personal information is strictly prohibited unless specific statutory exemptions apply. 

Project Avatar operates under the **Scientific, Statistical, and Public Health Exemption** pursuant to:
- **Section 12(e)**: Processing is necessary to protect the life and health of the data subject and public.
- **Section 13(f)**: Processing concerns information necessary for historical, statistical, or scientific research, carried out pursuant to law with adequate guarantees for the protection of personal data.
- **Section 19(d) of the IRR**: Personal data repurposed for scientific and statistical research must be **aggregated or rendered into a form that does not permit the identification of data subjects**.

### 4.2 Prevention of Re-Identification: Spatial $k$-Anonymity & Cell Suppression
Direct identifiers (patient names, PhilHealth identification numbers, residential street addresses, contact details) are **never ingested, accessed, or persisted** at any stage of the Project Avatar pipeline. 

To eliminate the danger of **re-identification via quasi-identifier linkage attacks** (e.g., cross-referencing rare disease occurrences with local death notices, social media announcements, or emergency dispatch logs), the following algorithmic disclosure controls are strictly enforced:

1. **Spatial Aggregation Ceiling**: 
   - Spatial reporting is capped strictly at the **Municipal / City LGU level** (the 16 cities and 1 municipality of NCR: *City of Manila, Quezon City, Caloocan, Las Piñas, Makati, Malabon, Mandaluyong, Marikina, Muntinlupa, Navotas, Parañaque, Pasay, Pasig, San Juan, Taguig, Valenzuela, and Pateros*).
   - Sub-municipal microdata (such as individual barangay polygons, puroks, or residential coordinates) are explicitly banned from public release and modeling tables.
2. **Mandatory Small Cell Suppression Rule ($k \ge 5$)**:
   - In any municipal-temporal reporting cell where the count of confirmed or suspected cases satisfies:
     $$1 \le n_{\text{cases}} < 5$$
   - The cell is flagged as privacy-sensitive and subjected to **mandatory suppression** (rendered as `"<5"` or pooled into sub-regional quadrants: CAMANAVA, Central NCR, Southern NCR, or Eastern NCR).
   - This guarantees that no unique individual ($k = 1$) or pair ($k = 2$) can be singled out from the data matrix.
3. **Attribute Generalization**:
   - Age is generalized into standardized public health cohorts: `[0-4]`, `[5-14]`, `[15-24]`, `[25-59]`, and `[60+]`.
   - Date of symptom onset is collapsed into weekly bins (`EpiWeek`), removing specific calendar dates.

### 4.3 Technical Security Safeguards & Repository Protections
In conformance with National Privacy Commission Circular No. 16-01 (*Security of Personal Data in Government Agencies*):
- **Automated Repository Guardrails**: The root `.gitignore` file contains hard rules prohibiting the staging, tracking, or committing of any files matching `data/raw/epidemiological/*_linelist*`, `*.csv` containing identifiable tokens, or patient spreadsheets.
- **Cryptographic Checksums**: All downloaded raw environmental assets are hashed upon retrieval using SHA-256 to ensure data provenance and prevent tampering:
```bash
sha256sum data/raw/hydrometeorological/* > data/raw/checksums.sha256
```
- **Differential Privacy Protocol for API Endpoints**: Public web application endpoints serving risk scores inject calibrated Laplace noise ($\epsilon = 0.5$) into aggregate query returns whenever underlying population denominators fall below $10,000$ individuals, eliminating reconstruction risks.

---

## 5. References (Strict APA 7th Edition)

Copernicus Climate Change Service. (2020). *ERA5-Land hourly data from 1950 to present* [Data set]. ECMWF. https://doi.org/10.24381/cds.e2161bac

Department of Environment and Natural Resources. (2020). *Administrative Order No. 2020-14: Revised national ambient air quality guideline values for particulate matter 2.5 (PM2.5)*. DENR Environmental Management Bureau. https://air.emb.gov.ph/wp-content/uploads/2020/07/DAO-2020-14-PM2.5.pdf

Department of Health. (2023). *Philippine integrated disease surveillance and response: System overview and operational manual*. Epidemiology Bureau, Department of Health, Republic of the Philippines. https://doh.gov.ph/

European Space Agency. (2021). *Sentinel-5P TROPOMI science product user guide* (Doc. No. S5P-MPC-SRON-SPUG). European Space Agency. https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-5p-tropomi/

Lyapustin, A., Wang, Y., Korkin, S., & Huang, D. (2018). MODIS collection 6 MAIAC algorithm. *Atmospheric Measurement Techniques*, 11(10), 5741–5765. https://doi.org/10.5194/amt-11-5741-2018

Muñoz-Sabater, J., Dutra, E., Agustí-Panareda, A., Albergel, C., Arduini, G., Balsamo, G., Boussetta, S., Choulga, M., Harrigan, S., Hersbach, H., Martens, B., Miralles, D. G., Piles, M., Rodríguez-Fernández, N. J., Zsoter, E., Buontempo, C., & Thépaut, J.-N. (2021). ERA5-Land: A state-of-the-art global reanalysis dataset for land applications. *Earth System Science Data*, 13(9), 4349–4383. https://doi.org/10.5194/essd-13-4349-2021

NASA Jet Propulsion Laboratory. (2013). *NASA Shuttle Radar Topography Mission (SRTM) global 1 arc-second* [Data set]. NASA EOSDIS Land Processes DAAC. https://doi.org/10.5067/MEaSUREs/SRTM/SRTMGL1.003

National Privacy Commission. (2016). *NPC Circular 16-01: Security of personal data in government agencies*. National Privacy Commission of the Philippines. https://privacy.gov.ph/wp-content/uploads/2016/10/NPC_Circular_No.16-01.pdf

Philippine Atmospheric, Geophysical and Astronomical Services Administration. (2024). *Manual of meteorological observation practices in the Philippines*. Department of Science and Technology. https://bagong.pagasa.dost.gov.ph/learning-tools/meteorological-instruments

Philippine Statistics Authority. (2021). *2020 census of population and housing (2020 CPH) population counts declared official by the President: National Capital Region*. Philippine Statistics Authority. https://psa.gov.ph/

Republic of the Philippines. (2012). *Republic Act No. 10173: Data Privacy Act of 2012*. Official Gazette of the Republic of the Philippines. https://www.officialgazette.gov.ph/2012/08/15/republic-act-no-10173/

Republic of the Philippines. (2019). *Republic Act No. 11332: Mandatory Reporting of Notifiable Diseases and Health Events of Public Health Concern Act*. Official Gazette of the Republic of the Philippines. https://www.officialgazette.gov.ph/2019/04/26/republic-act-no-11332/

U.S. Geological Survey. (2021). *Landsat 8-9 Collection 2 Level 2 Science Product Guide* (LSDS-1619, Version 2.0). Earth Resources Observation and Science (EROS) Center, U.S. Geological Survey. https://www.usgs.gov/media/files/landsat-8-9-collection-2-level-2-science-product-guide

Wan, Z., Hook, S., & Hulley, G. (2021). *MOD11A1 MODIS/Terra Land Surface Temperature/Emissivity Daily L3 Global 1km SIN Grid V061* [Data set]. NASA EOSDIS Land Processes DAAC. https://doi.org/10.5067/MODIS/MOD11A1.061

World Health Organization. (2021). *WHO global air quality guidelines: Particulate matter (PM2.5 and PM10), ozone, nitrogen dioxide, sulfur dioxide and carbon monoxide*. World Health Organization. https://apps.who.int/iris/handle/10665/345329

WorldPop. (2020). *Global high resolution population denominators project: Philippines 100m population counts* [Data set]. University of Southampton. https://hub.worldpop.org/geodata/summary?id=24785
