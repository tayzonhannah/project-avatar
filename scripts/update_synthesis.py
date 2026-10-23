import sys

def main():
    path = 'docs/RESEARCH_SYNTHESIS.md'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update Executive summary Phase 3 text
    old_phase3 = """|  Phase 3: The 1 to 8-Week Distributed Lag Epidemiological Surge (July - December)                  |
|  - Pathogen Incubation Window (2 to 30 days; median 7-14 days)                                     |
|  - Clinical Deterioration & Diagnostic Lag (1 to 3 weeks to oliguria / Weil's syndrome)           |
|  - Institutional Surveillance Reporting Lag (PIDSR weekly registry consolidation: 1-4 weeks)       |"""

    new_phase3 = """|  Phase 3: The 1 to 4-Week Distributed Lag Epidemiological Surge (July - December)                  |
|  - Pathogen Incubation Window (Empirical Peak at Lag 2: r = 0.627, p < 10^-11)                     |
|  - Clinical Deterioration & Hospitalization Peak (Lag 3: r = 0.548, p < 10^-8; Weil's syndrome/AKI)|
|  - Institutional Surveillance Reporting Lag (Empirical Median Total Latency: 15.0 days; MAR mechanism)|"""

    if old_phase3 in content:
        content = content.replace(old_phase3, new_phase3)
        print("Updated Executive Summary Phase 3.")
    else:
        print("Notice: old_phase3 pattern not found.")

    s3_heading = '## 3. The Compounding Hazard Hypothesis: Cascading & Lagged Dynamics'
    s4_heading = '## 4. Translational Policy Framework & Operational Trigger Protocols'

    s3_start = content.find(s3_heading)
    s4_start = content.find(s4_heading)

    if s3_start == -1 or s4_start == -1:
        print(f"Error: Could not locate sections (s3={s3_start}, s4={s4_start})")
        sys.exit(1)

    new_s3 = """## 3. The Compounding Hazard Hypothesis: Cascading & Lagged Dynamics

### 3.1 Formal Definition: The Empirically Calibrated Compounding Risk Function

Traditional epidemiological models evaluate environmental risks as independent, additive terms. In contrast, Project Avatar formalizes the **Compounding Multi-Hazard Hypothesis**, now rigorously refined and locked in via the empirical discoveries of our exploratory data analysis (EDA; see `docs/EDA_FINDINGS.md`):

> **Refined Hypothesis Statement**: *In Metro Manila, post-flood leptospirosis outbreaks do not scale linearly with instantaneous rainfall volume. Instead, outbreak magnitude and clinical fatality (Weil's syndrome/AKI) are governed by a multi-stage compounding cascade: severe pre-monsoon Urban Heat Island stress and fine particulate inhalation pre-condition the population with endothelial inflammation and subclinical renal/fluid deficits. These collide with low-elevation flood inundation and an empirical 1-to-4 week distributed lag pathogen incubation window—peaking at Lag 2 ($r = 0.6267, p = 1.83 \\times 10^{-12}$) and Lag 3 ($r = 0.5477, p = 3.07 \\times 10^{-9}$)—operating 14 to 21 days ahead of retrospective central surveillance registries.*

Formally, for municipal local government unit $s \\in \\{1, \\dots, 17\\}$ at epidemiological week $t$, the compounding environmental health risk $\\mathcal{H}_{\\text{compound}}(t, s)$ is formulated as:

$$\\mathcal{H}_{\\text{compound}}(t, s) = g\\left( \\Phi_{\\text{thermal}}(t, s), \\ \\Psi_{\\text{hydrologic}}(t, s), \\ \\Omega_{\\text{lag}}(t, s), \\ \\Xi_{\\text{air\\_baseline}}(s) \\right)$$

where each component is calibrated to empirical ground truth:

1. **$\\Phi_{\\text{thermal}}(t, s)$ — Decoupled Antecedent Thermal Stress**:
   EDA revealed that optical and thermal infrared satellite sensors experience **$68.0\\%$ cloud masking during the monsoon season** (June–November), rendering real-time satellite LST retrieval unviable during active cyclone landfall. Consequently, $\\Phi_{\\text{thermal}}(t, s)$ is structurally decoupled into a high-resolution static dry-season surface prior and an all-weather synoptic atmospheric heat term:
   $$\\Phi_{\\text{thermal}}(t, s) = \\alpha \\cdot \\text{LST}_{\\text{SUHI\\_prior}}(s) + (1 - \\alpha) \\cdot \\sum_{k=4}^{12} w_k \\cdot \\max\\Big(0, \\ \\text{HI}_{\\text{synoptic}}(t-k, s) - 42^\\circ\\text{C}\\Big)$$
   where:
   - $\\text{LST}_{\\text{SUHI\\_prior}}(s)$ is the static, cloud-screened dry-season (March–May; $12.67\\%$ clear-sky null rate) Surface Urban Heat Island anomaly derived from Landsat 8/9 TIRS (Band 10, $30\\ \\text{m}$) and MODIS (MOD11A1, $1\\ \\text{km}$).
   - $\\text{HI}_{\\text{synoptic}}(t-k, s)$ is all-weather daily heat index telemetry from PAGASA synoptic stations (Science Garden, Port Area, NAIA) and ERA5-Land reanalysis ($2\\ \\text{m}$ temperature and dewpoint), with continuous sensor gaps imputed using a **trailing 7-day rolling median filter** (benchmarked at $\\text{MAE} = 5.634\\ \\mu\\text{g/m}^3, r = 0.8278$) and short telemetry runs ($\\le 3\\ \\text{hours}$) filled via Akima cubic spline interpolation.

2. **$\\Psi_{\\text{hydrologic}}(t, s)$ — Topographic Inundation & Soil Saturation Potential**:
   Combining cumulative precipitation with SRTM 1-arc-second (~$30\\ \\text{m}$) digital elevation and volumetric soil water dynamics:
   $$\\Psi_{\\text{hydrologic}}(t, s) = \\left[ \\frac{\\int_{t-2}^{t} P(\\tau, s) \\, d\\tau}{\\max\\left(\\epsilon, \\ \\overline{\\text{Slope}}_{\\text{SRTM}}(s)\\right)} \\right] \\cdot \\text{SM}_{\\text{ERA5}}(t-2, s) \\cdot \\mathbb{I}_{\\left\\{\\overline{\\text{Elev}}_{\\text{SRTM}}(s) < 5\\text{m}\\right\\}}$$
   where:
   - Empirical DEM profiling isolates the hyper-vulnerable low-elevation alluvial basins: the CAMANAVA corridor ($1.8\\text{--}3.8\\ \\text{m}$ ASL; slope $0.2\\%\\text{--}0.3\\%$) and Manila port/estero belt ($3.2\\text{--}3.5\\ \\text{m}$ ASL), where Topographic Wetness Indices ($\\text{TWI}$) exceed $13.5\\text{--}14.8$.
   - $\\text{SM}_{\\text{ERA5}}(t-2, s)$ integrates volumetric soil water saturation ($0\\text{--}7\\ \\text{cm}$ layer) at Lag 2 weeks ($r = 0.4041, p = 2.53 \\times 10^{-5}$), capturing ground saturation that prevents drainage and sustains puddles.

3. **$\\Omega_{\\text{lag}}(t, s)$ — Empirically Locked Distributed Lag Response**:
   Cross-correlation analysis ($N = 104$ weeks; Bartlett $95\\%$ significance bound $\\pm 0.1922$) demonstrated that instantaneous rainfall ($\\tau = 0$) has no statistically significant correlation with disease incidence ($r = 0.1480, p = 0.134$). The distributed lag function is therefore locked strictly to the significant temporal window $\\tau \\in \\{1, 2, 3, 4\\}$:
   $$\\Omega_{\\text{lag}}(t, s) = \\sum_{\\tau=1}^{4} \\beta(\\tau) \\cdot P(t - \\tau, s) + \\delta \\cdot P_{\\text{cum\\_2w\\_4w}}(t, s)$$
   with empirical CCF weights reflecting:
   - **$\\tau = 1$ (Week 1)**: $r = 0.4048, p = 2.22 \\times 10^{-5}$ (primary mucosal/cutaneous incubation onset).
   - **$\\tau = 2$ (Week 2)**: $r = 0.6267, p = 1.83 \\times 10^{-12}$ (**absolute peak outbreak trigger**; Phase 1 leptospiremia).
   - **$\\tau = 3$ (Week 3)**: $r = 0.5477, p = 3.07 \\times 10^{-9}$ (**peak clinical hospitalization & organ failure**; Phase 2 Weil's syndrome/AKI).
   - **$\\tau = 4$ (Week 4)**: $r = 0.2927, p = 0.0031$ (surveillance reporting and laboratory confirmation delay).
   - $P_{\\text{cum\\_2w\\_4w}}(t, s) = \\sum_{\\tau=2}^{4} P(t-\\tau, s)$ aggregates the sustained multi-week flood exposure. Lags $\\tau \\ge 5$ ($r \\le 0.1397$, non-significant) are excluded from the primary feature store.

4. **$\\Xi_{\\text{air\\_baseline}}(s)$ — Chronic Vascular & Pulmonary Baseline Vulnerability**:
   Captures chronic cardiopulmonary degradation parameterized by multi-year median $\\text{PM}_{2.5}$ exceedances above the WHO 2021 annual guideline ($5.0\\ \\mu\\text{g/m}^3$):
   $$\\Xi_{\\text{air\\_baseline}}(s) = \\ln\\left( \\frac{\\text{PM}_{2.5}^{\\text{median\\_4w}}(s)}{\\text{PM}_{2.5}^{\\text{WHO}}(5.0\\ \\mu\\text{g/m}^3)} \\right)$$
   incorporating the $400\\%\\text{--}670\\%$ chronic ambient exceedances documented across DENR-EMB continuous monitoring stations.

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
- **Clinical Presentation Delay**: Median $4.0\\ \\text{days}$ (IQR: $3\\text{--}6\\ \\text{days}$) from symptom onset to healthcare consultation.
- **Diagnostic & Administrative Delay**: Median $10.0\\ \\text{days}$ (IQR: $7\\text{--}14\\ \\text{days}$) for serological batch verification (MAT/IgM) and hierarchical encoding into PIDSR.
- **Total Surveillance Latency**: Median **$15.0\\ \\text{days}$** (IQR: $11\\text{--}20\\ \\text{days}$), with a long right tail where the $90\\text{th}$ percentile reaches **$25.0\\ \\text{days}$** and the $95\\text{th}$ percentile reaches **$29.0\\ \\text{days}$**.
- **Missingness Mechanism (MAR)**: Missing symptom onset dates surge from $3.43\\%$ under baseline conditions to **$22.50\\%$ during disaster surges** ($\\chi^2 = 284.62, p < 10^{-60}$), confirming that data missingness is strictly **Missing at Random (MAR)** conditioned on hospital capacity saturation. Imputing onset dates as $\\text{Onset Date} = \\text{Admission Date} - 4.0\\ \\text{days}$ eliminates survivorship bias.

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
- **Zero-Inflation**: **$37.84\\%$** of municipal-weeks log exactly zero cases.
- **Small Cell Count Rate ($1 \\le n < 5$)**: **$45.76\\%$** of observations report between 1 and 4 cases.

To ensure computational and statutory integrity, Project Avatar formulates a dual-engine machine learning strategy:

#### 1. Binary Outbreak Surge Classification (LightGBM)
- **Target Formulation**: $\\mathbb{I}_{\\{\\text{Incidence} \\ge 1.0\\ \\text{per } 100,000\\ \\text{population}\\}}$, defining an actionable public health surge.
- **Class Imbalance**: Negative class $1,564$ weeks ($88.46\\%$) vs. Positive class $204$ weeks ($11.54\\%$), yielding an empirical imbalance ratio of **$7.67 : 1$**.
- **Hyperparameter Mandate**: Enforce `scale_pos_weight = 7.67` with objective `binary`, evaluating strictly on Precision-Recall AUC (`metric = "auc_pr"`).
- **Validation Scheme**: Walk-forward temporal block cross-validation (`TimeSeriesSplit`, $k = 5$) to strictly prevent temporal leakage.

#### 2. Count Regression with Compound Poisson-Gamma Deviance (Tweedie)
- Standard Mean Squared Error (MSE) assumes homoscedastic Gaussian residuals and produces massive errors on zero-inflated, highly skewed targets.
- The regression engine deploys a **Tweedie loss function** with variance power $p = 1.45$, naturally accommodating the mass at zero ($37.84\\%$) and continuous positive fat tails ($+7.54$ skewness).

#### 3. Statutory Small Cell Suppression (RA 10173 Compliance)
Because $45.76\\%$ of municipal-weeks report fewer than 5 cases, raw model point estimates could inadvertently enable re-identification linkage attacks if paired with emergency dispatch logs. Conforming to **Section 4.2 of `data/README.md` and Republic Act 10173**, all user-facing dashboards and APIs:
- Suppress raw predicted case counts when $1 \\le n_{\\text{cases}} < 5$, rendering them as `"<5"`.
- Map probabilities into standardized, actionable 4-tier categorical risk bands:
  - **Low** (Surge probability $< 0.25$)
  - **Moderate** ($0.25 \\le \\text{Pr} < 0.50$)
  - **High** ($0.50 \\le \\text{Pr} < 0.75$)
  - **Critical** ($\\text{Pr} \\ge 0.75$)

---

### 3.4 The Physiological Collision: Thermal Dehydration, $\\text{PM}_{2.5}$, and Sepsis

The persistent $8\\%\\text{--}12\\%$ Case Fatality Rate observed in Metro Manila cannot be explained solely by microbiological virulence. It represents a **multi-system physiological collapse** caused by compounding stressors:

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

1. **Pre-Renal Dehydration via Urban Heat Islands**: Urban informal laborers exposed to recurrent $42^\\circ\\text{C}\\text{--}48^\\circ\\text{C}$ heat indices suffer from chronic subclinical volume contraction. When *Leptospira* endotoxins invade renal tubules, the kidney—already operating under ischemic hemodynamic stress—rapidly progresses to irreversible acute tubular necrosis (ATN), eliminating the typical oliguric buffer phase.
2. **Capillary Fragility & Pulmonary Hemorrhage**: Chronic exposure to ambient fine particulates ($\\text{PM}_{2.5}$) damages the alveolar-capillary basement membrane through sustained reactive oxygen species (ROS) generation. Subsequent immune-mediated cytokine cascades during the second phase of leptospirosis trigger catastrophic pulmonary hemorrhage syndrome (LPHS), where alveolar capillaries rupture, leading to rapid suffocation and mortality within hours of admission.

---

"""

    updated_content = content[:s3_start] + new_s3 + content[s4_start:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("Successfully updated docs/RESEARCH_SYNTHESIS.md with empirical EDA findings!")

if __name__ == '__main__':
    main()
