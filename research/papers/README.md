# Research paper collection

This collection contains **exactly 50 distinct publications dated 2024–2026**, selected for their direct relationship to Alzheimer MRI/clinical fusion or for a specific supporting method (transformers, explainability, validation, leakage, or efficient inference). It is a curated technical review, not a claim that every paper evaluates the same task. Paper IDs are stable IEEE-style reference numbers: `[1]` means `P001`.

`papers.csv` and `papers.json` have identical catalog fields. `references.bib` contains the same bibliographic identity fields. `notes/Pxxx.md` contains an indexed abstract, required research headings, and source-located method/result/limitation findings where full text could be accessed. Fields marked **Not verified from available source** must not be repeated as paper facts. `candidates.json` is the raw Europe PMC search audit; `pdf_download_log.csv` records which PDF responses passed a `%PDF` signature check. Publisher full-text pages and official conference proceedings supplement the Europe PMC records for P001–P004.

`fulltext_section_index.json` records section titles/IDs from 45 Europe PMC open full-text XML files. Forty-five XML sources and P001/P002/P018 PDFs supply the 48 full-text note audits. P003 and P004 are restricted to official abstract evidence. The section index is navigation, while each note's **Verified full-text audit** identifies the source sections actually used.

The 44 PDF files exist in this workspace but are Git-ignored until article-by-article redistribution licenses are checked. A fresh Git clone will have the catalog, source URLs and download log, but must retrieve permitted PDFs anew. Missing local PDFs do not invalidate source metadata.

## Taxonomy

Papers can appear in multiple topics. The categories are methodological labels, not equal-sized bins:

| Category | Paper IDs |
|---|---|
| Multimodal medical AI / clinical-data fusion | P001–P006, P009, P011–P013, P016–P017, P019–P024, P027, P029–P030, P040, P043, P046 |
| Medical image / vision Transformers | P001–P004, P007–P010, P012, P014, P023, P027, P038–P041, P043–P050 |
| Swin Transformer | P001, P009, P043–P044 |
| Clinical Transformer or BERT branch | P001–P002, P009, P027 |
| Cross-attention / cross-modal attention | P002–P003, P009 (ablation), P027, P040 |
| Joint multimodal Transformer fusion | P002–P004, P040, P046 |
| MRI disease detection / Alzheimer research | P001–P008, P010, P012–P030, P039, P041 |
| Explainable medical AI / SHAP / visual attribution | P001–P002, P007–P010, P013, P019–P022, P027, P031, P036–P037 |
| Medical AI evaluation / leakage / generalization | P006, P013–P014, P016–P017, P027, P029–P030, P032–P037, P047, P049 |
| Efficient inference / deployment methods | P038–P045, P047, P050 |
| Other directly relevant methods | P024–P026, P028, P031, P034–P035, P046 |

Disease-specific non-Alzheimer papers support a *method*, not a claim of transferable clinical performance. In particular, P005 does not fuse paired MRI and clinical records, and P040 includes simulated laboratory data in part of its evaluation.

## Evidence policy

- `open_access=YES` reflects source-indexed access or an official open proceedings page; it does not mean local PDF download succeeded.
- A missing `pdf_path` means no valid, lawful PDF was saved. Consult the linked full-text page or abstract.
- Notes distinguish publisher-reported results from our interpretation and retain exact section locations. P003/P004 cannot support claims beyond their official abstracts. Check the source before reproducing any reported metric.
- Do not add two versions of the same publication as separate entries. Re-run `scripts/build_research_catalog.py` after editing the selected source set; it regenerates notes and catalog, so preserve any manual additions elsewhere before doing so.

## Search and screening

Search date: 2026-09-29. Europe PMC core search used ten topic queries bounded by first publication date and open-access indexing; 315 unique candidate records were saved. Official publisher and IEEE/CVF conference pages were used for four especially close comparison papers. Selection favored MRI plus independently measured clinical information and architecture evidence; supporting papers address a concrete project risk. See [quality report](research_quality_report.md) for remaining verification limits.
