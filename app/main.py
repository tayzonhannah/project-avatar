"""
Project Avatar: Metro Manila Multi-Hazard Epidemiological Intelligence Platform.
Interactive Streamlit Dashboard.

Features:
1. Interactive PyDeck / Folium Risk Choropleth across 17 Metro Manila LGUs.
2. 1.0 km x 1.0 km Spatial PM2.5 Downscaling Raster Overlay (1,350 cells).
3. Dynamic TreeSHAP Feature Attribution Watermarks.
4. Deterministic RAG-Generated LGU Emergency Action Cards (DOH / WHO / NKTI / RA 10173).
"""

from __future__ import annotations

from typing import Dict, List, Tuple
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

from src.utils.seed import GLOBAL_SEED, set_seed
from src.data.feature_engineering import build_ncr_feature_store
from src.models.leptospirosis_model import LeptospirosisRiskEngine
from src.models.pm25_downscaler import SpatialPM25Downscaler
from src.rag.advisory_engine import ChromaAdvisoryEngine
from src.api_contracts import (
    RiskTier,
    StakeholderRole,
    LanguageCode,
    RAGAdvisoryRequest,
    LeptospirosisLguPrediction,
    PM25GridPrediction,
)

set_seed(GLOBAL_SEED)

# Page Configuration
st.set_page_config(
    page_title="Project Avatar | NCR Public Health Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Geographic Coordinates & Bounding Box for Metro Manila LGUs
NCR_LGU_CENTROIDS: Dict[str, Tuple[float, float]] = {
    "City of Manila": (14.5995, 120.9842),
    "Quezon City": (14.6760, 121.0437),
    "City of Caloocan": (14.6571, 120.9841),
    "City of Las Piñas": (14.4445, 120.9939),
    "City of Makati": (14.5547, 121.0244),
    "City of Malabon": (14.6625, 120.9569),
    "City of Mandaluyong": (14.5794, 121.0359),
    "City of Marikina": (14.6507, 121.1029),
    "City of Muntinlupa": (14.4081, 121.0415),
    "City of Navotas": (14.6667, 120.9417),
    "City of Parañaque": (14.4793, 121.0198),
    "City of Pasay": (14.5378, 120.9993),
    "City of Pasig": (14.5764, 121.0851),
    "City of San Juan": (14.6019, 121.0355),
    "City of Taguig": (14.5176, 121.0509),
    "City of Valenzuela": (14.7011, 120.9830),
    "Municipality of Pateros": (14.5454, 121.0687),
}

RISK_COLORS: Dict[RiskTier, List[int]] = {
    RiskTier.LOW: [46, 204, 113, 180],         # Green
    RiskTier.MODERATE: [241, 196, 15, 190],    # Yellow
    RiskTier.HIGH: [230, 126, 34, 210],        # Orange
    RiskTier.CRITICAL: [192, 57, 43, 230],     # Dark Red
}


# =====================================================================
# CACHED SERVICE INITIALIZATION
# =====================================================================

@st.cache_resource(show_spinner="Loading feature store and models...")
def initialize_system() -> Tuple[
    pd.DataFrame, pd.DataFrame, LeptospirosisRiskEngine, SpatialPM25Downscaler, ChromaAdvisoryEngine
]:
    """Pre-trains models and loads vector knowledge database into memory."""
    muni_df, grid_df = build_ncr_feature_store()

    # Train Leptospirosis Risk Engine
    lepto_engine = LeptospirosisRiskEngine()
    lepto_engine.train(muni_df)

    # Train Spatial PM2.5 Downscaler
    downscaler = SpatialPM25Downscaler()
    station_df = pd.read_csv("data/raw/atmospheric/denr_emb_pm25_stations_2023_2024.csv")
    downscaler.train_on_stations(station_df)

    # Ingest ChromaDB Knowledge Corpus
    rag_engine = ChromaAdvisoryEngine()

    return muni_df, grid_df, lepto_engine, downscaler, rag_engine


# Load cached singletons
muni_df, grid_df, lepto_engine, downscaler, rag_engine = initialize_system()


# =====================================================================
# SIDEBAR CONTROLS & SCENARIO SELECTION
# =====================================================================

st.sidebar.image("https://raw.githubusercontent.com/feathericons/feather/master/icons/activity.svg", width=48)
st.sidebar.title("Project Avatar")
st.sidebar.caption("PJDSC 2026 | National Capital Region Multi-Hazard System")
st.sidebar.divider()

# Surveillance Temporal Horizon
st.sidebar.subheader("📅 Temporal Horizon")
available_years = sorted(muni_df["year"].unique())
selected_year = st.sidebar.selectbox("Surveillance Year", options=available_years, index=len(available_years) - 1)

max_week = int(muni_df[muni_df["year"] == selected_year]["epi_week"].max())
selected_week = st.sidebar.slider("ISO Epidemiological Week", min_value=1, max_value=max_week, value=min(32, max_week))

# Decision Stakeholder Persona
st.sidebar.subheader("👤 Stakeholder Persona")
role_mapping = {
    "Municipal Health Officer (MHO)": StakeholderRole.MUNICIPAL_HEALTH_OFFICER,
    "Disaster Risk Reduction Officer (LDRRMO)": StakeholderRole.DISASTER_RISK_REDUCTION_OFFICER,
    "Barangay Health Worker (BHW)": StakeholderRole.BARANGAY_HEALTH_WORKER,
    "General Public": StakeholderRole.GENERAL_PUBLIC,
}
selected_role_label = st.sidebar.selectbox("Operational Persona", options=list(role_mapping.keys()))
target_role = role_mapping[selected_role_label]

# Language Selection
lang_mapping = {"English (EN)": LanguageCode.ENGLISH, "Tagalog (TL)": LanguageCode.TAGALOG}
selected_lang_label = st.sidebar.selectbox("Advisory Language", options=list(lang_mapping.keys()))
target_lang = lang_mapping[selected_lang_label]

# Map Visualization Layers
st.sidebar.subheader("🗺️ Layer Toggles")
show_pm25_raster = st.sidebar.checkbox("Overlay 1km PM2.5 Downscaling Surface", value=True)
show_lgu_centroids = st.sidebar.checkbox("Show LGU Risk Nodes", value=True)

st.sidebar.divider()
st.sidebar.info(
    "⚖️ **Statutory Compliance: RA 10173**\n"
    "Reporting cells containing 1 to 4 cases are suppressed (`<5`) to eliminate re-identification risk."
)


# =====================================================================
# MODEL INFERENCE FOR SELECTED EPIDEMIOLOGICAL HORIZON
# =====================================================================

# Filter week data
week_data = muni_df[(muni_df["year"] == selected_year) & (muni_df["epi_week"] == selected_week)]
if week_data.empty:
    week_data = muni_df.groupby("lgu_name").last().reset_index()

# Generate 17-LGU predictions
lgu_predictions: List[LeptospirosisLguPrediction] = []
for _, row in week_data.iterrows():
    pred = lepto_engine.predict_lgu(
        lgu_feature_row=row.to_dict(),
        lgu_id="PH130000000",
        epi_week=selected_week,
        year=selected_year,
    )
    lgu_predictions.append(pred)

# Downscale PM2.5 Grid
grid_predictions: List[PM25GridPrediction] = downscaler.downscale_grid(grid_df)

# Regional Aggregate Metrics
total_surge_lgus = sum(1 for p in lgu_predictions if p.risk_tier in [RiskTier.HIGH, RiskTier.CRITICAL])
regional_alert = "CRITICAL" if total_surge_lgus >= 5 else ("ELEVATED" if total_surge_lgus >= 2 else "NORMAL")
mean_pm25 = float(np.mean([p.predicted_pm25_ug_m3 for p in grid_predictions]))
peak_pm25 = float(np.max([p.predicted_pm25_ug_m3 for p in grid_predictions]))
who_exceedance_pct = float(np.mean([p.who_24h_exceedance_factor > 1.0 for p in grid_predictions]) * 100.0)


# =====================================================================
# MAIN DASHBOARD HEADER & KPI METRICS
# =====================================================================

st.title("Project Avatar: High-Resolution Multi-Hazard Health Intelligence")
st.markdown(
    f"**National Capital Region (NCR) | Epidemiological Week {selected_week}, {selected_year}** &nbsp;•&nbsp; "
    f"*Anticipatory surveillance 14-21 days ahead of central registries.*"
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(
    label="Surge Outbreak Alert Tier",
    value=regional_alert,
    delta=f"{total_surge_lgus} of 17 LGUs at Risk",
    delta_color="inverse" if total_surge_lgus > 0 else "normal",
)
kpi2.metric(
    label="Regional Mean PM2.5",
    value=f"{mean_pm25:.1f} µg/m³",
    delta=f"{mean_pm25 / 15.0:.1f}x WHO 24h Threshold",
    delta_color="inverse",
)
kpi3.metric(
    label="Peak 1km Cell PM2.5",
    value=f"{peak_pm25:.1f} µg/m³",
    delta=f"{who_exceedance_pct:.1f}% Grid Cells Non-Compliant",
    delta_color="inverse",
)
kpi4.metric(
    label="Statutory Privacy Status",
    value="k ≥ 5 Active",
    delta="RA 10173 Enforced",
    delta_color="off",
)

st.divider()


# =====================================================================
# SECTION 1: INTERACTIVE PYDECK CHOROPLETH & 1KM PM2.5 RASTER
# =====================================================================

st.subheader("🗺️ Spatial Multi-Hazard Risk Surface")
st.caption(
    "Visualizing 17 NCR Municipal Health Risk Tiers alongside the "
    "continuous 1.0 km x 1.0 km Spatial XGBoost PM2.5 downscaling surface."
)

col_map, col_details = st.columns([1.6, 1.0])

with col_map:
    # Prepare PyDeck Point & Hexagon/Scatterplot data
    map_rows = []
    for pred in lgu_predictions:
        lgu_key = pred.lgu_name.value
        coords = NCR_LGU_CENTROIDS.get(lgu_key, (14.5995, 120.9842))
        color = RISK_COLORS.get(pred.risk_tier, [128, 128, 128, 180])

        map_rows.append({
            "lgu_name": lgu_key,
            "lat": coords[0],
            "lon": coords[1],
            "risk_tier": pred.risk_tier.value,
            "surge_prob": f"{pred.outbreak_surge_probability:.1%}",
            "cases_display": pred.suppressed_case_display,
            "color": color,
            "radius": 1800 + (pred.outbreak_surge_probability * 1500),
            "elevation": pred.outbreak_surge_probability * 4000,
        })
    map_df = pd.DataFrame(map_rows)

    # Prepare PM2.5 Grid 1km Raster data
    grid_rows = []
    for gp in grid_predictions:
        # Color mapping for PM2.5
        val = gp.predicted_pm25_ug_m3
        if val <= 12.0:
            c = [46, 204, 113, 110]
        elif val <= 35.4:
            c = [241, 196, 15, 120]
        elif val <= 55.4:
            c = [230, 126, 34, 140]
        else:
            c = [192, 57, 43, 160]

        grid_rows.append({
            "cell_id": gp.cell_id,
            "lat": gp.latitude,
            "lon": gp.longitude,
            "pm25": val,
            "aqi": gp.aqi_category.value,
            "color": c,
        })
    raster_df = pd.DataFrame(grid_rows)

    # Define PyDeck layers
    layers = []
    if show_pm25_raster:
        raster_layer = pdk.Layer(
            "ScatterplotLayer",
            data=raster_df,
            get_position=["lon", "lat"],
            get_fill_color="color",
            get_radius=550,
            pickable=True,
            auto_highlight=True,
        )
        layers.append(raster_layer)

    if show_lgu_centroids:
        lgu_layer = pdk.Layer(
            "ColumnLayer",
            data=map_df,
            get_position=["lon", "lat"],
            get_elevation="elevation",
            get_fill_color="color",
            radius=1200,
            elevation_scale=1,
            pickable=True,
            auto_highlight=True,
        )
        layers.append(lgu_layer)

    view_state = pdk.ViewState(
        latitude=14.585,
        longitude=121.015,
        zoom=10.2,
        pitch=38,
        bearing=15,
    )

    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/dark-v11",
        tooltip={
            "html": "<b>{lgu_name}</b><br/>"
                    "Risk Tier: <b>{risk_tier}</b><br/>"
                    "Surge Probability: <b>{surge_prob}</b><br/>"
                    "Expected Cases (RA 10173): <b>{cases_display}</b>",
            "style": {"backgroundColor": "#1e293b", "color": "white", "fontSize": "12px", "padding": "8px"},
        },
    )
    st.pydeck_chart(deck, use_container_width=True)

with col_details:
    st.markdown("#### 📋 Municipal Risk Tiers")
    display_table = pd.DataFrame([
        {
            "LGU": p.lgu_name.value.replace("City of ", "").replace("Municipality of ", ""),
            "Tier": p.risk_tier.value,
            "Surge Prob": f"{p.outbreak_surge_probability:.1%}",
            "Cases": p.suppressed_case_display,
        }
        for p in sorted(lgu_predictions, key=lambda x: x.outbreak_surge_probability, reverse=True)
    ])
    st.dataframe(display_table, height=390, use_container_width=True)


# =====================================================================
# SECTION 2: LGU DEEP DIVE & DYNAMIC SHAP WATERMARKS
# =====================================================================

st.divider()
st.subheader("🔍 LGU Deep Dive & TreeSHAP Attribution Waterfall")
st.caption("Explainable AI reveals exact percentage contributions of antecedent rainfall lags and environmental priors.")

lgu_options = [p.lgu_name.value for p in lgu_predictions]
selected_lgu_name = st.selectbox("Select Target LGU for Deep Diagnostic", options=lgu_options, index=0)

selected_pred = next(p for p in lgu_predictions if p.lgu_name.value == selected_lgu_name)

c_diag1, c_diag2 = st.columns([1.0, 1.4])

with c_diag1:
    st.markdown(f"### {selected_pred.lgu_name.value}")
    st.markdown(f"**Assigned Tier:** `{selected_pred.risk_tier.value}`")
    st.markdown(f"**Surge Probability:** `{selected_pred.outbreak_surge_probability:.2%}`")
    st.markdown(f"**Expected Weekly Cases:** `{selected_pred.suppressed_case_display}`")

    if selected_pred.is_suppressed:
        st.warning(
            "🔒 **Small Cell Suppressed (1-4 cases)**\n\n"
            f"{selected_pred.statutory_privacy_notice}"
        )
    else:
        st.success("✅ **Unsuppressed Cell**: Case count exceeds privacy threshold (k ≥ 5).")

with c_diag2:
    st.markdown("#### 📊 Dynamic Feature Contribution Watermarks (TreeSHAP)")
    shap_data = selected_pred.top_shap_drivers
    shap_df = pd.DataFrame(list(shap_data.items()), columns=["Driver Feature", "Normalized Contribution"])
    shap_df = shap_df.sort_values(by="Normalized Contribution", ascending=True)

    # Display Streamlit native bar chart
    st.bar_chart(shap_df.set_index("Driver Feature"), horizontal=True, height=220)
    st.caption("Empirical Lag 2w (primary mucosal incubation peak) and Soil Moisture 2w dominate early surge signals.")


# =====================================================================
# SECTION 3: DETERMINISTIC RAG-GENERATED EMERGENCY ACTION CARDS
# =====================================================================

st.divider()
st.subheader("🚨 Deterministic RAG Emergency Action Advisory Card")
st.caption(
    "Grounding retrieved directives from DOH AO 2010-0018, DOH Memo 2024-0288, WHO 2021 AQG, and NKTI AKI Staging."
)

# Synthesize RAG response
rag_req = RAGAdvisoryRequest(
    lgu_id="PH130000000",
    lgu_name=selected_pred.lgu_name,
    risk_tier=selected_pred.risk_tier,
    outbreak_surge_probability=selected_pred.outbreak_surge_probability,
    suppressed_case_display=selected_pred.suppressed_case_display,
    dominant_shap_drivers=selected_pred.top_shap_drivers,
    target_role=target_role,
    language=target_lang,
)

advisory_resp = rag_engine.generate_advisory(rag_req)

# Executive Alert Banner
alert_box_type = st.error if selected_pred.risk_tier in [RiskTier.HIGH, RiskTier.CRITICAL] else st.info
alert_box_type(
    f"**ADVISORY TRACKING ID: `{advisory_resp.advisory_id}`**\n\n"
    f"{advisory_resp.executive_summary}"
)

# Directives Tabbed View
tab_dir, tab_rx, tab_cits = st.tabs([
    "📋 Prioritized Operational Directives",
    "💊 Clinical Prophylaxis Guidance",
    "📚 Regulatory Citations & Grounding",
])

with tab_dir:
    for d in advisory_resp.prioritized_directives:
        with st.container(border=True):
            st.markdown(f"#### ⚡ [{d.priority.value}] {d.action_title}")
            st.markdown(f"**Instructions:** {d.action_description}")
            st.markdown(f"**Execution Lead:** `{d.target_stakeholder}`")
            st.markdown(f"**Resource Allocation:** `{d.resource_requirement}`")

with tab_rx:
    if advisory_resp.clinical_guidance:
        cg = advisory_resp.clinical_guidance
        with st.container(border=True):
            st.markdown(f"#### 🩺 {cg.regimen_name}")
            st.markdown(f"**Standard Drug & Dosage:** {cg.drug_and_dosage}")
            st.markdown(f"**Administration Window:** `{cg.timing_window}`")
            st.markdown(f"**Contraindications:** ⚠️ *{cg.contraindications}*")
            st.markdown(f"**Approved Safe Alternative:** {cg.alternative_drug}")

with tab_cits:
    for c in advisory_resp.retrieved_citations:
        with st.container(border=True):
            st.markdown(f"**[{c.citation_id}] {c.document_title}** ({c.issuing_authority})")
            st.caption(f"Reference: `{c.statutory_or_cpg_reference}`")
            st.markdown(f"> *\"{c.exact_excerpt}\"*")
            if c.url_or_doi:
                st.markdown(f"[🔗 Official Source Link]({c.url_or_doi})")

# Export Action Card JSON
st.divider()
col_exp1, col_exp2 = st.columns([1.0, 3.0])
with col_exp1:
    advisory_json = advisory_resp.model_dump_json(indent=2)
    st.download_button(
        label="📥 Export Action Card (JSON Contract)",
        data=advisory_json,
        file_name=f"action_card_{selected_pred.lgu_name.value}_{selected_week}.json",
        mime="application/json",
    )
with col_exp2:
    st.caption("Statutory payload compatible with LGU Emergency Management Information Systems (EMIS) via Pydantic v2 schemas.")
