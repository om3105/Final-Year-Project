# Dataset access and cohort assembly protocol

**Status:** research specification; no access granted and no participant-level extraction performed. This protocol applies to the selected ADNI-first baseline classification study. It does not authorize a cloud transfer, model training or public demo.

## 1. Access and environment gate

1. Name the investigator, institution, authorized collaborators and intended project in the source request. ADNI requires an [IDA application](https://adni.loni.usc.edu/data-samples/adni-data/); OASIS-3 has a [separate request](https://sites.wustl.edu/oasisbrains/request-access/); [NACC](https://www.naccdata.org/data-request-process/) requires a data request and acceptance of its DUA.
2. Save the dataset release/version, approval scope, agreement revision and allowable processing locations in a **private** record. Recheck provider terms when they change.
3. Review whether the chosen Colab/cloud environment contains all inputs and artifacts under the relevant agreement. The [ADNI DUA](https://adni.loni.usc.edu/wp-content/themes/adni_2023/documents/ADNI_Data_Use_Agreement.pdf) distinguishes contained AI use from tools that can disclose participant data and addresses third-party compute and model weights. The [OASIS DUA](https://bpb-us-e2.wpmucdn.com/sites.wustl.edu/dist/6/4383/files/2025/07/Data-Use-Agreement_July2025.pdf) restricts sharing with third parties. No raw data, row-level output or prompts containing participant information go to this repository or a public service.
4. If a compliant cloud environment cannot be established at ₹0, stop the real-data workflow and report the constraint. Do not treat free Colab availability as data-use permission.

## 2. Define the estimand before extraction

**Proposed index:** one quality-controlled structural T1 MRI scan per participant at the earliest eligible baseline visit. **Primary endpoint proposal:** same-period clinically assessed CU / MCI / dementia, using ADNI `DXSUM.DIAGNOSIS` coding 1/2/3. ADNI's [current diagnostic guide](https://adni.loni.usc.edu/quick-start-guide-asset101625/diagnostic.html) says code 3 is dementia; AD etiology requires extra fields. This is cross-sectional status classification, not prospective prediction. The exact scan-label window is a **project parameter**: start with an eligibility window of at most 90 days, require the clinical reference at or before the scan for feature availability, and compare 30/180-day windows as predeclared sensitivity analyses. If this ordering leaves too few cases, document a revised task and rationale before evaluation; do not silently include post-index features.

For an AD-specific analysis, define the diagnosis criteria and phase-specific etiology codes before looking at model results. MCI-to-dementia conversion, if pursued later, needs a prediction horizon, follow-up completeness, handling of death/dropout and a separate preregistration.

## 3. Build the candidate pool

Use a private extraction manifest with a row per MRI series and source visit. In ADNI, map image identifiers to `PTID`/`RID`; preserve `PHASE`, actual acquisition/exam date and protocol. [ADNI's table anatomy](https://adni.loni.usc.edu/quick-start-guide-asset/anatomy2.html) warns against relying on `VISCODE` alone. Filter to T1 structural images and documented QC pass; record the reason for every exclusion. Choose one series with a deterministic rule fixed in advance, such as approved standardized/processed series priority, then highest QC and closest allowable visit. Do not choose the visually most disease-like scan.

For OASIS-3, use subject and session identifiers plus relative [days from entry](https://sites.wustl.edu/oasisbrains/home/oasis-resources-and-faq/). For NACC, use participant, UDS visit and MRI dates; the [NACC guide](https://www.naccdata.org/the-nacc-researchers-guide) explicitly leaves scan-to-visit matching to investigators. Record how ties and missing dates are handled. Do not combine OASIS-1/-2/-3 as independent samples, as the [official FAQ](https://sites.wustl.edu/oasisbrains/home/oasis-resources-and-faq/) warns of overlap.

## 4. Link label and candidate clinical predictors

Use the nearest eligible diagnosis visit under the preregistered window. Reject ambiguous, conflicting or missing diagnoses; do not fill them from a later outcome. Store scan-to-label and scan-to-clinical time gaps. The first clinical feature inventory should emphasize demographics and verified pre-index history. Quarantine same-visit CDR, MMSE and Logical Memory II because [ADNI's diagnostic cohort guide](https://adni.loni.usc.edu/quick-start-guide-asset/cohorts.html) identifies them as diagnostic inputs. Document missingness by class and source phase before choosing an imputation policy. Numeric features derived from MRI must be tagged as image derivatives.

## 5. Inclusion flow and frozen manifest

Publish an aggregate flow for each source:

`available participants → T1 MRI present → QC pass → linkable visit → diagnosis in window → eligible clinical features → one baseline sample per participant → train/validation/test`.

For every arrow record participant and scan counts plus exclusion reasons. Then report class counts, demographic and site summaries, scan/visit gaps, MRI voxel characteristics, missingness, ADNI phase or external-source composition, and any duplicate scans. The private manifest stores pseudonymous IDs and source keys; the public repository stores only the manifest schema, processing rules and aggregate counts.

## 6. Splitting and external testing

Deduplicate and group by participant **before** slice/patch creation or learned preprocessing. Use one locked ADNI participant-level test partition and grouped training/validation folds; document seed and class/site balance. Fit all preprocessing and calibration only on training folds. The external OASIS-3 or NACC cohort receives a frozen ADNI-trained pipeline. It qualifies as an external test only if the same endpoint and input set can be mapped without inspecting outcome performance. Otherwise describe it as a feasibility or domain-shift analysis, not external validation. Report participant-level metrics and confidence intervals.

## 7. Reproducibility and exit criteria

Before training, an authorized researcher signs off on: access and cloud terms; release versions; label definitions; feature registry; pair-window choices; cohort flow and real eligible counts; zero subject overlap; split manifest; storage/deletion plan; checkpoint sharing policy. Any failure leaves the experiment blocked. The public [data dictionary](data_dictionary.md) specifies the canonical schema, and the [leakage protocol](../research/data_leakage_and_validation.md) lists invalidation checks.
