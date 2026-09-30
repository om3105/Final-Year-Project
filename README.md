# Deep Multimodal Learning Framework for Early Disease Detection Using Medical Images and Clinical Data

## One-line Description

A final-year IT **research prototype plan** for studying paired brain MRI and structured clinical information in Alzheimer-related classification. **No application has been implemented or trained.**

**Scope review:** the user has proposed a broader ADNI + MIMIC chest X-ray + cancer framework. The cancer task is **breast lesion benign-versus-malignant classification**, with CMMD mammography as a candidate dataset pending audit (ADR-013). The MIMIC prediction task remains undecided. The [multi-dataset proposal review](docs/architecture/multi_dataset_proposal_review.md) records the design and its unresolved questions; the Alzheimer experiment below remains the current specified baseline.

## Problem

MRI and clinical observations can contain complementary information, but medical AI evaluations are vulnerable to patient overlap, target leakage, dataset shift, calibration errors and misleading explanations. A reported paper score does not establish clinical diagnostic utility `[1]`, `[2]`, `[33]`, `[35]`.

## Proposed Solution

Use one coherent Alzheimer/MCI domain, a legally obtained paired cohort, patient-level splits and a controlled comparison of image-only, clinical-only, concatenation, cross-attention and optional post-fusion Transformer models. The intended output is an AI-assisted research prediction with class probabilities, QC status and method-labeled attributions, never a medical diagnosis.

## Architecture

T1 MRI → validated preprocessing → MRI encoder candidate (pretrained brain-MRI model or Swin) → image tokens. Independent time-valid clinical fields → validated train-fold preprocessing → MLP or FT-Transformer → clinical tokens. Compare concatenation with masked cross-attention; test an optional multimodal Transformer. Classification and calibration follow. [Detailed design](docs/architecture/system_architecture.md) and [math](docs/architecture/mathematical_formulation.md). The heavy branches are conditional on results and free compute.

## Research Base

The closest starting point is **OmniBrain** `[2]`, selected for its MRI, clinical/tabular Transformer, cross-attention, Grad-CAM and SHAP design. **TriFusion-ADFormer** `[1]` is the Swin V2 MRI reference but uses concatenation and MRI-derived text. NeuroNet-AD `[27]` is a direct MRI/metadata cross-attention comparator. [Evidence-based comparison](docs/research/base_paper_selection.md). Fifty publications, 48 consulted full texts and 44 verified local PDFs are documented in [research/papers](research/papers/README.md), with access limits in its [quality report](research/papers/research_quality_report.md).

## Research Gap and Key Contributions

The proposed work tests the added value of *independent* clinical fields and cross-attention under matched patient splits, calibration and resource constraints. It is an **architecture synthesis and reproducibility contribution**, not a claim of new attention mathematics or proven clinical benefit. [Gap](docs/research/research_gap.md); [contribution](docs/research/proposed_contribution.md); [literature review](docs/research/literature_review.md).

## Technology Stack

Proposed Python/PyTorch/MONAI, FastAPI and Next.js, with browser-based Colab/Codespaces development and a versioned checkpoint store only if data terms permit. [Stack rationale](docs/technology/technology_stack.md).

## Dataset

The research strategy selects ADNI as the **primary source** and OASIS-3/NACC as conditional external sources for one Alzheimer-spectrum study. The auditable baseline target is **cognitively unimpaired / MCI / dementia**; ADNI's diagnosis code for dementia does not itself confirm Alzheimer etiology. An AD-specific subset requires a separate diagnostic-field audit. No dataset has been obtained. Access, cloud processing, paired counts and input-feature provenance must be cleared before training. [Dataset strategy](docs/data/dataset_strategy.md), [cohort protocol](docs/data/dataset_access_and_cohort_protocol.md) and [data dictionary](docs/data/data_dictionary.md).

## Training and Evaluation

Train the matched baselines before adding attention. Split by participant, preserve repeated visits and prevent train-test preprocessing contamination. Report per-class F1, sensitivity, specificity, AUROC, AUPRC, calibration and confidence intervals. [Experiments](docs/ml/experiment_plan.md), [leakage protocol](docs/research/data_leakage_and_validation.md), [evaluation](docs/ml/evaluation.md).

