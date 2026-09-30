# Instructions for every future coding agent

**Read AGENTS.md first. Then read README.md. Then read docs/architecture/system_architecture.md. Then read docs/requirements/software_requirements_specification.md. Inspect the relevant research documents before modifying ML architecture.**

## Purpose and current status

This is a final-year IT research project about paired brain MRI and independent clinical variables for Alzheimer/MCI research classification. The repository contains a 50-paper catalog and completed pre-development specifications with access limits stated. **Application implementation has not started.** Do not infer that documented endpoints or screens already exist. An explicit user instruction to implement is required before writing frontend/backend/model application code.

The user has since proposed a **multi-dataset diagram** with ADNI, MIMIC chest X-ray and cancer. The intended tasks are ADNI CU/MCI/dementia (Alzheimer etiology not yet verified), MIMIC-CXR pneumonia label present/absent (report-derived), and CMMD breast lesion benign/malignant (clinical-feature suitability unresolved). Read [its review](docs/architecture/multi_dataset_proposal_review.md) and ADR-012 through ADR-014 before treating the full diagram as adopted. The current single-domain research design remains the operative specification until the scope and evidence are revised.

## Source of truth

1. Verified research papers.
2. Official dataset documentation and data-use agreements.
3. Official framework/provider documentation.
4. Project architecture specification.
5. Project requirements.
6. Recorded experiment results.
7. Implementation.
8. General model knowledge.

If implementation and architecture disagree, document the discrepancy first in an ADR and CHANGELOG; do not silently rewrite either. Paper catalog fields marked “Not verified from available source” are unresolved, not facts. Paper IDs `[1]`–`[50]` map to P001–P050. The [quality report](research/papers/research_quality_report.md) lists full-text and PDF access limits.

## Dataset and ML rules

- Obtain and obey each dataset's access agreement. ADNI and OASIS-3 data cannot be casually copied to a cloud runtime, model assistant, public service or this repository. Verify a cloud provider's terms with the authorized investigator before ingestion. Never expose patient-level raw or derived data.
- Split at participant level before slice generation, augmentation, imputation, normalization, selection or calibration. Keep repeated visits together. Record feature source and time relative to label; exclude target-defining cognitive scores from the primary predictor unless explicitly justified. See [leakage protocol](docs/research/data_leakage_and_validation.md).
- Use matched splits and comparable training budgets for image-only, clinical-only, concatenation and attention arms. Do not hard-code expected winners or borrow performance numbers from papers. Log every config and aggregate result; keep immutable private split manifests and checkpoint hashes.
- Swin, FT-Transformer, cross-attention and post-fusion Transformer are **candidates**, not an automatic final stack. Adopt only with ablation and resource evidence. Maintain MRI spatial metadata and validate attribution alignment.

## Medical safety and privacy

The product must say “AI-assisted prediction,” “research prototype,” and “not a medical diagnosis.” Do not output treatment advice or causal claims from attention/SHAP. Abstain on unsupported/failed-QC input. Never log upload contents, names, identifiers or raw clinical values. Do not add analysis history without an approved authentication, retention and deletion design. See [medical safety](docs/medical/medical_safety.md) and [security](docs/security/security_and_privacy.md).

## Coding and API conventions for future phases

When authorized to implement, use small typed modules and explicit schema contracts; separate preprocessing, model, evaluation and serving. Keep scripts reproducible and configurations versioned. API responses use stable error codes, request IDs and no patient payload reflection; follow [API spec](docs/backend/api_specification.md). Frontend uses accessible semantic controls, responsive layouts, explicit loading/error/empty states and research-only copy; follow [UI spec](docs/frontend/ui_ux_specification.md). Never commit secrets, model caches, raw/processed datasets or unreviewed checkpoint files.

## Tests and documentation

Test leakage invariants, schema/file validation, tensor shapes and missing masks, metric/calibration code, API errors, integration on synthetic fixtures, accessibility and security. See [testing strategy](docs/testing/testing_strategy.md). Do not include restricted subject examples in tests. After any architecture or dataset change, update the architecture, mathematical formulation, experiment plan, ADR and README. Record dated work in CHANGELOG. For each experiment, store config, environment, data release, split hash, model hash, metrics and failures as described in [reproducibility](docs/reproducibility/reproducibility.md). For any new important decision, add an ADR with date, context, alternatives, reason and consequences.

## Next agent's first task

Wait for a clear user instruction before application implementation. Read [implementation readiness](docs/project/implementation_readiness.md): the user currently has no ADNI applicant or IDA access. The [application packet](docs/data/adni_access_request_packet.md), [cloud review](docs/security/cloud_data_use_review.md) and [aggregate cohort audit template](docs/data/authorized_cohort_audit_template.md) are prepared but not approved. When instructed, settle ADNI authorization and cloud-only compute terms before real-data work; inspect pairing, clinical-feature timing and patient counts, then measure baseline resource fit before selecting the final trained variant. Synthetic-fixture development after clear authorization must not imply real-data validation. P003/P004 remain official-abstract-only and six local PDFs are missing as documented; seek lawful additional source access if research is revisited. Record any new evidence in the catalog, notes, comparison matrix, ADRs and CHANGELOG.
