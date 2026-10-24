# Project Avatar: UI/UX Design System & Specification
**High-Resolution Multi-Hazard Epidemiological Intelligence Platform**  
*Philippine Junior Data Science Challenge (PJDSC) 2026*

---

## 1. Executive Design Vision & Paradigm

The user interface of **Project Avatar** translates complex, multi-hazard epidemiological and spatial data into an authoritative, calm, and high-impact executive command center. Inspired by state-of-the-art health intelligence aesthetics (such as *Metric.IQ*), the design balances **urgent frontline epidemiological triage** with **clinical elegance and statutory rigor**.

### Core Visual Philosophy
- **Modular Bento-Grid Architecture**: Information is segmented into high-contrast, rounded containers with distinct visual hierarchies. Each card acts as an autonomous intelligence node (predictive surge horizon, focal hotspot, air quality raster, operational directives, and biomedical vulnerability).
- **Dual-Tone Atmospheric Depth**: High-contrast juxtaposition of deep carbon charcoal (`#15171A` / `#1E2227`) and pristine alabaster cards (`#FFFFFF`) against a soft ceramic canvas (`#F4F5F7`).
- **Signature Solar Amber Accent (`#FF5B14` / `#FF7A00`)**: A vivid, warm amber-orange pulse used exclusively for high-urgency epidemiological signals, active focal hotspots, critical threshold exceedances, and actionable primary buttons.
- **Micro-Data Density**: Dot-matrix frequency arrays, hairline sparklines, glowing pill tags, and tabular display typography that present deep data without cognitive overload.

---

## 2. Design Tokens & Visual Hierarchy

### 2.1 Color Palette
```css
:root {
  /* Canvas & Foundations */
  --avatar-canvas-bg: #F4F5F7;
  --avatar-canvas-subtle: #ECEEF1;
  --avatar-text-primary-dark: #0F172A;
  --avatar-text-secondary-dark: #64748B;
  
  /* Dark Bento Modules (Timeline & Operational Stack) */
  --avatar-card-dark-bg: #15171A;
  --avatar-card-dark-surface: #1E2227;
  --avatar-card-dark-border: rgba(255, 255, 255, 0.08);
  --avatar-text-primary-light: #F8FAFC;
  --avatar-text-secondary-light: #94A3B8;

  /* Light Bento Modules (Metrics & Biomedical Tracking) */
  --avatar-card-light-bg: #FFFFFF;
  --avatar-card-light-surface: #F8F9FA;
  --avatar-card-light-border: rgba(0, 0, 0, 0.06);

  /* Signature Accents & Epidemiological Tiers */
  --avatar-solar-amber: #FF5B14;        /* Outbreak surge / Active hotspot / Primary CTA */
  --avatar-solar-amber-glow: rgba(255, 91, 20, 0.25);
  --avatar-amber-subtle: #FFF3EB;
  
  /* Multi-Hazard & Clinical Signals */
  --avatar-emerald-safe: #10B981;       /* Compliant / Normal / Low risk */
  --avatar-cyan-atmospheric: #06B6D4;   /* PM2.5 Downscaling / Rainfall */
  --avatar-purple-genomic: #8B5CF6;     /* Environmental priors / Soil saturation */
  --avatar-crimson-critical: #EF4444;   /* Critical outbreak surge */
}
```

### 2.2 Typography & Numerical Formatting
- **Display & Headings**: *Plus Jakarta Sans* / *Inter* / *SF Pro Display* (Weight: 600, 700, 800).
- **Tabular KPI Figures**: `font-variant-numeric: tabular-nums; letter-spacing: -0.03em; font-weight: 700;`.
- **Micro-Labels & Meta Chips**: `font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em;`.
- **Statutory / Monospace Badges**: `JetBrains Mono` or `Roboto Mono` for RA 10173 identifiers and advisory codes (`ADV-2024-W32-QC`).

### 2.3 Geometry, Borders & Elevation
- **Outer Bento Modules**: `border-radius: 24px;` with subtle outer stroke (`1px solid var(--border-color)`).
- **Sub-Cards & Inner Capsules**: `border-radius: 14px - 18px;`.
- **Status Chips & Pills**: `border-radius: 9999px;` (fully rounded capsule pill).
- **Elevation**: Diffuse, ambient drop shadows (`box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.04), 0 20px 30px -15px rgba(15, 23, 42, 0.06);`).

