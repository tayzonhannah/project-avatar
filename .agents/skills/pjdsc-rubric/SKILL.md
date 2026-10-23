---
name: pjdsc-rubric
description: >-
  Guides end-to-end ideation, data engineering, statistical modeling, software development,
  documentation, and deliverable creation aligned with the Philippine Junior Data Science Challenge
  (PJDSC) 2026 competition rubric (rubric1). Use when planning, executing, evaluating, or auditing
  project deliverables for PJDSC, including Philippine public health analytics, reproducible repository
  architecture, strict 20-slide deck limits, and 3-minute demo video scripts.
---

# PJDSC 2026 Competition Alignment & Execution (`pjdsc-rubric`)

Operational skill for autonomous and collaborative agents working in Antigravity. Guides end-to-end ideation, data engineering, statistical modeling, software development, documentation, and deliverable creation according to the Philippine Junior Data Science Challenge (PJDSC) 2026 official evaluation criteria.

---

## Agent System Directives & Core Constraints

> [!TIP]
> For an audit checklist and weighting table, refer to the [Evaluation Scorecard & Checklist](./resources/scorecard.md).

When executing tasks or generating artifacts under this skill, all agents must adhere to the following hard bounds:
1. **Domain Context**: Philippine Public Health Analytics (LGUs, DOH, regional epidemiology, health equity, disease surveillance, clinical resource allocation).
2. **Deliverables Checklist**:
   - **Slide Deck**: Maximum **20 slides** (strictly enforced; -1 pt per 1–2 excess slides).
   - **Demonstration Video**: Maximum **3 minutes / 180 seconds** (strictly enforced; -1 pt per 15s excess).
   - **Code Repository**: Public/reproducible repository, modular architecture, environment lockfiles, executable README, and interactive web/app prototype.
   - **Citations**: Strictly **APA 7th Edition** format for all academic literature, data sources, and clinical protocols.

---

## Rubric Breakdown & Execution Protocols

### 1. Project Rationale & Design (Weight: 20%)
*Focus: Problem formulation, epidemiological grounding, and ethical data foundation.*

- **1.1 Public Health Problem Statement & Urgency**
  - **Directive**: Anchor the problem in concrete Philippine public health statistics (e.g., PSA, DOH surveillance, PhilHealth, WHO Western Pacific).
  - **Agent Action**: Clearly answer: *Who suffers? What is the baseline burden (mortality, morbidity, DALYs, economic load)? Why does traditional surveillance or intervention fail?* Avoid generic statements; specify geographic/demographic scope (e.g., Region VII dengue surge, BARMM maternal healthcare deserts).

- **1.2 Ethical Sourcing, Quality & Dataset Hygiene**
  - **Directive**: Prioritize open and ethically sourced datasets (e.g., DOH Data Collect, Philippine Open Data, Humanitarian Data Exchange, OpenStreetMap, NASA POWER / ERA5 for climate correlations).
  - **Agent Action**:
    - Audit for anonymization and data privacy (adherence to Republic Act 10173 - Data Privacy Act of 2012).
    - Maintain a `/data` audit document describing provenance, licensing, resolution, null-handling, and ethical constraints.

- **1.3 Soundness of Analytical Methodology**
  - **Directive**: Establish a clear lineage from hypothesis to analytical framing.
  - **Agent Action**: Formulate the problem formally (e.g., spatial-temporal Bayesian modeling, counterfactual impact assessment, multi-objective optimization for vaccine allocation). Document why simpler baselines were rejected or benchmarked.

---

### 2. Execution & Impact (Weight: 25%)
*Focus: Real-world findings, statistical validity, and frontline utility.*

