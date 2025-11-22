#!/usr/bin/env python3
"""
Script de prueba para verificar si el modelo MLP se carga correctamente
"""

import os
import sys
import json
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.neural_network.mlp import MLP
from src.data_processing.feature_extractor import GoFeatureExtractor

def test_model_loading():
    """Prueba carga del modelo y predicciones."""
    
    print("\n" + "=" * 70)
    print("PRUEBA DE CARGA DEL MODELO MLP")
    print("=" * 70 + "\n")
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_path, 'experiments', 'models', 'mlp_complexity_classifier.npz')
    dataset_path = os.path.join(base_path, 'data', 'dataset.json')
    
    # 1. Verificar archivos
    print("[1/5] Verificando archivos...")
    if not os.path.exists(model_path):
        print(f"  ❌ Modelo no encontrado: {model_path}")
        return False
    print(f"  ✓ Modelo: {model_path}")
    
    if not os.path.exists(dataset_path):
        print(f"  ❌ Dataset no encontrado: {dataset_path}")
        return False
    print(f"  ✓ Dataset: {dataset_path}")
    
    # 2. Cargar dataset
    print("\n[2/5] Cargando dataset...")
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        
        code_samples = []
        for algo in dataset['algorithms']:
            algo_path = os.path.join(base_path, algo['path'])
            if os.path.exists(algo_path):
                with open(algo_path, 'r', encoding='utf-8') as f:
                    code_samples.append(f.read())
        
        print(f"  ✓ Cargados {len(code_samples)} algoritmos")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # 3. Entrenar feature extractor
    print("\n[3/5] Entrenando feature extractor...")
    try:
        extractor = GoFeatureExtractor(max_features=200)
        extractor.fit(code_samples)
        print(f"  ✓ Features: {len(extractor.feature_names)}")
        
        # Transformar un código de prueba
        test_code = code_samples[0]
        X = extractor.transform([test_code])
        print(f"  ✓ Shape: {X.shape}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 4. Cargar modelo
    print("\n[4/5] Cargando modelo MLP...")
    try:
        input_dim = X.shape[1]
        print(f"  Input dim: {input_dim}")
        
        mlp = MLP(
            input_dim=input_dim,
            hidden_dims=[256, 128, 64],
            num_classes=6,
            learning_rate=0.001,
            batch_size=4
        )
        mlp.load_weights(model_path)
        print(f"  ✓ Modelo cargado")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 5. Hacer predicciones
    print("\n[5/5] Haciendo predicciones de prueba...")
    try:
        complexity_labels = {
            0: "O(1)",
            1: "O(log n)",
            2: "O(n)",
            3: "O(n log n)",
            4: "O(n²)",
            5: "O(2^n)"
        }
        
        # Prueba con varios algoritmos
        test_indices = [0, 1, 5, 10, 20, 30, 40, 50, 60, 70]
        
        print("\n  Pruebas de predicción:")
        for idx in test_indices:
            if idx < len(code_samples):
                X_test = extractor.transform([code_samples[idx]])
                pred = mlp.predict(X_test)[0]
                probs = mlp.predict_proba(X_test)[0]
                
                algo_name = dataset['algorithms'][idx]['name']
                predicted = complexity_labels[pred]
                confidence = probs[pred] * 100
                
                print(f"    [{idx:2d}] {algo_name:40} → {predicted} ({confidence:.1f}%)")
        
        print("\n  ✓ Predicciones funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_model_loading()
    
    if success:
        print("\n" + "=" * 70)
        print("✓ TODO FUNCIONANDO CORRECTAMENTE")
        print("=" * 70 + "\n")
    else:
        print("\n" + "=" * 70)
        print("❌ PROBLEMAS DETECTADOS")
        print("=" * 70 + "\n")
