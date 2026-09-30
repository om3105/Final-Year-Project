"""Build a traceable paper catalog from locally saved Europe PMC records.

This script does not fetch or synthesize paper facts. Fields absent from the indexed
record remain explicitly unverified. The four non-indexed comparison papers are
listed from their official publisher/conference pages in EXTERNAL below.
"""

import csv
import html
import json
import re
from pathlib import Path

ROOT = Path('research/papers')
existing_paths = {}
if (ROOT / 'papers.csv').exists():
    with (ROOT / 'papers.csv').open() as f:
        existing_paths = {r['doi'] or r['title']: r.get('pdf_path', '') for r in csv.DictReader(f)}
CANDIDATES = json.loads((ROOT / 'candidates.json').read_text())
INDICES = [
    1, 4, 13, 15, 28, 57, 66, 72, 82, 83, 86, 91, 93, 96, 97,
    102, 113, 118, 126, 128, 133, 137, 142, 152, 159, 164, 174,
    179, 185, 189, 191, 196, 214, 260, 266, 269, 270, 280, 282,
    285, 288, 297, 308, 310, 313, 314,
]
EXTERNAL = [
    dict(title="TriFusion-ADFormer: a deep learning framework for early Alzheimer's disease detection using MRI and cognitive metrics", authors="S Sabari Vasan; P Jayalakshmi", year=2026, venue="Frontiers in Artificial Intelligence", doi="10.3389/frai.2026.1849315", url="https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1849315/full", publisher="Frontiers", open_access="YES", pmcid="PMC13454240", abstract="TriFusion-ADFormer uses structural MRI, MRI-derived clinical text, and cognitive assessment scores for AD/MCI/CN classification. Swin Transformer V2 encodes MRI, BERT encodes the MRI-derived text, and an MLP encodes cognitive scores. Embeddings are concatenated and passed to feed-forward layers. The authors report accuracy 86.0%, macro AUC 0.93, and F1 0.86 on ADNI.", source="Publisher full text, sections 3.3, 4 and 5", full_text_available="YES"),
    dict(title="Not Only Grey Matter: OmniBrain for Robust Multimodal Classification of Alzheimer's Disease", authors="Ahmed Sharshar; Yasser Ashraf; Tameem Bakr; Salma Hassan; Hosam Elgendy; Mohammad Yaqub; Mohsen Guizani", year=2025, venue="Proceedings of the IEEE/CVF International Conference on Computer Vision Workshops", doi="", url="https://openaccess.thecvf.com/content/ICCV2025W/CVAMD/html/Sharshar_Not_Only_Grey_Matter_OmniBrain_for_Robust_Multimodal_Classification_of_ICCVW_2025_paper.html", publisher="IEEE/CVF", open_access="YES", pmcid="", abstract="OmniBrain integrates brain MRI, radiomics, gene expression, and clinical data using a pretrained MRI encoder, FT-Transformer for tabular inputs, cross-attention and modality dropout. It reports 92.2 ± 2.4% accuracy on ANMerge and 70.4 ± 2.7% on an MRI-only ADNI external test. The paper uses Grad-CAM and SHAP.", source="Official CVF proceedings abstract and paper sections 3–5", full_text_available="YES"),
    dict(title="A Multimodal Cross-Attention Model for Alzheimer's Disease Diagnosis", authors="Zhou Li; Yongbin Liu; Chunping Ouyang; Jiangtao Zhang; Xue Pan; Lu Jiang; Jin Zhong", year=2025, venue="Acta Scientiarum Naturalium Universitatis Pekinensis", doi="10.13209/j.0479-8023.2024.121", url="https://xbna.pku.edu.cn/CN/Y2025/V61/I4/629", publisher="Peking University Press", open_access="NOT VERIFIED", pmcid="", abstract="MAMDF integrates medical imaging and clinical data for AD/MCI classification using asymmetric cross-attention and a Transformer-based feature-fusion module; evaluated on ADNI. The publisher abstract does not report exact numeric performance.", source="Official journal page, abstract and bibliographic block", full_text_available="ABSTRACT VERIFIED; PDF ACCESS NOT VERIFIED"),
    dict(title="A transformer-based unified multimodal framework for Alzheimer's disease assessment", authors="Qi Yu; Qian Ma; Lijuan Da; Jiahui Li; Mengying Wang; Andi Xu; Zilin Li; Wenyuan Li", year=2024, venue="Computers in Biology and Medicine", doi="10.1016/j.compbiomed.2024.108979", url="https://doi.org/10.1016/j.compbiomed.2024.108979", publisher="Elsevier", open_access="NO VERIFIED OA COPY", pmcid="", abstract="AD-Transformer combines structural MRI, clinical and genetic data from 1,651 ADNI subjects. A Patch-CNN forms image tokens; a linear layer projects non-image tokens; Transformer blocks model joint features. The publisher reports AUC 0.993 for AD diagnosis and 0.845 for MCI conversion prediction.", source="Publisher abstract and Crossref metadata", full_text_available="NO"),
]
FIELDS = "paper_id title authors year venue doi url publisher open_access pdf_path domain disease medical_modality clinical_data image_encoder clinical_encoder fusion_method cross_attention multimodal_transformer explainability dataset sample_size evaluation_metrics main_result limitations relevance_score relevance_reason base_paper_candidate notes".split()

