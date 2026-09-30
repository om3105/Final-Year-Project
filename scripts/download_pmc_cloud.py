"""Complete missing PDFs from the official PMC OA Cloud Service."""
import csv
import json
import subprocess
from pathlib import Path

root=Path('research/papers'); rows=list(csv.DictReader((root/'papers.csv').open()))
raw=json.loads((root/'candidates.json').read_text())
by_doi={x.get('doi','').lower():x for x in raw if x.get('doi')}
log_path=root/'pdf_download_log.csv'; log=list(csv.DictReader(log_path.open()))
by_id={x['paper_id']:x for x in log}
for r in rows:
    if r['pdf_path']: continue
    x=by_doi.get(r['doi'].lower(),{})
    pmcid=x.get('pmcid') or ('PMC13454240' if r['paper_id']=='P001' else '')
    if not pmcid or x.get('isOpenAccess')=='N': continue
    target=root/'pdf'/f"{r['paper_id']}.pdf"
    for version in (1,2):
        url=f'https://pmc-oa-opendata.s3.amazonaws.com/{pmcid}.{version}/{pmcid}.{version}.pdf'
        p=subprocess.run(['curl','-L','-sS','--max-time','20','-o',str(target),url],capture_output=True)
        if p.returncode==0 and target.exists() and target.read_bytes()[:4]==b'%PDF':
            r['pdf_path']=str(target)
            by_id[r['paper_id']].update(status='downloaded',verified_pdf_url=url)
            print(r['paper_id'],'downloaded',flush=True)
            break
        target.unlink(missing_ok=True)
fields=list(rows[0])
with (root/'papers.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
(root/'papers.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
with log_path.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['paper_id','status','verified_pdf_url']);w.writeheader();w.writerows(log)
print('PDFs verified:',sum(bool(r['pdf_path']) for r in rows))
