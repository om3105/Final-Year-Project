"""Apply manually checked full-text findings to the research catalog and notes.

Findings below are paraphrases checked against the named JATS sections or PDFs.
This script deliberately preserves unknown fields rather than guessing them.
"""

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "research/papers"

# Each record states only findings supported by the source locations recorded here.
# "caution" is our interpretation unless explicitly attributed to the authors.
FINDINGS = {
    "P005": {
        "methods": "Two separate pathways: 1D CNN plus random forest for structured clinical records, and ImageNet-pretrained VGG19 for 2D MRI images. They are trained on different Kaggle datasets, so this is not paired image–clinical fusion.",
        "evaluation": "The paper reports 2,000 clinical records and about 40,000 MRI images, separate 70/30 random splits, and 90.2% clinical-pathway versus 92.2% image-pathway test accuracy. Patient grouping for the image split is not established in the stated split description.",
        "caution": "Interpretation: a useful unimodal baseline pair, but the two accuracies cannot establish the benefit of multimodal fusion. Check the provenance and patient identities of the augmented MRI dataset before reuse.",
        "sections": "Dataset (Sec7); Network training (Sec8–Sec10); Results (Sec11–Sec13); Conclusion (Sec17).",
        "fields": {"medical_modality":"2D brain MRI", "clinical_data":"Separate structured clinical Kaggle records", "image_encoder":"VGG19 transfer learning", "clinical_encoder":"1D CNN plus random forest", "fusion_method":"No paired fusion; independent pathways", "dataset":"Separate Kaggle clinical and augmented MRI sets; ADNI/OASIS checks reported", "sample_size":"~2,000 clinical records; ~40,000 MRI images", "main_result":"Authors report 90.2% clinical and 92.2% MRI test accuracy on separate Kaggle splits", "limitations":"Unpaired modalities; random image split grouping unclear; class imbalance"}},
    "P006": {
        "methods": "Systematic review of multimodal Alzheimer AI; organizes datasets and early, intermediate, late and attention/graph fusion rather than introducing one model.",
        "evaluation": "The review compares published dataset, modality and reporting practices; no new patient-level model was trained by this article.",
        "caution": "Interpretation: use its taxonomy and methodological warnings, not its cross-study performance numbers as a common benchmark.",
        "sections": "Multimodal Dataset Overview (s3-5-1); ADNI Dataset (s3-5-4); Fusion Taxonomy (s3-8); Dataset-Specific Limitations (s4-8).",
        "fields": {"domain":"Systematic review: multimodal Alzheimer AI", "fusion_method":"Review of early, intermediate, late, attention/graph fusion", "dataset":"Multiple published cohorts, including ADNI", "limitations":"Heterogeneous cohorts, modality availability and reporting across reviewed studies"}},
    "P007": {
        "methods": "DeepAttentionADNet uses CNN features followed by a Transformer for MRI-only, ordinal Alzheimer severity staging, with consistency regularization and attention visualization.",
        "evaluation": "Authors report cross-validation mean F1 0.991 ± 0.003 and AUROC 0.9998 ± 0.0002 on an Alzheimer multiclass MRI image dataset. The source describes images; scan/patient grouping must be established before treating these as independent patient results.",
        "caution": "Interpretation: an image-only architecture comparator. The very high image-level scores should not set expected performance for a patient-level ADNI task.",
        "sections": "Dataset Description (3.1); Results (4); Discussion (5).",
        "fields": {"medical_modality":"MRI images", "clinical_data":"None reported", "image_encoder":"CNN–Transformer hybrid", "fusion_method":"Image-only", "explainability":"Attention visualization", "main_result":"Authors report mean cross-validation F1 0.991 and AUROC 0.9998", "limitations":"Patient-level grouping for the image collection not established in reviewed sections"}},
    "P008": {
        "methods": "ViTTL combines a Vision Transformer with pretrained CNN features from 2D MRI slices; the article examines DenseNet201 and other backbones and visualizes decisions with LIME and Grad-CAM.",
        "evaluation": "The paper uses OASIS cross-sectional T1 MRI from 416 people and reports 99.89% classification accuracy for a ViT–DenseNet201–ANN variant. The authors themselves identify sparse moderate-dementia cases as a limitation.",
        "caution": "Interpretation: extracted slice count and participant count must not be conflated. This is image-only severity classification, not paired clinical fusion.",
        "sections": "Overall architecture (Sec3); Dataset (Sec7); Dataset pre-processing (Sec8); Results (Sec12); Limitations (Sec17).",
        "fields": {"medical_modality":"OASIS T1 MRI, 2D slices", "clinical_data":"None in model", "image_encoder":"ViT plus pretrained CNN; best reported DenseNet201 variant", "fusion_method":"Fusion of two image encoders", "explainability":"LIME; Grad-CAM", "dataset":"OASIS cross-sectional", "sample_size":"416 participants in source cohort", "main_result":"Authors report 99.89% accuracy for ViT–DenseNet201–ANN", "limitations":"Small moderate-dementia class; clinical data absent"}},
    "P009": {
        "methods": "Ovarian tumor study uses ultrasound DenseNet-121 and Swin image branches plus Bio-ClinicalBERT report embeddings. Its selected fusion is concatenation through an MLP, after testing cross-attention and bidirectional attention.",
        "evaluation": "1,342 ultrasound images came from 1,062 patients; the paper explicitly uses subject-level splitting. Its fusion ablation found the attention alternatives worse on this cohort, which the authors attribute to extra capacity/overfitting.",
        "caution": "Interpretation: this is direct evidence to test rather than assume attention superiority. Clinical reports describe the ultrasound and may not be independent observations; the disease and image modality differ from ours.",
        "sections": "Subject-level data splitting (sec8); Multimodal architecture (sec11); Fusion strategy comparison (sec19); Limitations (sec25).",
        "fields": {"disease":"Ovarian tumor classification", "medical_modality":"2D ultrasound", "clinical_data":"Ultrasound clinical text reports; age", "image_encoder":"DenseNet-121 plus Swin Transformer", "clinical_encoder":"Bio-ClinicalBERT plus MLP", "fusion_method":"Concatenation plus MLP selected; attention variants ablated", "cross_attention":"Tested in ablation; not selected architecture", "dataset":"National Taiwan University Hospital; external three-center cohort", "sample_size":"1,342 images from 1,062 patients in development cohort", "limitations":"Single-system development; text reporting variation; limited independent clinical variables"}},
    "P010": {
        "methods": "Separate 3D CNNs encode structural MRI and FDG-PET; an improved Transformer models their representations before fusion and classification. It is image–image fusion, not clinical-tabular fusion.",
        "evaluation": "ADNI experiment comprises 210 subjects (88 AD, 122 cognitively normal). Authors report 98.10% mean accuracy and 98.35% AUC for AD/CN discrimination with tenfold cross-validation and region visualizations.",
        "caution": "Interpretation: the small binary cohort and different second modality make its headline performance non-transferable to MCI/clinical fusion.",
        "sections": "Performance (Sec3); Visualization (Sec4); Network model framework (Sec14); Data and preprocessing (Sec18); Experiment settings (Sec19).",
        "fields": {"medical_modality":"Structural MRI plus FDG-PET", "clinical_data":"None used as fusion modality", "image_encoder":"Separate 3D CNNs", "fusion_method":"Transformer-mediated image–image feature fusion", "dataset":"ADNI", "sample_size":"210 subjects: 88 AD and 122 CN", "evaluation_metrics":"Accuracy, precision, sensitivity, specificity, F1, AUC", "main_result":"Authors report 98.10% accuracy and 98.35% AUC", "limitations":"Small AD/CN cohort; no clinical-tabular input"}},
    "P011": {
        "methods": "MedFusionNet combines CNN/DenseNet features, self-attention/Transformer components and feature pyramid components for multilabel risk stratification, extending to image, text and clinical inputs.",
        "evaluation": "The article evaluates NIH ChestX-ray14 and a constructed cervical-cancer dataset; the latter's text/clinical inputs need provenance checking before treating it as a paired independent clinical benchmark.",
        "caution": "Interpretation: architecture comparator for multilabel fusion; not an Alzheimer cohort or direct evidence that its components improve MCI prediction.",
        "sections": "Hybrid architecture (Sec10, Sec18); Dataset utilization (Sec23); Experimental results (Sec25); Discussion (Sec29).",
        "fields": {"disease":"Chest disease and cervical cancer risk stratification", "medical_modality":"Chest X-ray and cervical imaging", "clinical_data":"Text and clinical inputs in multimodal extension", "image_encoder":"DenseNet/CNN and Transformer components", "fusion_method":"Parallel multimodal feature fusion", "dataset":"NIH ChestX-ray14 and constructed cervical dataset", "limitations":"Task and cohort differ from AD/MCI; input provenance requires audit"}},
    "P012": {
        "methods": "AFCG-Net aligns MRI features to clinical-description text through anatomy-aware visual encoding, cross-modal semantic alignment and gated fusion; this is MRI–text rather than structured clinical table fusion.",
        "evaluation": "The paper reports 2,106 self-collected and 2,091 ADNI samples with precision 96.3%, recall 96.5%, F-score 95.8%. The dataset section says the hospital supplied only ten de-identified clinical text samples, with additional text drawn from public platforms; exact image–text pairing and text independence need scrutiny.",
        "caution": "Interpretation: useful cross-modal architecture comparator, but text construction and unit of analysis limit direct use as evidence for independent clinical observations.",
        "sections": "Methods (s3); Dataset and preprocessing (under Methods); Comparison with state of the art (under Results).",
        "fields": {"medical_modality":"Brain MRI", "clinical_data":"Clinical description text; pairing/provenance requires scrutiny", "image_encoder":"Anatomy- and frequency-aware visual encoder", "clinical_encoder":"Clinical-text semantic representation", "fusion_method":"Cross-modal alignment and gated fusion", "dataset":"Self-constructed plus ADNI", "sample_size":"2,106 self-collected and 2,091 ADNI samples reported", "main_result":"Authors report precision 96.3%, recall 96.5%, F-score 95.8%", "limitations":"Only ten hospital text samples stated; text provenance and independence unclear"}},
    "P013": {
        "methods": "Radiomics from T1, DWI and T2 MRI in eight brain regions feeds logistic-regression and random-forest classifiers; SHAP explains selected features. This is engineered MRI-feature fusion, not a learned image encoder.",
        "evaluation": "110 participants (48 AD, 62 controls); 856 initial radiomic features reduced to 16 inside training-fold procedures. ROC, calibration and decision-curve analyses are reported.",
        "caution": "Authors acknowledge a small single-center retrospective cohort and absence of an MCI group; interpretation: its explainability and fold-contained feature selection are transferable practices, but diagnostic accuracy is not an early-MCI benchmark.",
        "sections": "Abstract; Radiomics feature selection (sec14); Overfitting/generalizability (sec23); Absence of MCI (sec26); Study limitations (sec27).",
        "fields": {"medical_modality":"T1, DWI and T2 MRI radiomics", "clinical_data":"Homocysteine and triglycerides in nomogram", "image_encoder":"Hand-engineered radiomics", "clinical_encoder":"Logistic regression/random forest", "fusion_method":"Selected radiomic and clinical factors in nomogram", "explainability":"SHAP; nomogram", "sample_size":"110 subjects: 48 AD, 62 controls", "evaluation_metrics":"ROC/AUC, calibration, decision-curve analysis", "limitations":"Small single-center retrospective sample; no MCI group"}},
    "P014": {
        "methods": "Review of MRI-centered AD deep learning, including CNN, Transformer and multimodal extensions; not a new trained model.",
        "evaluation": "Authors describe a PRISMA search across six databases through June 2025 and 70 included peer-reviewed studies; their narrative/results contain an inconsistent smaller denominator in one dataset summary, so counts should be attributed precisely.",
        "caution": "Interpretation: supports external validation and harmonization planning, not an accuracy target for this project.",
        "sections": "Research methodology (Sec8); Datasets/pre-processing (Sec11); Challenges (Sec13); Limitations (Sec18).",
        "fields": {"domain":"Review: MRI-based Alzheimer AI", "dataset":"70 included studies claimed in abstract", "fusion_method":"Review of multimodal extensions", "limitations":"Heterogeneous reporting and external generalization in included studies"}},
    "P015": {
        "methods": "Review of multimodal neuroimaging, clinical data, fusion timing and explainability across cognitive disorders; no new patient classifier.",
        "evaluation": "Synthesizes published studies and research directions, including missing-modality handling; cross-study numbers are not a common held-out test.",
        "caution": "Interpretation: use for research framing only; primary experimental papers carry stronger evidence for model choices.",
        "sections": "Multimodal fusion strategies (sec2-2); early biomarker discovery (sec5-1); article abstract.",
        "fields": {"domain":"Review: multimodal cognitive-disorder AI", "clinical_data":"Reviewed clinical and cognitive inputs", "fusion_method":"Reviews early, intermediate and late fusion", "limitations":"Narrative synthesis, not a directly comparable experiment"}},
    "P016": {
        "methods": "Community MCI identification with elastic-net models combining demographics, cognitive scores and structural/perfusion/diffusion MRI-derived biomarkers; no raw MRI deep encoder.",
        "evaluation": "148 community-dwelling older adults; paper reports test AUC 0.81 for multisource model and examines calibration. MCI reference is based on Memory Performance Index, so cognitive predictors need timing/label-dependence review.",
        "caution": "Interpretation: valuable clinical baseline and a warning that label-defining cognitive scores can create target leakage if used as predictors.",
        "sections": "Abstract; Model development (S3.SS2); Test performance (S3.SS3); Strengths and limitations (S4.SS6).",
        "fields": {"medical_modality":"MRI-derived structural, perfusion and diffusion biomarkers", "clinical_data":"Demographics and cognitive test scores", "image_encoder":"Derived MRI measurements, no raw-image encoder", "clinical_encoder":"Elastic net", "fusion_method":"Feature-level multisource regression", "sample_size":"148 people", "evaluation_metrics":"AUROC; calibration", "main_result":"Authors report AUC 0.81", "limitations":"Limited single-community sample; potential dependence between cognitive predictor and MCI definition"}},
    "P017": {
        "methods": "Forecasts two-year change in CDR sum-of-boxes with a hybrid 3D MRI CNN plus clinical variables and an AutoGluon image/tabular baseline; outcome is continuous regression, not diagnosis classification.",
        "evaluation": "ADNI, OASIS and another independent cohort are discussed; ADNI alone has 1,136 participants in the source. Five-fold cross-validation and mean absolute error are used. The 3D CNN uses batch size two due to GPU memory.",
        "caution": "Authors note clinical covariates can explain much variance. Interpretation: include a strong clinical-only baseline and costed 3D encoder, with longitudinal time ordering.",
        "sections": "Materials and methods (sec2); Results (sec3); Discussion (sec4); Limitations (sec5).",
        "fields": {"medical_modality":"3D T1 MRI and 2D MRI slices in alternative model", "clinical_data":"Demographic/clinical covariates", "image_encoder":"3D CNN; AutoGluon multimodal alternative", "fusion_method":"Hybrid CNN plus tabular fusion", "dataset":"ADNI and independent cohorts", "sample_size":"ADNI 1,136 participants; other cohorts also studied", "evaluation_metrics":"Mean absolute error; cross-validation", "limitations":"3D GPU memory limits; covariate-dominant task"}},
    "P018": {
        "methods": "Review of machine-learning and deep-learning Alzheimer classification using neuroimaging, including CNNs, Transformers and generative models; no new patient classifier is trained.",
        "evaluation": "The paper compares published data sources, preprocessing, models and evaluation issues rather than reporting one common held-out experiment.",
        "caution": "Interpretation: supports careful cohort and validation design; model-performance claims within the review remain claims of the cited primary studies.",
        "sections": "Local PDF P018, pp. 1–3 (abstract and review methods); Sections 3–9 (datasets, methods, limitations).",
        "fields": {"domain":"Review: Alzheimer neuroimaging AI", "medical_modality":"MRI/PET and other neuroimaging in reviewed studies", "clinical_data":"Clinical assessments in reviewed literature", "fusion_method":"Review of multimodal approaches", "limitations":"Secondary synthesis rather than direct paired-clinical experiment"}},
    "P019": {
        "methods": "Dementia-risk modeling joins derived MRI measures with brief cognitive assessments, comparing single-visit and repeated-visit models; SHAP is used for feature interpretation.",
        "evaluation": "312 older adults from a KU Alzheimer center; the paper reports cross-sectional and longitudinal analyses. It notes enrichment for memory-concerned participants as a generalizability limitation.",
        "caution": "Interpretation: useful for testing added value of MRI over cognitive baselines; review visit dates and prevent repeated-person leakage.",
        "sections": "Article abstract; Discussion (sec0026); Strengths and limitations (sec0030).",
        "fields": {"medical_modality":"MRI-derived hippocampal/gray-matter measures", "clinical_data":"Brief cognitive assessments and demographics", "image_encoder":"Derived MRI biomarkers", "fusion_method":"Statistical integration of MRI and clinical measures", "explainability":"SHAP", "dataset":"KU Alzheimer Disease Center cohort", "sample_size":"312 older adults", "limitations":"Memory-concerned cohort enrichment; independent-site validation needed"}},
    "P020": {
        "methods": "ADNI study fuses structural/functional MRI features and genetic SNPs; a cycle-GAN in latent space imputes missing views before classification and attribution.",
        "evaluation": "Evaluates AD versus control and converting versus stable MCI tasks, explicitly including missing-modality scenarios. This is imaging–genomics rather than independent clinical table fusion.",
        "caution": "Interpretation: missing-view handling and conversion labels are useful comparators; do not treat generated data as independent measurements.",
        "sections": "Dataset (jneae087ds2-1); Framework (jneae087ds2-3); Fusion (jneae087ds2-3-3); Limitations (jneae087ds5-3-1).",
        "fields": {"medical_modality":"Multimodal MRI", "clinical_data":"Genetic SNPs, not routine clinical table", "fusion_method":"Latent feature fusion with cycle-GAN missing-view imputation", "dataset":"ADNI", "limitations":"ADNI-specific generalization; imputed views differ from observed data"}},
    "P021": {
        "methods": "NACC neuropathology prediction combines volumetric MRI and clinical/genetic covariates in a 3D CNN plus ANN, and compares ViT variants; explanations include occlusion, Grad-CAM and Integrated Gradients.",
        "evaluation": "Primary NACC cohort has 950 people with imaging and autopsy-linked labels. Reports covariate-only, image-only and multimodal comparisons over multiple pathology targets.",
        "caution": "Interpretation: valuable modality ablation and explanation design; autopsy-associated neuropathology labels differ from prospective MCI detection, and selection of autopsied cases limits generalizability.",
        "sections": "Imaging data (sec2); Hybrid CNN (sec15); Transformer architecture (sec16); Results (sec17); Limitations (sec22).",
        "fields": {"medical_modality":"Volumetric T1 MRI", "clinical_data":"Clinical and genetic covariates", "image_encoder":"3D CNN; ViT comparators", "clinical_encoder":"Parallel ANN", "fusion_method":"Hybrid CNN/ANN representation fusion", "explainability":"Occlusion, Grad-CAM, Integrated Gradients", "dataset":"NACC", "sample_size":"950 people", "limitations":"Autopsy-linked cohort selection; one main source cohort"}},
    "P022": {
        "methods": "TriLightNet joins structural MRI, PET and tabular clinical features. ResNet extracts imaging features; hierarchical/bidirectional attention modules fuse modalities; Integrated Gradients provides attributions.",
        "evaluation": "Uses complete-modality ADNI-1/2 subjects for progressive-versus-stable MCI; authors report accuracy 81.25%, AUROC 0.8146 and F1 69.39% in comparison experiments.",
        "caution": "Interpretation: closest disease/outcome comparator for three modalities, but complete-case selection can reduce representativeness and PET is outside our primary two-modality design.",
        "sections": "Materials (sec11); Methodology (sec12); Comparisons (sec21); Interpretability (sec25); Discussion (s5).",
        "fields": {"medical_modality":"Structural MRI plus PET", "clinical_data":"Clinical tabular features", "image_encoder":"ResNet imaging branches", "fusion_method":"Hierarchical/bidirectional attention triple-modal fusion", "explainability":"Integrated Gradients", "dataset":"ADNI-1/ADNI-2", "evaluation_metrics":"Accuracy, AUROC, F1, sensitivity", "main_result":"Authors report 81.25% accuracy and AUROC 0.8146", "limitations":"Complete-case multimodal selection; PET requirement"}},
    "P023": {
        "methods": "ADNI dementia/MCI/control image study compares CNNs, ViT, 3D CNN, capsule network and a multimodal-attention variant; source workflow extracts coronal slices from volumes.",
        "evaluation": "Uses a 70/validation/test training procedure and reports classwise metrics; the model comparison is within one dataset, with no clearly established independent external cohort in reviewed sections.",
        "caution": "Interpretation: an architecture comparison, not proof of general multimodal clinical benefit; verify grouping of all slices by subject before relying on its numbers.",
        "sections": "Methodology (sec3); Workflow (sec7); Training/validation/testing (sec9); Model limitations (sec14).",
        "fields": {"medical_modality":"ADNI structural MRI/coronal slices", "clinical_data":"Not clearly a paired independent clinical input", "image_encoder":"CNN, ViT, 3D CNN and capsule comparators", "fusion_method":"Multimodal attention variant among model comparisons", "dataset":"ADNI", "limitations":"Patient grouping and external generalization need independent verification"}},
    "P024": {
        "methods": "Unsupervised similarity-network fusion combines patient-level cognitive, imaging and other measurements for Alzheimer/MCI heterogeneity and subtype clustering, not a supervised neural classifier.",
        "evaluation": "972 subjects (370 cognitively normal, 565 MCI, 37 AD) form similarity networks; spectral clustering and progression trajectories characterize groups.",
        "caution": "Interpretation: useful for heterogeneity framing but SNF subtype clusters do not supply the proposed image-token cross-attention architecture.",
        "sections": "Article abstract; SNF-based method (Sec12); Trajectory validation (Sec18); Discussion (Sec19).",
        "fields": {"medical_modality":"MRI-derived measurements", "clinical_data":"Cognitive and other patient measurements", "fusion_method":"Similarity network fusion and spectral clustering", "sample_size":"972 subjects: 370 CN, 565 MCI, 37 AD", "limitations":"Small AD subgroup; unsupervised subtype labels not direct diagnosis test"}},
    "P025": {
        "methods": "Narrative review of MRI modalities and AI for MCI-to-AD conversion; it does not train a new model.",
        "evaluation": "Synthesizes structural, functional and perfusion MRI studies and their prediction methods; published scores are not one common cohort experiment.",
        "caution": "Interpretation: supports defining a longitudinal conversion outcome but not expecting a fixed improvement from any architecture.",
        "sections": "Article abstract; review discussion of deep learning/machine learning (sec5).",
        "fields": {"domain":"Review: MCI-to-AD prediction", "medical_modality":"Structural, functional and perfusion MRI in reviewed studies", "fusion_method":"Review of multimodal MRI approaches", "limitations":"Review rather than a new paired image–clinical experiment"}},
    "P026": {
        "methods": "Systematically compares MRI-derived morphometric, microstructural and graph features alone and in combinations, using conventional ML with nested cross-validation.",
        "evaluation": "ADNI diagnosis/staging and cognitive-decline tasks; authors conclude morphometry was most robust and adding MRI feature families gave limited task-dependent benefit.",
        "caution": "Interpretation: more modalities/features should be justified by an ablation, not assumed to help.",
        "sections": "Materials and methods (s3); Base learners and nested CV (sec15); Experimental setup (sec19); Limitations (sec27).",
        "fields": {"medical_modality":"MRI-derived morphometry, diffusion microstructure and graph features", "clinical_data":"Cognitive outcome/variables, not primary raw clinical branch", "image_encoder":"Engineered MRI features with conventional ML", "fusion_method":"Concatenated MRI feature-family combinations", "dataset":"ADNI", "evaluation_metrics":"Nested cross-validation", "limitations":"Single primary cohort; feature value varies by task"}},
    "P027": {
        "methods": "NeuroNet-AD combines ResNet-18/CBAM slice features, BERT-encoded textual metadata and meta-guided cross-attention for NC/MCI/AD classification.",
        "evaluation": "ADNI1 data are stated as 200 subjects with ten slices each; authors describe subject-level five-fold CV on 80% and a held-out 20%, plus OASIS-3 external evaluation. They report 98.68% held-out accuracy and 94.10% external multiclass accuracy.",
        "caution": "Interpretation: very relevant cross-attention comparator. The paper also lists MMSE/CDR/FAQ among metadata, raising prediction-time/label-proxy concerns. Reported OASIS external count is 921 images, not 921 people; patient aggregation must be checked.",
        "sections": "Method overview (3.2); Dataset (4.1); CV/held-out test (5.2); External validation (5.3).",
        "fields": {"medical_modality":"3D MRI sampled to ten 2D slices/subject", "clinical_data":"Metadata including age, APOE, MMSE, CDR and FAQ", "image_encoder":"ResNet-18 plus CBAM", "clinical_encoder":"BERT text encoder for metadata", "fusion_method":"Meta-guided cross-attention", "cross_attention":"YES", "dataset":"ADNI1; OASIS-3 external", "sample_size":"200 ADNI1 subjects; 2,000 slices; 921 OASIS-3 external images", "main_result":"Authors report 98.68% held-out and 94.10% external multiclass accuracy", "limitations":"Cognitive label proxies; image-vs-patient result denominator needs checking"}},
    "P028": {
        "methods": "YOLOv11 detection/classification using MRI and DTI image fusion for four Alzheimer/MCI classes; no separate structured-clinical branch.",
        "evaluation": "ADNI-derived imaging; authors report precision 93.6%, recall 91.6% and mAP50 96.7%. Methods discuss MRI/DTI fusion and article reports Colab Pro training.",
        "caution": "Interpretation: image–image fusion and detection metrics cannot be compared directly with patient-level disease-classification AUROC. Paid Colab Pro is incompatible with the ₹0 plan.",
        "sections": "Fusion (sec4); Dataset collection (sec5); YOLOv11 architecture (sec6); Results (sec15).",
        "fields": {"medical_modality":"MRI plus DTI", "clinical_data":"None as separate model branch", "image_encoder":"YOLOv11", "fusion_method":"Image–image fusion", "dataset":"ADNI-derived imaging", "evaluation_metrics":"Precision, recall, mAP50", "main_result":"Authors report 93.6% precision, 91.6% recall, 96.7% mAP50", "limitations":"Different detection task; Colab Pro used"}},
    "P029": {
        "methods": "Ensemble Integration combines heterogeneous TADPOLE baseline data from MCI participants to forecast later dementia, compared with XGBoost and an autoencoder approach.",
        "evaluation": "841 MCI patients total; 672 baseline patients in five-fold nested CV development and a held-out test set. Authors report test AUC 0.81 and F-measure 0.68 versus XGBoost AUC 0.68/F 0.57.",
        "caution": "Interpretation: strong longitudinal label/split example using derived imaging measurements rather than a raw-image encoder; conversion follow-up and baseline timing should guide our outcome definition.",
        "sections": "Materials and methods (sec2); Evaluation (sec2.5); Cohort (sec3.1); Performance (sec3.3); Discussion (sec4).",
        "fields": {"medical_modality":"MRI-derived regional volumes among multimodal variables", "clinical_data":"TADPOLE baseline clinical/cognitive data", "image_encoder":"Derived MRI measurements", "fusion_method":"Ensemble Integration of heterogeneous features", "dataset":"ADNI-derived TADPOLE", "sample_size":"841 baseline MCI patients; 672 development", "evaluation_metrics":"AUC, F-measure", "main_result":"Authors report held-out AUC 0.81 and F-measure 0.68", "limitations":"Derived imaging, not raw MRI; follow-up outcome availability"}},
    "P030": {
        "methods": "Three-City longitudinal dementia-risk modeling adds single/repeated MRI atrophy and small-vessel markers to demographics, health, cognition and function using competing-risk methods.",
        "evaluation": "1,716 participants; reported five-year AUC increases from 0.80 to 0.83 after adding MRI, and repeated MRI adds little beyond one MRI once cognition is available.",
        "caution": "Interpretation: multimodality adds modest value in this population; compare against strong clinical baseline and use time-aware evaluation.",
        "sections": "Abstract; Three-City cohort (dad212578-sec-0050); Discussion (dad212578-sec-0160).",
        "fields": {"medical_modality":"MRI-derived atrophy and small-vessel markers", "clinical_data":"Demographics, health, cognition, function", "image_encoder":"Derived MRI biomarkers", "fusion_method":"Longitudinal competing-risk integration", "dataset":"French Three-City Study", "sample_size":"1,716 participants", "evaluation_metrics":"Five-year AUROC and confidence intervals", "main_result":"Authors report AUC 0.80 to 0.83 with MRI markers", "limitations":"Added value of repeat MRI was small after cognition"}},
    "P031": {
        "methods": "Review of histopathology with genomic and clinical data for breast cancer, covering early/intermediate/late fusion and XAI methods such as Grad-CAM, SHAP, LIME and attention.",
        "evaluation": "This review surveys published methods; it does not provide one newly trained image–clinical model or common held-out cohort.",
        "caution": "Interpretation: explanation methods can be considered, but pathologist utility and fidelity must be checked rather than assumed from saliency pictures.",
        "sections": "Datasets (s3); Explainability perspective (section 5.1); abstract.",
        "fields": {"domain":"Review: multimodal breast-cancer XAI", "medical_modality":"Histopathology and radiology in reviewed studies", "clinical_data":"Clinical records and genomics in reviewed studies", "fusion_method":"Review of early/intermediate/late fusion", "explainability":"Review of Grad-CAM, SHAP, LIME and attention", "limitations":"Review rather than an AD or prospective utility experiment"}},
    "P032": {
        "methods": "Registered systematic methodological review of 2025 neuroimaging AI studies, examining validation, leakage, calibration, human comparators and reporting.",
        "evaluation": "Among 91 included studies, authors report external validation in 75.8%, calibration in 30.8%, human comparison in 18.7%, and no full CLAIM/TRIPOD-AI compliance.",
        "caution": "Interpretation: supports our calibration, external test and reporting gates; reported low leakage risk depends on published descriptions rather than source-code verification.",
        "sections": "Methods (sec2); Validation/datasets (sec3dot4); Bias/transparency (sec3dot5); External validation (sec4dot2).",
        "fields": {"domain":"Systematic methodological review", "dataset":"91 published neuroimaging AI studies", "evaluation_metrics":"External validation, calibration, comparators, reporting and leakage indicators", "main_result":"Authors report 75.8% external validation and 30.8% calibration reporting", "limitations":"Quality assessment relies on study reporting"}},
    "P033": {
        "methods": "Parkinson clinical-data experiment compares models with and without overt diagnostic motor symptoms to demonstrate target/feature leakage effects.",
        "evaluation": "Structured dataset of 2,105 people; including motor symptoms substantially changes apparent test performance. The authors use held-out confusion matrices to show specificity failures when obvious features are removed.",
        "caution": "Interpretation: not imaging research, but directly motivates an availability/label-proxy audit of MMSE, CDR and other cognitive variables in our project.",
        "sections": "Dataset/preprocessing (sec2dot1); With/without features (sec2dot7); Confusion matrices (sec3dot3); Discussion (sec4).",
        "fields": {"disease":"Parkinson disease", "medical_modality":"None; structured clinical data", "clinical_data":"Motor and non-motor features", "fusion_method":"No multimodal image fusion", "dataset":"Public structured Parkinson dataset", "sample_size":"2,105 people", "limitations":"One dataset; symptom availability is task-dependent"}},
    "P034": {
        "methods": "Systematic review of radiomics guidelines covering reproducible extraction, internal/external validation and reporting standards; no new diagnostic model.",
        "evaluation": "Authors identify five major guidance frameworks or regulations for robust radiomics study design.",
        "caution": "Interpretation: translate its provenance/preprocessing/validation expectations to MRI pipelines even if final model uses learned image features.",
        "sections": "Dissemination (s3e); Clinical validation (s4b); Biological validation (s4c); abstract.",
        "fields": {"domain":"Review: radiomics reproducibility", "medical_modality":"Multiple imaging types in reviewed guidance", "dataset":"Guideline literature", "limitations":"Guideline synthesis, not a direct architecture comparison"}},
    "P035": {
        "methods": "MIMIC-IV prognostic study shows that diagnosis codes finalized after discharge can leak outcomes into same-admission prediction features.",
        "evaluation": "422,534 admissions from 180,640 unique patients; paper reports 40.2% of surveyed same-admission AI models used ICD codes and evaluates ICD-only predictive models.",
        "caution": "Interpretation: define every clinical feature by its actual availability time, not its presence in a retrospective record. Analogously, an AD severity score documented after diagnosis cannot be used as an early predictor.",
        "sections": "Study population (H2-1); Model development (H2-2); Results (H2-5); Discussion (H1-4); Limitations (H2-7).",
        "fields": {"disease":"Same-admission hospital outcomes", "medical_modality":"None; EHR diagnosis codes", "clinical_data":"ICD codes", "fusion_method":"No image fusion", "dataset":"MIMIC-IV 2.2", "sample_size":"180,640 patients; 422,534 admissions", "main_result":"40.2% of surveyed same-admission models used ICD codes, per authors", "limitations":"MIMIC-focused study; not direct AD evidence"}},
    "P036": {
        "methods": "PRISMA-informed scoping mini-review of responsible medical-imaging AI: bias, XAI, privacy, uncertainty, calibration and clinical workflow.",
        "evaluation": "Synthesizes 24 studies published during 2020–2025, explicitly not a full pooled meta-analysis; notes many studies lack independent prospective validation.",
        "caution": "Interpretation: use its checklist themes as a design prompt, not as evidence of a certified clinical system.",
        "sections": "Methods (s2); Quality/risk of bias (s5); External validation (s6); Limitations (s7).",
        "fields": {"domain":"Scoping review: responsible medical imaging AI", "dataset":"24 reviewed studies", "evaluation_metrics":"Fairness, calibration, validation and privacy reporting", "limitations":"Scoping sample, no pooled effect; heterogeneous studies"}},
    "P037": {
        "methods": "TRIAGE is an evaluation/reporting framework covering discrimination, confusion-matrix measures, calibration, grouped/temporal/external validation, subgroup fairness and deployment cost.",
        "evaluation": "This is a methodological framework, not a new trained disease classifier; it recommends a structured checklist and statistically sound comparisons.",
        "caution": "Interpretation: adopt the reporting dimensions but select task-specific thresholds only after cohort and model measurements.",
        "sections": "Confusion matrix (sec2dot1dot3); Statistical analysis (sec2dot1dot4); Cross-validation (sec6); abstract.",
        "fields": {"domain":"Clinical AI evaluation framework", "evaluation_metrics":"Sensitivity, specificity, AUROC, calibration, grouped/temporal/external validation", "limitations":"Framework proposal, not prospective validation of our system"}},
    "P038": {
        "methods": "Lightweight Conformer combines convolutional local features and Transformer context for medical image classification; no clinical tabular input.",
        "evaluation": "Evaluates eight image datasets including ROP and MedMNIST subsets; the paper describes five-fold CV for ROP, BloodMNIST and RetinaMNIST.",
        "caution": "Interpretation: plausible efficient image-encoder comparator, but no evidence here for MRI–clinical fusion or free-CPU full-volume inference.",
        "sections": "Dataset/preprocessing (sec3dot1); CV strategy (sec9); Evaluation (sec5dot1/5dot2).",
        "fields": {"medical_modality":"Retinal and other image benchmarks", "clinical_data":"None", "image_encoder":"Lightweight Conformer", "fusion_method":"Image-only CNN/Transformer feature integration", "dataset":"Eight image datasets, including ROP and MedMNIST subsets", "evaluation_metrics":"Cross-validation and classification metrics", "limitations":"No MRI–clinical evaluation"}},
    "P039": {
        "methods": "Masked Autoencoder pretraining on large multi-cohort 2D brain MRI, then frozen Transformer plus linear head for classification or CNN/Transformer fusion for segmentation.",
        "evaluation": "Authors report over 31 million 2D slices in pretraining and few-shot tests including independent NFBS, SynthStrip and MRBrainS18 datasets. Slice count is not participant count.",
        "caution": "Interpretation: pretrained/frozen encoder can reduce compute; segmentation fusion architecture does not establish value for clinical-tabular fusion.",
        "sections": "Pretraining data (sec4); Fine-tuning data (sec10); MAE pretraining (sec17); Fusion architecture (sec20); Results (sec25).",
        "fields": {"medical_modality":"2D brain MRI slices", "clinical_data":"None", "image_encoder":"Masked Autoencoder ViT", "fusion_method":"CNN/Transformer fusion for segmentation, not clinical fusion", "dataset":"NACC, OASIS, ADNI and independent task sets", "sample_size":">31 million slices in pretraining; participant count not equivalent", "limitations":"Pretraining scale not replicable on free compute"}},
    "P040": {
        "methods": "CMAP-Fusion applies ViT-B/16 image encoding, laboratory feature alignment/pruning and a Cross-Modal Transformer with cross-attention.",
        "evaluation": "Experiments combine three image datasets with laboratory data; the article explicitly distinguishes a real cross-modal case from image datasets paired with simulated cross-modal data.",
        "caution": "Interpretation: architecture and pruning comparator only. Performance on simulated clinical variables is not evidence that real independent clinical observations help.",
        "sections": "Model design (sec004); CMT fusion (sec007); Experimental data (sec008); Comparisons (sec014); Discussion (sec019).",
        "fields": {"medical_modality":"X-ray and dermoscopy/image datasets", "clinical_data":"Laboratory data, partly simulated in evaluation", "image_encoder":"ViT-B/16", "clinical_encoder":"Laboratory feature alignment/pruning", "fusion_method":"Cross-Modal Transformer with cross-attention", "cross_attention":"YES", "multimodal_transformer":"YES", "dataset":"Three public image datasets; real and simulated laboratory pairing", "limitations":"Part of multimodal evaluation uses simulated clinical features"}},
    "P041": {
        "methods": "Hierarchical multi-scale Vision Transformer for four-class brain-tumor MRI image classification, with multi-resolution patch embeddings; no clinical branch.",
        "evaluation": "The paper uses 7,023 Kaggle contrast-enhanced T1 images and reports AUROC 0.988, F1 0.987, and ECE 0.023.",
        "caution": "Interpretation: image encoder and calibration comparator, not evidence for Alzheimer MRI–clinical fusion; image-level metrics need patient provenance checks.",
        "sections": "Dataset (Sec10); Architecture (Sec11); Hybrid comparison (Sec25/26); abstract.",
        "fields": {"disease":"Brain tumor", "medical_modality":"Contrast-enhanced T1 MRI images", "clinical_data":"None", "image_encoder":"Hierarchical multi-scale ViT", "fusion_method":"Image-only multi-scale feature integration", "dataset":"Kaggle brain-tumor MRI set", "sample_size":"7,023 images", "evaluation_metrics":"AUROC, F1, ECE", "main_result":"Authors report AUROC 0.988 and ECE 0.023", "limitations":"Image-level dataset provenance differs from patient-level Alzheimer cohort"}},
    "P042": {
        "methods": "Weighted soft-voting ensemble of image classifiers for CT liver-metastasis detection in colorectal-cancer surveillance; reports 0.39-second per-image inference.",
        "evaluation": "The article describes a KHCC imaging/clinical source and image-level model comparisons; its primary fusion is model-probability ensemble, not cross-attention between independently measured clinical variables and image tokens.",
        "caution": "Interpretation: deployment latency needs hardware and image-size context; its per-image time cannot be projected onto full MRI volumes.",
        "sections": "Methodology (s3); Dataset (sec9); Ensemble voting (sec22); abstract.",
        "fields": {"disease":"Colorectal liver metastasis", "medical_modality":"Liver CT", "clinical_data":"Clinical context described, but model input pairing needs audit", "fusion_method":"Weighted soft-voting image-model ensemble", "dataset":"KHCC Liver Metastasis study as described", "main_result":"Authors report 0.39 s per-image inference", "limitations":"CT/image workflow and hardware differ from MRI volume inference"}},
    "P043": {
        "methods": "Federated pancreatic-cancer framework combines RegNetZ and Swin Transformer representations from CT/MRI/histology with tabular genetic/clinical inputs using feature-level fusion.",
        "evaluation": "The article reports 44,269 annotated images in simulation; a Kaggle data source is described. The source does not establish that all modality samples are naturally paired across sites.",
        "caution": "Interpretation: consider Swin as an image-encoder comparator, but do not assume this simulation demonstrates privacy compliance or authentic multimodal paired clinical validity.",
        "sections": "Dataset (Sec6); Fusion (Sec19); Simulation results (Sec22); Future scope (Sec23).",
        "fields": {"disease":"Pancreatic cancer", "medical_modality":"CT, MRI, histology as described", "clinical_data":"Clinical/genetic inputs described", "image_encoder":"RegNetZ plus Swin Transformer", "fusion_method":"Feature-level fusion in federated framework", "dataset":"Kaggle source described; simulated federated setting", "sample_size":"44,269 images reported for simulation", "limitations":"Authentic pairing/site provenance and prospective privacy evidence not established"}},
    "P044": {
        "methods": "MedPTQ performs real INT8 post-training quantization of 3D medical segmentation networks, including SwinUNETR, and contrasts it with simulated quantization.",
        "evaluation": "Tests seven segmentation architectures across CT/MRI datasets, comparing model size, speed and segmentation performance.",
        "caution": "Interpretation: quantization is a post-training deployment experiment, not a guaranteed optimization of our different classifier on a free CPU host.",
        "sections": "Method (sec3); Dataset (sec4.1); Quantization results (sec4.3); Discussion (sec5).",
        "fields": {"medical_modality":"3D CT and MRI segmentation", "clinical_data":"None", "image_encoder":"Segmentation models including SwinUNETR", "fusion_method":"No clinical fusion", "dataset":"BTCV and other segmentation sets", "evaluation_metrics":"Segmentation quality, model size, inference latency", "limitations":"Segmentation/GPU quantization results may not transfer to CPU MRI classifier"}},
    "P045": {
        "methods": "CD-DETR modifies a detection Transformer with ResNet-50 image features and multi-scale feature fusion for small thoracic findings on chest X-rays.",
        "evaluation": "Uses NIH Chest X-ray and VinBigData datasets; authors report 88.3% precision and 86.6% recall on NIH.",
        "caution": "Interpretation: detection and bounding-box results do not supply a disease-classification threshold or image–clinical architecture.",
        "sections": "Multi-scale fusion (sec009); Feature fusion (sec018); NIH data (sec023); VinBigData (sec024); abstract.",
        "fields": {"disease":"Thoracic disease detection", "medical_modality":"Chest X-ray", "clinical_data":"None", "image_encoder":"ResNet-50 plus DETR", "fusion_method":"Image feature multi-scale fusion", "dataset":"NIH Chest X-ray; VinBigData", "evaluation_metrics":"Detection precision, recall and IoU", "main_result":"Authors report NIH precision 88.3%, recall 86.6%", "limitations":"Detection task differs from patient-level MRI classification"}},
    "P046": {
        "methods": "BAE-ViT turns sex into a non-image token and jointly processes it with hand-radiograph patch tokens in a Transformer for bone-age regression.",
        "evaluation": "Uses RSNA pediatric bone-age challenge training/validation sets and an external set; training set is 12,611 images, validation 1,425 images.",
        "caution": "Interpretation: token-level non-image fusion is architecturally relevant, but its one-bit sex variable and regression target differ greatly from richer, potentially leaking Alzheimer clinical features.",
        "sections": "Dataset (sec2dot1); Results (sec3); Discussion (sec4); Limitations (sec4dot2).",
        "fields": {"disease":"Pediatric bone-age estimation", "medical_modality":"Hand radiograph", "clinical_data":"Sex token", "image_encoder":"ViT", "clinical_encoder":"Non-image token embedding", "fusion_method":"Joint image/sex token Transformer", "dataset":"RSNA bone-age and external set", "sample_size":"12,611 training and 1,425 validation images", "limitations":"Single clinical variable; regression task"}},
    "P047": {
        "methods": "MedMNIST+ benchmarking compares CNN and ViT models over medical-image datasets, resolutions and training schemes; no clinical data branch.",
        "evaluation": "Authors emphasize standardized cross-dataset benchmarking and report CNN competitiveness versus ViTs.",
        "caution": "Interpretation: maintain a modest CNN baseline; the collection's image datasets cannot be pooled as a single Alzheimer cohort.",
        "sections": "Datasets (Sec3); Discussion/conclusion (Sec8); abstract.",
        "fields": {"domain":"Medical image benchmark study", "medical_modality":"Multiple MedMNIST+ image types", "clinical_data":"None", "image_encoder":"CNN and ViT comparisons", "fusion_method":"Image-only", "dataset":"MedMNIST+ collection", "limitations":"Benchmark scale/tasks differ from paired patient MRI–clinical study"}},
    "P048": {
        "methods": "Vision Transformer chest-X-ray pneumonia classifier; no structured clinical or cross-modal branch.",
        "evaluation": "Authors report 97.61% accuracy, 95% sensitivity and 98% specificity on their chest-X-ray classification experiment.",
        "caution": "Interpretation: an image-only ViT comparator; those X-ray scores are not expected Alzheimer MRI performance.",
        "sections": "Methodology (Sec4–Sec6); Training (Sec16); article abstract.",
        "fields": {"disease":"Pneumonia", "medical_modality":"Chest X-ray", "clinical_data":"None", "image_encoder":"Vision Transformer", "fusion_method":"Image-only", "evaluation_metrics":"Accuracy, sensitivity, specificity", "main_result":"Authors report 97.61% accuracy, 95% sensitivity, 98% specificity", "limitations":"Different imaging and disease domain"}},
    "P049": {
        "methods": "ViT-B chest-radiograph study compares self-supervised versus supervised pretraining on medical/non-medical images before downstream classification.",
        "evaluation": "Six international radiograph cohorts, more than 800,000 images as described in Discussion; evaluates transfer across data sources.",
        "caution": "Interpretation: pretrained encoder choice must be ablated under our MRI task; image source and label prevalence affect apparent gains.",
        "sections": "Patient cohorts (Sec3); Experimental design (Sec11); Network (Sec12); Discussion (Sec23).",
        "fields": {"disease":"Thoracic abnormalities", "medical_modality":"Chest radiographs", "clinical_data":"None", "image_encoder":"ViT-B with different pretraining", "fusion_method":"Image-only", "dataset":"Six international chest-radiograph cohorts", "sample_size":">800,000 images across sources, per authors", "limitations":"Pretraining domain and target MRI domain differ"}},
    "P050": {
        "methods": "Stitched/parameter-sharing ViT builds efficient OCT AMD classifiers from pretrained transformer components.",
        "evaluation": "Authors report over 94.9% accuracy after 100 epochs on NEH OCT images when another OCT pretrained model is available.",
        "caution": "Interpretation: efficient transfer strategy only; it does not validate MRI–clinical fusion or free-resource feasibility for our model.",
        "sections": "Method (sec009); Experiments (sec015); abstract.",
        "fields": {"disease":"Age-related macular degeneration", "medical_modality":"Retinal OCT", "clinical_data":"None", "image_encoder":"Stitched Vision Transformer", "fusion_method":"Image-only model stitching", "dataset":"NEH OCT and pretraining source", "main_result":"Authors report >94.9% accuracy after 100 epochs in stated setting", "limitations":"Needs suitable pretrained OCT model; domain differs from MRI"}},
}

