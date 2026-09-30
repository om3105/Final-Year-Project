"""Build BibTeX from the verified catalog and Europe PMC author records."""
import csv
import json
from pathlib import Path

root=Path('research/papers')
rows=list(csv.DictReader((root/'papers.csv').open(encoding='utf-8')))
raw=json.loads((root/'candidates.json').read_text(encoding='utf-8'))
by_doi={x.get('doi','').lower():x for x in raw if x.get('doi')}

manual={
 'P001':'S. Sabari Vasan and P. Jayalakshmi',
 'P002':'Ahmed Sharshar and Yasser Ashraf and Tameem Bakr and Salma Hassan and Hosam Elgendy and Mohammad Yaqub and Mohsen Guizani',
 'P003':'Zhou Li and Yongbin Liu and Chunping Ouyang and Jiangtao Zhang and Xue Pan and Lu Jiang and Jin Zhong',
 'P004':'Qi Yu and Qian Ma and Lijuan Da and Jiahui Li and Mengying Wang and Andi Xu and Zilin Li and Wenyuan Li',
}

def bibvalue(s):
    return '{'+str(s).replace('{','\\{').replace('}','\\}').replace('%','\\%').replace('&','\\&')+'}'

def authors(row):
    if row['paper_id'] in manual:return manual[row['paper_id']]
    item=by_doi.get(row['doi'].lower(),{})
    people=item.get('authorList',{}).get('author',[])
    names=[]
    for a in people:
        first=a.get('firstName','').strip()
        last=a.get('lastName','').strip()
        name=' '.join(x for x in (first,last) if x)
        if name:names.append(name)
    return ' and '.join(names) if names else row['authors'].replace(';',' and ')

parts=[]
for row in rows:
    pid=row['paper_id']
    typ='inproceedings' if pid=='P002' else 'article'
    d={'title':row['title'],'author':authors(row),'year':row['year'],
       ('booktitle' if typ=='inproceedings' else 'journal'):row['venue'],
       'publisher':row['publisher'],'url':row['url']}
    if row['doi']:d['doi']=row['doi']
    if row['pdf_path']:d['file']=row['pdf_path']
    body='\n'.join('  '+k+' = '+bibvalue(v)+',' for k,v in d.items())
    parts.append('@'+typ+'{'+pid+',\n'+body+'\n}')
(root/'references.bib').write_text('\n\n'.join(parts)+'\n',encoding='utf-8')
print('references',len(parts))
