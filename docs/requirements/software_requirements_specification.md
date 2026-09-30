# Software requirements specification (draft research baseline)

## Users and scope

Users are an authorized researcher running experiments, a guide/evaluator viewing aggregate results or synthetic demo cases, and a developer maintaining the prototype. No patient self-diagnosis or clinical workflow is in scope.

## Functional requirements

FR-01 ingest one quality-controlled T1 MRI and a schema-validated, time-valid clinical vector for an authorized research subject. FR-02 enforce patient-level split and provenance before training. FR-03 train/evaluate image-only, clinical-only, concatenation and attention variants on matched partitions. FR-04 output class probabilities, version, QC/abstention and research disclaimer. FR-05 provide method-labeled image and clinical attributions when supported. FR-06 expose draft health/model/analyze/explain endpoints. FR-07 present landing, analysis, result, explanation, model information and about screens. FR-08 keep history disabled until retention/auth policy is approved.

## Nonfunctional requirements

NFR-01 reject corrupt, oversized, unsupported and potentially identifying uploads. NFR-02 use TLS, bounded requests, no secrets in code and no patient values in logs. NFR-03 train-fold-only preprocessing and immutable patient split manifests. NFR-04 record environment, dataset release, config, checkpoint and aggregate metrics for reproduction. NFR-05 keyboard and screen-reader accessible interface; responsive layouts. NFR-06 profile end-to-end latency and memory before setting production targets. NFR-07 use free/open software and stay within a ₹0 cost target; disclose any unmet hosting goal. NFR-08 no raw restricted dataset or participant-level derivatives in the repository or AI prompts.

## Acceptance gates

Research evidence and data-use approval precede real-data work. Model acceptance requires leakage checks, a locked patient-level evaluation, per-class and calibrated metrics, subgroup/generalization discussion, and uncertainty limits. Deployment acceptance requires provider eligibility, checkpoint-release approval, security review and measured resource fit. The demo may remain synthetic if these gates are unmet.
