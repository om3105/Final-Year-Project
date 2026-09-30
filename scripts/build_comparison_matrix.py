"""Build the explicit-evidence comparison matrix; unknowns stay NOT REPORTED."""
import csv
from pathlib import Path

rows = list(csv.DictReader(open('research/papers/papers.csv', encoding='utf-8')))
cols = ['Medical images','Clinical data','Swin Transformer','Clinical Transformer','Cross-Attention','Multimodal Transformer','Explainability','SHAP','Heatmaps','Disease classification','Early detection','Multi-dataset capability','Deployment','Evaluation','Patient-level validation']

def ids(s):
    return {f'P{int(x):03d}' for x in s.split()} if s else set()

# Every nonempty cell was checked against the note's abstract/full-text section.
# A review's YES means it discusses the concept, not that it trained the model.
yes = {
 'Medical images': set(r['paper_id'] for r in rows) - ids('33 35 37'),
 'Clinical data': ids('1 2 3 4 5 6 9 11 12 13 15 16 17 19 21 22 24 27 29 30 31 33 35 36 37 40 43 46'),
 'Swin Transformer': ids('1 9 43 44'),
 'Clinical Transformer': ids('2 9 27'),
 'Cross-Attention': ids('2 3 27 40'),
 'Multimodal Transformer': ids('4 40 46'),
 'Explainability': ids('2 7 8 9 10 12 13 19 20 21 22 27 31 36 37 40'),
 'SHAP': ids('2 13 19 31'),
 'Heatmaps': ids('2 7 8 10 21 22 31'),
 'Disease classification': ids('1 2 3 4 5 7 8 9 10 11 12 13 16 21 22 23 27 28 33 35 38 40 41 42 43 45 46 48 50'),
 'Early detection': ids('17 19 20 22 29 30 33 35 42'),
 'Multi-dataset capability': ids('2 5 9 11 12 17 21 27 38 39 40 44 45 46 47 49'),
 'Evaluation': set(r['paper_id'] for r in rows),
 'Patient-level validation': ids('1 9 16 17 19 21 27 29 30 35'),
}
partial = {
 'Clinical data': ids('10 20 26 28 39 42'),
 'Clinical Transformer': ids('1'),
 'Cross-Attention': ids('9'),
 'Multimodal Transformer': ids('2 3'),
 'Explainability': ids('1 18 34'),
 'Heatmaps': ids('1 27'),
 'Early detection': ids('1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 18 21 23 24 25 26 27 28 31 32 34 36 37 38 39 40 41 43 44 45 46 47 48 49 50'),
 'Multi-dataset capability': ids('14 15 18 25 31 32 34 36 37'),
 'Deployment': ids('11 36 37 38 39 40 42 44'),
 'Patient-level validation': ids('2 5 10 13 22 23 26 40 43'),
}
no = {
 'Clinical data': ids('7 8 38 41 44 45 47 48 49 50'),
 'Cross-Attention': ids('1 5'),
 'Multimodal Transformer': ids('1 5'),
}
lines=[]
for r in rows:
    pid=r['paper_id']; vals=[]
    for c in cols:
        vals.append('YES' if pid in yes.get(c,set()) else 'PARTIAL' if pid in partial.get(c,set()) else 'NO' if pid in no.get(c,set()) else 'NOT REPORTED')
    lines.append('| '+pid+' | '+' | '.join(vals)+' |')
Path('docs/research/comparison_matrix.md').write_text(
 '# Systematic comparison matrix\n\nYES means explicit support in a reviewed source; PARTIAL means indirect or limited support; NO means an explicit incompatible architecture or scope; NOT REPORTED means the evidence was not established. A review may discuss a method without training it. Early detection is YES only for a future/prognostic outcome, while cross-sectional early-stage tasks are PARTIAL. Multi-dataset capability is not synonymous with external patient-level validation. This is a methods map, not a performance ranking.\n\n| Paper | '+' | '.join(cols)+' |\n|---|'+'---|'*len(cols)+'\n'+'\n'.join(lines)+'\n\nSee [paper notes](../../research/papers/notes) and [base selection](base_paper_selection.md) for evidence and caveats.\n',encoding='utf-8')