def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', str(s or '')))).strip()

items = []
for x in EXTERNAL:
    items.append(dict(x))
for idx in INDICES:
    x = CANDIDATES[idx]
    items.append(dict(title=clean(x.get('title')), authors=clean(x.get('authorString')),
                      year=int(x.get('pubYear')), venue=clean(x.get('journalInfo', {}).get('journal', {}).get('title')),
                      doi=x.get('doi', ''), url='https://doi.org/' + x['doi'] if x.get('doi') else 'https://europepmc.org/article/MED/' + x.get('pmid', ''),
                      publisher='Not verified from available source',
                      open_access='YES' if x.get('isOpenAccess') == 'Y' else 'NOT VERIFIED',
                      pmcid=x.get('pmcid', ''), abstract=clean(x.get('abstractText')),
                      source='Europe PMC core record: https://europepmc.org/article/MED/' + x.get('pmid', ''),
                      full_text_available='YES' if x.get('inEPMC') == 'Y' else 'NOT VERIFIED'))

assert len(items) == 50
assert len({x['doi'].lower() or x['title'].lower() for x in items}) == 50
ROOT.joinpath('notes').mkdir(exist_ok=True)
rows = []
for n, x in enumerate(items, 1):
    pid = f'P{n:03d}'
    title = x['title']
    lower = (title + ' ' + x.get('abstract', '')).lower()
    ad = any(t in lower for t in ('alzheimer', 'dementia', 'cognitive impairment'))
    image = any(t in lower for t in ('mri', 'imaging', 'image', 'ct', 'radiom'))
    clinical = any(t in lower for t in ('clinical data', 'clinical information', 'cognitive assessment', 'tabular'))
    direct = ad and image and clinical
    score = 5 if direct else 4 if ad and image else 3
    reason = ('Directly studies AD/dementia imaging with clinical or cognitive information.' if direct
              else 'Supports a relevant imaging, fusion, evaluation, explainability, or deployment method.')
    row = {k: '' for k in FIELDS}
    row.update(paper_id=pid, title=title, authors=x['authors'], year=x['year'], venue=x['venue'],
               doi=x['doi'], url=x['url'], publisher=x['publisher'], open_access=x['open_access'],
               pdf_path=existing_paths.get(x['doi'] or title, ''), domain='Medical AI', disease='Alzheimer disease / dementia' if ad else 'See title',
               medical_modality='See source abstract' if image else 'Not verified from available source',
               clinical_data='Mentioned in source abstract' if clinical else 'Not verified from available source',
               image_encoder='Not verified from available source', clinical_encoder='Not verified from available source',
               fusion_method='Not verified from available source', cross_attention='NOT REPORTED',
               multimodal_transformer='NOT REPORTED', explainability='Not verified from available source',
               dataset='Not verified from available source', sample_size='Not verified from available source',
               evaluation_metrics='Not verified from available source', main_result='See source abstract in note',
               limitations='Not verified from available source', relevance_score=score, relevance_reason=reason,
               base_paper_candidate='YES' if n <= 4 else 'NO', notes=x['source'])
    if n == 1:
        row.update(medical_modality='Structural MRI', clinical_data='Cognitive scores; MRI-derived text', image_encoder='Swin Transformer V2', clinical_encoder='BERT for MRI-derived text; MLP for scores', fusion_method='Concatenation + FFN', cross_attention='NO', multimodal_transformer='NO', dataset='ADNI', evaluation_metrics='Accuracy; macro AUROC; F1; calibration', main_result='Authors report accuracy 86.0%; macro AUROC 0.93; F1 0.86.', limitations='Single ADNI cohort; no external or prospective validation; MRI-derived text is not independent clinical data.')
    if n == 2:
        row.update(medical_modality='Brain MRI', clinical_data='Clinical, radiomics, gene expression', image_encoder='AnatCL / y-Aware InfoNCE', clinical_encoder='FT-Transformer', fusion_method='Cross-attention with modality masking', cross_attention='YES', multimodal_transformer='PARTIAL', explainability='Grad-CAM; SHAP', dataset='ANMerge; external MRI-only ADNI', evaluation_metrics='Accuracy; external validation', main_result='Authors report 92.2 ± 2.4% ANMerge accuracy; 70.4 ± 2.7% external ADNI accuracy.', limitations='External ADNI test is MRI-only; no clinical deployment validation.')
    if n == 3:
        row.update(medical_modality='Medical imaging; exact modality not verified from abstract', clinical_data='Clinical data', fusion_method='Asymmetric cross-attention; Transformer feature module', cross_attention='YES', multimodal_transformer='PARTIAL', dataset='ADNI')
    if n == 4:
        row.update(medical_modality='Structural MRI', clinical_data='Clinical and genetic data', image_encoder='Patch-CNN', clinical_encoder='Linear projection of non-image features', fusion_method='Unified Transformer tokens', cross_attention='NOT REPORTED', multimodal_transformer='YES', dataset='ADNI', sample_size='1,651 subjects', evaluation_metrics='AUROC', main_result='Authors report AUROC 0.993 (AD diagnosis) and 0.845 (MCI conversion).')
    rows.append(row)
    abstract = x.get('abstract', '') or 'Abstract not verified from available source.'
    sections = [
      ('Research Problem', 'See source abstract below.'), ('Dataset', row['dataset']),
      ('Modalities', row['medical_modality'] + '; clinical: ' + row['clinical_data']),
      ('Architecture', 'See verified abstract and catalog fields; full architecture not verified for this entry.'),
      ('Image Encoder', row['image_encoder']), ('Clinical Encoder', row['clinical_encoder']),
      ('Fusion Strategy', row['fusion_method']), ('Attention Mechanism', row['cross_attention']),
      ('Multimodal Learning', row['multimodal_transformer']), ('Explainability', row['explainability']),
      ('Training', 'Not verified from available source.'), ('Evaluation', row['evaluation_metrics']),
      ('Results', row['main_result']), ('Limitations', row['limitations']),
      ('What We Can Learn', 'Interpretation: evaluate the stated method as a baseline or design comparator; no performance transfer is assumed.'),
      ('What We Should NOT Copy', 'Proposed adaptation: do not copy reported accuracy or validation design without reproducing the cohort and split.'),
      ('Relevance to Our Project', row['relevance_reason']),
      ('Exact Evidence / Source Locations', x['source'] + '\n\nEvidence level: catalog metadata and abstract verified. Detailed methods not verified unless specified above.'),
    ]
    body = [f'# {title}', '', f'**Paper ID:** {pid}', '', '## Bibliographic Information', '',
            f"{x['authors']}. *{x['venue']}*, {x['year']}. DOI: {x['doi'] or 'not assigned/verified'}. [Source]({x['url']}).",
            '', f"**Publication/full-text status:** {x['full_text_available']}; open access: {x['open_access']}.", '',
            ('## Verified Source Summary' if n <= 4 else '## Indexed Source Abstract'), '', abstract, '']
    for heading, content in sections:
        body += [f'## {heading}', '', content, '']
    (ROOT / 'notes' / f'{pid}.md').write_text('\n'.join(body))

with (ROOT / 'papers.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader(); writer.writerows(rows)
(ROOT / 'papers.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n')
def esc(s): return str(s).replace('{', '\\{').replace('}', '\\}').replace('&', '\\&')
bib = []
for row in rows:
    fields = {'title': row['title'], 'author': row['authors'].replace('; ', ' and '),
              'year': row['year'], 'journal': row['venue'], 'url': row['url']}
    if row['doi']: fields['doi'] = row['doi']
    if row['pdf_path']: fields['file'] = row['pdf_path']
    entry_type = 'inproceedings' if row['paper_id'] == 'P002' else 'article'
    if entry_type == 'inproceedings': fields['booktitle'] = fields.pop('journal')
    bib.append('@' + entry_type + '{' + row['paper_id'] + ',\n' + ''.join(f'  {k} = {{{esc(v)}}},\n' for k,v in fields.items()) + '}')
(ROOT / 'references.bib').write_text('\n\n'.join(bib) + '\n')
print(f'Wrote {len(rows)} papers, notes, CSV, JSON, BibTeX')
