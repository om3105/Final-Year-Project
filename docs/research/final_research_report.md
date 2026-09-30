# Final research report — 2026-09-30

## 1. Executive Summary

Fifty distinct 2024–2026 publications were cataloged. Full text was consulted for 48, and 44 legally sourced PDFs were verified locally; P003 and P004 remain official-abstract-only because full text could not be lawfully or technically obtained. OmniBrain `[2]` is the closest architectural starting point for MRI plus clinical data, a clinical Transformer, cross-attention and dual explanation methods. The project should study a single Alzheimer/MCI task with patient-level validation. Dataset authorization, cloud privacy and live free inference remain Phase 1/deployment gates. See the [quality report](../../research/papers/research_quality_report.md).

## 2. Problem Definition

Study whether paired structural brain MRI and independent, time-valid clinical observations improve research classification of cognitively normal, MCI and AD states compared with simpler single-modality models. No clinical diagnostic use is intended. TriFusion `[1]`, OmniBrain `[2]` and AD-Transformer `[4]` establish relevant but non-identical tasks and designs.

## 3. Research Questions

Does clinical data add value to MRI under one locked cohort? Does cross-attention improve a matched concatenation baseline? Does a post-fusion Transformer justify its complexity? How stable are explanations and calibration? Can any trained variant fit a lawful ₹0 CPU-serving path? These are empirical questions, not predicted outcomes.

## 4. Search Strategy

On 2026-09-29, ten date-bounded Europe PMC core queries covered AD/MRI/clinical fusion, Transformers, explainability, leakage, validation and efficiency. The first publication cutoff was 2026-09-29. Official publisher and ICCV pages supplemented four close comparator papers. The raw 315-candidate search audit is in `research/papers/candidates.json`; selection records and source locations are in the [paper database](../../research/papers/README.md).

## 5. Paper Selection Criteria

Inclusion: 2024–2026, verified publication identity, substantive relevance to the disease/fusion method or a concrete evaluation/deployment risk. Exclusion: unrelated tasks without transferable method insight, duplicate versions, unsupported bibliographic claims and papers after cutoff. Disease-specific methods outside AD are cited only for their methods. See [quality report](../../research/papers/research_quality_report.md).

## 6. 2024 Literature

AD-Transformer `[4]` demonstrates joint MRI/clinical/genetic token modeling. An improved Transformer study `[10]` addresses sMRI/PET fusion rather than independent clinical observations. Dementia-risk studies `[29]`, `[30]` contribute longitudinal/clinical outcome perspectives. Vision models `[46]`, `[48]`, `[49]` show efficient encoder directions in other imaging tasks; they provide no direct AD performance estimate.

## 7. 2025 Literature

OmniBrain `[2]` provides the strongest architecture overlap. DeepALZNET `[5]` uses **separate** MRI and clinical pathways trained on different datasets, so it is a unimodal-baseline comparator rather than evidence for paired fusion. NeuroNet-AD `[27]` fuses ADNI MRI slices with BERT-encoded metadata by meta-guided cross-attention and reports subject-grouped development plus OASIS-3 external testing; its 921 external observations are *images*, and MMSE/CDR/FAQ metadata require label-proxy review. TriLightNet `[22]` evaluates MRI/PET/clinical information for MCI conversion with Integrated Gradients. Clinical-statistical studies `[16]`, `[19]`, `[29]`, `[30]` supply non-neural and longitudinal comparators. The leakage experiments `[33]`, `[35]` reinforce feature-time and target-definition audits.

## 8. 2026 Literature

TriFusion `[1]` shows Swin V2 MRI encoding with BERT/MLP branches and concatenation. Its text is MRI-derived, and its 105 subjects/306 scan sessions were evaluated within ADNI. A recent MRI/clinical decline study `[17]` tackles regression rather than diagnosis and reports a two-sample 3D batch due to GPU limits. CMAP-Fusion `[40]` uses a Cross-Modal Transformer but evaluates some image sets with simulated laboratory data. Reviews `[6]`, `[14]`, `[32]`, `[36]` summarize generalization and responsible use concerns.

## 9. Multimodal Medical AI

Imaging and clinical fields provide distinct measurements only when clinical values are independently observed. MRI-derived radiomics or generated summaries add image features but do not establish independent modality benefit `[1]`, `[2]`. An ovarian ultrasound/clinical-report paper `[9]` shows that image-describing text has related provenance and that its cross-attention ablations performed worse than concatenation. The primary experiment must track source provenance and compare matched fusion arms.

## 10. Medical Vision Transformers

Patch/image Transformers and Swin are candidate encoders `[1]`, `[4]`, `[8]`. 3D MRI memory and cohort size favor comparing against a smaller pretrained MRI or CNN baseline `[2]`.

## 11. Clinical Transformers

FT-Transformer tokenizes numerical/categorical features in OmniBrain `[2]`; TriFusion uses an MLP for scores `[1]`; AD-Transformer projects non-image features linearly `[4]`. These are the justified clinical branch ablations.

## 12. Cross-Attention

OmniBrain and MAMDF explicitly use cross-attention `[2]`, `[3]`; NeuroNet-AD has an Alzheimer MRI/metadata cross-attention model `[27]`. MAMDF's detailed split/encoder information remains abstract-only, so it cannot be a fully reproducible base from available evidence. The ovarian study's attention-versus-concatenation comparison `[9]` demonstrates why interaction must be tested, not assumed superior.

## 13. Multimodal Transformers

AD-Transformer uses a shared Transformer `[4]`, while MAMDF's abstract describes a Transformer fusion module `[3]`. A post-cross-attention Transformer is an optional complexity ablation, not a fixed requirement.

