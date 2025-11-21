"""
Demo rápida del sistema de clasificación de complejidad.

Este script carga el modelo entrenado y realiza predicciones
sobre nuevos algoritmos Go.
"""

import os
import json
import numpy as np
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.neural_network.mlp import MLP
from src.data_processing.feature_extractor import GoFeatureExtractor


def demo_prediction():
    """Demostración de predicción con el modelo entrenado."""
    
    print("\n" + "=" * 70)
    print("DEMO: Sistema de Clasificación de Complejidad Computacional")
    print("=" * 70 + "\n")
    
    # Rutas
    base_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_path, 'experiments', 'models', 'mlp_complexity_classifier.npz')
    dataset_path = os.path.join(base_path, 'data', 'dataset.json')
    labels_path = os.path.join(base_path, 'data', 'complexity_labels.json')
    
    # Cargar etiquetas
    with open(labels_path, 'r') as f:
        complexity_data = json.load(f)
        complexity_labels = {c['class_id']: c for c in complexity_data['complexity_classes']}
    
    # Cargar dataset para ajustar el extractor
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
    
    code_samples = []
    for algo in dataset['algorithms']:
        code_path = os.path.join(base_path, algo['path'])
        with open(code_path, 'r') as f:
            code_samples.append(f.read())
    
    # Configurar extractor
    extractor = GoFeatureExtractor(max_features=200)
    extractor.fit(code_samples)
    
    # Crear modelo
    mlp = MLP(
        input_dim=extractor.transform([code_samples[0]]).shape[1],
        hidden_dims=[128, 64],
        num_classes=len(complexity_labels)
    )
    
    # Cargar pesos entrenados
    mlp.load_weights(model_path)
    
    print("✓ Modelo cargado exitosamente\n")
    
    # Ejemplo: Nuevo algoritmo para predecir
    new_algorithm = """
package main

// Insertion Sort
func insertionSort(arr []int) []int {
    n := len(arr)
    for i := 1; i < n; i++ {
        key := arr[i]
        j := i - 1
        for j >= 0 && arr[j] > key {
            arr[j+1] = arr[j]
            j--
        }
        arr[j+1] = key
    }
    return arr
}
"""
    
    print("Algoritmo a analizar:")
    print("-" * 70)
    print(new_algorithm)
    print("-" * 70 + "\n")
    
    # Extraer features
    X = extractor.transform([new_algorithm])
    
    # Predecir
    prediction = mlp.predict(X)[0]
    probabilities = mlp.predict_proba(X)[0]
    
    # Mostrar resultado
    predicted_class = complexity_labels[prediction]
    confidence = probabilities[prediction] * 100
    
    print(f"📊 PREDICCIÓN:")
    print(f"   Complejidad: {predicted_class['notation']}")
    print(f"   Nombre: {predicted_class['name']}")
    print(f"   Confianza: {confidence:.1f}%")
    print(f"   Descripción: {predicted_class['description']}\n")
    
    # Mostrar distribución de probabilidades
    print("Distribución de probabilidades:")
    print("-" * 70)
    sorted_probs = sorted(enumerate(probabilities), key=lambda x: x[1], reverse=True)
    for class_id, prob in sorted_probs:
        class_label = complexity_labels[class_id]
        bar_length = int(prob * 50)
        bar = "█" * bar_length
        print(f"{class_label['notation']:12} {bar:50} {prob*100:5.1f}%")
    
    print("\n" + "=" * 70)
    print("ANÁLISIS COMPLETO")
    print("=" * 70)
    print(f"\nRespuesta esperada: O(n²) (Cuadrático)")
    print(f"Razón: Insertion Sort tiene dos loops anidados.\n")
    
    # Top features importantes
    print("Top 5 features más significativas:")
    importance = extractor.get_feature_importance(X[0])
    for i, (name, value) in enumerate(importance[:5], 1):
        print(f"  {i}. {name}: {value:.4f}")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    demo_prediction()
