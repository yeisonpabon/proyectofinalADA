"""
Script para calcular la precisión de predicción por cada clase de complejidad.

Carga el modelo entrenado y calcula métricas detalladas por clase.
"""

import os
import json
import numpy as np
from pathlib import Path

# Importar módulos del proyecto
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.neural_network.mlp import MLP
from src.data_processing.feature_extractor import GoFeatureExtractor


def load_dataset(dataset_path, base_path):
    """Carga el dataset de algoritmos Go."""
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    code_samples = []
    labels = []
    metadata = []
    
    for algo in dataset['algorithms']:
        label = algo['complexity_class']
        path = algo['path']
        
        full_path = os.path.join(base_path, path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                code = f.read()
            code_samples.append(code)
            labels.append(label)
            metadata.append({
                'name': algo['name'],
                'path': path,
                'complexity': label
            })
    
    return code_samples, np.array(labels), metadata


def split_dataset(X, labels, test_size=0.2, random_state=42):
    """Divide dataset en train/test."""
    np.random.seed(random_state)
    n_samples = X.shape[0]
    indices = np.random.permutation(n_samples)
    
    split_idx = int(n_samples * (1 - test_size))
    
    train_indices = indices[:split_idx]
    test_indices = indices[split_idx:]
    
    X_train, X_test = X[train_indices], X[test_indices]
    y_train, y_test = labels[train_indices], labels[test_indices]
    
    return X_train, X_test, y_train, y_test, train_indices, test_indices


def calculate_metrics_per_class(predictions, y_test, complexity_labels):
    """
    Calcula precisión, recall, F1-score por clase.
    
    Args:
        predictions: Predicciones del modelo
        y_test: Etiquetas reales
        complexity_labels: Diccionario de complejidades
        
    Returns:
        dict: Métricas por clase
    """
    metrics = {}
    
    for class_id, label in complexity_labels.items():
        notation = label['notation']
        name = label['name']
        
        # Máscara para esta clase
        class_mask = y_test == class_id
        
        if class_mask.sum() == 0:
            metrics[class_id] = {
                'notation': notation,
                'name': name,
                'total_examples': 0,
                'correct_predictions': 0,
                'precision': 0.0,
                'examples': []
            }
        else:
            correct = (predictions[class_mask] == y_test[class_mask]).sum()
            total = class_mask.sum()
            precision = correct / total * 100
            
            metrics[class_id] = {
                'notation': notation,
                'name': name,
                'total_examples': int(total),
                'correct_predictions': int(correct),
                'precision': precision,
                'examples': []
            }
    
    return metrics


def main():
    """Función principal."""
    
    print("\n")
    print("=" * 70)
    print("ANÁLISIS DE PRECISIÓN POR COMPLEJIDAD")
    print("=" * 70)
    print()
    
    # Rutas
    base_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_path, 'data', 'dataset.json')
    labels_path = os.path.join(base_path, 'data', 'complexity_labels.json')
    model_path = os.path.join(base_path, 'experiments', 'models', 'mlp_complexity_classifier.npz')
    
    # Validar que el modelo existe
    if not os.path.exists(model_path):
        print(f"❌ Error: Modelo no encontrado en {model_path}")
        print("Por favor ejecuta: python train_model.py")
        return
    
    # Cargar etiquetas de complejidad
    with open(labels_path, 'r', encoding='utf-8') as f:
        complexity_data = json.load(f)
        complexity_labels = {c['class_id']: c for c in complexity_data['complexity_classes']}
    
    # 1. Cargar dataset
    print("=" * 70)
    print("CARGANDO DATASET")
    print("=" * 70)
    
    code_samples, labels, metadata = load_dataset(dataset_path, base_path)
    print(f"[OK] Algoritmos cargados: {len(code_samples)}")
    
    # 2. Extraer features
    print("\n" + "=" * 70)
    print("EXTRACCIÓN DE FEATURES")
    print("=" * 70)
    
    # IMPORTANTE: El modelo fue entrenado con max_features=171 
    # (171 TF-IDF + 25 sintácticas = 196)
    extractor = GoFeatureExtractor(max_features=171)
    X = extractor.fit_transform(code_samples)
    print(f"[OK] Features extraídas: {X.shape}")
    print(f"  (171 TF-IDF + 25 sintácticas = 196 total)")
    
    # 3. Dividir dataset
    print("\n" + "=" * 70)
    print("DIVISIÓN DEL DATASET")
    print("=" * 70)
    
    X_train, X_test, y_train, y_test, train_idx, test_idx = split_dataset(X, labels, test_size=0.2)
    print(f"[OK] Training set: {X_train.shape[0]} ejemplos")
    print(f"[OK] Test set: {X_test.shape[0]} ejemplos")
    
    # 4. Cargar modelo
    print("\n" + "=" * 70)
    print("CARGANDO MODELO")
    print("=" * 70)
    
    num_classes = len(complexity_labels)
    input_dim = X_train.shape[1]
    
    mlp = MLP(
        input_dim=input_dim,
        hidden_dims=[256, 128, 64],
        num_classes=num_classes,
        learning_rate=0.005,
        batch_size=8
    )
    
    mlp.load_weights(model_path)
    print(f"[OK] Modelo cargado desde: {model_path}")
    
    # 5. Hacer predicciones
    print("\n" + "=" * 70)
    print("REALIZANDO PREDICCIONES")
    print("=" * 70)
    
    predictions = mlp.predict(X_test)
    probabilities = mlp.predict_proba(X_test)
    
    overall_accuracy = np.mean(predictions == y_test)
    print(f"[OK] Precisión general: {overall_accuracy:.4f} ({overall_accuracy*100:.2f}%)")
    
    # 6. Calcular métricas por clase
    print("\n" + "=" * 70)
    print("MÉTRICAS POR CLASE DE COMPLEJIDAD")
    print("=" * 70 + "\n")
    
    metrics = calculate_metrics_per_class(predictions, y_test, complexity_labels)
    
    # Imprimir tabla de resultados
    print(f"{'Clase':<15} {'Nombre':<20} {'Ejemplos':<12} {'Correctas':<12} {'Precisión':<12}")
    print("-" * 71)
    
    total_examples = 0
    total_correct = 0
    
    for class_id in sorted(metrics.keys()):
        m = metrics[class_id]
        notation = m['notation']
        name = m['name']
        total = m['total_examples']
        correct = m['correct_predictions']
        precision = m['precision']
        
        total_examples += total
        total_correct += correct
        
        precision_str = f"{precision:.2f}%" if total > 0 else "N/A"
        print(f"{notation:<15} {name:<20} {total:<12} {correct:<12} {precision_str:<12}")
    
    print("-" * 71)
    overall = (total_correct / total_examples * 100) if total_examples > 0 else 0
    print(f"{'TOTAL':<15} {'':<20} {total_examples:<12} {total_correct:<12} {overall:.2f}%")
    
    # 7. Detalles por ejemplo
    print("\n" + "=" * 70)
    print("PREDICCIONES DETALLADAS POR EJEMPLO")
    print("=" * 70 + "\n")
    
    for i in range(len(predictions)):
        test_sample_idx = test_idx[i]
        meta = metadata[test_sample_idx]
        pred = predictions[i]
        true = y_test[i]
        probs = probabilities[i]
        
        correct = "[OK]" if pred == true else "[X]"
        confidence = probs[pred] * 100
        
        pred_label = complexity_labels[pred]['notation']
        true_label = complexity_labels[true]['notation']
        
        print(f"{correct} {meta['name']}")
        print(f"   Predicción: {pred_label} (confianza: {confidence:.1f}%)")
        print(f"   Real: {true_label}")
        
        # Top 3 clases predichas
        top_3_indices = np.argsort(probs)[-3:][::-1]
        print(f"   Top predicciones:")
        for idx in top_3_indices:
            print(f"     - {complexity_labels[idx]['notation']}: {probs[idx]*100:.1f}%")
        print()
    
    # 8. Estadísticas finales
    print("\n" + "=" * 70)
    print("ESTADÍSTICAS FINALES")
    print("=" * 70 + "\n")
    
    # Clases mejor y peor predichas
    best_class = max(metrics.items(), key=lambda x: x[1]['precision'] if x[1]['total_examples'] > 0 else 0)
    worst_class = min(metrics.items(), key=lambda x: x[1]['precision'] if x[1]['total_examples'] > 0 else 0)
    
    print(f"[OK] Clase mejor predicha: {best_class[1]['notation']} ({best_class[1]['name']}) - {best_class[1]['precision']:.2f}%")
    print(f"[X]  Clase peor predicha: {worst_class[1]['notation']} ({worst_class[1]['name']}) - {worst_class[1]['precision']:.2f}%")
    print(f"[OK] Precisión general: {overall_accuracy*100:.2f}%")
    print()


if __name__ == "__main__":
    main()