BASE_FIELDS = {
    "P001": {"sample_size": "105 distinct subjects; 306 scan sessions reported", "dataset": "ADNI", "evaluation_metrics": "Accuracy, macro AUROC, F1, sensitivity, specificity, ECE; subject-level 3-fold CV"},
    "P002": {"sample_size": "ANMerge resource 1,702 participants; selected experiment 319 unique patients/919 samples; 453 had MRI, per paper", "dataset": "ANMerge development; ADNI MRI-only external test", "evaluation_metrics": "Accuracy, recall, F1; group-based 5-fold CV; external MRI-only ADNI test"},
}
SUPPLEMENTAL_FIELDS = {
    'P007': {'dataset':'Alzheimer Disease Multiclass MRI image dataset (Singhal 2022), per Section 3.1', 'evaluation_metrics':'Cross-validation F1 and AUROC'},
    'P013': {'dataset':'Single-center retrospective AD/control MRI cohort'},
    'P016': {'dataset':'Nobeoka City community older-adult cohort'},
    'P024': {'dataset':'972-subject multimodal AD/MCI/CN cohort described in article'},
    'P038': {'sample_size':'Multiple image datasets; no single patient denominator'},
    'P040': {'evaluation_metrics':'Accuracy, model efficiency, robustness to image noise/missing laboratory data'},
    'P042': {'evaluation_metrics':'Classification metrics and per-image inference latency'},
    'P044': {'evaluation_metrics':'Segmentation quality, model size and real inference latency'},
    'P045': {'sample_size':'NIH and VinBigData images; see source dataset sections'},
}

