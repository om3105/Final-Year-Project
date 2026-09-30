# Research quality report — 2026-09-30

## Identity and selection

The catalog contains **exactly 50 distinct 2024–2026 publications**, with unique title/DOI identities, a verified official DOI/publisher or Europe PMC source for each, and no duplicate publication versions. Forty-nine entries have DOIs; P002 is an official ICCV 2025 workshop paper without a DOI in its proceedings record. Crossref registration metadata independently matched the titles and publisher for 42 entries; the remaining seven publisher identities use official venue/publisher pages. P003's publisher DOI page exists, but Crossref's lookup returned 404 for that DOI, so no Crossref registration is claimed for it. Ten date-bounded Europe PMC queries returned 328 records; 13 repeated search hits were removed, leaving 315 candidates before relevance screening and four official comparator additions. Those 13 are *search overlaps*, not duplicates in the selected 50. The most recent selected paper was available before the 2026-09-29 search cutoff. The DOI check audit is in `crossref_verification.json`.

## Full-text access and PDFs

| Measure | Count |
|---|---:|
| Selected and identity verified | 50 |
| Confirmed open-access publication/full-text page | 48 |
| Paywalled with no lawful OA copy verified | 1 (P004) |
| Full-text access not verified | 1 (P003) |
| Full texts consulted | 48 (P001–P002 and P005–P050) |
| Local PDFs with `%PDF` and `pdfinfo` page validation | 44, 840 pages total |
| Local PDFs not obtained | 6 |

Missing local PDFs: **P003** (journal page indicates a PDF, but direct retrieval could not be validated), **P004** (publisher paywall), and **P029/P033/P035/P038** (lawful open full text was read through Europe PMC XML, but publisher/PMC PDF retrieval did not yield a PDF response in this environment). XML access is not the same as a downloaded PDF. The 44 local files are Git-ignored until individual redistribution licenses are audited. The catalog's `open_access` and `pdf_path` fields deliberately describe separate facts.

## Evidence depth

P001 and P002 were checked against publisher/conference full text, P018 against its local PDF, and the other 45 accessible full texts against Europe PMC JATS XML, including named method, dataset, result or limitation sections. Each of these 48 notes now has a source-located methodological audit that separates paper facts and author-reported results from our interpretation. P003 and P004 are limited to their official abstracts, and their detailed training/encoder/split information remains **Not verified from available source**. Some other note fields retain that marker where the specific point was not established by the checked sections; absence of evidence is never converted into a claimed NO.

The comparison matrix was rebuilt from explicit paper evidence rather than title keywords. Important corrections during full-text review: P005's two branches use separate datasets; P009 found concatenation stronger than its attention ablations; P012 has only ten hospital text samples explicitly described; P027's external denominator is 921 images and its metadata include potential diagnostic-score proxies; P040 has partly simulated laboratory data. These limits appear in the notes, literature review and base-paper decision.

## Consistency checks

`papers.csv` and `papers.json` are row-for-row identical on their core fields. `references.bib` has 50 unique citation keys and uses Europe PMC's structured author list for indexed papers. All note IDs P001–P050 exist and contain the required headings. The local PDF signature/page check passed for every cataloged `pdf_path`; 840 pages were counted. `scripts/check_research_catalog.py` reproduces these counts and checks the required document paths. The OpenAPI file parses as YAML with five paths, and the local Markdown link scan found zero broken local targets. Use the DOI/official link in each note to verify any high-impact claim before implementation.

## Residual limits and external gates

P003/P004 cannot be reviewed beyond official abstracts without lawful full-text access. Four other open papers lack local PDFs although their XML full text was reviewed. No dataset access has been granted in this repository; ADNI/OASIS data-use terms and cloud processing must be checked by an authorized investigator. The paired cohort size, label/feature timing, release rights, and full-volume inference cost remain empirical Phase 1/deployment gates. These limits do **not** justify fabricated methods or a claim of clinical readiness. Application implementation has not begun.
