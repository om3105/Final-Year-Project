"""Add navigation-only full-text section indexes from Europe PMC OA XML.

This does not infer methods or results. It gives future reviewers section
titles/IDs to verify the abstract-level notes against the actual publication.
"""
import csv
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

root=Path('research/papers')
raw=json.loads((root/'candidates.json').read_text())
by_doi={x.get('doi','').lower():x for x in raw if x.get('doi')}
rows=list(csv.DictReader((root/'papers.csv').open()))
index={}
for row in rows[4:]:
    pid=row['paper_id'];x=by_doi.get(row['doi'].lower(),{})
    pmcid=x.get('pmcid')
    if not pmcid: continue
    url=f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML'
    p=subprocess.run(['curl','-fsSL','--max-time','25',url],capture_output=True)
    if p.returncode: print(pid,'XML unavailable',flush=True);continue
    try: tree=ET.fromstring(p.stdout)
    except ET.ParseError: print(pid,'XML invalid',flush=True);continue
    sections=[]
    for sec in tree.findall('.//body//sec'):
        title=sec.find('title')
        if title is None:continue
        name=' '.join(''.join(title.itertext()).split())
        if not name:continue
        sections.append({'id':sec.attrib.get('id',''), 'title':name})
    index[pid]={'pmcid':pmcid,'url':url,'sections':sections}
    note=root/'notes'/f'{pid}.md'; text=note.read_text()
    marker='## Full-text section navigation (automatically indexed)'
    if marker in text:text=text.split(marker)[0].rstrip()+'\n'
    selected=[s for s in sections if re.search(r'data|method|experiment|model|result|evaluat|discussion|limitation|conclusion|train|fusion',s['title'],re.I)]
    if not selected:selected=sections[:12]
    lines=['',marker,'',f'[Europe PMC full-text XML]({url}). These are section pointers, not reviewed factual summaries.','']
    lines += [f"- {s['title']}"+(f" (section ID `{s['id']}`)" if s['id'] else '') for s in selected[:25]]
    note.write_text(text+'\n'.join(lines)+'\n')
    print(pid,len(sections),'sections',flush=True)
(root/'fulltext_section_index.json').write_text(json.dumps(index,indent=2,ensure_ascii=False)+'\n')
print('indexed',len(index),'papers')
