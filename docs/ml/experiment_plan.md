# Machine learning experiment plan

**Primary question:** on identical patient-level partitions, does independent clinical information and attention-based fusion improve a pre-registered metric over image-only and concatenation baselines without unacceptable calibration or inference cost? The base paper `[2]` motivates the cross-attention branch; `[1]` motivates the Swin comparison. No expected winner is assigned.

| Arm | Input and model | Isolated question |
|---|---|---|
| B0 | Clinical-only logistic regression or small MLP | How predictive are time-valid clinical fields? |
| B1 | Image-only pretrained MRI encoder plus linear head | What does MRI contribute alone? |
| B2 | Same encoders, concatenation plus MLP | Simple paired fusion benchmark `[1]` |
| B3 | Same encoders, masked cross-attention | Incremental interaction effect `[2]` |
| B4 | B3 plus post-fusion Transformer | Added self-attention value `[3]`, `[4]` |
| B5 | Swap image encoder for Swin at comparable budget | Encoder effect `[1]` |

Pre-register cohort, label definition, primary metric (macro AUROC, subject to class support), safety metric (MCI sensitivity), calibration metric (ECE and Brier score), and a maximum acceptable memory/latency budget after profiling. Use one locked patient-level test set and group-stratified validation or nested grouped cross-validation if sample size allows. All visits and scans from a participant remain grouped. If sites are adequate, reserve one for external testing; otherwise describe the limit. Use seeds 17, 29 and 41 for model variability, with identical splits; record deterministic settings and residual nondeterminism.

**Initial search ranges, not fixed outcomes:** AdamW; learning rate (10^{-5})–(3\times10^{-4}) (separate encoder/head rates), batch size 1–16 constrained by MRI volume memory, up to 100 epochs, patience 10–20 validation checks, cosine or plateau scheduler, weight decay 0–0.05. Validate image augmentations (small affine/intensity perturbations) for anatomical plausibility and apply only to training subjects. Freeze pretrained encoders initially, then selectively unfreeze if validation supports it. Record every attempted configuration, checkpoint hash, cohort version, preprocessing fit, GPU/CPU type, training time, parameter count, and failure.

**Ablations:** remove clinical branch; remove image branch; replace attention with concatenation; remove post-fusion Transformer; compare clinical MLP with FT-Transformer; withhold MRI-derived variables; mask clinical features; test missing-modality handling; assess same-cohort versus external performance. Calibration fitting uses validation only. Each test result is generated once from a frozen checkpoint and immutable split manifest.
