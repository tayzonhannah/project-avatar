"""
Project Avatar: Ground Truth Raw Fixture Generator
Grounded in DOH PIDSR, DENR-EMB, PAGASA, ERA5, Landsat/MODIS, and SRTM DEM
Generates reproducible synthetic raw data for PJDSC 2026 EDA.
"""

import os
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set global random state for absolute reproducibility
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Metro Manila Spatial Bounds
BBOX = {
    "min_lon": 120.85,
    "max_lon": 121.15,
    "min_lat": 14.35,
    "max_lat": 14.80,
    "crs_storage": "EPSG:4326",
    "crs_metric": "EPSG:32651",
    "grid_res_km": 1.0,
    "n_cols": 30, # ~1 km step in lon (~0.01 deg)
    "n_rows": 45  # ~1 km step in lat (~0.01 deg)
}

LGUS = [
    {"name": "City of Manila", "pop": 1846513, "basin": "Core Estero Belt", "base_elev": 3.2, "base_slope": 0.4},
    {"name": "Quezon City", "pop": 2960048, "basin": "Marikina River Basin / Plateau", "base_elev": 38.5, "base_slope": 3.8},
    {"name": "Caloocan", "pop": 1661584, "basin": "CAMANAVA Coastal Corridor", "base_elev": 6.5, "base_slope": 0.8},
    {"name": "Las Piñas", "pop": 606293, "basin": "Southern Coastal Plains", "base_elev": 8.0, "base_slope": 1.1},
    {"name": "Makati", "pop": 629616, "basin": "Pasig River Corridor", "base_elev": 15.2, "base_slope": 1.4},
    {"name": "Malabon", "pop": 380522, "basin": "CAMANAVA Coastal Corridor", "base_elev": 2.1, "base_slope": 0.3},
    {"name": "Mandaluyong", "pop": 425758, "basin": "Pasig River Corridor", "base_elev": 16.0, "base_slope": 1.8},
    {"name": "Marikina", "pop": 456059, "basin": "Marikina River Basin", "base_elev": 7.4, "base_slope": 0.6},
    {"name": "Muntinlupa", "pop": 543445, "basin": "Laguna Lake Shoreline", "base_elev": 12.5, "base_slope": 1.5},
    {"name": "Navotas", "pop": 247543, "basin": "CAMANAVA Coastal Corridor", "base_elev": 1.8, "base_slope": 0.2},
    {"name": "Parañaque", "pop": 689992, "basin": "Southern Coastal Plains", "base_elev": 5.5, "base_slope": 0.7},
    {"name": "Pasay", "pop": 440655, "basin": "Core Estero Belt / Bayfront", "base_elev": 3.5, "base_slope": 0.4},
    {"name": "Pasig", "pop": 803159, "basin": "Marikina / Manggahan Basin", "base_elev": 8.2, "base_slope": 0.7},
    {"name": "San Juan", "pop": 126347, "basin": "San Juan River Basin", "base_elev": 14.0, "base_slope": 1.5},
    {"name": "Taguig", "pop": 886722, "basin": "Laguna Lake Shoreline", "base_elev": 9.0, "base_slope": 1.0},
    {"name": "Valenzuela", "pop": 714978, "basin": "CAMANAVA Coastal Corridor", "base_elev": 3.8, "base_slope": 0.5},
    {"name": "Pateros", "pop": 65227, "basin": "Pasig / Manggahan Tributary", "base_elev": 4.1, "base_slope": 0.4}
]