## 14. Explainable AI

OmniBrain reports Grad-CAM and SHAP `[2]`. The project will test method compatibility and stability, and label both as model attributions rather than causal disease evidence `[31]`, `[36]`.

## 15. Medical AI Evaluation

Report per-class F1, sensitivity, specificity, AUROC, AUPRC, calibration, confusion matrices and participant-bootstrap intervals. TriFusion reports many such metrics within ADNI `[1]`; separate-cohort validation remains distinct from cross-validation `[2]`. The methodology review `[32]` reports calibration in only 30.8% of its reviewed studies, while TRIAGE `[37]` includes grouped, temporal and external validation. Patient is the primary unit: all slices and visits from a patient stay in one partition, and uncertainty intervals resample patients, not slices.

## 16. Data Leakage

Participant, slice and repeated-visit overlap; train/test preprocessing contamination; post-label features; diagnostic score circularity; and site/metadata proxies are all pre-specified audit targets. Evidence from feature/label leakage studies `[33]`, `[35]` and the MRI-derived text in `[1]` motivates these controls.

## 17. Deployment

No source establishes that this architecture can run live on a free host. Render Free provides 0.1 CPU/512 MB with spin-down; Colab is interactive with no guaranteed GPU. The [free-tier analysis](../deployment/free_tier_strategy.md) details verified current policies.

## 18. Technology Stack

Proposed Python/PyTorch/MONAI/medical IO/SHAP for research, FastAPI for serving, Next.js for UI, Colab/Codespaces for browser development and an approved model repository for checkpoints. All are contingent on compatibility and dataset terms. See [stack](../technology/technology_stack.md).

## 19. Dataset Analysis

ADNI is the primary paired-cohort candidate; OASIS-3 or NACC is a conditional external candidate. No unrelated disease datasets will be mixed. ADNI's current [diagnostic documentation](https://adni.loni.usc.edu/quick-start-guide-asset101625/diagnostic.html) maps harmonized `DXSUM.DIAGNOSIS` to CU, MCI and **dementia**; code 3 alone is not proof of Alzheimer etiology. The primary auditable task is therefore CU/MCI/dementia baseline classification, with an AD-etiology subset only after a field-level audit. ADNI's [cohort documentation](https://adni.loni.usc.edu/quick-start-guide-asset/cohorts.html) identifies CDR, MMSE and Logical Memory II as diagnostic inputs, so same-visit scores are excluded from the primary independent-clinical set pending leakage review. Authorized access and data-use review are required. The [ADNI DUA](https://adni.loni.usc.edu/wp-content/themes/adni_2023/documents/ADNI_Data_Use_Agreement.pdf) permits only AI processing with adequate containment and requires third-party compute and checkpoint release review. See [dataset strategy](../data/dataset_strategy.md), [cohort protocol](../data/dataset_access_and_cohort_protocol.md) and [data dictionary](../data/data_dictionary.md).

## 20. Base Paper Analysis

OmniBrain `[2]` is selected for its MRI, tabular Transformer, cross-attention, missing-modality design, Grad-CAM and SHAP. TriFusion `[1]` remains the Swin reference; MAMDF `[3]` the cross-attention comparator; AD-Transformer `[4]` the joint-token comparator. See [decision evidence](base_paper_selection.md).

## 21. Research Gap

The testable gap is controlled incremental value under matched patient splits, independent clinical provenance, calibration and generalization, plus honest compute feasibility. This is an investigation priority, not a universal novelty claim. See [research gap](research_gap.md).

## 22. Proposed Architecture

Start with MRI and clinical baselines, then concatenation, masked cross-attention, and optional post-fusion Transformer; compare Swin against a lighter/pretrained MRI encoder. See [architecture](../architecture/system_architecture.md).

## 23. Proposed Contribution

An architecture synthesis and reproducible implementation is proposed, with source-aware clinical variables, leakage auditing, calibration and a research-only UI. No new clinical utility or mathematical novelty is claimed. See [contribution](proposed_contribution.md).

## 24. Feasibility

Training and live inference on free resources are conditional; privacy-compatible cloud processing is unresolved. See [feasibility](../project/feasibility_review.md).

## 25. Free-Cost Strategy

Use free browser development and static hosting first; only deploy CPU inference after measured host fit and eligibility. Synthetic demonstration is fallback. See [strategy](../deployment/free_tier_strategy.md).

## 26. Risks

Paired-cohort access, DUA/cloud restrictions, target leakage through cognitive scores, small sample size, site shift, model memory, cold-start, explanation instability and false clinical interpretation.

## 27. Limitations

Two papers remain abstract-only (P003 and P004), and six PDFs are missing locally; four of those six have legally accessible XML full text already reviewed. Method/detail depth varies across the 48 full-text notes, and a future reproducer should consult original articles for exact hyperparameters. No dataset has been acquired, model trained, checkpoint profiled, external validation performed or cloud host provisioned. Source evidence does not support a clinical deployment claim or a guarantee that ₹0 live MRI inference will work.

## 28. Development Roadmap

Research closure and data-access gate precede baseline, fusion, evaluation, explanation, backend, frontend, deployment and final demonstration. See [phase roadmap](../project/project_roadmap.md).

## 29. References

`[1]`–`[50]` correspond to `P001`–`P050` in the [bibliography](../../research/papers/references.bib) and [paper notes](../../research/papers/README.md). Each catalog entry has a direct DOI or official source URL. The four key references are `[1]` TriFusion-ADFormer, `[2]` OmniBrain, `[3]` MAMDF and `[4]` AD-Transformer.
