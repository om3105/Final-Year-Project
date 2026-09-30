# ADNI access request packet

**Prepared 30 September 2026. Status: draft for an actual investigator; not submitted.** No credentials, approval, institution or participant data are recorded in this repository. The applicant must enter truthful identity and affiliation details directly in the [ADNI LONI IDA application](https://adni.loni.usc.edu/data-samples/adni-data/). ADNI says the application requires an institutional affiliation and proposed uses, and its committee generally reviews complete requests within two weeks; approval is not guaranteed.

## Information the applicant must supply privately

| Item | Required action |
|---|---|
| Investigator identity and institutional affiliation | Enter in the ADNI form, with institutional email and supervisor/guide involvement if applicable. Do not put credentials in Git or this document. |
| Named users | List every collaborator who will handle ADNI data under the applicable access process. |
| Project scope | Confirm whether the application may cover baseline T1 MRI, diagnosis, demographics and pre-index clinical history; do not request unrelated modalities by default. |
| Institutional review | Determine whether the institution requires ethics/IRB review, exemption or data-protection sign-off before access or cloud processing. |
| Storage and compute | State the actual account, region, service, access controls, retention and backup design. “Google Colab” alone is not enough detail to establish DUA compliance. |
| Publication and sharing | Review ADNI acknowledgement/manuscript requirements and checkpoint-release restrictions in the [DUA](https://adni.loni.usc.edu/wp-content/themes/adni_2023/documents/ADNI_Data_Use_Agreement.pdf). |

## Proposed-use text for the investigator to adapt

> This academic final-year research project will study whether quality-controlled T1-weighted brain MRI and independently collected, time-valid clinical variables improve participant-level classification of cognitive status. The initial endpoint is cognitively unimpaired, mild cognitive impairment, or dementia, following the current ADNI diagnostic coding. An Alzheimer-etiology subset will be analyzed only after the relevant diagnostic fields and cohort criteria are verified. We will compare image-only, clinical-only, simple fusion and attention-based models using participant-level partitions, documented feature provenance, calibration and aggregate performance reporting. We will exclude diagnostic outcome fields from model inputs and review cognitive assessments used to define cohort status for target leakage. Participant-level ADNI data and derivatives will remain inside an approved, access-controlled research environment and will not be placed in a public repository, public AI prompt or public web application. The intended compute environment and any model-weight release will undergo a separate data-use review before use.

This paragraph is a **draft description**, not a representation that access, cloud use, ethics review, or a specific model has been approved. The applicant should edit it to match the actual study and ADNI form.

## Applicant sequence

1. Review the [ADNI data page](https://adni.loni.usc.edu/data-samples/adni-data/) and current [DUA](https://adni.loni.usc.edu/wp-content/themes/adni_2023/documents/ADNI_Data_Use_Agreement.pdf).
2. Confirm institution and any research/ethics requirements with the project guide or authorized investigator.
   ADNI's [answer to an undergraduate applicant](https://adni.loni.usc.edu/support/experts-knowledge-base/question/?QID=1853) suggests asking a professor to apply and list the student as an affiliated investigator. If that is not possible, ADNI says the student may apply personally using the department of the thesis and the degree being pursued.
3. Submit the IDA application under the investigator's own account. No agent may impersonate the applicant or accept the DUA for them.
4. Keep the approval decision and authorized-user list in a private institutional record. Record only an aggregate gate status in [implementation readiness](../project/implementation_readiness.md).
5. Before download, complete the [cloud review](../security/cloud_data_use_review.md). If Colab is not approved, identify another DUA-compliant browser-accessible environment or keep work synthetic.
6. After authorized access, run the [cohort audit](authorized_cohort_audit_template.md) in the approved environment. Publish aggregate counts only.

**Current evidence:** ADNI access **not verified**. The next external action belongs to a real investigator. The project cannot report an ADNI sample size or real-data feasibility until that action and the cohort audit are complete.