def generate_epidemiological_data():
    """Generates weekly municipal DOH leptospirosis surveillance data for 2023-2024."""
    records = []
    linelist_records = []
    
    # 104 weeks (52 weeks for 2023, 52 weeks for 2024)
    start_date_2023 = datetime(2023, 1, 1) # Sunday
    
    # Pre-generate meteorological surge factors (typhoons, monsoon)
    weeks = []
    for yr in [2023, 2024]:
        for wk in range(1, 53):
            weeks.append((yr, wk))
            
    for yr, wk in weeks:
        week_idx = (yr - 2023) * 52 + (wk - 1)
        epi_date = start_date_2023 + timedelta(days=week_idx * 7)
        epiweek_str = f"{yr}-W{wk:02d}"
        
        # Hydrological flood shock event definition
        # 2023: Monsoon Habagat in weeks 28-31; Typhoon Egay (week 30), Goring (week 35)
        # 2024: Massive surges: Carina + Habagat in week 30 (July), Kristine in week 43 (Oct)
        rain_shock = 0.0
        if yr == 2023 and 28 <= wk <= 34:
            rain_shock = 1.2 * np.sin((wk - 27) / 7.0 * np.pi)
        elif yr == 2024 and 29 <= wk <= 35: # Typhoon Carina shock wave
            rain_shock = 3.5 * np.exp(-0.5 * ((wk - 30) / 1.5)**2)
        elif yr == 2024 and 42 <= wk <= 46: # Typhoon Kristine shock wave
            rain_shock = 2.4 * np.exp(-0.5 * ((wk - 43) / 1.2)**2)
            
        for lgu in LGUS:
            lgu_name = lgu["name"]
            pop = lgu["pop"]
            basin = lgu["basin"]
            elev = lgu["base_elev"]
            
            # Vulnerability multiplier based on elevation and drainage
            flood_vuln = max(0.5, (15.0 - min(15.0, elev)) / 5.0)
            if "CAMANAVA" in basin or "Marikina" in basin or "Estero" in basin:
                flood_vuln *= 1.4
                
            # Base endemic incidence per 100k per week
            base_rate_per_100k = 0.15 + 0.10 * np.sin((wk - 10) / 52.0 * 2 * np.pi)
            if yr == 2024:
                base_rate_per_100k *= 1.2 # slightly higher baseline
                
            # Surge driven by lagged hydrological shock (we model it directly here so CCF picks it up)
            # Leptospirosis surge peaks 2-4 weeks after rain shock
            lagged_shock = 0.0
            if yr == 2024 and 31 <= wk <= 38: # 1-4 weeks after Carina (week 30)
                lag_w = wk - 30
                # Biologically peaks at lag 2-3 weeks
                peak_factor = np.exp(-0.5 * ((lag_w - 2.5) / 1.2)**2)
                lagged_shock += 4.5 * peak_factor * flood_vuln
            elif yr == 2024 and 44 <= wk <= 49: # 1-3 weeks after Kristine (week 43)
                lag_w = wk - 43
                peak_factor = np.exp(-0.5 * ((lag_w - 2.2) / 1.0)**2)
                lagged_shock += 3.2 * peak_factor * flood_vuln
            elif yr == 2023 and 30 <= wk <= 36:
                lag_w = wk - 29
                peak_factor = np.exp(-0.5 * ((lag_w - 2.5) / 1.4)**2)
                lagged_shock += 1.8 * peak_factor * flood_vuln
                
            total_rate_per_100k = max(0.02, base_rate_per_100k + lagged_shock)
            expected_cases = (total_rate_per_100k * pop) / 100000.0
            
            # Poisson draw for case count
            cases = int(np.random.poisson(lam=expected_cases))
            
            # Case fatality rate: baseline ~10-11% in 2023, ~7.9% in 2024
            cfr_prob = 0.108 if yr == 2023 else 0.079
            # Slight increase in CFR when cases spike due to dialysis bed saturation
            if cases > 15:
                cfr_prob += 0.02
            deaths = int(np.random.binomial(n=cases, p=min(0.25, cfr_prob)))
            
            # Hospital admissions (~85-92% of cases)
            hosp_admissions = int(np.random.binomial(n=cases, p=0.88))
            
            # Flood exposure proportion (>72% in confirmed cases)
            flood_exp_prob = 0.74 if lagged_shock > 0.5 else 0.45
            flood_exposed = int(np.random.binomial(n=cases, p=flood_exp_prob))
            
            records.append({
                "epiweek": epiweek_str,
                "year": yr,
                "week": wk,
                "start_date": epi_date.strftime("%Y-%m-%d"),
                "lgu_name": lgu_name,
                "population": pop,
                "reported_cases": cases,
                "reported_deaths": deaths,
                "hospital_admissions": hosp_admissions,
                "flood_exposed_cases": flood_exposed
            })
            
            # Sample patient surveillance linelist records for reporting delay profiling
            # Generate individual case rows for this LGU & week
            for c_id in range(min(cases, 8)): # sample up to 8 cases per cell for linelist
                # Incubation & symptom onset (2 to 14 days prior to admission)
                incubation_days = int(np.random.gamma(shape=3.0, scale=3.0)) # mean ~9 days
                onset_offset = int(np.random.gamma(shape=2.5, scale=2.0)) # 5 days before admission
                
                # Admission date within the current week
                adm_offset = np.random.randint(0, 7)
                adm_date = epi_date + timedelta(days=adm_offset)
                onset_date = adm_date - timedelta(days=max(1, onset_offset))
                
                # Reporting lag from admission to DOH central registration (MAT test + transmission)
                # Normal conditions: 7-14 days. Monsoonal crisis / surge: MAR (missingness/delay extends to 18-35 days)
                is_surge = (yr == 2024 and 30 <= wk <= 36) or (yr == 2024 and 43 <= wk <= 47)
                if is_surge:
                    reporting_lag = int(np.random.lognormal(mean=2.8, sigma=0.4)) # median ~16 days, tail up to 35
                    # Introduce Missing at Random (MAR) in onset date during surge crisis
                    onset_missing = (np.random.rand() < 0.22)
                else:
                    reporting_lag = int(np.random.lognormal(mean=2.2, sigma=0.35)) # median ~9 days
                    # Introduce Missing Completely at Random (MCAR)
                    onset_missing = (np.random.rand() < 0.04)
                    
                report_date = adm_date + timedelta(days=reporting_lag)
                total_delay = (report_date - onset_date).days
                
                linelist_records.append({
                    "case_uuid": f"LEP-{yr}-{wk:02d}-{lgu_name[:3].upper()}-{c_id:03d}",
                    "lgu_name": lgu_name,
                    "epiweek": epiweek_str,
                    "symptom_onset_date": None if onset_missing else onset_date.strftime("%Y-%m-%d"),
                    "admission_date": adm_date.strftime("%Y-%m-%d"),
                    "doh_report_date": report_date.strftime("%Y-%m-%d"),
                    "clinical_admission_lag_days": (adm_date - onset_date).days if not onset_missing else None,
                    "lab_and_reporting_delay_days": reporting_lag,
                    "total_surveillance_lag_days": total_delay if not onset_missing else None,
                    "outcome": "Fatal" if (c_id < deaths) else "Recovered/Discharged",
                    "waded_in_flood": bool(np.random.rand() < flood_exp_prob)
                })
                
    df_surv = pd.DataFrame(records)
    df_line = pd.DataFrame(linelist_records)
    return df_surv, df_line

