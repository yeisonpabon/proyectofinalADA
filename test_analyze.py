#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script para verificar si _analyze_code funciona"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.neural_network.mlp import MLP
import numpy as np
import re

# Cargar modelo v6
model = MLP(3, [64, 32], 6)
model.load_weights("experiments/models/mlp_complexity_classifier_220.npz")

# Función para extraer features (igual a GUI)
def extract_v6_features(code):
    try:
        # Feature 1: Contar loops (for, while)
        loop_count = len(re.findall(r'\b(for|while)\b', code))
        loops = min(loop_count, 5)
        
        # Feature 2: Detectar recursión
        recursion = 0
        func_defs = re.findall(r'\bfunc\s+(\w+)\s*\(', code)
        for func_name in func_defs:
            if re.search(rf'\b{func_name}\s*\(', code):
                recursion = 1
                break
        
        # Feature 3: Profundidad
        depth = 1
        max_indent = 0
        for line in code.split('\n'):
            indent = len(line) - len(line.lstrip())
            max_indent = max(max_indent, indent)
        depth = min(max(1, max_indent // 4 + 1), 5)
        
        features = np.array([[loops, recursion, depth]], dtype=np.float32)
        return features
        
    except Exception as e:
        print(f"Error: {e}")
        return None

# Test código
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

print("Extrayendo features...")
features = extract_v6_features(code)
if features is not None:
    print(f"Features: {features}")
    
    print("Haciendo predicción...")
    probs = model.predict_proba(features)
    print(f"Probabilidades: {probs}")
    
    pred_class = np.argmax(probs[0])
    confidence = probs[0][pred_class]
    
    classes = {0: "O(1)", 1: "O(log n)", 2: "O(n)", 3: "O(n²)", 4: "O(n³)", 5: "O(2^n)"}
    print(f"\nPredicción: {classes[pred_class]} ({confidence*100:.1f}%)")
else:
    print("Error extrayendo features")
