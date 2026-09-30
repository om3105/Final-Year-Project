# Glossary

| Term | Plain-language meaning |
|---|---|
| MRI / CT / PET | MRI uses magnetic fields to image tissue; CT uses X-rays; PET images tracer activity. This project targets structural brain MRI. |
| Transformer | A neural network that relates input pieces through attention. |
| Swin Transformer | A vision Transformer that attends within shifted image windows at several scales. |
| Clinical Transformer / FT-Transformer | A Transformer that treats structured clinical fields as tokens and learns interactions among them. |
| Token / embedding | A token is one input piece; an embedding is its numeric representation. |
| Cross-attention | One modality asks which features of another modality matter for its current representation. |
| Multimodal learning / feature fusion | Learning from more than one data type, such as MRI and clinical measurements; fusion combines their representations. |
| SHAP | A method estimating each input feature's contribution relative to a chosen background; not a causal explanation. |
| Grad-CAM / heatmap | A gradient-based rough image localization displayed as a colored overlay; not proof of pathology. |
| AUROC / AUPRC | Areas under ranking and precision–recall curves; AUPRC is especially informative for rare positive classes. |
| F1 / sensitivity / specificity | F1 balances precision and recall; sensitivity finds true positives; specificity excludes true negatives. |
| Calibration | Whether predictions near a stated probability occur at about that rate in the evaluated population. |
| Inference | Applying a trained model to new inputs. |
| Fine-tuning / transfer learning | Adapting a model trained on another task to this task. |
| Data leakage | Information unavailable at prediction time or from held-out subjects entering training. |
| Patient-level split | Every scan and visit from one person stays in a single train/validation/test partition. |
| External validation | Testing on a truly independent cohort, site or time period after model choices are fixed. |
| Abstention | The system declines to give a class prediction when its input or model support is inadequate. |
