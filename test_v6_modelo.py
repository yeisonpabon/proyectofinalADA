#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Prueba - Ensayar con el Modelo v6
Experimenta con diferentes features y ve las predicciones
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.neural_network.mlp import MLP
import numpy as np


def load_model():
    """Carga el modelo v6."""
    model_path = "experiments/models/mlp_complexity_classifier_220.npz"
    if not Path(model_path).exists():
        print(f"❌ Modelo no encontrado: {model_path}")
        return None
    
    model = MLP(input_dim=3, hidden_dims=[64, 32], num_classes=5)
    model.load_weights(model_path)
    print("✅ Modelo v6 cargado\n")
    return model


def predict_and_show(model, loops, recursion, nested_depth):
    """Predice y muestra los resultados."""
    X = np.array([[loops, recursion, nested_depth]], dtype=np.float32)
    output = model.forward(X)
    
    pred_class = int(np.argmax(output[0]))
    confidence = float(output[0][pred_class])
    
    # Mapeo de clases del modelo v6
    class_map = {0: "O(1)", 1: "O(log n)", 2: "O(n)", 3: "O(n²)", 4: "O(2^n)"}
    class_names = class_map.get(pred_class, f"Unknown({pred_class})")
    
    print(f"Input: loops={loops}, recursion={recursion}, nested_depth={nested_depth}")
    print(f"→ Predicción: {class_names} (confianza: {confidence*100:.1f}%)")
    print()


def test_suite():
    """Suite de pruebas predefinidas."""
    model = load_model()
    if not model:
        return
    
    print("=" * 70)
    print("SUITE DE PRUEBAS - MODELO v6")
    print("=" * 70)
    print()
    
    test_cases = [
        # (loops, recursion, nested_depth, descripción)
        (0, 0, 1, "Operación constante (get variable)"),
        (0, 1, 1, "Recursión terminal simple"),
        (1, 0, 1, "Un loop simple (linear search)"),
        (1, 1, 2, "Binary search (recursivo)"),
        (2, 0, 2, "Dos loops (bubble sort)"),
        (2, 1, 3, "Merge sort (recursivo con loops)"),
        (3, 0, 3, "Tres loops (triple nested)"),
        (0, 1, 3, "Recursión profunda (fibonacci)"),
        (1, 0, 2, "Un loop con anidamiento (matrix traverse)"),
        (2, 1, 2, "Two loops + recursion (hybrid)"),
    ]
    
    for loops, recursion, nested_depth, desc in test_cases:
        print(f"[CASO] {desc}")
        predict_and_show(model, loops, recursion, nested_depth)
    
    print("=" * 70)
    print("✅ Suite de pruebas completada")
    print("=" * 70)


def interactive_test():
    """Prueba interactiva personalizada."""
    model = load_model()
    if not model:
        return
    
    print("=" * 70)
    print("PRUEBA INTERACTIVA - INGRESA TUS PROPIAS FEATURES")
    print("=" * 70)
    print()
    print("Guía de Features:")
    print("  loops: 0-5 (número de bucles anidados)")
    print("  recursion: 0 o 1 (es recursivo?)")
    print("  nested_depth: 1-5 (profundidad de anidamiento)")
    print()
    
    while True:
        try:
            entrada = input("Ingresa (loops,recursion,depth) o 'salir': ").strip()
            if entrada.lower() == 'salir':
                break
            
            parts = entrada.split(',')
            if len(parts) != 3:
                print("❌ Formato incorrecto. Usa: 1,0,1")
                continue
            
            loops, recursion, nested_depth = map(float, parts)
            
            if not (0 <= loops <= 5 and recursion in [0, 1] and 1 <= nested_depth <= 5):
                print("❌ Valores fuera de rango")
                continue
            
            predict_and_show(model, loops, int(recursion), nested_depth)
            
        except ValueError:
            print("❌ Error al parsear entrada")
            continue
        except KeyboardInterrupt:
            print("\n✅ Terminado")
            break


def compare_test():
    """Compara predicciones de diferentes configuraciones."""
    model = load_model()
    if not model:
        return
    
    print("=" * 70)
    print("COMPARACIÓN - VARIANDO UN FEATURE A LA VEZ")
    print("=" * 70)
    print()
    
    print("1️⃣  Variando LOOPS (recursion=0, nested_depth=1):")
    print("-" * 70)
    for loops in range(0, 6):
        X = np.array([[loops, 0, 1]], dtype=np.float32)
        output = model.forward(X)
        pred = int(np.argmax(output[0]))
        conf = float(output[0][pred])
        class_map = {0: "O(1)", 1: "O(log n)", 2: "O(n)", 3: "O(n²)", 4: "O(2^n)"}
        class_name = class_map.get(pred, f"Unknown({pred})")
        print(f"  loops={loops} → {class_name:10s} ({conf*100:5.1f}%)")
    
    print()
    print("2️⃣  Variando RECURSION (loops=1, nested_depth=2):")
    print("-" * 70)
    for recursion in [0, 1]:
        X = np.array([[1, recursion, 2]], dtype=np.float32)
        output = model.forward(X)
        pred = int(np.argmax(output[0]))
        conf = float(output[0][pred])
        class_map = {0: "O(1)", 1: "O(log n)", 2: "O(n)", 3: "O(n²)", 4: "O(2^n)"}
        class_name = class_map.get(pred, f"Unknown({pred})")
        recursion_text = "No recursivo" if recursion == 0 else "Recursivo"
        print(f"  {recursion_text:15s} → {class_name:10s} ({conf*100:5.1f}%)")
    
    print()
    print("3️⃣  Variando NESTED_DEPTH (loops=1, recursion=1):")
    print("-" * 70)
    for depth in range(1, 6):
        X = np.array([[1, 1, depth]], dtype=np.float32)
        output = model.forward(X)
        pred = int(np.argmax(output[0]))
        conf = float(output[0][pred])
        class_map = {0: "O(1)", 1: "O(log n)", 2: "O(n)", 3: "O(n²)", 4: "O(2^n)"}
        class_name = class_map.get(pred, f"Unknown({pred})")
        print(f"  depth={depth} → {class_name:10s} ({conf*100:5.1f}%)")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "suite":
            test_suite()
        elif cmd == "compare":
            compare_test()
        elif cmd == "interactive":
            interactive_test()
        else:
            print("Comandos disponibles:")
            print("  python test_v6_modelo.py suite        → Pruebas predefinidas")
            print("  python test_v6_modelo.py compare      → Comparar features")
            print("  python test_v6_modelo.py interactive  → Prueba interactiva")
    else:
        print("=" * 70)
        print("SELECCIONA UN MODO DE PRUEBA:")
        print("=" * 70)
        print()
        print("  1. python test_v6_modelo.py suite")
        print("     → 10 casos de prueba predefinidos")
        print()
        print("  2. python test_v6_modelo.py compare")
        print("     → Comparar variaciones de features")
        print()
        print("  3. python test_v6_modelo.py interactive")
        print("     → Prueba interactiva personalizada")
        print()
