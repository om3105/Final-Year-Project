# Explainability plan

The interface may show **model-attribution aids**, never anatomical or causal diagnoses. OmniBrain `[2]` uses Grad-CAM for MRI and SHAP for tabular features; TriFusion `[1]` includes MRI volume interpretation and clinical correlations, which are different forms of evidence.

1. Choose an image method compatible with the trained encoder: Grad-CAM for a convolutional final feature map, or a gradient/token method with validated projection back into the MRI volume for a pure Transformer. Never call raw attention weights a guaranteed explanation. Show the target class, slice/plane, overlay opacity, orientation and unmodified image beside the overlay.
2. Estimate clinical contribution with SHAP or a validated approximation on a fixed training-background sample. Include feature names, units, observed/missing status, reference population, and whether a feature was measured independently or derived from MRI. Correlated variables can split attribution unpredictably.
3. Test stability under small scan perturbations, bootstrap model refits and alternative background samples. Check whether marked regions are outside the brain, on scan edges or site artifacts. Store aggregate QA results, not patient images.
4. Display calibrated class probabilities, model version, input QC status and the phrase “research prototype; not a medical diagnosis.” Explain that high probability does not equal certainty. Suppress explanations when input QC fails or the model abstains.

Attribution agreement with a clinician is a separate future study. No explanation is proof that the model has learned disease biology.