---

## 3. High-Fidelity Bento Grid Layout Architecture

```
+--------------------------------------------------------------------------------------------------------------------+
|  [Logo: Avatar.IQ]  (QC - NCR) (W32 - 2024) (RA 10173: k>=5)       [ Q Search LGU, hazard, or DOH protocol... ]  (Bell) (Menu) |
+--------------------------------------------------------------------------------------------------------------------+
|                                                          |                                                         |
|  CARD 1: MULTI-HAZARD SURGE HORIZON (Dark Charcoal - 60%) |  CARD 2: ACTIVE OUTBREAK EPICENTER (Solar Orange - 40%) |
|  - Title: [O] Epidemiological Surge Horizon & Rainfall Lags|  - Title: District 2 Hotspot Focal Node                 |
|  - Metrics: +34% Surge Risk [Pill] | ISO Epi-Week 32      |  - Hero: Topographic Satellite / Spatial Extent         |
|  - Visualization: Tweedie Surge Curve + 1-8w Lags Matrix   |  - Floating Glass Pills:                                |
|    * Upper: Anticipatory 14-21 day pre-hospital curve     |    * [Doxycycline Stockpile: 94%]                       |
|    * Lower: Daily PAGASA rainfall mm dot-matrix bars      |    * [Sluggish Slope Ponding: 0.8%]                     |
|                                                          |    * [NKTI AKI Risk: Tier IV]                           |
|                                                          |    * [Population Exposed: 142,000]                      |
+----------------------------------------------------------+---------------------------------------------------------+
|                               |                          |                                                         |
|  CARD 3: ATMOSPHERIC EXPOSURE |  CARD 4: LGU DIRECTIVES  |  CARD 5: BIOMEDICAL VULNERABILITY                       |
|  (Pristine Alabaster - 33%)   |  (Dark Charcoal - 33%)   |  (Pristine Alabaster - 34%)                             |
|  - Title: [O] PM2.5 Downscaling|  - Title: [O] Operational|  - Title: [O] Biomedical Surveillance & Compliance      |
|  - KPI: 48.6 ug/m3 (Peak Cell)|    Directives & Prophy    |  - Graphic: 3D Anatomical Human Profile                 |
|    Tag: 3.2x WHO 24h Threshold|  - Stacked Action Rows:  |    * Pulmonary target ring (PM2.5 fine dust)            |
|  - Dot-Matrix Hazard Spectrum |    * DOH PEP Rollout     |    * Hepatorenal target ring (Leptospira AKI)           |
|    (Good, Mod, Unhealthy, Crit)|    * NKTI AKI Screening  |  - Metric: 139 / 160h Critical Wading Exposure Index   |
|  - Dual Sub-Kpis:             |    * LDRRMO Culvert Drain|  - Verification Checklist Pills:                        |
|    * 28.4 ug/m3 Regional Mean |    * DENR Emission Curbs |    * [Check] RA 10173: 1-4 Cases Suppressed (<5)        |
|    * 82% Non-compliant Cells  |  - Bottom Pulse Capsule: |    * [Check] DOH Memo 2024-0288 PEP Protocol Active     |
|                               |    * Risk Score: 84.2%   |    * [Button: Orange] Export Action Card JSON Contract  |
|                               |    * SHAP: +41% Rain Lag |                                                         |
+-------------------------------+--------------------------+---------------------------------------------------------+
```

---

## 4. Module-by-Module Component Specifications

### 4.1 Global Command Header Bar
- **Brand Pill**: Modern glyph representing the 3 interconnected risk factors (Rainfall, Leptospirosis, Air Quality) with bold mark `Avatar.IQ`.
- **Context Capsules**:
  - `Location`: `📍 Quezon City · NCR`
  - `Surveillance Horizon`: `📅 Epi-Week 32 · 2024`
  - `Statutory Compliance`: `🔒 RA 10173 Active (k ≥ 5)`
