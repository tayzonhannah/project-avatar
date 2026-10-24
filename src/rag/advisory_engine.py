"""
Project Avatar: ChromaDB Clinical & Disaster Risk Advisory Engine.
Retrieves and synthesizes public health directives grounded in:
1. DOH AO 2010-0018 (Leptospirosis Prevention & PEP Protocols)
2. DOH Memorandum 2024-0288 (Urgent Flooding PEP Prophylaxis)
3. WHO Global Air Quality Guidelines 2021
4. NKTI Acute Kidney Injury & Hemodialysis Surge Protocol Guidelines
5. Republic Act 10121 (DRRM) & Republic Act 10173 (Data Privacy Act of 2012)
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
import numpy as np
import chromadb

from src.utils.seed import GLOBAL_SEED, set_seed
from src.api_contracts import (
    StakeholderRole,
    ActionPriority,
    LanguageCode,
    RiskTier,
    RAGAdvisoryRequest,
    RAGAdvisoryResponse,
    ActionDirective,
    RetrievedCitation,
    ClinicalPrescription,
)

set_seed(GLOBAL_SEED)

# Regulatory and clinical guidance summaries (transparently labeled as project adaptations)
REGULATORY_CORPUS: List[Dict[str, str]] = [
    {
        "id": "CORPUS-DOH-PEP-01",
        "title": "Project Summary adapted from DOH Administrative Order No. 2010-0018",
        "authority": "Department of Health (Philippines)",
        "reference": "DOH AO 2010-0018, Section VI.B (Post-Exposure Prophylaxis Guidelines)",
        "content": (
            "Post-Exposure Prophylaxis (PEP) for Leptospirosis: Single dose Doxycycline 200 mg orally "
            "taken within 24 to 48 hours of wading in contaminated floodwaters for low-risk casual exposure. "
            "For moderate exposure (wading with minor scratches or wounds): Doxycycline 200 mg once daily for 3-5 days. "
            "For continuous or high-risk exposure (residents in persistent low-lying floodwaters): "
            "Doxycycline 200 mg orally once weekly until exposure ends. "
            "Absolute contraindications: pregnant women, lactating mothers, and children under 8 years of age. "
            "Approved alternative: Amoxicillin 500 mg orally TID for 7 days or Azithromycin 500 mg daily for 3 days."
        ),
        "url": "https://doh.gov.ph/",
    },
    {
        "id": "CORPUS-DOH-MEMO-02",
        "title": "Project Summary adapted from DOH Memorandum No. 2024-0288",
        "authority": "Department of Health (Philippines)",
        "reference": "DOH Memo 2024-0288 (Flood Season Prophylaxis Stockpiling & Mobilization)",
        "content": (
            "All Metro Manila Local Health Offices and Rural Health Units are instructed to maintain emergency buffer stocks "
            "of Doxycycline capsules during southwest monsoon (Habagat) and typhoon occurrences. "
            "Community distribution must be proactive through Barangay Health Centers "
            "and evacuation centers before floodwaters recede. "
            "Stockpiles should scale proportionally with municipal population and local inundation vulnerability."
        ),
        "url": "https://doh.gov.ph/",
    },
    {
        "id": "CORPUS-WHO-AIRQ-03",
        "title": "Project Summary adapted from WHO Global Air Quality Guidelines (2021)",
        "authority": "World Health Organization",
        "reference": "WHO Global AQG 2021, Executive Summary & Health Endpoints",
        "content": (
            "Ambient PM2.5 24-hour mean concentrations exceeding 15 ug/m3 trigger acute respiratory irritation. "
            "Sustained elevated exposure exacerbates underlying cardiopulmonary disorders. "
            "Advisory: Vulnerable demographics (elderly, pediatric, asthmatics) should limit strenuous outdoor activity "
            "and utilize well-fitted particulate filtration masks (N95 or KF94) during elevated atmospheric stagnation episodes."
        ),
        "url": "https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health",
    },
    {
        "id": "CORPUS-NKTI-AKI-04",
        "title": "Project Summary adapted from NKTI Acute Kidney Injury Clinical Protocol",
        "authority": "National Kidney and Transplant Institute",
        "reference": "NKTI Clinical Guidance: Acute Kidney Injury Management in Leptospirosis",
        "content": (
            "During post-typhoon flooding events, tertiary referral centers prepare "
            "surge capacity for Acute Kidney Injury (AKI). "
            "Severe leptospirosis presents with rapid renal impairment, "
            "pulmonary involvement (Weil's syndrome), and hyperkalemia. "
            "Frontline triage screening: Oliguria (< 0.5 mL/kg/h for 6 hours), severe calf tenderness, "
            "conjunctival suffusion, and elevated serum creatinine require prompt "
            "referral for continuous renal replacement therapy."
        ),
        "url": "https://nkti.gov.ph/",
    },
    {
        "id": "CORPUS-RA10121-DRRM-05",
        "title": "Project Summary adapted from Republic Act 10121 (DRRM Act of 2010)",
        "authority": "NDRRMC / Office of Civil Defense",
        "reference": "RA 10121, Sections 6 & 12 (Local Disaster Risk Reduction Management)",
        "content": (
            "Local Disaster Risk Reduction and Management Councils (LDRRMCs) must enforce preemptive clearing "
            "of drainage pumping stations, esteros, and floodgates in CAMANAVA and Pasig-Marikina basins. "
            "Provide protective rubber boots and waterproof personal protective equipment to all rescue personnel, "
            "sanitation workers, and evacuees wading through municipal stagnant floodwaters."
        ),
        "url": "https://www.officialgazette.gov.ph/2010/05/27/republic-act-no-10121/",
    },
    {
        "id": "CORPUS-RA10173-PRIV-06",
        "title": "Project Summary adapted from Republic Act 10173 (Data Privacy Act of 2012)",
        "authority": "National Privacy Commission (Philippines)",
        "reference": "RA 10173, Sections 12(e) & 13(f) (Public Health Research & Disclosure Controls)",
        "content": (
            "Public health surveillance processing operates under lawful scientific research and emergency health protections. "
            "To safeguard patient confidentiality, epidemiological reporting adheres to statistical disclosure limitation: "
            "cells with small counts (1 to 4 cases) are suppressed (<5) on public interfaces "
            "to prevent indirect re-identification linkage."
        ),
        "url": "https://www.officialgazette.gov.ph/2012/08/15/republic-act-no-10173/",
    },
]


class ChromaAdvisoryEngine:
    """
    RAG-driven knowledge retrieval and clinical decision advisory engine.
    Indexes WHO, DOH, NKTI, and statutory public health summaries in ChromaDB.
    """

    def __init__(
        self,
        collection_name: str = "avatar_clinical_knowledge",
        persist_directory: Optional[str] = None,
    ):
        if persist_directory:
            self.client = chromadb.PersistentClient(path=persist_directory)
        else:
            self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Project Avatar Philippine Public Health Regulatory Corpus"},
        )
        self._index_corpus()

    def _index_corpus(self) -> None:
        if self.collection.count() == 0:
            ids = [doc["id"] for doc in REGULATORY_CORPUS]
            documents = [doc["content"] for doc in REGULATORY_CORPUS]
            metadatas = [
                {
                    "title": doc["title"],
                    "authority": doc["authority"],
                    "reference": doc["reference"],
                    "url": doc["url"],
                }
                for doc in REGULATORY_CORPUS
            ]
            self.collection.add(ids=ids, documents=documents, metadatas=metadatas)

    def retrieve_relevant_citations(
        self,
        query: str,
        n_results: int = 3,
    ) -> List[RetrievedCitation]:
        results = self.collection.query(query_texts=[query], n_results=min(n_results, len(REGULATORY_CORPUS)))

        citations: List[RetrievedCitation] = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if "metadatas" in results and results["metadatas"] else []
            ids = results["ids"][0] if "ids" in results and results["ids"] else []

            for i in range(len(docs)):
                meta = metas[i] if i < len(metas) else {}
                cid = ids[i] if i < len(ids) else f"CIT-{i:02d}"
                citations.append(
                    RetrievedCitation(
                        citation_id=cid,
                        document_title=str(meta.get("title", "Clinical Protocol")),
                        issuing_authority=str(meta.get("authority", "Department of Health")),
                        statutory_or_cpg_reference=str(meta.get("reference", "Clinical Protocol")),
                        exact_excerpt=docs[i],
                        url_or_doi=str(meta.get("url", "https://doh.gov.ph/")),
                    )
                )

        return citations

    def generate_advisory(
        self,
        request: RAGAdvisoryRequest,
    ) -> RAGAdvisoryResponse:
        """
        Synthesizes role-specialized and risk-calibrated action directives.
        Directives scale dynamically across LOW, MODERATE, HIGH, and CRITICAL risk tiers.
        """
        query_text = (
            f"Leptospirosis prophylaxis treatment protocol {request.risk_tier.value} "
            f"for role {request.target_role.value} under post-flood exposure"
        )
        citations = self.retrieve_relevant_citations(query_text, n_results=2)

        # Dynamic confidence score based on retrieval depth
        confidence_score = round(float(np.clip(0.85 + (len(citations) * 0.05), 0.70, 0.95)), 2)

        # Grounding clinical prescription
        clinical_guidance = ClinicalPrescription(
            regimen_name="DOH Leptospirosis Post-Exposure Prophylaxis (PEP)",
            drug_and_dosage=(
                "Low risk: Doxycycline 200 mg single dose within 24-48h; "
                "Moderate risk: 200 mg daily for 3-5 days; "
                "High risk: 200 mg once weekly until exposure ends"
            ),
            timing_window="Within 24 to 48 hours of flood exposure",
            contraindications="Absolute contraindication in pregnancy, nursing mothers, and children under 8 years",
            alternative_drug="Amoxicillin 500 mg orally TID for 7 days (or Azithromycin 500 mg daily for 3 days)",
        )

        advisory_id = f"ADV-{request.lgu_id}-{uuid.uuid4().hex[:6].upper()}"
        directives: List[ActionDirective] = []
        is_tagalog = request.language == LanguageCode.TAGALOG
        tier = request.risk_tier

        # -------------------------------------------------------------
        # Tier-sensitive dynamic directive generation
        # -------------------------------------------------------------
        if request.target_role == StakeholderRole.MUNICIPAL_HEALTH_OFFICER:
            if tier == RiskTier.LOW:
                directives.append(
                    ActionDirective(
                        directive_id=f"{advisory_id}-DIR-01",
                        priority=ActionPriority.P3_ROUTINE,
                        action_title="Maintain Routine Sentinel Surveillance and Standard Clinic Buffer",
                        action_description=(
                            f"Risk level is LOW in {request.lgu_name.value}. Maintain standard baseline inventory "
                            "at municipal health centers and verify weekly PIDSR reporting consistency."
                        ),
                        target_stakeholder="City Health Officer / Clinic Supervisors",
                        resource_requirement="Standard baseline inventory (1,000 capsules Doxycycline 200mg)",
                    )
                )
                summary = (
                    f"ROUTINE MONITORING for {request.lgu_name.value}: Assessed at LOW risk "
                    f"({request.outbreak_surge_probability:.1%} surge probability). Expected weekly cases: "
                    f"{request.suppressed_case_display}. Standard baseline surveillance maintained."
                )
            elif tier == RiskTier.MODERATE:
                directives.append(
                    ActionDirective(
                        directive_id=f"{advisory_id}-DIR-01",
                        priority=ActionPriority.P2_URGENT,
                        action_title="Pre-position Doxycycline Buffer Stocks in Vulnerable Barangays",
                        action_description=(
                            f"Risk level is MODERATE in {request.lgu_name.value}. Pre-position prophylactic supplies "
                            "in flood-prone barangay stations and alert local physicians to early febrile presentations."
                        ),
                        target_stakeholder="City Health Officer / Rural Health Physicians",
                        resource_requirement="3,000 - 5,000 capsules Doxycycline 200mg + Amoxicillin suspensions",
                    )
                )
                summary = (
                    f"ELEVATED RISK ADVISORY for {request.lgu_name.value}: Assessed at MODERATE risk "
                    f"({request.outbreak_surge_probability:.1%}). Expected weekly cases: "
                    f"{request.suppressed_case_display}. Pre-positioning of prophylaxis recommended."
                )
            else:  # HIGH or CRITICAL
                directives.append(
                    ActionDirective(
                        directive_id=f"{advisory_id}-DIR-01",
                        priority=ActionPriority.P1_IMMEDIATE,
                        action_title="Mobilize Surge Doxycycline Stockpiles to Frontline Clinics",
                        action_description=(
                            f"EPIDEMIC SURGE ALERT in {request.lgu_name.value}. Activate DOH Memo 2024-0288 emergency reserves. "
                            "Distribute prophylactic blisters to all frontline clinics and evacuation centers immediately."
                        ),
                        target_stakeholder="City Health Officer / Rural Health Physicians",
                        resource_requirement="15,000 - 25,000 capsules Doxycycline 200mg + 2,000 Amoxicillin 500mg suspensions",
                    )
                )
                directives.append(
                    ActionDirective(
                        directive_id=f"{advisory_id}-DIR-02",
                        priority=ActionPriority.P2_URGENT,
                        action_title="Activate Acute Kidney Injury (AKI) Oliguria Screening Triage",
                        action_description=(
                            "Implement NKTI Clinical Staging protocol. Monitor suspected patients for oliguria (<0.5 mL/kg/h) "
                            "and coordinate immediate referral for continuous renal replacement."
                        ),
                        target_stakeholder="Hospital Medical Directors & Triage Nurses",
                        resource_requirement="Foley catheters, point-of-care creatinine test cartridges, IV penicillin G",
                    )
                )
                summary = (
                    f"SURGE ALERT for {request.lgu_name.value}: Assessed at {tier.value} risk "
                    f"with an outbreak probability of {request.outbreak_surge_probability:.1%}. Predicted weekly cases: "
                    f"{request.suppressed_case_display}. Dominant drivers: {', '.join(request.dominant_shap_drivers.keys())}."
                )

        elif request.target_role == StakeholderRole.DISASTER_RISK_REDUCTION_OFFICER:
            if tier in [RiskTier.LOW, RiskTier.MODERATE]:
                directives.append(
                    ActionDirective(
                        directive_id=f"{advisory_id}-DIR-01",
                        priority=ActionPriority.P3_ROUTINE,
                        action_title="Routine Drainage Inspection and Chokepoint Maintenance",
                        action_description=(
                            f"Inspect municipal floodgates and remove debris along esteros in {request.lgu_name.value} "
                            "to maintain gravity drainage readiness."
                        ),
                        target_stakeholder="LDRRMO Maintenance & Engineering Teams",
                        resource_requirement="Standard maintenance equipment and safety gear",
                    )
                )
                summary = (
                    f"DISASTER READINESS MONITORING for {request.lgu_name.value}: Risk level is {tier.value}. "
                    "Routine inspection of drainage infrastructure recommended."
                )
            else:
                directives.append(
                    ActionDirective(
                        directive_id=f"{advisory_id}-DIR-01",
                        priority=ActionPriority.P1_IMMEDIATE,
                        action_title="Activate Pumping Stations and Enforce Floodgate Clearance",
                        action_description=(
                            "Enforce RA 10121 disaster protocols. Expedite floodgate clearance along esteros "
                            f"and river tributaries "
                            f"in {request.lgu_name.value} to prevent prolonged water stagnation."
                        ),
                        target_stakeholder="LDRRMO Engineering & Operations Teams",
                        resource_requirement="Submersible heavy-duty pump fuel, backhoes, and debris disposal trucks",
                    )
                )
                directives.append(
                    ActionDirective(
                        directive_id=f"{advisory_id}-DIR-02",
                        priority=ActionPriority.P2_URGENT,
                        action_title="Distribute Waterproof PPE and Knee-High Rubber Boots",
                        action_description=(
                            "Mandate all emergency responders and rescue teams wear protective knee-high rubber boots "
                            "before traversing flooded alleys."
                        ),
                        target_stakeholder="Disaster Response Quick Action Teams",
                        resource_requirement="1,500 pairs heavy-duty rubber boots, sanitation disinfectants",
                    )
                )
                summary = (
                    f"DISASTER CONTINGENCY ADVISORY for {request.lgu_name.value}: Hydrological and topographical risk level is "
                    f"{tier.value}. Urgent mitigation required for low-elevation drainage sluggishness."
                )

        elif request.target_role == StakeholderRole.BARANGAY_HEALTH_WORKER:
            if is_tagalog:
                if tier == RiskTier.LOW:
                    summary = (
                        f"PAALALA SA KALUSUGAN ({request.lgu_name.value}): Mababang panganib ng leptospirosis sa kasalukuyan. "
                        "Ipagpatuloy ang pag-iingat at pagtuturo ng kalinisan sa komunidad."
                    )
                    directives.append(
                        ActionDirective(
                            directive_id=f"{advisory_id}-DIR-01",
                            priority=ActionPriority.P3_ROUTINE,
                            action_title="Pangkaraniwang Pagtuturo sa Kalinisan at Pag-iwas sa Baha",
                            action_description=(
                                f"Ipaalala sa mga residente ng {request.lgu_name.value} na iwasang magbabad sa maruming tubig "
                                "at hugasang mabuti ang katawan pagkatapos ng ulan."
                            ),
                            target_stakeholder="Barangay Health Workers & BHERTs",
                            resource_requirement="Impormasyong polyeto, logbook",
                        )
                    )
                elif tier == RiskTier.MODERATE:
                    summary = (
                        f"BABALA SA KALUSUGAN ({request.lgu_name.value}): Katamtamang panganib ng leptospirosis. "
                        "Maging alerto sa mga may lagnat o lumusong sa baha."
                    )
                    directives.append(
                        ActionDirective(
                            directive_id=f"{advisory_id}-DIR-01",
                            priority=ActionPriority.P2_URGENT,
                            action_title="Pamamahagi ng Prophylaxis sa mga Lumusong sa Baha",
                            action_description=(
                                f"Tukuyin ang mga residenteng lumusong sa baha sa {request.lgu_name.value} at "
                                "bigyan ng Doxycycline 200mg ayon sa DOH protocol (bawal sa buntis at bata)."
                            ),
                            target_stakeholder="Barangay Health Workers",
                            resource_requirement="Doxycycline 200mg blisters, intake forms",
                        )
                    )
                else:
                    summary = (
                        f"KRITIKAL NA BABALA SA KALUSUGAN ({request.lgu_name.value}): Mataas ang panganib ng leptospirosis. "
                        "Agad uminom ng prophylaxis kung lumusong sa baha at pumunta sa health center kung may lagnat."
                    )
                    directives.append(
                        ActionDirective(
                            directive_id=f"{advisory_id}-DIR-01",
                            priority=ActionPriority.P1_IMMEDIATE,
                            action_title="Pabahay-bahay na Pamamahagi ng Doxycycline PEP",
                            action_description=(
                                f"Bisitahin ang mga kabahayan sa binahang lugar ng {request.lgu_name.value}. "
                                "Ipamahagi ang Doxycycline 200mg sa mga lumusong sa baha sa nakalipas na 24-48 oras. "
                                "Bawal sa buntis, nagpapasuso, at mga batang wala pang 8 taong gulang."
                            ),
                            target_stakeholder="Barangay Health Workers & BHERTs",
                            resource_requirement="Doxycycline 200mg blisters, logbook, polyeto",
                        )
                    )
            else:
                if tier in [RiskTier.LOW, RiskTier.MODERATE]:
                    summary = (
                        f"COMMUNITY HEALTH ADVISORY for {request.lgu_name.value}: Risk level is {tier.value}. "
                        "Routine education and early symptom monitoring active."
                    )
                    directives.append(
                        ActionDirective(
                            directive_id=f"{advisory_id}-DIR-01",
                            priority=ActionPriority.P2_URGENT if tier == RiskTier.MODERATE else ActionPriority.P3_ROUTINE,
                            action_title="Community Hygiene Outreach & Exposure Logging",
                            action_description=(
                                f"Educate residents in {request.lgu_name.value} on flood exposure risks "
                                f"and log any accidental contact."
                            ),
                            target_stakeholder="Barangay Health Workers",
                            resource_requirement="Information leaflets and clinic intake sheets",
                        )
                    )
                else:
                    summary = (
                        f"COMMUNITY SURGE ALERT for {request.lgu_name.value}: Elevated {tier.value} risk. "
                        "Frontline door-to-door prophylaxis mobilization initiated under DOH guidelines."
                    )
                    directives.append(
                        ActionDirective(
                            directive_id=f"{advisory_id}-DIR-01",
                            priority=ActionPriority.P1_IMMEDIATE,
                            action_title="Door-to-Door Prophylaxis & Symptom Monitoring Mobilization",
                            action_description=(
                                f"Conduct house-to-house outreach across inundated zones in {request.lgu_name.value}. "
                                "Administer Doxycycline 200mg within 24-48h of flood contact. Screen for red-flag symptoms: "
                                "high fever, muscle aches (especially calves), and yellowing eyes."
                            ),
                            target_stakeholder="Barangay Health Workers & Community Volunteers",
                            resource_requirement="Doxycycline blisters, patient intake sheets, IEC Tagalog leaflets",
                        )
                    )
        else:  # GENERAL_PUBLIC
            summary = (
                f"PUBLIC HEALTH ADVISORY for {request.lgu_name.value}: Public health risk is {tier.value}. "
                "Protect yourself against floodborne leptospirosis and elevated particulate exposure."
            )
            directives.append(
                ActionDirective(
                    directive_id=f"{advisory_id}-DIR-01",
                    priority=(
                        ActionPriority.P1_IMMEDIATE
                        if tier in [RiskTier.HIGH, RiskTier.CRITICAL]
                        else ActionPriority.P2_URGENT
                    ),
                    action_title="Avoid Wading in Floodwaters & Seek Care if Exposed",
                    action_description=(
                        "Avoid walking or swimming in floodwaters. If contact is unavoidable, wear protective rubber boots "
                        "and visit your nearest health center within 24 hours for free preventive medicine."
                    ),
                    target_stakeholder="General Public & Commuters",
                    resource_requirement="Protective rubber boots, clean water, soap for skin washing",
                )
            )

        return RAGAdvisoryResponse(
            advisory_id=advisory_id,
            generated_at=datetime.now(timezone.utc),
            lgu_name=request.lgu_name,
            target_role=request.target_role,
            risk_tier=tier,
            executive_summary=summary,
            prioritized_directives=directives,
            clinical_guidance=clinical_guidance,
            retrieved_citations=citations,
            confidence_score=confidence_score,
        )
