import json

with open('data/dataset.json') as f:
    data = json.load(f)

print(f'Total algoritmos: {len(data["algorithms"])}')
print(f'Claves del primer algoritmo original: {list(data["algorithms"][0].keys())}')
print()
print(f'Claves del nuevo algoritmo (pos 74): {list(data["algorithms"][74].keys())}')
