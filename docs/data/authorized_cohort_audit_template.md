# Authorized cohort audit: aggregate report template

**Status: blank template. No ADNI/OASIS/NACC data have been accessed.** Run this audit only after [access approval](adni_access_request_packet.md) and [cloud-use review](../security/cloud_data_use_review.md). Participant-level rows and split manifests remain in approved private storage; this public file may contain aggregate counts only.

## Version and task registration

| Field | Value after authorization |
|---|---|
| Dataset/release/download date | Pending |
| Authorized environment reference | Pending |
| Study endpoint | Proposed CU/MCI/dementia at baseline; confirm before extraction |
| AD-etiology subset definition and codes | Pending phase-specific audit |
| Index T1 series, QC rule and priority | Pending release-specific audit |
| Maximum scan–label gap / direction | Proposed ≤90 days and label at/before scan; register exact rule |
| Candidate clinical fields and cutoff | Pending feature registry |
| Split seed / grouped split policy | Pending preregistration |
| Private manifest hash | Pending; hash only, no IDs |

## Inclusion flow: fill with **participant counts** and separate scan counts

| Stage | Participants | MRI series | Exclusion reason summary |
|---|---:|---:|---|
| Authorized release available | Pending | Pending | — |
| Structural T1 identified | Pending | Pending | Missing or unsupported MRI |
| QC-eligible T1 | Pending | Pending | QC fail / duplicate / unsuitable protocol |
| Date and participant linkage valid | Pending | Pending | Missing/ambiguous linkage |
| Label in registered window | Pending | Pending | Missing, conflicting or late label |
| Clinical feature eligibility | Pending | Pending | No time-valid independent features |
| One baseline example per participant | Pending | Pending | Repeated scans/visits removed by fixed rule |
| Train / validation / locked test | Pending | Pending | Grouped by participant |

## Required aggregate summaries

- Counts by CU, MCI, dementia and any AD-etiology subset; do not relabel dementia as AD automatically.
- Missingness for every candidate feature by class and source phase, with source field/measurement time and diagnostic role.
- Scan-to-label and scan-to-clinical gap distributions, T1 resolution/protocol and QC exclusions.
- Age, recorded sex, site/scanner and phase distributions by split; flag small cells before release.
- Duplicate image/patient audit and **zero participant overlap** evidence between partitions.
- External OASIS-3/NACC endpoint and feature mapping table, or a documented reason external validation is infeasible.

The audit fails if any target-defining diagnostic field enters model inputs, visits cross split boundaries, preprocessing uses held-out data, or restricted row-level information is published. See [data dictionary](data_dictionary.md) and [leakage rules](../research/data_leakage_and_validation.md).