## Explainability

Test a compatible image attribution method and SHAP/clinical importance, with stability and feature-provenance checks. Explanations are supportive model behavior views, not causal evidence. [Plan](docs/ml/explainability.md).

## Web Application and Deployment

Planned Next.js screens and FastAPI endpoints are [specified](docs/frontend/ui_ux_specification.md) in [API docs](docs/backend/api_specification.md), but do not exist. The ₹0 target is **partially feasible**: free static UI/browser development is credible; reliable live 3D MRI inference and private durable history are not established. [Free-tier strategy](docs/deployment/free_tier_strategy.md) and [feasibility](docs/project/feasibility_review.md).

## Cost

Target **₹0**, with no paid APIs, database, GPU or mandatory local machine. Colab GPU access and free hosting are limited and can change. A synthetic research demo is the fallback if lawful live inference cannot fit a free host.

## Project Structure

`research/papers/` holds catalog, notes, PDFs and search evidence; `docs/` holds research, architecture, requirements, ML, data, deployment, API, UI, safety and roadmap specifications; `scripts/` contains research catalog helpers. `data/`, `experiments/`, `model/`, `backend/`, `frontend/` and `tests/` are reserved for later phases. No restricted data or application code is included.

## How a Future Agent Should Understand This Repository

Read [AGENTS.md](AGENTS.md) first, then this README, [architecture](docs/architecture/system_architecture.md), [requirements](docs/requirements/software_requirements_specification.md), [research quality](research/papers/research_quality_report.md), and the relevant source paper notes. Source authority is verified papers → official dataset docs → official framework docs → architecture → requirements → experiments → implementation → general knowledge. Document any discrepancy before changing the architecture.

## Development Status and Known Limitations

**Research phase: complete with documented access limits.** The catalog has 50 verified identities, full-text audits for 48 papers and 44 local PDFs. P003/P004 remain official-abstract-only; six PDFs are not available locally. Dataset access, DUA-compatible cloud training, final model sizing and host eligibility are implementation-entry gates. **Implementation: not started.** See [pre-development review](docs/project/pre_development_review.md).

The [implementation readiness record](docs/project/implementation_readiness.md) tracks the remaining human-controlled access gates. An [ADNI application packet](docs/data/adni_access_request_packet.md), [cloud data-use review](docs/security/cloud_data_use_review.md) and [aggregate cohort audit template](docs/data/authorized_cohort_audit_template.md) are ready. No ADNI investigator or access has been identified.

The [alternative dataset review](docs/data/alternative_dataset_decision.md) documents MIRIAD as a possible small binary AD/control pilot after registration and explains why other publicly described sources do not directly replace the ADNI-first study.

If ADNI access is unavailable, review the [alternative dataset decision](docs/data/alternative_dataset_decision.md) before changing the primary study. OASIS-1 is the most plausible course-project fallback, with a narrower scientific claim and its own access terms.

## Roadmap

Explicit authorization to implement → authorized dataset preparation → baselines → fusion model → training/evaluation → explanations → API/UI → feasible deployment → testing/documentation → final demo. [Detailed phase gates](docs/project/project_roadmap.md).

## References

Primary `[1]` S. Sabari Vasan and P. Jayalakshmi, “TriFusion-ADFormer,” *Frontiers in Artificial Intelligence*, 2026, DOI: [10.3389/frai.2026.1849315](https://doi.org/10.3389/frai.2026.1849315). `[2]` A. Sharshar *et al.*, “Not Only Grey Matter: OmniBrain,” *ICCV Workshops*, 2025, [official proceedings](https://openaccess.thecvf.com/content/ICCV2025W/CVAMD/html/Sharshar_Not_Only_Grey_Matter_OmniBrain_for_Robust_Multimodal_Classification_of_ICCVW_2025_paper.html). Complete [BibTeX bibliography](research/papers/references.bib).