- **Search & Command Bar**: Pill-shaped capsule input with subtle inner glow:
  - *Placeholder*: `"Search 17 LGUs, PM2.5 hotspots, or DOH AO 2010-0018 clinical guidance..."`
  - *Shortcuts*: Interactive instant filter tags for quick triage (`#Leptospirosis`, `#PM25`, `#DoxycyclinePEP`).
- **Utility Actions**:
  - Outbreak Notification Bell (with pulsating orange alert badge).
  - Operational Persona Switcher (`Municipal Health Officer (MHO)` | `LDRRMO` | `BHW`).

---

### 4.2 Bento Card 1: Multi-Hazard Epidemiological Surge Horizon (Dark Carbon)
*Direct translation of the top-left dark timeline chart from the reference design.*

- **Header**:
  - `Indicator`: Orange rounded square `🟠 Health Surge Horizon`.
  - `Pills`: `+34% Surge Risk` (Solar orange pill), `Epi-Week 32` (Dark slate pill).
- **Dual-Layer Chart Visualization**:
  - **Upper Wave Curve (Surge Forecast)**:
    - Renders the Tweedie GLM regression forecast across a 10-week sliding horizon (`Week -6` to `Week +4`).
    - Highlights the **14–21 day anticipatory surveillance window** before hospital central registries reflect cases.
    - Shaded orange area under the curve (`rgba(255, 91, 20, 0.18)`) indicates the surge threshold breach.
  - **Lower Dot-Matrix Micro-Bars (Environmental Antecedent Matrix)**:
    - Replaces generic time bars with multi-colored daily environmental metrics:
      - *Cyan bars*: Daily PAGASA rainfall volume (mm).
      - *Solar orange bars*: Soil moisture saturation index exceeding 80%.
      - *Vivid purple bars*: Sluggish flood ponding hours (slope gradient <0.8%).
- **Axis Details**:
  - Y-Axis: Weekly incidence / Outbreak surge probability (`0.0`, `0.5`, `1.0`).
  - X-Axis: `Lag 4w`, `Lag 3w`, `Lag 2w (Incubation Peak)`, `Lag 1w`, `Week 0 (Surveillance Horizon)`.

---

### 4.3 Bento Card 2: Active Outbreak Epicenter & Focal Node (Vibrant Solar Orange)
*Direct translation of the top-right warm editorial photographic card with floating node pills.*

- **Visual Canvas**:
  - Deep warm sunset radial gradient (`#FF5B14` to `#C23E00`) paired with a high-contrast topographic/satellite radar overlay of the active focal LGU (e.g. Quezon City / District 2 or Marikina Basin).
- **Pagination Header**:
  - `Title`: `District 2 Focus`
  - `Horizon Strip`: `W27 · W28 · W29 · W30 · W31 · [W32] · W33`
- **Floating Glassmorphic Node Branch Pills**:
  Branching visual connectors linking directly to four operational parameters:
  1. `[💊 Doxycycline PEP Stockpile: 94% Available]` (Frosted glass with glowing amber ring).
  2. `[🌊 Lowland Ponding (Slope <0.8%): 14.2 km²]` (Frosted glass pill).
  3. `[🩺 NKTI AKI Risk: Tier IV Emergency]` (Frosted glass pill).
  4. `[👥 Population Exposed: 142,000 Residents]` (Frosted glass pill).

---

### 4.4 Bento Card 3: Atmospheric Exposure & 1km PM2.5 Downscaling (Pristine Alabaster)
*Direct translation of the bottom-left white metric card with massive counters and dot-matrix clusters.*

- **Header**: `🟠 Atmospheric Exposure & Downscaled PM2.5` with `...` action menu.
- **Primary Hero Metric**:
  - Number: `48.6` <span style="font-size: 20px; color: #64748B;">µg/m³</span>
  - Label: `PEAK 1.0 KM GROUND CELL EXPOSURE`
  - Alert Badge: `3.2x WHO 24h Threshold` (Solar orange pill).
