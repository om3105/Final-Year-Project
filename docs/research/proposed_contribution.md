# Proposed contribution and claim boundaries

**Existing literature:** MRI plus clinical fusion, clinical/tabular Transformers, cross-attention, modality masking, Grad-CAM, and SHAP already appear together in OmniBrain `[2]`. Swin-based MRI encoding and multimodal concatenation appear in TriFusion `[1]`. Unified token Transformers appear in AD-Transformer `[4]`.

**Base paper:** OmniBrain `[2]` provides the closest architecture and validation comparator. It includes more modalities than the planned two-input prototype and uses pretrained MRI encoders rather than a Swin encoder.

**Our proposed project:** an architecture synthesis and reproducible implementation for paired brain MRI plus independent clinical variables in one Alzheimer/MCI task. Run image-only, tabular-only, concatenation, cross-attention, and optional post-fusion Transformer variants under one patient-level protocol. Add source-aware feature auditing, calibration, explanation stability checks, resource profiling, and a research-only web demonstration.

No claim of new attention mathematics or clinical diagnostic utility is made. A novel outcome would require measured improvement with adequate uncertainty estimates and external validation. The working research question is whether cross-modal attention provides useful discrimination and calibration over a simpler fusion model at acceptable complexity on a legally usable paired cohort.