def generate_atmospheric_data():
    """Generates daily DENR-EMB station PM2.5 readings for 2023-2024."""
    stations = [
        {"station_id": "EMB-NCAL", "name": "North Caloocan", "lat": 14.755, "lon": 121.038, "base_pm": 34.5},
        {"station_id": "EMB-QC-CW", "name": "Commonwealth QC", "lat": 14.685, "lon": 121.082, "base_pm": 31.0},
        {"station_id": "EMB-PASIG", "name": "Pasig City Hall", "lat": 14.558, "lon": 121.060, "base_pm": 29.2},
        {"station_id": "EMB-MALABON", "name": "Malabon", "lat": 14.662, "lon": 120.957, "base_pm": 36.8},
        {"station_id": "EMB-VAL", "name": "Valenzuela", "lat": 14.700, "lon": 120.983, "base_pm": 35.1},
        {"station_id": "EMB-BICUTAN", "name": "Bicutan Parañaque", "lat": 14.493, "lon": 121.048, "base_pm": 28.5},
        {"station_id": "EMB-TAFT", "name": "Taft Ave Manila", "lat": 14.576, "lon": 120.988, "base_pm": 38.2}
    ]
    
    dates = pd.date_range("2023-01-01", "2024-12-31", freq="D")
    records = []
    
    for d in dates:
        day_of_year = d.dayofyear
        month = d.month
        # Seasonal modulation: High PM2.5 in dry/cool months (Nov - Feb), lower during monsoonal washout (June - Oct)
        season_mod = 12.0 * np.cos((day_of_year + 15) / 365.0 * 2 * np.pi)
        
        # Heavy rain wash-out events (e.g. Typhoon Carina late July 2024, Kristine late Oct 2024)
        rain_washout = 0.0
        if d.year == 2024 and 7 <= month <= 10:
            rain_washout = -14.0 * (1.0 if month in [7, 8, 10] else 0.5)
            
        for stn in stations:
            # Baseline + seasonal + station bias + random variation
            daily_pm = stn["base_pm"] + season_mod + rain_washout + np.random.normal(0, 5.5)
            daily_pm = max(5.0, daily_pm)
            
            # Missingness due to station maintenance/telemetry failure (18% missing)
            # Higher missingness during heavy storm events
            miss_prob = 0.28 if (d.year == 2024 and month in [7, 10]) else 0.16
            is_missing = (np.random.rand() < miss_prob)
            
            records.append({
                "date": d.strftime("%Y-%m-%d"),
                "year": d.year,
                "month": d.month,
                "epiweek": f"{d.isocalendar().year}-W{d.isocalendar().week:02d}",
                "station_id": stn["station_id"],
                "station_name": stn["name"],
                "latitude": stn["lat"],
                "longitude": stn["lon"],
                "pm25_ug_m3": None if is_missing else round(daily_pm, 2),
                "is_valid_reading": not is_missing
            })
            
    return pd.DataFrame(records)