- **Dot-Matrix Hazard Spectrum**:
  - 4 vertical dot-matrix towers illustrating the distribution of the 1,350 uniform 1km downscaled grid cells across standard WHO/DENR AQI tiers:
    - *Emerald Tower*: Compliant (<15.0 µg/m³).
    - *Amber Tower*: Moderate (15.1–35.4 µg/m³).
    - *Orange Tower*: Unhealthy for Sensitive Groups (35.5–55.4 µg/m³).
    - *Crimson Tower*: Critical Outbreak (>55.5 µg/m³).
- **Grounding Citation Subtext**:
  > *"Spatial XGBoost downscaling (1,350 cells) synthesized from DENR-EMB ground stations, Sentinel-5P AOD, and ERA5 atmospheric reanalysis."*
- **Split Sub-Metrics**:
  - **Left Tile**: `28.4 µg/m³` (Regional Mean) accompanied by 3 circular sensor source badges (DENR, ESA, ECMWF).
  - **Right Tile**: `82%` Non-Compliant Cells (`+14% 1w surge`), with a circular `+` button triggering the interactive 3D PyDeck map modal.

---

### 4.5 Bento Card 4: LGU Operational Directives & Prophylaxis Tracking (Dark Carbon)
*Direct translation of the bottom-middle dark stacked card with micro-sparklines and bottom pulse capsule.*

- **Header**: `🟠 LGU Operational Action Directives` with sandglass / siren pill icon.
- **Stacked Modular Capsule Rows**:
  Four dark container rows with fine borders (`1px solid rgba(255,255,255,0.06)`):

  1. **Doxycycline Post-Exposure Prophylaxis (DOH AO 2010-0018)**
     - *Left*: Title `Doxycycline PEP` & Status `88% Dispensed to Health Centers`
     - *Center*: Orange dot cluster + Green trajectory sparkline
     - *Right*: Target execution `Sun, W32` + Medicine icon 💊

  2. **NKTI Early AKI Serum Creatinine Screening**
     - *Left*: Title `NKTI AKI Triage` & Status `Stage 1/2 Wading Cohort Screen`
     - *Center*: Orange dot cluster + Green trajectory sparkline
     - *Right*: Target execution `Mon, W32` + Renal Activity icon 🩺

  3. **LDRRMO Drainage Culvert Clearing**
     - *Left*: Title `Culvert Desilting` & Status `Low-Slope Zone (<0.8%) Clearing`
     - *Center*: Orange dot cluster + Amber trajectory sparkline
     - *Right*: Target execution `Tue, W32` + Hazard/Excavator icon ⚠️

  4. **DENR PM2.5 Traffic & Dust Suppression**
     - *Left*: Title `Aerosol Masking` & Status `BHW Particulate Protection Rollout`
     - *Center*: Orange dot cluster + Crimson trajectory sparkline
     - *Right*: Target execution `Wed, W32` + Shield icon 🛡️

- **Embedded Bottom Pulse Widget**:
  - Left Section: `Surge Outbreak Probability` | `84.2% Risk Score` with cyan dot cluster.
  - Right Section: **Dynamic TreeSHAP Signal Capsule** (Glowing heart/shield badge):
    - Highlights the dominant predictive driver: `+41% Lag 2w Rain`.

---

### 4.6 Bento Card 5: Biomedical Vulnerability & Statutory Integrity (Pristine Alabaster)
*Direct translation of the bottom-right anatomical card with silhouette and checklist pills.*

