# Literature review, 2024–2026

References `[n]` map to `Pnnn` in the [catalog](../../research/papers/papers.csv). Forty-eight accessible full texts now have source-located audits in their paper notes; `[3]` and `[4]` remain limited to official abstracts.

## Evolution and scope

In 2024, AD-Transformer encoded structural MRI and non-image clinical/genetic inputs as tokens for one Transformer `[4]`; a separate improved-Transformer study fused sMRI and PET, which is imaging-to-imaging rather than image-to-clinical fusion `[10]`. In 2025, OmniBrain combined MRI features with an FT-Transformer tabular branch and cross-attention, while measuring performance on ANMerge and an MRI-only ADNI external set `[2]`. In 2026, TriFusion-ADFormer used Swin V2 for MRI, BERT for MRI-derived text, and an MLP for cognitive scores, then concatenated the features `[1]`. Reviews `[6]`, `[14]`, and `[32]` catalog more methods but do not establish a universal winning architecture.

## Medical image and Swin Transformers

Transformers operate on image patches or learned tokens and can capture long-range relationships, but 3D scan token counts impose memory costs. TriFusion provides a directly relevant Swin V2 MRI encoder example `[1]`; other transformer classification studies `[8]`, `[41]`, `[48]` and deployment work `[39]` support considering pretrained and lighter image encoders. Evidence from another disease or image modality cannot be treated as AD performance evidence. Swin should therefore be a measured encoder candidate, with an affordable CNN or pretrained brain-MRI encoder baseline `[2]`, `[4]`.

## Clinical modeling and fusion

Independent structured inputs need explicit measurement time, missingness, category encoding, and provenance. OmniBrain uses FT-Transformer for tabular clinical, radiomic, and genomic variables `[2]`; AD-Transformer uses a linear projection of non-image features `[4]`; TriFusion uses an MLP for cognitive scores `[1]`. Those alternatives justify a simple MLP baseline before a clinical Transformer. Concatenation `[1]`, unified self-attention `[4]`, and cross-attention `[2]`, `[3]`, `[27]` represent distinct feature-level fusion mechanisms. DeepALZNET trains its clinical and MRI pathways on separate datasets, so its scores do not establish paired fusion benefit `[5]`. An ovarian ultrasound/report study found its concatenation baseline beat its cross-attention variants `[9]`. Published metrics cannot be compared directly because tasks, cohorts, and partitions differ.

## Cross-attention and a multimodal Transformer

Cross-attention lets MRI tokens query clinical tokens (or conversely) so interactions depend on the current patient. OmniBrain uses cross-attention with modality masks `[2]`; MAMDF's abstract states asymmetric cross-attention and a Transformer feature module `[3]`; NeuroNet-AD uses BERT-encoded metadata with meta-guided cross-attention `[27]`. AD-Transformer instead puts heterogeneous tokens in a shared Transformer `[4]`. A post-fusion Transformer after cross-attention is an optional ablation, since no reviewed paper establishes that its added complexity will help this exact paired cohort. A single tabular summary token would make cross-attention weakly expressive; use feature tokens only if sufficient clinical variables and samples exist.

## Explainability

OmniBrain reports Grad-CAM on MRI and SHAP for tabular variables `[2]`. Image-only interpretable models `[7]`, `[8]` and explainability reviews `[31]`, `[36]` motivate visual and feature-attribution comparisons. Saliency and attention indicate model sensitivity or weights under a method, not a causal explanation or tissue diagnosis. Clinical feature importance can be unstable under correlated variables; test bootstrap stability and display missingness and source provenance.

## Evaluation, leakage, generalization

TriFusion reports patient-level three-fold cross-validation, AUROC, F1, sensitivity, specificity and ECE, but no external cohort `[1]`. OmniBrain reports an external MRI-only ADNI test with substantially lower accuracy than its development cohort `[2]`. NeuroNet-AD describes patient-level splitting of 200 ADNI subjects, then reports OASIS-3 external evaluation on 921 *images*; its metadata include MMSE/CDR/FAQ and merit prediction-time/label-proxy audit `[27]`. Clinical outcome-code leakage `[35]` and diagnostic feature leakage `[33]` show why target time and feature provenance matter. The Three-City study found AUC changed from 0.80 to 0.83 when MRI markers were added to a strong clinical/longitudinal model `[30]`. Accuracy alone is inadequate when classes are uneven; per-class recall, precision, AUROC/AUPRC, calibration, confusion matrices, and patient-level uncertainty intervals are needed `[32]`, `[37]`. The proposed evaluation protocol is specified in [evaluation](../ml/evaluation.md).

## Deployment and efficiency

Efficient imaging models and pruning/quantization studies `[38]`–`[45]` suggest methods to test, not guaranteed latency. A 3D MRI pipeline also incurs upload, decoding, resampling, and model-load time. The free-host strategy must benchmark the full request path before promising interactive response. CMAP-Fusion uses a relevant Cross-Modal Transformer, but part of its laboratory evaluation uses simulated data `[40]`. Clinical deployment would require external and prospective validation, privacy review, quality management, and clinician oversight beyond this project `[32]`, `[36]`, `[37]`.

## Research gaps

The collection supports a controlled question about the *incremental* value of independent clinical data and cross-attention under one locked patient-level split, plus a resource-aware implementation and honest uncertainty reporting. See [research gaps](research_gap.md). It does not support a blanket claim that transformers or attention outperform simpler models.
