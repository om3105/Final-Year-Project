"""Extract local research PDF text for paper-by-paper verification.

The extracted text is a temporary research aid, not a published dataset or a
replacement for reading figures and tables in the PDF.
"""
import csv
import json
from pathlib import Path
from pypdf import PdfReader

root=Path('research/papers')
out=root/'extracted_text';out.mkdir(exist_ok=True)
summary=[]
for r in csv.DictReader((root/'papers.csv').open()):
    if not r['pdf_path']:continue
    reader=PdfReader(r['pdf_path'])
    pages=[page.extract_text(extraction_mode='layout') or '' for page in reader.pages]
    text='\n\n'.join(f'[[PDF PAGE {i+1}]]\n{body}' for i,body in enumerate(pages))
    (out/f"{r['paper_id']}.txt").write_text(text)
    summary.append({'paper_id':r['paper_id'],'pages':len(pages),'chars':len(text)})
    print(r['paper_id'],len(pages),len(text),flush=True)
(out/'manifest.json').write_text(json.dumps(summary,indent=2)+'\n')
