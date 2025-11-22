#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENTRENAR MODELO v6 - 75.86% Accuracy
Dataset limpio: 144 algoritmos
Clases: 6 (O(1), O(log n), O(n), O(n²), O(n³), O(2^n))
Sin la clase ambigua O(n log n)
"""

import json
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.neural_network.mlp import MLP

def main():
    print("=" * 80)
    print("ENTRENAMIENTO MODEL v6 - DATASET LIMPIO (144 ALGORITMOS)")
    print("=" * 80)
    
    # Cargar dataset v6
    print("\n[1/3] Cargando dataset v6...")
    with open("data/dataset.json", "r") as f:
        data = json.load(f)
    
    algorithms = data["algorithms"]
    print(f"✅ Cargados {len(algorithms)} algoritmos")
    
    # Verificar distribución
    dist = {}
    for algo in algorithms:
        cc = algo["complexity_class"]
        dist[cc] = dist.get(cc, 0) + 1
    
    names = {0: "O(1)", 1: "O(log n)", 2: "O(n)", 4: "O(n²)", 5: "O(n³)", 6: "O(2^n)"}
    print("\nDistribución:")
    for cc in sorted(dist.keys()):
        count = dist[cc]
        print(f"  {names.get(cc, f'Class {cc}'):12} {count:3}")
    
    # Extraer features
    print("\n[2/3] Extrayendo features...")
    X = np.array([algo["features"].get(k, 0) for algo in algorithms 
                  for k in ["loops", "recursion", "nested_depth"]])
    X = X.reshape(-1, 3)
    
    # Ajustar labels (mapear 0,1,2,4,5,6 → 0,1,2,3,4,5)
    y_raw = np.array([algo["complexity_class"] for algo in algorithms])
    
    # Mapeo de clases original → indices
    class_map = {0: 0, 1: 1, 2: 2, 4: 3, 5: 4, 6: 5}
    y = np.array([class_map[cc] for cc in y_raw])
    
    print(f"✅ Features shape: {X.shape}")
    print(f"✅ Labels shape: {y.shape}")
    
    # Split train/test (80/20)
    np.random.seed(42)
    indices = np.random.permutation(len(X))
    split_idx = int(0.8 * len(X))
    
    train_idx = indices[:split_idx]
    test_idx = indices[split_idx:]
    
    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]
    
    print(f"\n✅ Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Crear y entrenar modelo
    print("\n[3/3] Entrenando modelo MLP...")
    print("  - Arquitectura: 3 → 64 → 32 → 6")
    print("  - Epochs: 2000")
    print("  - Learning Rate: 0.01")
    print("  - Batch Size: 32")
    print("  - Optimizer: SGD")
    print("  - Loss: Cross-Entropy\n")
    
    model = MLP(3, [64, 32], 6)
    model.learning_rate = 0.01
    history = model.fit(
        X_train, y_train,
        X_val=X_test, y_val=y_test,
        epochs=2000,
        verbose=True
    )
    
    # Evaluación final
    train_acc = model.evaluate(X_train, y_train)
    test_acc = model.evaluate(X_test, y_test)
    
    print("\n" + "=" * 80)
    print("RESULTADOS FINALES")
    print("=" * 80)
    print(f"Train Accuracy: {train_acc*100:.2f}%")
    print(f"Test Accuracy:  {test_acc*100:.2f}%")
    
    # Guardar modelo e historial
    print("\n[GUARDANDO]")
    model.save_weights("experiments/models/mlp_complexity_classifier_220.npz")
    print("✅ Modelo guardado: experiments/models/mlp_complexity_classifier_220.npz")
    
    with open("experiments/logs/training_history_220.json", "w") as f:
        json.dump(history, f, indent=2)
    print("✅ Historial guardado: experiments/logs/training_history_220.json")
    
    print("\n" + "=" * 80)
    print("✅ ENTRENAMIENTO COMPLETADO")
    print("=" * 80)

if __name__ == "__main__":
    main()
