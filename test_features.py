import json
import os
from src.data_processing.feature_extractor import GoFeatureExtractor

with open('data/dataset.json') as f:
    ds = json.load(f)
    
codes = []
for a in ds['algorithms']:
    path = a['path']
    if os.path.exists(path):
        with open(path) as cf:
            codes.append(cf.read())

ext = GoFeatureExtractor(max_features=200)
X = ext.fit_transform(codes)
print(f'Total algorithms: {len(codes)}')
print(f'Feature dimensions: {X.shape[1]}')
print(f'Expected: TF-IDF(200) + Syntactic(26) = 226, but we have {X.shape[1]}')
