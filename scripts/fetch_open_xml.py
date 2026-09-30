"""Cache Europe PMC OA JATS XML for detailed research review (Git-ignored)."""
import csv
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import xml.etree.ElementTree as ET

root=Path('research/papers'); out=root/'xml';out.mkdir(exist_ok=True)
raw=json.loads((root/'candidates.json').read_text())
by_doi={x.get('doi','').lower():x for x in raw if x.get('doi')}
rows=list(csv.DictReader((root/'papers.csv').open()))

def fetch(row):
    pid=row['paper_id'];pmcid=by_doi.get(row['doi'].lower(),{}).get('pmcid')
    if not pmcid:return pid,'no pmcid'
    path=out/f'{pid}.xml'
    if path.exists():return pid,'existing'
    url=f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML'
    p=subprocess.run(['curl','-fsSL','--max-time','30',url],capture_output=True)
    if p.returncode:return pid,'unavailable'
    try:ET.fromstring(p.stdout)
    except ET.ParseError:return pid,'invalid'
    path.write_bytes(p.stdout)
    return pid,'saved'

with ThreadPoolExecutor(max_workers=4) as pool:
    for future in as_completed(pool.submit(fetch,r) for r in rows[4:]):
        print(*future.result(),flush=True)