def generate_hydrometeorological_data():
    """Generates PAGASA synoptic station observations and ERA5-Land gridded reanalysis."""
    pagasa_stns = [
        {"stn_id": "PAGASA-98429", "name": "Science Garden (Quezon City)", "lat": 14.65, "lon": 121.04},
        {"stn_id": "PAGASA-98425", "name": "Port Area (Manila)", "lat": 14.59, "lon": 120.97},
        {"stn_id": "PAGASA-98430", "name": "NAIA (Pasay City)", "lat": 14.51, "lon": 121.01}
    ]
    
    dates = pd.date_range("2023-01-01", "2024-12-31", freq="D")
    pagasa_records = []
    
    for d in dates:
        month = d.month
        # Rainfall seasonality: dry (Jan-April), monsoonal wet (May-Nov)
        base_rain = 2.0 if month in [1, 2, 3, 4] else 12.0
        
        # Extreme cyclone rainfall events
        # July 22-25, 2024: Typhoon Carina (Gaemi) + Habagat
        if d.year == 2024 and d.month == 7 and 22 <= d.day <= 25:
            base_rain += 140.0 * np.exp(-0.5 * ((d.day - 24) / 1.0)**2)
        # Oct 22-24, 2024: Severe Tropical Storm Kristine
        elif d.year == 2024 and d.month == 10 and 22 <= d.day <= 24:
            base_rain += 95.0 * np.exp(-0.5 * ((d.day - 23) / 1.0)**2)
        # July 25-28, 2023: Typhoon Egay
        elif d.year == 2023 and d.month == 7 and 25 <= d.day <= 28:
            base_rain += 65.0 * np.exp(-0.5 * ((d.day - 26) / 1.0)**2)
            
        # Thermal: March-May heat waves (El Niño 2024)
        is_heatwave = (d.year == 2024 and month in [3, 4, 5])
        base_tmax = 36.5 if is_heatwave else (33.0 if month in [4, 5] else 30.5)
        
        for stn in pagasa_stns:
            stn_rain = max(0.0, np.random.exponential(scale=base_rain) if base_rain > 5 else (np.random.exponential(scale=2.0) if np.random.rand() < 0.25 else 0.0))
            if base_rain > 40: # forced intense cyclone rain
                stn_rain = max(50.0, base_rain + np.random.normal(0, 15))
                
            tmax = base_tmax + np.random.normal(0, 1.2)
            rh = 65.0 + (18.0 if stn_rain > 10 else -5.0) + np.random.normal(0, 4.0)
            rh = min(98.0, max(45.0, rh))
            
            # Simplified PAGASA Heat Index calculation
            # HI approx formula
            hi = -8.784 + 1.611 * tmax + 2.338 * (rh/100) * tmax - 0.146 * rh
            if is_heatwave:
                hi = max(42.0, min(48.5, hi + 4.5)) # danger threshold
            else:
                hi = max(28.0, min(41.0, hi))
                
            pagasa_records.append({
                "date": d.strftime("%Y-%m-%d"),
                "year": d.year,
                "month": d.month,
                "epiweek": f"{d.isocalendar().year}-W{d.isocalendar().week:02d}",
                "station_id": stn["stn_id"],
                "station_name": stn["name"],
                "rainfall_daily_mm": round(stn_rain, 1),
                "tmax_celsius": round(tmax, 1),
                "relative_humidity_pct": round(rh, 1),
                "pagasa_heat_index_celsius": round(hi, 1)
            })
            
    df_pagasa = pd.DataFrame(pagasa_records)
    
    # ERA5-Land gridded reanalysis (0.1 deg, ~9 km resolution, aggregated to weekly)
    # Covering bbox: lat 14.3 to 14.9, lon 120.8 to 121.2
    era5_lats = [14.4, 14.5, 14.6, 14.7, 14.8]
    era5_lons = [120.9, 121.0, 121.1]
    
    era5_records = []
    weeks = df_pagasa[["year", "epiweek"]].drop_duplicates().values
    
    # Calculate weekly rain benchmark from pagasa
    weekly_pagasa_rain = df_pagasa.groupby(["year", "epiweek"])["rainfall_daily_mm"].sum().reset_index()
    pagasa_rain_map = dict(zip(weekly_pagasa_rain["epiweek"], weekly_pagasa_rain["rainfall_daily_mm"] / 3.0)) # avg station total
    
    for yr, ew in weeks:
        mean_rain = pagasa_rain_map.get(ew, 15.0)
        # Soil moisture saturation lags rainfall and accumulates
        soil_moisture_base = 0.22 + min(0.30, mean_rain / 500.0)
        
        for lat in era5_lats:
            for lon in era5_lons:
                # Spatial gradient: higher rain toward eastern Sierra Madre foothills (lon 121.1)
                east_grad = (lon - 120.9) * 20.0
                cell_rain = max(0.0, mean_rain + east_grad + np.random.normal(0, 5.0))
                cell_soil_water = min(0.55, max(0.18, soil_moisture_base + (0.05 if lat < 14.6 else 0.0) + np.random.normal(0, 0.02)))
                
                era5_records.append({
                    "year": int(yr),
                    "epiweek": ew,
                    "grid_lat": lat,
                    "grid_lon": lon,
                    "total_precipitation_weekly_mm": round(cell_rain, 2),
                    "volumetric_soil_water_layer_1": round(cell_soil_water, 4),
                    "temp_2m_weekly_mean_c": round(28.5 + np.random.normal(0, 1.2), 2)
                })
                
    df_era5 = pd.DataFrame(era5_records)
    return df_pagasa, df_era5

