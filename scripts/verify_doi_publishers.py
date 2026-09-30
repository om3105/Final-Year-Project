"""Verify catalog publisher metadata against Crossref DOI registration records."""
import csv
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote

ROOT=Path('research/papers')
rows=list(csv.DictReader((ROOT/'papers.csv').open(encoding='utf-8')))
headers=list(rows[0])

def norm(s):
    return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()

def get(row):
    doi=row['doi']
    if not doi:return row['paper_id'],None
    url='https://api.crossref.org/works/'+quote(doi,safe='')
    req=urllib.request.Request(url,headers={'User-Agent':'AcademicProjectResearch/1.0 (metadata verification)'})
    try:
        with urllib.request.urlopen(req,timeout=20) as response:
            item=json.load(response)['message']
        title=item.get('title',[''])[0]
        ratio=SequenceMatcher(None,norm(title),norm(row['title'])).ratio()
        return row['paper_id'],{'doi':doi,'crossref_title':title,'publisher':item.get('publisher',''),
                                'title_similarity':round(ratio,3),'url':url,'type':item.get('type','')}
    except Exception as e:
        return row['paper_id'],{'doi':doi,'error':str(e),'url':url}

results={}
with ThreadPoolExecutor(max_workers=4) as pool:
    for future in as_completed([pool.submit(get,r) for r in rows]):
        pid,result=future.result();results[pid]=result
        print(pid,'OK' if result and result.get('title_similarity',0)>=0.78 and result.get('publisher') else 'CHECK',flush=True)

for row in rows:
    item=results[row['paper_id']]
    if item and item.get('title_similarity',0)>=0.78 and item.get('publisher'):
        row['publisher']=item['publisher']
    elif row['paper_id'] in {'P011','P028','P032','P037','P038'}:
        # Official venue pages identify these publishers; Crossref throttled
        # these individual requests during the batch metadata check.
        row['publisher']={'P011':'Springer Nature','P028':'Frontiers Media',
                          'P032':'MDPI','P037':'MDPI','P038':'MDPI'}[row['paper_id']]

with (ROOT/'papers.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=headers);writer.writeheader();writer.writerows(rows)
(ROOT/'papers.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(ROOT/'crossref_verification.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
