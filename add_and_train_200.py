#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v5: Agregar 30 O(1) + Rebalancear dataset
- Usa v2 base (114 algoritmos - estable)
- Agrega 30 nuevos O(1) sintéticos
- Total: 144 algoritmos con distribución balanceada
"""

import json
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.neural_network.mlp import MLP

# 30 nuevos O(1)
NEW_O1 = [
    {"id": "first", "name": "First", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "last", "name": "Last", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "get_at", "name": "GetAt", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "set_at", "name": "SetAt", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "swap", "name": "Swap", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "add", "name": "Add", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "sub", "name": "Sub", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "mul", "name": "Mul", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "div", "name": "Div", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "mod", "name": "Mod", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "greater", "name": "Greater", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "abs", "name": "Abs", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "max2", "name": "Max2", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "min2", "name": "Min2", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "is_even", "name": "IsEven", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "negate", "name": "Negate", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "length", "name": "Length", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "capacity", "name": "Capacity", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "make_pair", "name": "MakePair", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "get_age", "name": "GetAge", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "set_age", "name": "SetAge", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "same_string", "name": "SameString", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "first_char", "name": "FirstChar", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "to_float", "name": "ToFloat", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "not", "name": "Not", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "bit_and", "name": "BitAnd", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "bit_or", "name": "BitOr", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "bit_xor", "name": "BitXor", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "shift_right", "name": "ShiftRight", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
    {"id": "shift_left", "name": "ShiftLeft", "complexity_class": 0, "features": {"loops": 0, "recursion": False, "nested_depth": 1}},
]

def main():
    print("=" * 80)
    print("v5: AGREGAR 30 O(1) + REBALANCEAR DATASET")
    print("=" * 80)
    
    # Cargar v2 base
    print("\n[1/4] Cargando dataset v2 (114 algoritmos)...")
    with open("data/dataset.json", "r") as f:
        data = json.load(f)
    
    v2_algorithms = data["algorithms"][:114]
    print(f"✓ Cargados {len(v2_algorithms)} algoritmos")
    
    # Agregar 30 O(1)
    print("\n[2/4] Agregando 30 nuevos O(1)...")
    combined = v2_algorithms + NEW_O1
    print(f"✓ Total: {len(combined)} algoritmos")
    
    # Distribución
    print("\n[3/4] Análisis de distribución...")
    dist = {}
    for algo in combined:
        cc = algo.get("complexity_class", 2)
        dist[cc] = dist.get(cc, 0) + 1
    
    names = {0: "O(1)", 1: "O(log n)", 2: "O(n)", 3: "O(n log n)", 4: "O(n²)", 5: "O(n³)", 6: "O(2^n)"}
    total = len(combined)
    print("\nDistribución final:")
    for cc in sorted(dist.keys()):
        pct = 100.0 * dist[cc] / total
        print(f"  {names.get(cc, f'C{cc}')}: {dist[cc]:3d} ({pct:5.1f}%)")
    print(f"  TOTAL: {total} algoritmos")
    
    # Preparar features
    print("\n[4/4] Preparando features...")
    X_list, y_list = [], []
    for algo in combined:
        feat = algo.get("features", {})
        X_list.append([
            float(feat.get("loops", 0)),
            float(feat.get("recursion", False)),
            float(feat.get("nested_depth", 1))
        ])
        y_list.append(algo.get("complexity_class", 2))
    
    X = np.array(X_list)
    y = np.array(y_list)
    
    # Train/Test split
    np.random.seed(42)
    idx = np.arange(len(X))
    np.random.shuffle(idx)
    train_size = int(0.8 * len(X))
    
    X_train, X_test = X[idx[:train_size]], X[idx[train_size:]]
    y_train, y_test = y[idx[:train_size]], y[idx[train_size:]]
    
    print(f"✓ Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Entrenar
    print("\n" + "=" * 80)
    print("ENTRENAMIENTO")
    print("=" * 80)
    
    n_classes = len(np.unique(y_train))
    model = MLP(input_dim=3, hidden_dims=[64, 32], num_classes=n_classes)
    
    history = model.fit(X_train, y_train, X_val=X_test, y_val=y_test, epochs=2000, verbose=True)
    
    # Evaluación
    train_preds = np.argmax(model.forward(X_train), axis=1)
    test_preds = np.argmax(model.forward(X_test), axis=1)
    
    train_acc = np.mean(train_preds == y_train)
    test_acc = np.mean(test_preds == y_test)
    
    print("\n" + "=" * 80)
    print("RESULTADOS")
    print("=" * 80)
    print(f"\nAccuracy:")
    print(f"  Train: {train_acc * 100:.2f}%")
    print(f"  Test:  {test_acc * 100:.2f}%")
    
    # Guardar
    print("\n[Guardando...]")
    model.save_weights("experiments/models/mlp_complexity_classifier_200.npz")
    print(f"✓ Modelo guardado")
    
    with open("experiments/logs/training_history_200.json", "w") as f:
        json.dump(history, f, indent=2)
    print(f"✓ History guardado")
    
    # Resumen
    print("\n" + "=" * 80)
    print("COMPARATIVA")
    print("=" * 80)
    print(f"""
  Versión   Algoritmos   Test Acc   Nota
  ──────────────────────────────────────
  v1            74       93.33%    Misleading
  v2           114       61.29%    ✓ Optimal
  v3           134       57.14%    Degraded
  v4           154       48.72%    Unbalanced
  v5           144       {test_acc*100:5.2f}%    Rebalanced
  ──────────────────────────────────────
    """)
    
    print("\n" + "=" * 80)
    print("✅ COMPLETADO")
    print("=" * 80)

if __name__ == "__main__":
    main()
