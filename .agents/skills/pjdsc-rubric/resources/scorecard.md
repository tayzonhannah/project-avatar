# PJDSC 2026 Evaluation Scorecard & Compliance Checklist

## Core Constraints Checklist (Hard Penalties)
- [ ] **Slide Deck Length**: $\le 20$ slides (Penalties: $-1$ pt per 1–2 slides over limit).
- [ ] **Video Duration**: $\le 3$ minutes / 180 seconds (Penalties: $-1$ pt per 15 seconds over limit).
- [ ] **Dataset Privacy & Ethics**: Anonymized data compliant with Republic Act 10173 (Data Privacy Act of 2012).
- [ ] **Citation Style**: Strict APA 7th Edition format for all references and data sources.

---

## Rubric Weighting Table

| Category | Weight | Key Verification Checklist |
| :--- | :--- | :--- |
| **1. Project Rationale & Design** | **20%** | • Clear target population & geographic burden (PSA/DOH statistics)<br>• Ethical data sourcing, audit log in `/data`<br>• Sound analytical problem formulation & hypothesis lineage |
| **2. Execution & Impact** | **25%** | • Rigorous statistical testing ($p$-values, CIs, spatial/temporal tests)<br>• Identification of operational bottlenecks (RHU connectivity, reporting lag)<br>• Explicit actionable LGU/health provider mitigation protocols |
| **3. Code Repository & Reproducibility** | **20%** | • Modular source under `src/` (notebooks reserved for EDA only)<br>• Pinned dependencies, universal seeds (`seed=42`)<br>• Single-command run via Dockerfile / docker-compose / Makefile<br>• Automated CI tests passing |
| **4. Technical Rigor & Innovation** | **15%** | • Baseline benchmarking (naive mean, ARIMA, standard regression)<br>• Leakage-free validation (`TimeSeriesSplit`, spatial blocks)<br>• Model explainability (SHAP/LIME)<br>• Novel multimodal data fusion |
| **5. Demonstration Video & Prototype Showcase** | **15%** | • Strict 180-second pacing (Hook $\rightarrow$ Method $\rightarrow$ Prototype $\rightarrow$ Impact)<br>• Live, high-resolution recording of interactive web application<br>• Clear audio narration and synchronized visual callouts |