TRAINING = {
    'P005': 'The clinical CNN/random-forest and MRI VGG19 pathways were trained separately on different Kaggle datasets; see Sec8–Sec10. The image split was 70/30 random, not established as patient-grouped.',
    'P007': 'The source uses a combined cross-entropy, ordinal and consistency loss; see Sections 3.8 and 3.10. Exact patient grouping of the source image set remains to be checked.',
    'P008': 'Implemented with Keras/TensorFlow on an RTX A4000 workstation; see Implementation details. This hardware is outside the assumed free deployment environment.',
    'P009': 'End-to-end PyTorch training with focal loss and AdamW; source methods report learning rate 0.00005, maximum 150 epochs and early stopping patience 30; see Multimodal architecture.',
    'P010': 'Separate 3D CNNs extract sMRI/PET features; the source evaluates with tenfold cross-validation; see Network model framework and Experiment settings.',
    'P011': 'Source architecture/training details are in Hybrid deep learning architecture and Experimental results; a single reproducible hyperparameter set was not extracted for this note.',
    'P012': 'The source reports comparative training/testing curves against multimodal baselines; see Training and testing analysis. Precise paired text construction remains a higher-priority replication issue than its optimizer choice.',
    'P013': 'Radiomic feature selection was restricted to training data with fivefold CV before logistic-regression/random-forest fitting; see Overfitting/generalizability.',
    'P016': 'Three elastic-net models were developed on training data and assessed on a separate test set; see Sections 3.2–3.3.',
    'P017': 'The volumetric CNN used fivefold CV and batch size two due to GPU memory; see Materials and methods and Limitations.',
    'P019': 'Single-visit and longitudinal statistical models were fit to MRI-derived and cognitive variables; see Methods and Discussion.',
    'P020': 'Training was staged rather than fully joint: bimodal classifiers and cycle-GAN missing-view modules precede fusion/classification; see Training scheme.',
    'P021': 'The source trains hybrid 3D CNN/ANN and ViT comparisons, with image-only, covariate-only and joint inputs; see Sections 15–17.',
    'P022': 'PyTorch 2.6/CUDA 11.8 implementation used one V100 32GB GPU, 200 epochs and batch size eight; see Section 4.1.',
    'P023': 'The source states a 70% training partition for its pretrained architecture comparison; see Training, validation and testing phase. Confirm subject grouping before reproduction.',
    'P024': 'Similarity networks were built and spectrally clustered; this is unsupervised cohort stratification, not supervised neural-network training; see SNF-based method.',
    'P026': 'Models and feature subsets were compared with nested cross-validation; see Base learners and nested cross-validation and Experimental setup.',
    'P027': 'PyTorch multiclass cross-entropy training; 80% of ADNI1 subjects used for fivefold subject-level CV, 20% held out; see Implementation, Dataset and Section 5.2.',
    'P028': 'YOLOv11 experiments used paid Colab Pro with an NVIDIA T4 as stated in Results; exact adaptation to free Colab is unverified.',
    'P029': 'Fivefold nested CV on 672 baseline MCI patients preceded a held-out test; see Evaluation methodology (sec2.5).',
    'P030': 'Longitudinal landmark competing-risk analysis uses repeated predictors and five-year dementia outcomes; see Three-City cohort and Discussion.',
    'P033': 'MATLAB R2023b analyses fixed rng(42), per Implementation Details; compare models with and without overt diagnostic symptoms.',
    'P035': 'Logistic regression, random forest and XGBoost models used ICD features; hyperparameters were tuned on validation data; see Model Development and Evaluation.',
    'P038': 'PyTorch on RTX 3090; AdamW with initial learning rate 1e-4, batch size 32 and 50 epochs; see Implementation Details.',
    'P039': 'Masked-autoencoder pretraining is followed by frozen-encoder/linear-head few-shot classification or CNN/Transformer segmentation adaptation; see MAE pretraining and Results.',
    'P040': 'The source describes end-to-end image/laboratory encoding, feature pruning and cross-modal Transformer prediction; see CMAP-Fusion model design.',
    'P041': 'The article specifies a three-phase progressive training scheme beginning with a five-epoch frozen-transformer warm-up; see Three-phase progressive training strategy.',
    'P042': 'PyTorch image backbones were trained on NVIDIA GPU and combined by weighted probability voting; see Implementation details and Ensemble learning methodology.',
    'P043': 'Federated simulation fits local RegNetZ/Swin models and aggregates updates; see Local loss function and federated training and Simulation results.',
    'P044': 'Post-training INT8 quantization is applied to already pretrained 3D segmentation models; see Implementation Details and Quantization Results.',
    'P045': 'PyTorch CD-DETR training used an NVIDIA A100 40GB and ImageNet-pretrained ResNet backbone; see Training setup.',
    'P046': 'The source discusses pretraining an image encoder then fitting image/sex-token fusion, including fixed versus trainable encoder variants; see Training Techniques.',
    'P047': 'Benchmarks compare end-to-end fitting with frozen-encoder linear probing; see Training pipeline.',
    'P048': 'Vision Transformer model training is described in Model’s training; exact patient-level grouping is not established by the benchmark description.',
    'P049': 'ViT-B downstream training compares self-supervised DINOv2, supervised ImageNet and medical pretraining; see Experimental design and Network architecture.',
    'P050': 'Pretrained OCT Transformer components are stitched and fine-tuned; the paper reports a 100-epoch setting for one NEH experiment; see Method and Experiments.',
}
REVIEWS = {'P006','P014','P015','P018','P025','P031','P032','P034','P036','P037'}

