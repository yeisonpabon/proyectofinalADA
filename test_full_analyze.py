#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test completo del análisis como lo haría el GUI"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.complexity_analysis.recurrence_parser import RecurrenceParser
from src.complexity_analysis.master_theorem import MasterTheorem
from src.neural_network.mlp import MLP
import numpy as np
import re

# Cargar modelo v6
print("Cargando modelo...")
mlp = MLP(3, [64, 32], 6)
mlp.load_weights("experiments/models/mlp_complexity_classifier_220.npz")

recurrence_parser = RecurrenceParser()
master_theorem = MasterTheorem()

complexity_labels = {
    0: "O(1)",
    1: "O(log n)",
    2: "O(n)",
    3: "O(n log n)",
    4: "O(n²)",
    5: "O(2^n)"
}

def extract_v6_features(code):
    try:
        loop_count = len(re.findall(r'\b(for|while)\b', code))
        loops = min(loop_count, 5)
        
        recursion = 0
        func_defs = re.findall(r'\bfunc\s+(\w+)\s*\(', code)
        for func_name in func_defs:
            if re.search(rf'\b{func_name}\s*\(', code):
                recursion = 1
                break
        
        depth = 1
        max_indent = 0
        for line in code.split('\n'):
            indent = len(line) - len(line.lstrip())
            max_indent = max(max_indent, indent)
        depth = min(max(1, max_indent // 4 + 1), 5)
        
        features = np.array([[loops, recursion, depth]], dtype=np.float32)
        return features
        
    except Exception as e:
        print(f"Error extrayendo features: {e}")
        return None

# Código de prueba
code = """
package main

func binarySearch(arr []int, target int) int {
    left, right := 0, len(arr)-1
    
    for left <= right {
        mid := (left + right) / 2
        if arr[mid] == target {
            return mid
        } else if arr[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }
    return -1
}
"""

print("Iniciando análisis...")

try:
    # Paso 1: Detectar recursión
    print("1. Detectando recurrencia...")
    recurrence = recurrence_parser.parse(code)
    print(f"   Recurrence: {recurrence}")
    
    # Paso 2: Extraer features y predicción MLP
    print("2. Extrayendo features...")
    features = extract_v6_features(code)
    if features is not None:
        print(f"   Features: {features}")
        
        print("3. Predicción MLP...")
        prediction_probs = mlp.predict_proba(features)
        predicted_class = np.argmax(prediction_probs[0])
        mlp_confidence = prediction_probs[0][predicted_class]
        mlp_prediction = complexity_labels.get(predicted_class, "Desconocida")
        
        print(f"   Predicción: {mlp_prediction} ({mlp_confidence:.1%})")
        print(f"   Distribución: {prediction_probs}")
    
    # Paso 3: Análisis de recurrencia
    if recurrence is None:
        print("4. No se detectó recursión (iterativo)")
    else:
        print("4. Recurrencia detectada")
        print(f"   Master Theorem...")
        mt_result = master_theorem.solve(recurrence.a, recurrence.b, recurrence.f_n)
        print(f"   Resultado: {mt_result}")
    
    print("\n✓ Análisis completado sin errores")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
