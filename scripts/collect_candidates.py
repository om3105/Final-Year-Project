"""Collect Europe PMC candidates for manual screening; not application code."""

import json
import subprocess
from pathlib import Path
from urllib.parse import urlencode

QUERIES = [
    'TITLE_ABS:(Alzheimer AND multimodal AND (MRI OR imaging) AND (clinical OR cognitive))',
    'TITLE_ABS:(Alzheimer AND (cross-attention OR transformer) AND (MRI OR imaging))',
    'TITLE_ABS:(Alzheimer AND (Swin OR vision transformer) AND MRI)',
    'TITLE_ABS:(medical AND image AND clinical AND multimodal AND transformer)',
    'TITLE_ABS:(medical AND imaging AND tabular AND fusion)',
    'TITLE_ABS:(multimodal AND (MRI OR neuroimaging) AND dementia)',
    'TITLE_ABS:(medical AND multimodal AND explainable AND SHAP)',
    'TITLE_ABS:(medical AND AI AND data leakage AND validation)',
    'TITLE_ABS:(medical AND imaging AND calibration AND external validation)',
    'TITLE_ABS:(medical AND imaging AND efficient AND transformer)',
]

out = Path('research/papers/candidates.json')
out.parent.mkdir(parents=True, exist_ok=True)
papers = {}
for query in QUERIES:
    params = urlencode({
        'query': f'FIRST_PDATE:[2024-01-01 TO 2026-09-29] AND OPEN_ACCESS:Y AND ({query})',
        'format': 'json', 'resultType': 'core', 'pageSize': 100,
    })
    result = subprocess.run(
        ['curl', '-fsSL', '--max-time', '45',
         f'https://www.ebi.ac.uk/europepmc/webservices/rest/search?{params}'],
        capture_output=True, text=True, check=True,
    )
    payload = json.loads(result.stdout)
    print(query, payload.get('hitCount'), flush=True)
    for paper in payload.get('resultList', {}).get('result', []):
        key = paper.get('doi') or paper.get('pmid') or paper.get('id')
        if key:
            papers[key] = paper
out.write_text(json.dumps(list(papers.values()), indent=2))
print('unique', len(papers), 'saved', out)