- **2.1 Depth of Findings & Statistical Significance**
  - **Directive**: Never stop at raw aggregations or surface correlations ($R^2$ alone is insufficient).
  - **Agent Action**:
    - Run hypothesis testing ($p$-values, confidence intervals, FDR correction) and sensitivity analyses.
    - Measure spatial autocorrelation (Moran's $I$, LISA) or temporal causality (Granger causality, cross-correlations) where applicable.

- **2.2 Real-World Bottlenecks & Operational Mitigation**
  - **Directive**: Acknowledge messy real-world deployment challenges.
  - **Agent Action**: Identify failure modes: sporadic internet connectivity in rural RHUs (Rural Health Units), reporting lag (backdating/right-censoring in DOH figures), cold-chain failures, or workforce shortages. Provide explicit mitigations (e.g., offline-first PWA caching, robust missingness imputation, low-bandwidth UI).

- **2.3 Translational Potential (LGUs, Healthcare Providers, Communities)**
  - **Directive**: Actionable policy-making and clinical utility over theoretical dashboards.
  - **Agent Action**: Include explicit "Action Protocols" triggered by model thresholds (e.g., *"If municipal outbreak probability > 0.75, trigger LGU Vector Control Protocol Tier 2 and dispatch BHW door-to-door larvae inspection within 48h"*).

---

### 3. Code Repository & Reproducibility (Weight: 20%)
*Focus: Clean software engineering, containerization, and zero-friction setup.*

- **3.1 Modular Code Architecture & Quality**
  - **Directive**: Notebooks are for initial EDA only; core logic belongs in structured Python modules or services.
  - **Standard Directory Structure**:
    ```text
    ├── .github/workflows/ci.yml       # Automated linting & reproducibility checks
    ├── data/
    │   ├── raw/                       # Immutable raw datasets (or download script)
    │   └── processed/                 # Feature-engineered artifacts
    ├── notebooks/                     # Numbered, reproducible EDA walkthroughs
    │   ├── 01_eda_and_cleaning.ipynb
    │   └── 02_model_benchmarking.ipynb
    ├── src/                           # Modular source code
    │   ├── __init__.py
    │   ├── data_loader.py
    │   ├── features.py
    │   ├── models/
    │   └── utils.py
    ├── app/                           # Interactive frontend / API (Streamlit/FastAPI/Dash)
    ├── tests/                         # Unit tests for transformation & inference logic
    ├── Dockerfile                     # Single-command containerized run
    ├── docker-compose.yml
    ├── Makefile                       # make setup, make run, make test
    ├── environment.yml / pyproject.toml / requirements.txt
    ├── LICENSE
    └── README.md
    ```

- **3.2 Flawless Reproducibility & Environment Control**
  - **Directive**: Pin all package versions down to exact builds. Set random seeds (42) universally across NumPy, PyTorch, Scikit-Learn, and Python `random`.
  - **Agent Action**: Generate a battle-tested `README.md` with a "Quickstart in 3 Commands" section:
    ```bash
    git clone <repo-url> && cd <repo-dir>
    docker compose up --build
    # or: make install && make run
    ```

---

### 4. Technical Rigor & Innovation (Weight: 15%)
*Focus: Algorithmic depth, novel problem formulation, and unconventional solutions.*

- **4.1 Validity & Appropriateness of ML / Statistical Models**
  - **Directive**: Match model complexity to data scale and inductive bias.
  - **Agent Action**:
    - Benchmark against meaningful baselines (e.g., naive historical mean, ARIMA, standard logistic regression) before demonstrating the superiority of advanced methods (e.g., XGBoost, Graph Neural Networks, Bayesian Structural Time Series).
    - Implement proper validation strategies preventing temporal or spatial leakage (e.g., `TimeSeriesSplit`, spatial block cross-validation).
    - Provide model explainability via SHAP, LIME, or counterfactual examples to enable non-technical clinical trust.

- **4.2 Novelty, Creativity & Deep Analytics**
  - **Directive**: Avoid boilerplate Kaggle-style pipelines.
  - **Agent Action**: Integrate non-obvious multimodal signals (e.g., satellite precipitation data coupled with topography for waterborne disease risk, or mobility metrics merged with hospital bed capacity).

---

### 5. Demonstration Video & Prototype Showcase (Weight: 15%)
*Focus: High-impact narrative, live software demonstration, and ruthless timekeeping.*

- **5.1 3-Minute Video Script Architecture (180 Seconds Max)**
  - **0:00 – 0:30 (Hook & Problem Statement)**: The Philippine public health crisis, local scale, urgency, and the gap in current responses.
  - **0:30 – 1:15 (Methodology & Technical Innovation)**: Novel data pipeline, ML/statistical modeling framework, cross-validation rigor, and explainability.
  - **1:15 – 2:20 (Live Working Prototype)**: User walkthrough demonstrating an end-to-end user journey (input, prediction, visual interpretation, automated recommendation).
  - **2:20 – 3:00 (Real-World Translation & Impact)**: LGU/provider deployment feasibility, operational mitigations, and systemic societal impact.

- **5.2 Video Production Quality Rules**
  - High-definition screen recordings of the real running application (no mockups or static slides during the prototype segment).
  - Clean audio narration with synchronized visual cues and callout annotations.

---

## Antigravity Agent Workflow Integrations

When operating in autonomous multi-agent pipelines:
1. **Researcher Agent**: Validates public health literature, finds primary Philippine datasets, and formats references in strict APA 7th.
2. **Data Science / ML Agent**: Implements modular code under `src/`, ensures spatial/temporal split integrity, tracks metrics, and generates SHAP explanations.
3. **Software / Full-Stack Agent**: Builds the interactive prototype (e.g., Streamlit, Gradio, or FastAPI + React), encapsulates the environment in Docker, and ensures sub-2-second inference latency.
4. **Reviewer / Auditor Agent**: Evaluates generated code against the 5 rubric criteria, tests reproducibility from scratch, and checks word counts and video timing scripts.