def generate_spatial_rasters():
    """Generates Landsat/MODIS LST, cloud occlusion masks, and SRTM DEM arrays."""
    n_rows = BBOX["n_rows"] # 45 rows (lat 14.35 to 14.80)
    n_cols = BBOX["n_cols"] # 30 cols (lon 120.85 to 121.15)
    
    lats = np.linspace(BBOX["max_lat"], BBOX["min_lat"], n_rows)
    lons = np.linspace(BBOX["min_lon"], BBOX["max_lon"], n_cols)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    
    # 1. SRTM DEM Elevation & Slope
    # Natural topography: Low near Manila Bay (west: lon < 120.98, elev 1-4m),
    # Marikina valley depression in middle-east (lat 14.6-14.7, lon 121.08-121.11, elev 5-9m),
    # QC Plateau (central north: elev 25-70m),
    # Rizal / Sierra Madre foothills to the far east (elev 50-120m).
    elev = np.zeros((n_rows, n_cols))
    for r in range(n_rows):
        for c in range(n_cols):
            curr_lat = lats[r]
            curr_lon = lons[c]
            
            # Distance from Manila bay coast (approx lon 120.95)
            coast_dist = max(0.0, curr_lon - 120.92)
            base_e = 2.0 + coast_dist * 180.0
            
            # QC Plateau bump
            if 14.62 <= curr_lat <= 14.74 and 121.00 <= curr_lon <= 121.08:
                base_e += 35.0 * np.exp(-((curr_lat - 14.68)/0.04)**2 - ((curr_lon - 121.04)/0.03)**2)
                
            # Marikina depression
            if 14.60 <= curr_lat <= 14.70 and 121.08 <= curr_lon <= 121.12:
                base_e = min(base_e, 7.5 + np.random.normal(0, 0.5))
                
            # CAMANAVA low-elevation coastal wetland
            if 14.63 <= curr_lat <= 14.75 and 120.92 <= curr_lon <= 120.98:
                base_e = min(base_e, 2.5 + np.random.normal(0, 0.4))
                
            elev[r, c] = max(0.5, base_e + np.random.normal(0, 0.8))
            
    # Calculate slope in percent: delta_z / delta_x
    dy, dx = np.gradient(elev, 1000.0) # ~1000m grid cell spacing
    slope_pct = np.sqrt(dx**2 + dy**2) * 100.0
    
    # Topographic Wetness Index (TWI): high where slope is flat and elevation is low
    twi = np.log((1000.0 + 10.0) / (np.tan(np.radians(np.clip(slope_pct, 0.1, 80.0))) + 1e-4))
    twi = np.clip(twi, 4.0, 16.0)
    
    # 2. Landsat 8/9 & MODIS LST (Celsius)
    # Urban Heat Island: High in dense commercial/residential built-up core (Manila, Pasay, Makati, Caloocan)
    # LST Anomalies: +3 to +7 deg C above coastal/rural baseline
    base_lst = 29.5
    uhi_anomaly = np.zeros((n_rows, n_cols))
    for r in range(n_rows):
        for c in range(n_cols):
            curr_lat = lats[r]
            curr_lon = lons[c]
            # Center of Manila/QC built-up zone
            dist_core = np.sqrt(((curr_lat - 14.60)/0.08)**2 + ((curr_lon - 121.00)/0.06)**2)
            uhi = max(0.0, 6.5 * np.exp(-0.5 * (dist_core / 1.0)**2))
            uhi_anomaly[r, c] = round(uhi + np.random.normal(0, 0.4), 2)
            
    lst_dry_season = base_lst + uhi_anomaly
    
    # 3. Cloud cover masking during monsoon season
    # High missingness due to cloud deck (up to 65% of pixels masked during wet season)
    cloud_mask_dry = np.random.rand(n_rows, n_cols) < 0.12 # 12% missing in dry season
    cloud_mask_wet = np.random.rand(n_rows, n_cols) < 0.68 # 68% missing in monsoon season
    
    # Save terrain npz
    terrain_path = "data/raw/terrain/srtm_dem_ncr_1km.npz"
    np.savez_compressed(
        terrain_path,
        elevation_m=elev,
        slope_pct=slope_pct,
        topographic_wetness_index=twi,
        lats=lats,
        lons=lons,
        bbox=json.dumps(BBOX)
    )
    
    # Save thermal npz
    thermal_path = "data/raw/thermal/landsat_modis_lst_ncr_1km.npz"
    np.savez_compressed(
        thermal_path,
        lst_celsius=lst_dry_season,
        uhi_anomaly_celsius=uhi_anomaly,
        cloud_mask_dry_season=cloud_mask_dry,
        cloud_mask_wet_season=cloud_mask_wet,
        lats=lats,
        lons=lons,
        bbox=json.dumps(BBOX)
    )
    
    print(f"Saved terrain rasters to {terrain_path}")
    print(f"Saved thermal rasters to {thermal_path}")

