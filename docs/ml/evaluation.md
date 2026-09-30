# Evaluation plan

The unit of analysis is a **participant**, not a slice. Report cohort flow, class counts, missingness and age/sex/site distributions before performance. Use an untouched patient-level test set. Report point estimates with participant-bootstrap 95% confidence intervals when sample size permits; disclose when intervals are unstable. Fix decision thresholds on validation only.

| Metric | Use and caveat |
|---|---|
| Accuracy | Overall correct fraction; can hide minority MCI errors. |
| Precision / positive predictive value | Fraction of predicted positives correct; prevalence-sensitive. |
| Recall / sensitivity | Fraction of true class detected; central for missed cases. |
| Specificity | Fraction of non-class subjects correctly excluded. |
| F1 | Harmonic mean of precision and recall at a fixed threshold; show per-class and macro. |
| AUROC | Threshold ranking across positives/negatives; one-vs-rest macro plus class curves for multiclass. |
| AUPRC | Precision–recall area; especially useful for uncommon classes, always report prevalence baseline. |
| Confusion matrix | Raw counts and row-normalized rates, at patient level. |
| Calibration | Reliability plot, Brier score and ECE with bin specification; probabilities are not clinical certainty. |

Also report missing-modality performance, scanner/site subgroup results where group sizes protect privacy, failed-QC counts, model size, peak memory and end-to-end latency. Compare arms on the same test participants; use paired bootstrap differences rather than comparing unrelated paper accuracies. External validation must preserve label definitions or clearly document mapping. TriFusion `[1]` reports several of these metrics; OmniBrain `[2]` illustrates that cross-dataset accuracy can differ markedly.
