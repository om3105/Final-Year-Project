# Pre-development review — 2026-09-30

| Research status item | Current result |
|---|---|
| Papers found / identities verified | 50 / 50 |
| Full PDFs downloaded | 44 / 50 |
| Open-access / paywalled / access unverified | 48 / 1 / 1 |
| Duplicate search hits removed | 13 |
| Base paper | OmniBrain `[2]` |
| Architecture | Finalized as a registered comparison design; model variant selected after training evidence |
| Dataset | CU/MCI/dementia baseline task with ADNI as primary source; applicant, access and cloud use not approved |
| ₹0 live deployment | Partially feasible |
| Documentation | Required research and design documents completed with source/access limits stated |
| Application implementation | **NOT STARTED** |

## Research completed so far

Search and screening produced 50 distinct 2024–2026 papers, a catalog, 50 evidence-bounded notes, 44 verified local PDFs, literature synthesis, a source-coded comparison matrix and architecture/requirements/ML/UI/API/privacy/feasibility specifications. Full text was consulted for 48; two notes are limited to official abstracts because legal or technical full-text access was not achieved. Six local PDFs remain unavailable, though four of these six have reviewed XML full text. The detailed research report is [here](../research/final_research_report.md); counts and residual evidence limits are in the [quality report](../../research/papers/research_quality_report.md).

## Selected base and architecture

OmniBrain `[2]` is closest because it already joins MRI, a tabular/clinical Transformer, cross-attention, Grad-CAM and SHAP, with a cross-cohort test. NeuroNet-AD `[27]` adds an MRI/metadata cross-attention comparator, but uses BERT metadata and possible cognitive label proxies. TriFusion `[1]` supports Swin V2 but uses concatenation and MRI-derived clinical text. The **research architecture is finalized as an experimental design**: simple MRI/clinical baselines, concatenation, masked cross-attention and optional post-fusion Transformer under one split, with Swin as an encoder ablation. The winning trained variant cannot be specified before experiments. See [selection](../research/base_paper_selection.md) and [architecture](../architecture/system_architecture.md).

## Dataset and technology decision

One Alzheimer-spectrum disease family and an ADNI-first paired-cohort strategy are selected; OASIS-3/NACC are conditional external sources. ADNI's harmonized diagnosis labels are CU/MCI/**dementia**, so the exact AD-etiology subset and eligible paired counts remain unresolved until an authorized audit. Same-visit cognitive assessments that help determine diagnosis are quarantined from the primary independent-clinical inputs. This **source strategy is final at design level**, while target refinement and cohort use cannot start without access and cloud-terms approval. Proposed stack: PyTorch/MONAI, FastAPI, Next.js, browser-based Colab/Codespaces, and a checkpoint repository only if permitted. See [dataset](../data/dataset_strategy.md), [cohort protocol](../data/dataset_access_and_cohort_protocol.md) and [stack](../technology/technology_stack.md).

## Cost and major risks

₹0 is plausible for research documentation, browser development and a static synthetic demonstration. Intermittent free GPU training is possible but not guaranteed; full 3D inference on a free always-on CPU backend is unproven. The principal risks are DUA-compatible cloud compute, target leakage through diagnostic cognitive scores, paired cohort size, cross-site generalization, memory/cold-start and public model-weight rights. The fallback is a small CPU model after measured fit or a clearly labeled synthetic-only demonstration. See [feasibility](feasibility_review.md).

## Open questions before implementation

1. Can an authorized investigator obtain a sufficiently large paired T1 MRI/clinical cohort and use the chosen cloud environment under the DUA?
2. Which ADNI dementia records satisfy a verified Alzheimer-etiology definition, and which clinical variables are measured before prediction time without helping define the label?
3. Can OASIS-3/NACC labels be mapped for independent validation without unacceptable cohort shift or rights conflict?
4. Which model variant fits available free compute, and is a free CPU backend actually provisionable?
5. May any trained checkpoint be publicly released, and can real inputs ever be used in a hosted demo?
6. Can lawful full text for P003/P004 or the four remaining open-access PDFs be obtained later? Their current limits are recorded and do not justify inferred details.

## Development phases

After research closure and explicit user authorization: dataset approval/preparation → baselines → attention/Transformer ablations → training → locked evaluation → explanation QA → FastAPI → Next.js → conditional cloud deployment → tests → final demonstration. [Roadmap](project_roadmap.md).

**RESEARCH PHASE: COMPLETE WITH DOCUMENTED ACCESS LIMITS.** The pre-development research deliverables are closed; dataset authorization, paired-cohort verification and cloud provisioning are implementation-entry gates, not claims of completed experiments.

**IMPLEMENTATION: NOT STARTED.**

**Scope note (30 September 2026):** a later user diagram proposes adding MIMIC chest X-ray and a cancer cohort. This review's “research complete” status applies to the original Alzheimer-domain design only. The cancer task is now breast lesion benign-versus-malignant classification (CMMD candidate); the MIMIC endpoint remains undecided. See the [multi-dataset proposal review](../architecture/multi_dataset_proposal_review.md) and ADR-012/013. A multi-disease research phase has not been completed.

The [implementation readiness record](implementation_readiness.md) captures the current access blocker and the two published ADNI undergraduate application routes. The [application packet](../data/adni_access_request_packet.md), [cloud review](../security/cloud_data_use_review.md) and [aggregate cohort audit template](../data/authorized_cohort_audit_template.md) are complete; none confers access or approves a cloud service.
