# Provisional data dictionary and feature provenance

This is a **design schema**, not a claim that an authorized ADNI/OASIS/NACC extract already exists. Confirm exact source table, field, code list, unit and release version from the official dictionary after access. ADNI's [dictionary guide](https://adni.loni.usc.edu/quick-start-guide-asset/datadic.html) says code mappings can vary by phase. This document separates **source fields named by official documentation** from **project-created canonical fields**.

## Source crosswalk to verify after access

| Source | Official identifiers / candidate tables | Project use | Verification needed |
|---|---|---|---|
| ADNI | `RID`, `PTID`, `ROSTER`; `PHASE`, `VISCODE`, `VISCODE2`, `EXAMDATE` / `VISDATE` | Participant grouping and visit linkage | MRI image-to-`RID` mapping, actual acquisition date and QC flags in the approved release. [ADNI table anatomy](https://adni.loni.usc.edu/quick-start-guide-asset/anatomy2.html). |
| ADNI | `DXSUM.DIAGNOSIS` | Label source: 1 CU, 2 MCI, 3 dementia | Confirm harmonized code and visit, no legacy `DXCHANGE` shortcut. [Diagnosis guide](https://adni.loni.usc.edu/quick-start-guide-asset101625/diagnostic.html). |
| ADNI | `DXAPP`, `DXAPROB`, `DXAPOSS`; `DXMDUE` for MCI etiology | Conditional AD-etiology subset definition | Phase-specific presence, codes and clinician interpretation; never use as model inputs. [Diagnosis guide](https://adni.loni.usc.edu/quick-start-guide-asset101625/diagnostic.html). |
| ADNI | `ADNIMERGE`, MRI-derived numeric CSVs | Convenience audit / optional derivative ablation | Inspect each column's original source and timing; merged diagnosis or image-derived values are not independent clinical observations. [Data organization](https://adni.loni.usc.edu/quick-start-guide-asset/data_org.html), [MRI](https://adni.loni.usc.edu/data-samples/adni-data/neuroimaging/mri/). |
| OASIS-3 | Subject and imaging session identifiers, released clinical CSVs, days-from-entry visit labels | External participant grouping and scan/visit pairing | Use release-specific dictionary and relative day fields; match visits under a predeclared window. [FAQ](https://sites.wustl.edu/oasisbrains/home/oasis-resources-and-faq/), [imaging dictionary](https://sites.wustl.edu/oasisbrains/files/2024/04/OASIS-3_Imaging_Data_Dictionary_v2.3-a93c947a586e7367.pdf). |
| NACC | `NACCID`, UDS visit date fields and MRI scan dates; SCAN/mixed-protocol files | External grouping and scan/visit pairing | Versioned UDS dictionary, imaging protocol and temporal linkage; NACC does not automatically bind a scan to a UDS visit. [Researcher guide](https://www.naccdata.org/the-nacc-researchers-guide). |

Do not join clinical and MRI rows on a visit code alone. ADNI [documentation](https://adni.loni.usc.edu/quick-start-guide-asset/anatomy2.html) explains that codes and dates have different meanings across phases and that one code may have multiple actual examination dates.

## Canonical project fields

| Canonical field | Type / unit | Role | Inclusion and leakage rule |
|---|---|---|---|
| `source_release` | String | Provenance | Record source, release and extraction date; no model input. |
| `subject_key` | Private string | Grouping | One participant across all scans/visits; never input, log, prompt or Git. |
| `visit_key` / `scan_key` | Private strings | Provenance | Version and QC tracing only. |
| `scan_time` / `clinical_time` / `label_time` | Date or relative day | Temporal audit | Compute absolute gaps; do not expose dates to model/UI. |
| `t1_volume` | 3D MRI, DICOM or NIfTI | Image input | Quality-controlled T1 only; record orientation, spacing, scanner and preprocessing provenance. |
| `diagnosis_label` | CU / MCI / dementia | Target | From approved visit diagnosis; never input. AD-etiology label is a separately defined subset. |
| `age_at_scan` | Years | Candidate clinical input | Confirm source calculation, valid range and availability at scan. |
| `sex_recorded` | Dataset category | Candidate clinical input | Preserve missing/unknown; assess demographic performance and privacy. |
| `preindex_history_*` | Dataset-specific | Conditional clinical input | Include only if measured before index and unrelated to direct target coding; each variable needs a provenance row. |
| `diagnostic_assessment_*` | Scale-specific | Quarantined candidate | Same-visit CDR/MMSE/Logical Memory II may help define ADNI's cohort; exclude from primary model unless a separate, justified sensitivity experiment is specified. [ADNI cohorts](https://adni.loni.usc.edu/quick-start-guide-asset/cohorts.html). |
| `mri_derived_*` | Defined units | Separate imaging derivative | Volumes, radiomics, segmentations and MRI-generated summaries are **not** independent clinical data. |
| `site_id` / `scanner_id` | Category | Audit | Check confounding and split distribution; not initial predictors. |
| `missing_mask` | Boolean vector | Model support | Distinguish missing from zero. Imputation is trained inside each training fold. |

## Required feature registry for the authorized extract

For **every** proposed model feature, record: source/release, original table and field, exact coding, unit, valid range, missing-value code, measurement time relative to scan and label, whether used by diagnostic adjudication, whether derived from MRI, preprocessing transform, number/percent missing by class and split, and inclusion decision with reviewer/date. A blank item means **not approved**. The registry must live in an access-controlled research environment if it contains participant values; this public document records only the schema and aggregate decisions.

Feature classes:

1. **Always excluded:** IDs, labels, etiology codes, clinician diagnosis/confidence, future visits, outcome status, split membership and post-label derived fields.
2. **Primary candidates after verification:** age, recorded sex and genuinely pre-index history variables. Limited features may make a simple tabular model preferable to a Clinical Transformer.
3. **Sensitivity-only:** diagnostic scales such as CDR/MMSE, with explicit acknowledgement of target-proxy risk and a comparison that excludes them.
4. **Imaging derivatives:** separate ablation, never represented as independent clinical modality.

See [dataset strategy](dataset_strategy.md), [cohort protocol](dataset_access_and_cohort_protocol.md) and [validation rules](../research/data_leakage_and_validation.md).
