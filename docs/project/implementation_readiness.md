# Implementation readiness record — 30 September 2026

**Overall status: preparation complete; restricted-data gates open. Application implementation has not started.** This record prevents a documented plan from being mistaken for an access approval or trained model.

The user's subsequent [ADNI/MIMIC/cancer diagram](../architecture/multi_dataset_proposal_review.md) is a **pending scope expansion**. This record's complete research/design gate applies only to the Alzheimer-domain baseline. The cancer task is selected as breast lesion benign-versus-malignant classification, with CMMD a candidate dataset pending audit; the MIMIC endpoint and both branches' literature/dataset audits are not complete.

| Gate | Current status | Evidence / next owner |
|---|---|---|
| 50-paper research and design specifications | Complete with documented full-text limits | [Pre-development review](pre_development_review.md), [quality report](../../research/papers/research_quality_report.md). Missing PDFs are a research limitation, not an application-code blocker. |
| Explicit instruction to implement application | **Not received in unambiguous form** | The user's “complete it” is being applied to the preparation gates discussed in this conversation. See [AGENTS.md](../../AGENTS.md). |
| Named ADNI applicant and institutional affiliation | **Missing** | User reported no existing investigator or IDA access. ADNI's [official answer to an undergraduate applicant](https://adni.loni.usc.edu/support/experts-knowledge-base/question/?QID=1853) suggests a professor apply and list the student, **or permits the student to apply personally** using the thesis department and degree being pursued when that is not possible. The user must choose a truthful route and submit the [application](../data/adni_access_request_packet.md); do not invent an identity. |
| ADNI approval and named-user scope | **Not obtained** | Applicant submits and accepts the [ADNI DUA](https://adni.loni.usc.edu/wp-content/themes/adni_2023/documents/ADNI_Data_Use_Agreement.pdf); ADNI decides. No account credentials belong in this repository. |
| DUA-compliant cloud compute/storage | **Unverified** | [Cloud review](../security/cloud_data_use_review.md) identifies questions; no restricted upload to Colab, Drive or third-party service until an authorized reviewer approves exact terms. |
| Actual paired cohort size and task feasibility | **Unknown** | Requires approved data access and the [aggregate audit](../data/authorized_cohort_audit_template.md). Source release counts are not eligible cohort counts. |
| Final target and independent clinical feature set | **Provisional** | Current design: CU/MCI/dementia; AD etiology requires extra fields. Exclude same-visit diagnostic assessments from the primary independent-clinical set pending provenance review. [Dataset strategy](../data/dataset_strategy.md). |
| External OASIS-3 or NACC validation | **Conditional** | Separate access plus endpoint, visit and feature harmonization. Failure does not prevent an ADNI-only within-source study. |
| Guaranteed ₹0 training and live deployment | **Unproven** | Free Colab resources fluctuate; live 3D inference host unproven. A synthetic demonstration remains viable without claiming real clinical performance. [Feasibility](feasibility_review.md). |
| Code, models, real data | **None** | No application implementation, dataset ingestion, training or checkpoint release. |

## Paths forward

**Research-data path:** ask a project guide/professor to apply and list the student, or follow ADNI's published option for an undergraduate to apply personally with the correct thesis department and degree. ADNI decides on access. Institution/applicant reviews the compute environment; the approved users audit the actual cohort and feature timing; only then does real-data preparation/training proceed.

**Lower-access exploratory path:** the student may separately request OASIS access under its [access process](https://sites.wustl.edu/oasisbrains/request-access/) and [DUA/form](https://sites.wustl.edu/oasisbrains/home/access/). The current form requires an institutional email and detailed research statement even for OASIS-1/2. Those releases are smaller and have limited independent clinical predictors; they do not preserve the proposed rich multimodal claim. OASIS-3/4 require NITRC registration and reviewed access. The [OASIS FAQ](https://sites.wustl.edu/oasisbrains/home/oasis-resources-and-faq/) warns against pooling OASIS-1/-2/-3 because participants overlap. See the [alternative dataset decision](../data/alternative_dataset_decision.md). Switching the primary dataset requires updating the research question, architecture/experiment scope and ADR, not silently swapping files.

MIRIAD offers a separate registration-based binary AD/control pilot with 69 people and limited independent clinical fields. It cannot validate the original three-class MCI claim; see the [alternative dataset decision](../data/alternative_dataset_decision.md).

**Synthetic development path:** after a clear instruction to implement, code contracts, validation and UI on synthetic fixtures can be developed without restricted data. Such a demo cannot claim validated disease detection. Real-data experiments remain blocked until the relevant dataset and environment approvals.

## What cannot be completed by a coding agent

An agent cannot truthfully provide the applicant's identity and affiliation, accept a personal DUA, grant ADNI/OASIS access, approve third-party cloud terms for an institution, produce paired counts without authorized data, or guarantee free GPU/hosting capacity. The next human-controlled step is to choose the professor-assisted or truthful student application route and use the prepared [access packet](../data/adni_access_request_packet.md).