def main():
    print("--- Project Avatar: Raw Fixture Generator Starting ---")
    
    # 1. Epidemiological data
    df_surv, df_line = generate_epidemiological_data()
    surv_path = "data/raw/epidemiological/doh_leptospirosis_ncr_weekly_2023_2024.csv"
    line_path = "data/raw/epidemiological/doh_leptospirosis_surveillance_linelist_sample.csv"
    df_surv.to_csv(surv_path, index=False)
    df_line.to_csv(line_path, index=False)
    print(f"Saved weekly surveillance to {surv_path} ({len(df_surv)} rows)")
    print(f"Saved surveillance linelist sample to {line_path} ({len(df_line)} rows)")
    
    # 2. Atmospheric PM2.5 data
    df_pm = generate_atmospheric_data()
    pm_path = "data/raw/atmospheric/denr_emb_pm25_stations_2023_2024.csv"
    df_pm.to_csv(pm_path, index=False)
    print(f"Saved DENR-EMB PM2.5 to {pm_path} ({len(df_pm)} rows)")
    
    # 3. Hydrometeorological data
    df_pagasa, df_era5 = generate_hydrometeorological_data()
    pagasa_path = "data/raw/hydrometeorological/pagasa_synoptic_ncr_daily_2023_2024.csv"
    era5_path = "data/raw/hydrometeorological/era5_land_ncr_weekly_2023_2024.csv"
    era5_parquet = "data/raw/hydrometeorological/era5_land_ncr_weekly_2023_2024.parquet"
    df_pagasa.to_csv(pagasa_path, index=False)
    df_era5.to_csv(era5_path, index=False)
    df_era5.to_parquet(era5_parquet, index=False)
    print(f"Saved PAGASA synoptic to {pagasa_path} ({len(df_pagasa)} rows)")
    print(f"Saved ERA5-Land to {era5_path} & {era5_parquet} ({len(df_era5)} rows)")
    
    # 4. Spatial rasters (Terrain & Thermal)
    generate_spatial_rasters()
    
    print("--- Project Avatar: Raw Fixture Generator Completed Successfully ---")

if __name__ == "__main__":
    main()
