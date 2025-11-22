#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script mejorado para entrenar con 200 algoritmos y 5000 épocas.
Versión robusta con mejor manejo de errores.
"""

import json
import os
import sys
import io
import numpy as np
from pathlib import Path

# Configurar stdout para UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from neural_network.mlp import MLP
from data_processing.feature_extractor import GoFeatureExtractor

def train_with_existing_dataset():
    """Entrena el modelo con el dataset existente (74 algoritmos reales)."""
    
    print("=" * 70)
    print("ENTRENAMIENTO AVANZADO - 5000 EPOCAS")
    print("=" * 70)
    
    # Cargar dataset actual
    print("\n[1/4] Cargando dataset...")
    with open('data/dataset.json', 'r') as f:
        dataset = json.load(f)
    
    algorithms = dataset['algorithms']
    print(f"    Total: {len(algorithms)} algoritmos")
    
    # Dividir en entrenamiento y prueba (80-20)
    train_size = int(len(algorithms) * 0.8)
    train_data = algorithms[:train_size]
    test_data = algorithms[train_size:]
    
    print(f"    Entrenamiento: {len(train_data)}")
    print(f"    Prueba: {len(test_data)}")
    
    # Extraer features usando feature extractor entrenado
    print("\n[2/4] Extrayendo features...")
    feature_extractor = GoFeatureExtractor(max_features=200)
    
    # Recolectar todos los códigos de entrenamiento
    train_codes = []
    train_indices = []
    
    for i, algo in enumerate(train_data):
        try:
            code_path = algo['path']
            if os.path.exists(code_path):
                with open(code_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                train_codes.append(code)
                train_indices.append(i)
        except Exception as e:
            pass
    
    print(f"    Codigos cargados: {len(train_codes)}")
    
    # Fit del extractor
    if train_codes:
        feature_extractor.fit(train_codes)
        print(f"    Feature extractor entrenado")
    
    # Transform
    X_train_list = feature_extractor.transform(train_codes)
    X_train = np.array(X_train_list)
    
    y_train = np.array([train_data[i]['complexity_class'] for i in train_indices])
    
    print(f"    Shape X_train: {X_train.shape}")
    print(f"    Shape y_train: {y_train.shape}")
    
    if X_train.shape[0] == 0:
        print("ERROR: No se pudieron extraer features")
        return
    
    # Entrenar modelo
    print("\n[3/4] Entrenando MLP con 5000 epocas...")
    print(f"    Arquitectura: {X_train.shape[1]} -> 256 -> 128 -> 64 -> 6")
    print(f"    Batch: 16 | Learning Rate: 0.005")
    
    try:
        mlp = MLP(
            input_dim=X_train.shape[1],
            hidden_dims=[256, 128, 64],
            num_classes=6,
            learning_rate=0.005,
            batch_size=16
        )
        
        history = mlp.fit(X_train, y_train, epochs=5000, verbose=True)
        
        # Guardar modelo
        os.makedirs('experiments/models', exist_ok=True)
        mlp.save_weights('experiments/models/mlp_complexity_classifier_5000.npz')
        print("\n    Modelo guardado: mlp_complexity_classifier_5000.npz")
        
        # Guardar historial
        os.makedirs('experiments/logs', exist_ok=True)
        with open('experiments/logs/training_history_5000.json', 'w') as f:
            json.dump(history, f)
        print("    Historial guardado: training_history_5000.json")
        
    except Exception as e:
        print(f"ERROR en entrenamiento: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Evaluación
    print("\n[4/4] Evaluando en test set...")
    test_codes = []
    test_indices = []
    
    for i, algo in enumerate(test_data):
        try:
            code_path = algo['path']
            if os.path.exists(code_path):
                with open(code_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                test_codes.append(code)
                test_indices.append(i)
        except Exception as e:
            pass
    
    if test_codes:
        X_test_list = feature_extractor.transform(test_codes)
        X_test = np.array(X_test_list)
        y_test = np.array([test_data[i]['complexity_class'] for i in test_indices])
        
        predictions = mlp.predict(X_test)
        accuracy = np.mean(predictions == y_test)
        
        print(f"    Precision: {accuracy*100:.2f}%")
        print(f"    Correctas: {np.sum(predictions == y_test)}/{len(y_test)}")
        
        # Precision por clase
        for class_id in range(6):
            mask = y_test == class_id
            if np.any(mask):
                class_acc = np.mean(predictions[mask] == y_test[mask])
                class_count = np.sum(mask)
                print(f"    Clase {class_id}: {class_acc*100:.1f}% ({class_count} ejemplos)")
    
    print("\n" + "=" * 70)
    print("ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
    print("=" * 70)

if __name__ == "__main__":
    try:
        train_with_existing_dataset()
    except Exception as e:
        print(f"\nERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
