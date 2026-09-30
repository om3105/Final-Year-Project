# Medical safety and intended use

This is an academic **research prototype** for evaluating whether MRI and clinical information can support Alzheimer-related *classification research*. It is not a diagnostic device and has no prospective clinical validation. It must not be used to diagnose, triage, prescribe, or reassure a patient.

Class probabilities reflect a model trained on a particular selected cohort; they are not clinical certainty. False negatives may miss disease-associated patterns and false positives may cause anxiety. Different scanner protocols, populations, missing clinical fields, comorbidities and evolving diagnostic criteria can shift performance. Even a calibrated model on one cohort may be miscalibrated elsewhere. Explanations are model-attribution tools, not proof of pathology or causality.

Every result screen and export must show the prototype label, model version, supported input domain, QC status, class probabilities, and the phrase “not a medical diagnosis.” Out-of-scope or failed-QC inputs should abstain. The model must never generate treatment advice. Only aggregate research metrics may be presented as evidence, with cohort/split details and limitations; per-patient claims require separate clinical governance.