def main():
    path = PAPERS / "papers.csv"
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames
    for row in rows:
        key = row["paper_id"]
        row.update(BASE_FIELDS.get(key, {}))
        row.update(SUPPLEMENTAL_FIELDS.get(key, {}))
        if key in REVIEWS:
            for field in ('image_encoder','clinical_encoder','sample_size'):
                if row.get(field) == 'Not verified from available source':
                    row[field] = 'Not applicable: review/framework article'
            if row.get('dataset') == 'Not verified from available source':
                row['dataset'] = 'Published studies or guidance reviewed; no new patient cohort'
            if row.get('evaluation_metrics') == 'Not verified from available source':
                row['evaluation_metrics'] = 'Methodological synthesis; no newly trained model'
        finding = FINDINGS.get(key)
        if not finding:
            note = PAPERS / "notes" / f"{key}.md"
            body = note.read_text(encoding="utf-8")
            if '**Publisher:**' not in body:
                body = body.replace('## Research Problem', f"**Publisher:** {row['publisher']}.\n\n## Research Problem", 1)
                note.write_text(body, encoding="utf-8")
            continue
        row.update(finding.get("fields", {}))
        note = PAPERS / "notes" / f"{key}.md"
        body = note.read_text(encoding="utf-8")
        if '**Publisher:**' not in body:
            body = body.replace('## Research Problem', f"**Publisher:** {row['publisher']}.\n\n## Research Problem", 1)
        marker = "\n## Verified full-text audit\n"
        if marker in body:
            body = body.split(marker)[0]
        heading_fields = {
            "Dataset": "dataset", "Modalities": "medical_modality",
            "Image Encoder": "image_encoder", "Clinical Encoder": "clinical_encoder",
            "Fusion Strategy": "fusion_method", "Explainability": "explainability",
            "Evaluation": "evaluation_metrics", "Results": "main_result",
            "Limitations": "limitations",
        }
        for heading, field in heading_fields.items():
            value = row.get(field, "")
            if not value or value in {"Not verified from available source", "See source abstract", "See source abstract in note"}:
                continue
            pattern = rf"(## {re.escape(heading)}\n\n)(.*?)(?=\n## |\Z)"
            match = re.search(pattern, body, re.S)
            if match and ("Not verified from available source" in match.group(2) or
                          "See source abstract" in match.group(2) or
                          "See verified abstract" in match.group(2)):
                body = body[:match.start(2)] + value + "\n" + body[match.end(2):]
        replacements = {
            "## Research Problem\n\nSee source abstract below.":
                "## Research Problem\n\n" + finding['methods'].split('.')[0] + ".",
            "## Architecture\n\nSee verified abstract and catalog fields; full architecture not verified for this entry.":
                "## Architecture\n\n" + finding['methods'],
            "## Evaluation\n\nNot verified from available source":
                "## Evaluation\n\n" + finding['evaluation'],
            "## What We Can Learn\n\nInterpretation: evaluate the stated method as a baseline or design comparator; no performance transfer is assumed.":
                "## What We Can Learn\n\n" + finding['caution'],
            "Evidence level: catalog metadata and abstract verified. Detailed methods not verified unless specified above.":
                "Evidence level: catalog/abstract and the named full-text sections in the audit below were reviewed; unfilled details remain unverified.",
        }
        for old, new in replacements.items():
            body = body.replace(old, new)
        fusion = row.get('fusion_method', '')
        if 'attention' in fusion.lower():
            body = body.replace('## Attention Mechanism\n\nNOT REPORTED',
                                '## Attention Mechanism\n\n' + fusion)
        if fusion and fusion not in {'Not verified from available source', 'Image-only'}:
            body = body.replace('## Multimodal Learning\n\nNOT REPORTED',
                                '## Multimodal Learning\n\n' + fusion)
        training = TRAINING.get(key, 'Not applicable: this article reviews or proposes evaluation guidance rather than training a new model.' if key in REVIEWS else None)
        if training:
            body = body.replace('## Training\n\nNot verified from available source.',
                                '## Training\n\n' + training)
        body += (f"{marker}\n**Paper facts / author-reported method:** {finding['methods']}\n\n"
                 f"**Author-reported evaluation and results:** {finding['evaluation']}\n\n"
                 f"**Our interpretation / proposed adaptation:** {finding['caution']}\n\n"
                 f"**Exact source locations:** {finding['sections']}\n")
        note.write_text(body, encoding="utf-8")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    (PAPERS / "papers.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
