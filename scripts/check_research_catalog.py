"""Verify the structural integrity of the research catalog and local PDFs."""
import csv
import json
import subprocess
import shutil
from pathlib import Path

root=Path('research/papers')
csv_rows=list(csv.DictReader((root/'papers.csv').open()))
json_rows=json.loads((root/'papers.json').read_text())
assert csv_rows == [{k:str(v) for k,v in row.items()} for row in json_rows]
assert len(csv_rows)==50
assert [r['paper_id'] for r in csv_rows]==[f'P{i:03d}' for i in range(1,51)]
assert len({(r['doi'] or r['title']).casefold() for r in csv_rows})==50
assert all(r['year'] in {'2024','2025','2026'} for r in csv_rows)
assert all(r['url'].startswith('https://') for r in csv_rows)
assert all(r['publisher'] and r['publisher']!='Not verified from available source' for r in csv_rows)
assert all((root/'notes'/f"{r['paper_id']}.md").exists() for r in csv_rows)
headings=['Bibliographic Information','Research Problem','Dataset','Modalities','Architecture','Image Encoder',
          'Clinical Encoder','Fusion Strategy','Attention Mechanism','Multimodal Learning','Explainability',
          'Training','Evaluation','Results','Limitations','What We Can Learn','What We Should NOT Copy',
          'Relevance to Our Project','Exact Evidence / Source Locations']
for r in csv_rows:
    note=(root/'notes'/f"{r['paper_id']}.md").read_text()
    assert all(f'## {h}' in note for h in headings),r['paper_id']
    assert '**Publisher:**' in note,r['paper_id']
    if r['paper_id'] not in {'P001','P002','P003','P004'}:
        assert '## Verified full-text audit' in note,r['paper_id']
for r in csv_rows:
    if r['pdf_path']:
        p=Path(r['pdf_path'])
        assert p.exists() and p.read_bytes()[:4]==b'%PDF',p
        if shutil.which('pdfinfo'):
            report=subprocess.run(['pdfinfo',str(p)],capture_output=True,text=True,check=True).stdout
            pages=next((int(line.split(':',1)[1]) for line in report.splitlines() if line.startswith('Pages:')),0)
            assert pages>=1,p
bib=(root/'references.bib').read_text()
assert sum(line.startswith('@') for line in bib.splitlines())==50
for r in csv_rows: assert '{'+r['paper_id']+',' in bib
required_docs=['README.md','AGENTS.md','CHANGELOG.md','docs/research/final_research_report.md',
               'docs/research/literature_review.md','docs/research/base_paper_selection.md',
               'docs/research/comparison_matrix.md','docs/research/research_gap.md',
               'docs/research/proposed_contribution.md','docs/research/data_leakage_and_validation.md',
               'docs/data/dataset_strategy.md','docs/data/data_dictionary.md',
               'docs/architecture/system_architecture.md','docs/architecture/mathematical_formulation.md',
               'docs/architecture/architecture.mmd','docs/ml/experiment_plan.md','docs/ml/evaluation.md',
               'docs/ml/explainability.md','docs/ml/performance_optimization.md',
               'docs/technology/technology_stack.md','docs/deployment/free_tier_strategy.md',
               'docs/development/cloud_only_workflow.md','docs/frontend/ui_ux_specification.md',
               'docs/backend/api_specification.md','docs/backend/openapi.yaml',
               'docs/security/security_and_privacy.md','docs/medical/medical_safety.md',
               'docs/reproducibility/reproducibility.md',
               'docs/requirements/software_requirements_specification.md',
               'docs/project/project_roadmap.md','docs/project/feasibility_review.md',
               'docs/project/pre_development_review.md','docs/decisions/architecture_decisions.md',
               'docs/glossary.md','docs/testing/testing_strategy.md']
assert all(Path(p).exists() and Path(p).stat().st_size>0 for p in required_docs)
print('catalog valid; papers=50; notes=50; PDFs=',sum(bool(r['pdf_path']) for r in csv_rows))
