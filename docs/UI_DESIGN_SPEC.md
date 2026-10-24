# Avatar.IQ: UI/UX Design System & Technical Specification
**Metric.IQ-Inspired Mixed-Contrast Bento Grid Architecture for Megacity Multi-Hazard Health Intelligence**  
*Philippine Junior Data Science Challenge (PJDSC) 2026*  
*Document Identifier:* [`docs/UI_DESIGN_SPEC.md`](file:///c:/Users/Hannah/Desktop/Hannah's%20lab/PJDSC/docs/UI_DESIGN_SPEC.md)

---

## 1. Executive Design Vision & Paradigm

The user interface of **Avatar.IQ** translates complex, multi-hazard epidemiological and spatial telemetry into an authoritative, high-impact executive decision support command center. Inspired by state-of-the-art health intelligence dashboards (specifically the *Metric.IQ* aesthetic), the architecture balances **urgent frontline epidemiological triage** with **clinical elegance and statutory rigor (RA 10173)**.

### Solving Prior Streamlit UX Bottlenecks
The previous prototype suffered from five major usability defects which this overhaul completely eliminates:
1. **Severe Column Truncation (`Regional Outbrea...`)**: Native `st.metric()` widgets suffered from rigid flex widths that cropped crucial public health titles. Replaced with custom HTML `.bento-light` and `.bento-dark` card containers with responsive typography and `JetBrains Mono` tabular metrics that never truncate.
2. **Squished 3-Column Text Wrapping**: Placing three frontline stakeholder cards (MHO, LDRRMO, BHW) side-by-side in skinny columns caused 1-word-per-line wrapping and poor legibility. Replaced with a unified **Tabbed Operational Directives Container** (`st.tabs`), giving each role 100% of the card's column width.
3. **Oversized PyDeck Scatterplot Circles**: The atmospheric overlay circles (radius 550m, high opacity) suffocated the underlying 3D LGU extrusion polygons. Calibrated to a refined `get_radius=350m`, clamped between `radius_min_pixels=2` and `radius_max_pixels=6`, with alpha opacity reduced to `110`, creating a clean atmospheric dot-matrix grid.
4. **Overlapping Plotly Titles & Legends**: Horizontal legends previously collided with chart titles and vertical disaster event markers (`Typhoon Carina (W30)`, `STS Kristine (W43)`). Chart titles are now removed from SVG canvases (delegated to Bento card headers) and legends are elevated (`y=1.12–1.15, orientation="h"`).
5. **Flat Dark-Mode Scroll Fatigue**: Replaced monolithic dark panels with a **Mixed-Contrast Bento Grid**: a Warm Alabaster canvas (`#F3F4F6`), a pristine white shell container (`#FFFFFF`), deep carbon charcoal Bento modules (`#16181D`), and an illuminated Solar Amber Spotlight (`#FF5B14`).

---

## 2. Design Tokens & Visual Hierarchy

### 2.1 Color Palette
```css
:root {
  /* Canvas & Foundations */
  --avatar-canvas-bg: #F3F4F6;          /* Warm Alabaster base canvas */
  --avatar-shell-bg: #FFFFFF;           /* Pristine White Dashboard Shell Container */
  --avatar-text-primary-dark: #0F172A;  /* Obsidian Slate */
  --avatar-text-secondary-dark: #64748B;/* Cool Slate */

  /* Dark Bento Modules (3D Spatial Map & 17-LGU Feed) */
  --avatar-bento-dark-start: #16181D;   /* Carbon Gradient Top */
  --avatar-bento-dark-end: #0F1115;     /* Carbon Gradient Base */
  --avatar-bento-dark-border: rgba(255, 255, 255, 0.06);
  --avatar-text-primary-light: #F9FAFB;
  --avatar-text-secondary-light: #94A3B8;

  /* Light Bento Modules (Diagnostics, SHAP & Operational Directives) */
  --avatar-bento-light-bg: #FFFFFF;
  --avatar-bento-light-border: #E5E7EB;
  --avatar-bento-light-surface: #F8FAFC;

  /* Signature Solar Amber (Urgent Hotspot & Card Accent) */
  --avatar-solar-amber: #FF5B14;        /* Primary Alert & Metric.IQ Accent */
  --avatar-solar-amber-dark: #C23B00;   /* Gradient Depth */
  --avatar-solar-amber-glow: rgba(255, 91, 20, 0.22);

  /* Epidemiological Tiers & Atmospheric Signals */
  --avatar-tier-critical: #EF4444;      /* Critical Outbreak Surge (>=5 LGUs) */
  --avatar-tier-high: #FF5B14;          /* High Outbreak Surge (>=2 LGUs) */
  --avatar-tier-moderate: #F59E0B;      /* Moderate Watch */
  --avatar-tier-low: #10B981;           /* Normal Baseline / Protective */
  --avatar-atmospheric-cyan: #0284C7;   /* Rainfall & PM2.5 Downscaler */
}
```

### 2.2 Typography & Formatting Rules
- **Display & Interface Headings**: `'Plus Jakarta Sans'`, sans-serif (Weights: 600, 700, 800).
- **Body & Secondary Copy**: `'Inter'`, -apple-system, sans-serif (Weights: 400, 500, 600).
- **Metrics, Lags, Dates & PSGC Codes**: `'JetBrains Mono'`, monospace (`font-variant-numeric: tabular-nums`).
- **Small-Cell Privacy Rule (RA 10173)**: All case counts between 1 and 4 are strictly masked as `<5` across all metric widgets, map tooltips, feeds, and cards.

### 2.3 Bento Container Geometry
- **Shell Container**: `max-width: 1440px !important; padding: 1.5rem 2rem !important; border-radius: 28px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04);`
- **Bento Modules (`.bento-dark`, `.bento-light`, `.bento-amber`)**: `border-radius: 22px; padding: 22px;`
- **Pill Badges (`.pill-orange`)**: `border-radius: 999px; padding: 3px 10px; font-size: 0.75rem; font-weight: 600;`
- **Metric.IQ Header Dots (`.orange-dot`)**: `width: 10px; height: 10px; background: #FF5B14; border-radius: 4px; display: inline-block; margin-right: 8px; vertical-align: middle;`

---

## 3. High-Fidelity Bento Grid Architecture

```text
+-----------------------------------------------------------------------------------------------------------------------------+
|  [🛡️ Avatar.IQ] (Surveillance Active)                    📅 Week 30, 2024 (July 22 – 28, 2024)      🔒 RA 10173 (k >= 5)    |
+-----------------------------------------------------------------------------------------------------------------------------+
|  [⚡ Disaster Preset: Typhoon Carina (W30)]  [📅 Week Slider: 30]  [📍 LGU Focus: City of Manila]  [🌫️ PM2.5 Grid: ON]     |
+-----------------------------------------------------------------------------------------------------------------------------+
|                                                                    |                                                        |
|  ROW 1, LEFT: REGIONAL 3D SPATIAL COMMAND (.bento-dark - 7 cols)    |  ROW 1, RIGHT: SPOTLIGHT + KPI GRID (5 cols)           |
|  - Header: [O] NCR Multi-Hazard Spatial Surveillance   [12/17 High]|  ┌───────────────────────────────────────────────────┐ |
|  - Sub: 3D Height = Outbreak Probability | Dots = 1km PM2.5        |  │ PRIORITY LGU SPOTLIGHT (.bento-amber)             │ |
|  - PyDeck 3D DeckGL Canvas (height=420):                           |  │ Manila | 88% Surge Risk | Expected Cases: 24       │ |
|    * Extruded 3D LGU Risk Pillars (radius=1200m)                   |  │ [Lepto: CRITICAL] [PM2.5: 2.8x WHO] [SUHI: +3.2C] │ |
|    * Calibrated 1km PM2.5 Surface (radius=350m, alpha=110)         |  └───────────────────────────────────────────────────┘ |
|    * Dark Matter Basemap with Clean Glassmorphic Tooltips          |  ┌───────────────────────────────────────────────────┐ |
|                                                                    |  │ 2x2 CRISP KPI BENTO GRID (.bento-light)           │ |
|                                                                    |  │ [Surge Status: CRIT] │ [Peak LGU Risk: 88%]        │ |
|                                                                    |  │ [Mean PM2.5: 42ug/m3]│ [SUHI Anomaly: +2.8C]       │ |
|                                                                    |  └───────────────────────────────────────────────────┘ |
+--------------------------------------------------------------------+--------------------------------------------------------+
|                                  |                                       |                                                  |
|  ROW 2, COL 1: TREESHAP (3.8)    |  ROW 2, COL 2: 17-LGU FEED (4.2)      |  ROW 2, COL 3: RAG DIRECTIVES (4.0)              |
|  (.bento-light card)             |  (.bento-dark card)                   |  (.bento-light card)                             |
|  - Header: [O] TreeSHAP Risk     |  - Header: [O] 17-LGU Stratification  |  - Header: [O] Operational Directives            |
|  - LGU Banner: Manila (88% Risk) |  - Sub: Ranked by Surge Probability   |  - Tabs (100% Card Width - Zero Squishing):      |
|    Expected Cases: 24 (RA 10173) |  - Scrollable Pill Rows (.bento-scroll):|    [🏥 MHO] [🛟 LDRRMO] [🏘️ BHW] [💊 Doxy PEP]    |
|  - Plotly Waterfall/Bar (h=260): |    #01 Manila      [=====] CRIT 88% 24|  - Directive Rows:                               |
|    * Transparent Background      |    #02 Quezon City [==== ] HIGH 72% 38|    * Priority Badge (🔴 Immediate / 🟠 Urgent)   |
|    * Elevated Legend (y=1.14)    |    #03 Malabon     [==== ] HIGH 68% <5|    * Action Title & Plain-Language Instructions  |
|    * Zero overlapping title      |    ... [All 17 LGUs with active glow] |    * Resource / Equipment Needed                |
+----------------------------------+---------------------------------------+--------------------------------------------------+
|                                                                                                                             |
|  ROW 3: ANALYST BACKTEST & STATUTORY CITATIONS (Full-Width Bento Container with Tabs)                                       |
|  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ |
|  │ [📈 Walk-Forward Epidemiological Backtest]              │ [⚖️ Statutory & Clinical Grounding (APA 7th)]                 │ |
|  ├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ |
|  │ - 4 Validation KPIs: [PR-AUC: 0.840] [Naive: 0.420] [Lift: +100.0%] [ROC-AUC: 0.880]                                   │ |
|  │ - Historical Horizon Selector: "All NCR LGUs (Regional Aggregate)" or individual LGU                                  │ |
|  │ - Plotly Backtest Chart: Observed Cases vs Tweedie Predicted vs Naive Baseline vs PAGASA Rainfall                     │ |
|  │   * Disaster Markers: Typhoon Carina (W30) & STS Kristine (W43) vertical lines with clear margins                     │ |
|  │ - Anticipatory Lead Time: 14-day environmental exposure signal vs 15.0-day median reporting delay                      │ |
|  └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ |
+-----------------------------------------------------------------------------------------------------------------------------+
```

---

## 4. Module-by-Module Technical Specifications

### 4.1 Top Command & Navigation Bar
- **Brand Lockup**: Shield glyph with solar amber gradient + bold `Avatar.IQ` wordmark (`.IQ` illuminated in `#FF5B14`).
- **Context Badges**:
  - `Surveillance Active` capsule pill (`.pill-orange`).
  - Active ISO Epidemiological Week & calendar date span (`Week 30, 2024 (July 22 – 28, 2024)`).
  - Statutory guardrail pill (`🔒 RA 10173 Active (k ≥ 5)`).
- **Interactive Control Bar (`st.columns([1.5, 1.0, 1.5, 1.5])`)**:
  1. `Disaster Event Preset`: `Normal Baseline`, `Typhoon Carina (W30)`, `STS Kristine (W43)`.
  2. `ISO Epi-Week Slider`: 1 to 52 (compact).
  3. `Municipality Focus`: All 17 Metro Manila LGUs (synced with TreeSHAP and RAG directives).
  4. `PM2.5 Surface Overlay Toggle`: Instant toggle for 1.0 km² downscaled grid.

---

### 4.2 Row 1: Executive Telemetry & 3D Spatial Command (7:5)

#### Left Column (7 cols): Regional Multi-Hazard Telemetry & 3D PyDeck Map
- **Container**: `.bento-dark` styled header with `.orange-dot`, title `"NCR Multi-Hazard Spatial Surveillance"`, and right-aligned `.pill-orange` showing `{n}/17 High Risk`.
- **PyDeck Spatial Canvas**:
  - `height=420` with full container width.
  - Basemap: CartoDB Dark Matter GL style (`https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json`).
  - ViewState: `latitude=14.585, longitude=121.015, zoom=10.2, pitch=38, bearing=15`.
  - **ScatterplotLayer (PM2.5 Raster Overlay)**:
    - Calibrated `get_radius=350` (meters).
    - Clamped to `radius_min_pixels=2` and `radius_max_pixels=6`.
    - Alpha opacity reduced to `110` (`[r, g, b, 110]`), ensuring the dot-matrix atmospheric grid floats cleanly above the terrain without obscuring municipal polygons.
  - **ColumnLayer (Leptospirosis 3D Extrusions)**:
    - `radius=1200`, `elevation_scale=1`.
    - Height mapped to `outbreak_surge_probability * 3500`.
    - Colors dynamically mapped to `RiskTier` (`#10B981`, `#F59E0B`, `#FF5B14`, `#EF4444`).
  - **Tooltip**: Glassmorphic dark card with LGU name, risk tier, outbreak surge probability, and suppressed expected cases.

#### Right Column (5 cols): Priority LGU Spotlight & 2x2 KPI Bento Grid
- **Top Sub-Card (`.bento-amber` gradient)**:
  - Header: `Priority LGU Spotlight` + `ACTIVE HOTSPOT` badge.
  - Highest-risk municipality name in massive typography (`font-size: 2.0rem; font-weight: 800`).
  - Large tabular metrics: Outbreak Surge Probability (`%`) and Expected Cases (enforcing `<5` mask if 1–4 under RA 10173).
  - Multi-hazard context pills:
    - `🌊 Lepto: {TIER}`
    - `💨 PM2.5: {X.Xx} WHO Limit`
    - `🌡️ SUHI: +{X.X}°C`
- **Bottom Sub-Card (`.bento-light` 2x2 internal CSS Grid)**:
  Four crisp KPI cells with zero truncation:
  1. `Regional Surge Status`: `CRITICAL SURGE` / `ELEVATED WATCH` / `NORMAL BASELINE` + `{n}/17 Cities at High Risk`.
  2. `Peak LGU Risk Score`: Probability `%` + municipality name.
  3. `Mean NCR PM2.5`: `XX.X µg/m³` + `X.Xx WHO 24h Safe Limit`.
  4. `SUHI Thermal Anomaly`: `+X.X °C` + Heat caution tier (`Extreme Caution (33–41°C)`).

---

### 4.3 Row 2: Three-Column Bento Diagnostics (3.8 : 4.2 : 4.0)

#### Column 1 (3.8 cols): Local TreeSHAP Risk Attribution & LGU Telemetry
- **Container**: `.bento-light` card with `.orange-dot`, title `"TreeSHAP Risk Attribution"`, and active risk tier badge.
- **LGU Telemetry Card**: Municipality name, PSGC code, surge probability (`%`), expected cases (`<5` mask), and `🔒 RA 10173 Protected` badge.
- **TreeSHAP Waterfall/Bar Chart**:
  - `px.bar` horizontal chart sorted by absolute SHAP contribution.
  - Friendly plain-English environmental labels (e.g., `🌊 Floodwaters (2 Weeks Ago)`, `🌧️ Recent Rain (Past 7 Days)`).
  - Colors: `#EF4444` (Risk Factor +) and `#10B981` (Protective -).
  - **Plotly Fixes**:
    - `height=260`
    - `paper_bgcolor="rgba(0,0,0,0)"`, `plot_bgcolor="rgba(0,0,0,0)"`
    - Margins: `dict(l=130, r=20, t=10, b=30)`
    - Elevated horizontal legend: `orientation="h", y=1.14, x=0`
    - Overlapping SVG title removed.

#### Column 2 (4.2 cols): 17-LGU Risk Stratification & Triage Feed
- **Container**: `.bento-dark` card inspired by the Metric.IQ center dark triage module.
- **Header**: `.orange-dot`, `"17-LGU Stratification Feed"`, and `All 17 LGUs` badge.
- **Scrollable Triage Rows (`.bento-scroll`)**:
  - Ranked from `#01` to `#17` by immediate outbreak surge probability.
  - Each row displays: `[Rank #] [City Name] [Mini Progress Bar] [Risk Badge: LOW/MOD/HIGH/CRIT] [Surge %] [Cases]`.
  - Active selection highlighting: The currently focused LGU receives an illuminated amber border (`rgba(255, 91, 20, 0.4)`) and subtle glow background.

#### Column 3 (4.0 cols): Role-Specialized RAG Action Cards
- **Container**: `.bento-light` card with `.orange-dot` and title `"Operational Directives"`.
- **Tabs Architecture (`st.tabs`)**:
  - Eliminates the previous 3-column horizontal squish by allocating 100% of the column width to each role.
  - Tab 1: `🏥 MHO (Clinical)` — Clinical triage, diagnostic stockpiling, leptospirosis bed capacity.
  - Tab 2: `🛟 LDRRMO (Ops)` — Drainage culvert clearing, mobile pump dispatch, water-rescue PPE.
  - Tab 3: `🏘️ BHW (Community)` — House-to-house fever syndromic surveillance, public health advisories.
  - Tab 4: `💊 DOH Doxy PEP` — DOH Administrative Order No. 2010-0018 post-exposure prophylaxis protocols:
    - Standard Dosage & Regimen
    - Timing Window (within 24–72 hours of exposure)
    - Safe Alternative Chemoprophylaxis
    - Absolute Contraindications (Pregnant, Lactating, Children <8 yrs) highlighted in high-visibility alert styling.

---

### 4.4 Row 3: Analyst Backtest & Statutory Citations (Full-Width Tabs)

- **Tab 1: 📈 Walk-Forward Epidemiological Backtest**:
  - 4 Model Validation KPI Cards:
    - Out-of-Sample PR-AUC (`0.840` vs. Naive Baseline `0.420`, `+100.0% Relative Lift`)
    - Naive Baseline PR-AUC
    - PR-AUC Relative Lift
    - Out-of-Sample ROC-AUC (`0.880`)
  - Timeline Horizon Selector (`All NCR LGUs (Regional Aggregate)` or any individual LGU).
  - Dual-Axis Plotly Chart (`height=400`):
    - Ground Truth Observed Cases (`#EF4444`, solid)
    - LightGBM Tweedie Predictions (`#10B981`, dashed)
    - Naive Lag-1 Persistence Baseline (`#94A3B8`, dotted)
    - Weekly Rainfall mm (`#0284C7`, secondary y-axis bars)
    - Disaster Surge Annotations: `Typhoon Carina (W30)` and `STS Kristine (W43)` vertical dashed lines with `margin=dict(t=50)` and legend at `y=1.15`, preventing text collisions.
  - Anticipatory Early Warning Mechanism Explanation: 14-day antecedent exposure vs. 15.0-day median DOH reporting lag.
- **Tab 2: ⚖️ Statutory & Clinical Grounding (APA 7th)**:
  - Dynamic RAG citation cards with exact quotes, statutory references, issuing authorities, and official source links:
    - Republic Act No. 10173 (Data Privacy Act of 2012)
    - DOH Administrative Order No. 2010-0018 (Post-Exposure Prophylaxis Guidelines)
    - National Kidney and Transplant Institute (NKTI) Leptospirosis AKI Clinical Practice Guidelines (2024)
    - World Health Organization (WHO) 2021 Global Air Quality Guidelines

---

## 5. Verification & Compliance Matrix

| Requirement | Specification Target | Status | Verification Evidence |
| :--- | :--- | :---: | :--- |
| **No Text Truncation** | Custom HTML Bento cards with responsive typography | **COMPLIANT** | Replaced `st.metric()` with `.bento-light` / `.bento-dark` 2x2 grid. Zero `...` clipping. |
| **No Column Squishing** | Full-width vertical tabs for MHO, LDRRMO, BHW, and DOH PEP | **COMPLIANT** | Implemented `st.tabs` inside Row 2 Col 3. Each role gets 100% of card width. |
| **PyDeck Scatterplot Fix** | Radius 350m, 2–6px clamp, 110 alpha opacity | **COMPLIANT** | Scatter circles form an atmospheric dot-matrix without obscuring 3D polygons. |
| **Plotly Title & Legend Fix**| Elevated horizontal legend (`y=1.12–1.15`), transparent bgs | **COMPLIANT** | No overlapping titles on TreeSHAP; Carina/Kristine vlines clear of legend. |
| **Contract Integrity** | Pydantic v2 schemas in `src/api_contracts.py` | **COMPLIANT** | All data types, validations, and field structures preserved. |
| **Small-Cell Suppression** | RA 10173 small-cell masking (`<5` for counts 1–4) | **COMPLIANT** | Enforced across spotlight, telemetry, feed, and tooltips. |
| **Unit Test Coverage** | 10 passed unit tests in `pytest tests/test_pipeline.py` | **COMPLIANT** | 10 passed, 0 failed in 13.62s. |
| **Linting Cleanliness** | Flake8 PEP 8 conformity | **COMPLIANT** | Zero linting errors across codebase (`flake8` exit code 0). |
| **Submission Caps** | 20-slide pitch deck & 180s demo script | **COMPLIANT** | `verify_submission_constraints.py` reports 100% PASS. |
