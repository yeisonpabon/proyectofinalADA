#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo - Demostración interactiva del modelo v6 (ÓPTIMO)
Clasifica algoritmos en tiempo real usando el modelo entrenado.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.neural_network.mlp import MLP
import numpy as np


def load_model():
    """Carga el modelo v6 entrenado."""
    model_path = "experiments/models/mlp_complexity_classifier_220.npz"
    
    if not Path(model_path).exists():
        print(f"\n❌ ERROR: Modelo no encontrado en {model_path}")
        print("Ejecuta primero: python add_and_train_220.py")
        sys.exit(1)
    
    # Crear modelo con arquitectura fija
    model = MLP(input_dim=3, hidden_dims=[64, 32], num_classes=5)
    model.load_weights(model_path)
    print(f"✓ Modelo v6 cargado exitosamente")
    return model


def load_dataset():
    """Carga el dataset para referencia."""
    with open("data/dataset.json", "r") as f:
        data = json.load(f)
    return data["algorithms"]


def predict(model, features):
    """Predice la complejidad de un algoritmo."""
    X = np.array([features], dtype=np.float32)
    output = model.forward(X)
    prediction = np.argmax(output[0])
    confidence = output[0][prediction]
    return prediction, confidence, output[0]


def complexity_name(class_id):
    """Convierte ID de clase a nombre legible."""
    names = {
        0: "O(1)",
        1: "O(log n)",
        2: "O(n)",
        3: "O(n log n)",
        4: "O(n²)",
        5: "O(n³)",
        6: "O(2^n)"
    }
    return names.get(class_id, f"Unknown({class_id})")


def demo_interactive():
    """Demostración interactiva."""
    print("\n" + "=" * 80)
    print("DEMO INTERACTIVA - CLASIFICADOR DE COMPLEJIDAD (v6 - 75.86%)")
    print("=" * 80)
    
    model = load_model()
    algorithms = load_dataset()
    
    print("\n📚 Ejemplos del dataset cargados")
    print(f"   Total: {len(algorithms)} algoritmos")
    
    # Class names
    complexity_classes = {
        0: "O(1)",
        1: "O(log n)",
        2: "O(n)",
        4: "O(n²)",
        6: "O(2^n)"
    }
    
    print("\n" + "=" * 80)
    print("INGRESA FEATURES DE UN ALGORITMO")
    print("=" * 80)
    print("""
Features esperados:
  - loops: Número de bucles anidados (0-5)
  - recursion: 1 si es recursivo, 0 si no
  - nested_depth: Profundidad de anidamiento (1-5)

Ejemplos:
  Algoritmo lineal:     loops=1, recursion=0, nested_depth=1
  Algoritmo recursivo:  loops=1, recursion=1, nested_depth=2
  Sort (merge):         loops=2, recursion=1, nested_depth=3
  Algoritmo constante:  loops=0, recursion=0, nested_depth=1
    """)
    
    while True:
        try:
            # Input
            loops = float(input("\nLoops (0-5): "))
            recursion = float(input("Recursion (0 o 1): "))
            nested_depth = float(input("Nested Depth (1-5): "))
            
            # Validar
            if loops < 0 or loops > 5:
                print("⚠️ Loops debe estar entre 0 y 5")
                continue
            if recursion not in [0, 1]:
                print("⚠️ Recursion debe ser 0 o 1")
                continue
            if nested_depth < 1 or nested_depth > 5:
                print("⚠️ Nested Depth debe estar entre 1 y 5")
                continue
            
            # Predecir
            features = [loops, recursion, nested_depth]
            pred_class, confidence, probabilities = predict(model, features)
            
            # Mostrar resultado
            print("\n" + "=" * 80)
            print("PREDICCIÓN")
            print("=" * 80)
            print(f"\n✅ Complejidad predicha: {complexity_name(pred_class)}")
            print(f"   Confianza: {confidence * 100:.2f}%")
            
            print("\nDistribución de probabilidades:")
            class_names = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)", "O(n³)", "O(2^n)"]
            for i, prob in enumerate(probabilities[:5]):  # Solo primeras 5 clases
                bar = "█" * int(prob * 50)
                print(f"  {class_names[i]:10s}: {bar:<50s} {prob * 100:5.1f}%")
            
            print("\n" + "-" * 80)
            
        except ValueError:
            print("⚠️ Input inválido. Intenta nuevamente.")
            continue
        except KeyboardInterrupt:
            print("\n\n✓ Demo finalizada")
            break


def demo_automatic():
    """Demostración automática con ejemplos."""
    print("\n" + "=" * 80)
    print("DEMO AUTOMÁTICA - CLASIFICADOR DE COMPLEJIDAD (v6)")
    print("=" * 80)
    
    model = load_model()
    algorithms = load_dataset()[:10]  # Primeros 10 algoritmos
    
    print(f"\n📊 Clasificando {len(algorithms)} algoritmos del dataset...\n")
    
    for algo in algorithms:
        features = algo.get("features", {})
        X_input = [
            float(features.get("loops", 0)),
            float(features.get("recursion", False)),
            float(features.get("nested_depth", 1))
        ]
        
        pred_class, confidence, _ = predict(model, X_input)
        actual_class = algo.get("complexity_class", -1)
        actual_name = complexity_name(actual_class)
        pred_name = complexity_name(pred_class)
        
        match = "✅" if pred_class == actual_class else "❌"
        
        print(f"{match} {algo['name']:20s} | Actual: {actual_name:10s} | "
              f"Predicho: {pred_name:10s} ({confidence*100:5.1f}%)")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        demo_automatic()
    else:
        demo_interactive()
