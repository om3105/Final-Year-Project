# Changelog

## 2026-09-30

- Named pneumonia label present-versus-absent as the intended MIMIC-CXR chest task (ADR-014), with report-derived-label and access limits explicit. Clarified the three domain targets; the multi-dataset research phase is incomplete and no model was implemented.

- Selected breast lesion benign-versus-malignant classification as the cancer branch's exact task (ADR-013); CMMD mammography is the candidate dataset pending clinical-feature and resource audit. Multi-dataset architecture remains under review; no application code was written.

- Recorded a user-proposed ADNI/MIMIC/cancer architecture as a pending scope revision (ADR-012). Documented task-specific heads, dataset/label/access gaps and the need for expanded literature review before adopting it. No application code was written.

- Extended the official-source dataset fallback review with MIRIAD, an OpenNeuro Synapse cohort and the Stanford SPHERE synthetic release. ADNI remains the primary research design; no alternative data were obtained.

- Compared OASIS-1/2/3/4, NACC and an OpenNeuro candidate against the project's access and paired-modality requirements; documented OASIS-1 as a narrower course-project fallback, not a silent ADNI replacement.
- Prepared an ADNI application packet, restricted-cloud review, aggregate cohort audit template and implementation-readiness record. User reported no ADNI investigator or IDA access; these external approvals remain open. No restricted data were accessed and no application code was written.

- Deepened official dataset research for ADNI, OASIS and NACC, including access, pairing and cohort-size limitations.
- Corrected the ADNI label proposal: `DXSUM.DIAGNOSIS=3` means dementia, with Alzheimer etiology requiring separate verification. Quarantined same-visit diagnostic assessments from primary clinical predictors.
- Added a versioned access/cohort protocol, expanded the data dictionary and dataset-specific leakage checks. No participant data were accessed and implementation remains unstarted.

## 2026-09-30 — Research and pre-development foundation

- Created 50-paper catalog, BibTeX, 50 source-bounded notes, conservative comparison matrix and research search audit.
- Downloaded 44 verified legal PDF files; consulted full text for 48 papers and documented six missing local PDFs, P003/P004 abstract-only limits, and source-located findings in the 50 notes.
- Verified 42 DOI titles/publishers with Crossref and the remaining publisher identities with official venue pages; rebuilt 50 BibTeX entries from verified author records.
- Selected OmniBrain as closest architectural base; added NeuroNet-AD, TriLightNet and ovarian attention-ablation comparisons to TriFusion, MAMDF and AD-Transformer evidence.
- Drafted dataset, leakage, architecture, experiment, evaluation, explainability, UI, API, security, safety, reproducibility, free-tier, testing and roadmap specifications.
- Finalized an ADNI-first research strategy and baseline-to-attention architecture comparison design. Identified ADNI/OASIS cloud data-use and ₹0 inference feasibility gates. Research phase closed with access limits stated; no data ingested, model trained or application implemented.
