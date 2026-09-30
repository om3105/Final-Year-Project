# Architecture decision records

All decisions dated **2026-09-30** and remain conditional until data/feasibility gates pass. A later change requires a new ADR, update to system architecture, and CHANGELOG entry.

| ADR | Decision | Context / alternatives | Reason and consequences |
|---|---|---|---|
| 001 | Next.js for research UI | Alternative: static React/Vite | Good route/component support; Vercel Hobby path. Server features may increase hosting cost; static export is fallback. |
| 002 | FastAPI for inference API | Alternative: Flask, one-process UI | Typed schema and OpenAPI; separate CPU service may be infeasible at ₹0. |
| 003 | Swin as image **candidate** | Alternatives: pretrained MRI encoder, CNN | TriFusion `[1]` uses Swin V2, but OmniBrain `[2]` offers a directly relevant pretrained MRI baseline. Profile before adopting. |
| 004 | FT-Transformer as clinical **candidate** | Alternative: MLP/linear | OmniBrain `[2]` supports its use; small tabular cohorts may favor MLP. |
| 005 | Cross-attention as experimental fusion | Alternative: concatenation `[1]` | OmniBrain `[2]` and MAMDF `[3]` support study; complexity and overfitting must be measured. |
| 006 | Post-fusion Transformer optional | Alternative: pool cross-attention output | AD-Transformer `[4]` supports joint attention; incremental value is unknown. |
| 007 | SHAP plus compatible MRI attribution | Alternatives: permutation importance, gradient methods | OmniBrain `[2]` uses SHAP/Grad-CAM; methods have stability and causality limits. |
| 008 | Browser-only development target | Alternative: local workstation | User constraint; Codespaces/Colab possible but dataset cloud terms need approval. |
| 009 | ₹0 cost target | Alternative: paid GPU/backend | User constraint; static/synthetic fallback if live inference cannot fit free resources. |
| 010 | One AD disease domain | Alternative: unrelated multi-disease collection | Cohort/label coherence; ADNI primary candidate and OASIS-3 validation candidate, both gated by access. |
| 011 | No default history | Alternative: stored analyses | Retention, authentication and medical-data hosting are not approved. |
| 012 | Multi-dataset diagram received; **decision pending** | Alternative: keep ADR-010 single AD domain | User proposes ADNI + MIMIC + cancer branches. The MIMIC and cancer endpoints are undecided, and these sources have different labels, image geometry and access terms. Preserve ADR-010 as the current experiment design while [reviewing the proposal](../architecture/multi_dataset_proposal_review.md). If adopted, use task-specific heads and validation, then revise all affected specifications before implementation. |
| 013 | Cancer task: breast lesion benign versus malignant | Alternatives: breast subtype, cancer versus healthy from TCGA-BRCA, other organs | CMMD has mammograms linked to biopsy-confirmed benign/malignant outcomes and supporting demographic/clinical data. Choose lesion malignancy as the cancer branch's exact endpoint; use CMMD as a candidate dataset after feature timing, class balance, access and compute audit. This selects the task, not the full multi-dataset architecture or a deployed diagnostic claim. |
| 014 | Chest task: pneumonia label present versus absent | Alternatives: pleural effusion, other MIMIC-CXR findings | Pneumonia is a named disease and MIMIC-CXR-JPG provides a report-derived label for it. Select pneumonia as the intended chest branch endpoint, with an explicit uncertain/missing-label policy and clinical time alignment before cohort construction. The label is not a confirmed clinical diagnosis. MIMIC remains credentialed and the full multi-dataset architecture remains under review. |

Source hierarchy: verified papers → official dataset documentation → official framework documentation → architecture spec → requirements → experiment results → implementation → general model knowledge. If implementation conflicts with architecture, document the discrepancy and update this log before changing the spec.
