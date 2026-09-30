"""Attempt lawful publisher-hosted PDF downloads for the selected catalog.

Each file is kept only when its response begins with a PDF signature. A failed
attempt is recorded; HTML error pages are never mislabeled as PDFs.
"""

import csv
import json
import subprocess
from pathlib import Path
from urllib.parse import quote

ROOT = Path('research/papers')
records = list(csv.DictReader((ROOT / 'papers.csv').open()))
raw = json.loads((ROOT / 'candidates.json').read_text())
by_doi = {x.get('doi', '').lower(): x for x in raw if x.get('doi')}
pdf_dir = ROOT / 'pdf'
pdf_dir.mkdir(exist_ok=True)
log = []

def urls_for(row):
    doi = row['doi']
    pid = row['paper_id']
    urls = []
    if pid == 'P001':
        urls.append(f'https://www.frontiersin.org/articles/{doi}/pdf')
    elif pid == 'P002':
        urls.append('https://openaccess.thecvf.com/content/ICCV2025W/CVAMD/papers/Sharshar_Not_Only_Grey_Matter_OmniBrain_for_Robust_Multimodal_Classification_of_ICCVW_2025_paper.pdf')
    elif pid == 'P003':
        urls.append('https://xbna.pku.edu.cn/EN/article/downloadArticleFile.do?attachType=PDF&id=4120')
    x = by_doi.get(doi.lower())
    if x:
        for entry in x.get('fullTextUrlList', {}).get('fullTextUrl', []):
            if entry.get('availabilityCode') == 'OA' and entry.get('documentStyle') == 'pdf' and entry.get('site') != 'Europe_PMC':
                urls.append(entry['url'])
    suffix = doi.split('/', 1)[-1]
    if doi.startswith('10.1038/'):
        urls.append(f'https://www.nature.com/articles/{suffix}.pdf')
    if doi.startswith('10.3389/'):
        urls.append(f'https://www.frontiersin.org/articles/{doi}/pdf')
    if doi.startswith('10.3390/'):
        urls.append(f'https://www.mdpi.com/{suffix}/pdf')
    if doi.startswith('10.1371/'):
        urls.append('https://journals.plos.org/plosone/article/file?id=' + quote(doi) + '&type=manuscript')
    if doi.startswith('10.1186/'):
        urls.append(f'https://link.springer.com/content/pdf/{doi}.pdf')
    if doi.startswith('10.2196/'):
        urls.append(f'https://www.jmir.org/{row["year"]}/1/e{suffix.rsplit("/",1)[-1]}/PDF')
    return list(dict.fromkeys(urls))

for row in records:
    target = pdf_dir / (row['paper_id'] + '.pdf')
    if target.exists() and target.read_bytes()[:4] == b'%PDF':
        log.append((row['paper_id'], 'downloaded', 'existing'))
        continue
    status = 'no legal direct PDF verified'
    used = ''
    for url in urls_for(row):
        result = subprocess.run(['curl', '-L', '-sS', '--max-time', '20', '-o', str(target), url], capture_output=True)
        if result.returncode == 0 and target.exists() and target.read_bytes()[:4] == b'%PDF':
            status, used = 'downloaded', url
            break
        target.unlink(missing_ok=True)
    print(row['paper_id'], status, flush=True)
    log.append((row['paper_id'], status, used))

with (ROOT / 'pdf_download_log.csv').open('w', newline='') as f:
    w = csv.writer(f); w.writerow(['paper_id', 'status', 'verified_pdf_url']); w.writerows(log)
by_id = {x['paper_id']: x for x in records}
for pid, status, url in log:
    if status == 'downloaded': by_id[pid]['pdf_path'] = f'research/papers/pdf/{pid}.pdf'
fields = list(records[0])
with (ROOT / 'papers.csv').open('w', newline='') as f:
    w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(records)
(ROOT / 'papers.json').write_text(json.dumps(records, indent=2, ensure_ascii=False)+'\n')
print('PDFs verified:', sum(s == 'downloaded' for _, s, _ in log))
