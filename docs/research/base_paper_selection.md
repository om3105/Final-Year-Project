# Base paper selection

**Decision reviewed 2026-09-30:** `[2]` OmniBrain is the closest *architectural and methodological starting point* for the proposed Alzheimer MRI plus clinical-data system. This is a similarity decision, not a performance ranking or novelty claim. The selection remains conditional on the usable dataset and compute feasibility described in the pre-development review.

| Dimension | [1] TriFusion-ADFormer | [2] OmniBrain | [3] MAMDF | [4] AD-Transformer |
|---|---|---|---|---|
| Disease / task | AD/MCI/CN classification | AD/MCI/control classification | AD and MCI subtype classification | AD classification and MCI conversion |
| Image input | Structural MRI | Grey-matter MRI | Medical imaging; precise image sequence needs full-text check | Structural MRI |
| Independent clinical inputs | Cognitive scores; text is **derived from MRI volumes** | Clinical/tabular metadata; also radiomics and gene expression | Clinical data | Clinical and genetic data |
| Image encoder | Swin Transformer V2 | Pretrained AnatCL or y-Aware MRI encoder | Frequency-domain/Transformer features per abstract | Patch-CNN |
| Clinical encoder | MLP for scores; BERT for MRI-derived text | FT-Transformer | Not verified from publisher abstract | Linear projection |
| Fusion | Concatenation and feed-forward layers | Cross-attention and modality masking | Asymmetric cross-attention plus Transformer feature module | Unified Transformer tokens |
| Explanations | Correlations and representative MRI volume analysis; no verified SHAP/Grad-CAM branch | Grad-CAM and SHAP | Not verified from abstract | Not verified from abstract |
| Validation | ADNI subject-level three-fold CV; no external site | ANMerge plus MRI-only external ADNI test | ADNI per abstract | ADNI, 1,651 subjects per publisher abstract |
| Dataset methodology similarity | Single paired ADNI cohort, slices grouped in CV | Paired ANMerge development cohort; explicit missing-modality and external MRI-only test | ADNI; participant split not verified from abstract | ADNI; split details not verified from abstract |
| Deployment relevance | GPU resource table; no deployed service | Missing-modality handling; no verified deployed service | Not reported in abstract | Not reported in abstract |

### Additional full-text candidates

| Dimension | [27] NeuroNet-AD | [22] TriLightNet | [9] Ovarian ultrasound/report fusion |
|---|---|---|---|
| Disease and modalities | ADNI MRI slices plus textual metadata, NC/MCI/AD | ADNI MRI, PET and clinical table, MCI conversion | Ovarian ultrasound plus clinical text report |
| Encoders | ResNet-18/CBAM and BERT | ResNet image branches and clinical feature branch | DenseNet-121 plus Swin; Bio-ClinicalBERT |
| Fusion | Meta-guided cross-attention | Hierarchical/bidirectional triple-modal attention | Concatenation chosen after attention ablation |
| Explanation | No dual MRI-heatmap plus clinical-SHAP pair verified in reviewed sections | Integrated Gradients | Attribution methods discussed, no AD task |
| Validation | 200 ADNI1 subjects grouped for CV/test; 921 external OASIS-3 **images** reported | Complete-modality ADNI-1/2 cohort | Subject-level development split and external three-center cohort |
| Main difference from intended project | BERT encoding of metadata, no FT-Transformer or SHAP branch; cognitive fields include possible label proxies | PET required; no clinical Transformer | Different disease and a report that describes the image |

Evidence: [NeuroNet-AD Sections 3.2, 4.1, 5.2–5.3](https://doi.org/10.3390/bioengineering12101107); [TriLightNet Sections 3.1–3.2, 4.2, 4.4.2](https://doi.org/10.3389/fnins.2025.1637291); [ovarian study Sections “Multimodal architecture” and “Comparison of multiple fusion strategies”](https://doi.org/10.1093/bib/bbag224). The ovarian study's attention variants performed worse than its concatenation model on that dataset, strengthening the requirement to ablate rather than assume attention benefits.

The comparison uses **modality, medical-image, clinical-data, disease task, image encoder, clinical encoder, Transformer, fusion/cross-attention, explainability, dataset validation and deployment** as separate dimensions. An unreported dimension is not scored as support. The closest choice is based on the number and importance of *documented architectural overlaps*, with independent clinical data and cross-attention prioritized for this project's central question. It is not a composite performance score or a “best paper” ranking.

The project's proposed medical image, independent structured clinical observations, clinical Transformer, cross-modal interaction, and both image and clinical explanations overlap most dimensions of OmniBrain `[2]`. Its published model uses FT-Transformer for mixed tabular features, cross-attention, modality dropout, Grad-CAM, and SHAP. NeuroNet-AD `[27]` matches the MRI plus cross-attention task more closely on disease alone but uses a BERT metadata encoder and does not establish the dual explanation design. Its metadata include MMSE/CDR/FAQ, so those inputs need particular attention to label dependence. OmniBrain's external MRI-only ADNI result is substantially lower than its ANMerge result (authors report 70.4 ± 2.7% versus 92.2 ± 2.4% accuracy), which argues for explicit generalization testing rather than assuming portability. [Official ICCV paper](https://openaccess.thecvf.com/content/ICCV2025W/CVAMD/html/Sharshar_Not_Only_Grey_Matter_OmniBrain_for_Robust_Multimodal_Classification_of_ICCVW_2025_paper.html).

TriFusion `[1]` is the closest **Swin MRI encoder** reference. It uses MRI, MRI-derived clinical text, and independent cognitive scores; Swin V2, BERT, and an MLP encode these branches. The paper explicitly uses concatenation followed by feed-forward layers, not the proposed cross-attention and multimodal Transformer. Its clinical text is generated from MRI volumetric measurements, so it cannot demonstrate the value of independently observed clinical notes. The authors report 86.0% accuracy, 0.93 macro AUROC and 0.86 F1 on ADNI and note no external validation. [Publisher methods and discussion](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1849315/full).

MAMDF `[3]` is a close cross-attention comparator because its publisher abstract explicitly describes clinical information, medical imaging, asymmetric cross-attention, and a Transformer feature module. We have not verified its full PDF or precise image/clinical encoders, which weakens it as a reproducible foundation. [Journal abstract](https://xbna.pku.edu.cn/CN/Y2025/V61/I4/629).

AD-Transformer `[4]` offers a joint-token Transformer design for MRI plus clinical and genetic data. Its patch-CNN image tokenizer and linear non-image projection differ from the proposed Swin plus clinical Transformer; a lawful open full text was not verified. [Publisher abstract](https://doi.org/10.1016/j.compbiomed.2024.108979).

**What changes from [2]:** begin with a paired MRI plus pre-specified non-image clinical cohort; compare the published-style image/tabular cross-attention against concatenation. A Swin encoder and a post-fusion Transformer are *experimental variants* only. Genetics and radiomics are optional ablations if access and independent clinical meaning permit. Avoid treating radiomics derived from the same MRI as independent clinical evidence.

**What is added as an implementation contribution:** reproducible patient-level splits, leakage audit, modality ablations, calibration, explicit abstention on unsupported inputs, a research-only web interface, and resource measurements. These are plans, not completed or proven novel contributions. Remaining limits include access to a suitable paired cohort, privacy terms for cloud training, model memory, small-cohort overfitting, and no prospective clinical validation.