- **Header**: `🟠 Biomedical Vulnerability & Statutory Integrity` with `...` action menu.
- **3D Anatomical Human Profile Visualization**:
  - High-precision anatomical human torso rendering mapping multi-hazard biological targets:
    - **Pulmonary Target Ring (Chest/Lungs)**: Glowing cyan target depicting PM2.5 alveolar deposition, microvascular inflammation, and respiratory aggravation.
    - **Hepatorenal Target Ring (Abdomen/Kidneys)**: Glowing orange target depicting *Leptospira interrogans* endothelial invasion, tubulointerstitial nephritis, and acute kidney injury (Weil's syndrome).
- **Core Exposure Metric**:
  - `139 / 160h` <span style="font-size: 13px; color: #64748B;">Cumulative Risk Exposure Hours</span>
  - Accompanied by dot-matrix vital indicators.
- **Statutory Verification Checklist Pills**:
  Elongated rounded capsule pills verifying strict legal and regulatory compliance:
  1. `[Check] RA 10173 Active: 1-4 Cases Suppressed (<5) | 🔒` (Enforces k-anonymity privacy).
  2. `[Check] DOH Memo 2024-0288 Pre-emptive PEP Active | 🩺` (Grounds clinical chemoprophylaxis).
  3. `[Checking] 1-Click LGU EMIS Action Card JSON Contract | 📥` (Bright solar orange interactive export button).

---

## 5. Streamlit Implementation Architecture & Custom CSS

To achieve this exact visual fidelity within Streamlit, inject the following modular CSS styles and structural container patterns:

### 5.1 Custom CSS Injection Snippet (`app/theme.py`)
```python
import streamlit as st

def inject_avatar_theme():
    st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    /* Global Root Resets */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #F4F5F7 !important;
        color: #0F172A;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1440px !important;
    }

    /* Bento Card Foundations */
    .bento-card-dark {
        background-color: #15171A;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 24px;
        color: #F8FAFC;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.2);
    }

    .bento-card-light {
        background-color: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.06);
        border-radius: 24px;
        padding: 24px;
        color: #0F172A;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.04);
    }

    .bento-card-hero-orange {
        background: linear-gradient(135deg, #FF5B14 0%, #D44200 100%);
        border-radius: 24px;
        padding: 24px;
        color: #FFFFFF;
        box-shadow: 0 12px 35px -5px rgba(255, 91, 20, 0.35);
        position: relative;
        overflow: hidden;
    }

    /* Capsule Status Pills */
    .pill-badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .pill-orange {
        background-color: rgba(255, 91, 20, 0.15);
        color: #FF5B14;
        border: 1px solid rgba(255, 91, 20, 0.3);
    }

    .pill-dark {
        background-color: rgba(255, 255, 255, 0.1);
        color: #F8FAFC;
    }

    .pill-green {
        background-color: rgba(16, 185, 129, 0.12);
        color: #10B981;
    }

    /* Tabular Big Numerical Displays */
    .display-metric {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.0;
        font-variant-numeric: tabular-nums;
    }

    /* Stacked Action Row Item */
    .action-row-item {
        background-color: #1E2227;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 12px 16px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    </style>
    """, unsafe_allow_html=True)
```

---

## 6. PJDSC 2026 Evaluation Alignment

| Evaluation Criteria | Weight | UI/UX Design System Contribution |
| :--- | :---: | :--- |
| **Project Rationale & Design** | **20%** | Clear, instant communication of multi-hazard compounding risk (flood ponds + PM2.5); eliminates confusing medical jargon via role-tailored views. |
| **Execution & Frontline Utility** | **25%** | Replaces static analytical tables with **actionable operational directives**, DOH prophylaxis tracking, and 1-click LGU EMIS JSON exports. |
| **Statistical & Algorithmic Rigor** | **25%** | Dynamic TreeSHAP attribution watermarks reveal *why* an LGU is at risk; WHO exceedance metrics and Tweedie outbreak probabilities are displayed cleanly. |
| **Code Reproducibility & Architecture** | **20%** | Modular, container-ready component design; strict separation between computational engines (`src/`) and visual presentation (`app/`). |
| **Presentation & Video Utility** | **10%** | High visual appeal for the strict 3-minute video pitch; intuitive scanning allows judges to immediately grasp the platform's novelty in under 10 seconds. |

---

## 7. Implementation Checklist & Phased Roadmap

- [x] **Phase 1: Design Specification Finalization** (`docs/UI_DESIGN_SPEC.md`).
- [ ] **Phase 2: Custom Component Styling & Theme Injection** (`app/theme.py`).
- [ ] **Phase 3: Hero Row Bento Layout** (Epidemiological Surge Horizon + District 2 Hotspot Focal Node).
- [ ] **Phase 4: Bottom Row Bento Layout** (PM2.5 Downscaling + Operational Directives Stack + Anatomical Vulnerability).
- [ ] **Phase 5: PyDeck 3D Map Modal Integration** (1.0 km x 1.0 km downscaled raster + 17-LGU risk columns).
- [ ] **Phase 6: End-to-End Verification & 3-Minute Demo Video Recording Alignment**.
