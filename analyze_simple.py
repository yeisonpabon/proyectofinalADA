#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple demo script for v6 model predictions
Análisis rápido de complejidad sin GUI
"""

from src.neural_network.mlp import MLP
import numpy as np

def analyze_algorithm(loops=0, recursion=False, nested_depth=1):
    """
    Analiza complejidad de un algoritmo basado en features
    
    Args:
        loops: Número de bucles (0-5)
        recursion: ¿Es recursivo? (True/False)
        nested_depth: Profundidad de anidamiento (1-5)
    
    Returns:
        complexity_class, confidence
    """
    
    # Cargar modelo v6
    model = MLP(3, [64, 32], 6)
    model.load_weights("experiments/models/mlp_complexity_classifier_220.npz")
    
    # Mapeo de clases
    class_names = {
        0: "O(1)",
        1: "O(log n)",
        2: "O(n)",
        3: "O(n²)",
        4: "O(n³)",
        5: "O(2^n)"
    }
    
    # Preparar features
    X = np.array([[loops, 1 if recursion else 0, nested_depth]])
    
    # Hacer predicción
    output = model.forward(X)
    pred_class = np.argmax(output[0])
    confidence = output[0][pred_class]
    
    return class_names[pred_class], confidence, output[0]

def print_analysis(loops, recursion, nested_depth):
    """Imprime análisis formateado"""
    print("=" * 70)
    print("ANÁLISIS DE COMPLEJIDAD v6")
    print("=" * 70)
    print(f"Features:")
    print(f"  • Loops: {loops}")
    print(f"  • Recursion: {'Sí' if recursion else 'No'}")
    print(f"  • Nested Depth: {nested_depth}")
    print()
    
    complexity, confidence, probs = analyze_algorithm(loops, recursion, nested_depth)
    
    print(f"📊 PREDICCIÓN: {complexity}")
    print(f"💯 Confianza: {confidence*100:.1f}%")
    print()
    
    # Mostrar distribución
    class_names = {
        0: "O(1)",
        1: "O(log n)",
        2: "O(n)",
        3: "O(n²)",
        4: "O(n³)",
        5: "O(2^n)"
    }
    
    print("Distribución de probabilidades:")
    sorted_indices = np.argsort(probs)[::-1]
    for idx in sorted_indices:
        name = class_names[idx]
        prob = probs[idx]
        bar_length = int(prob * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)
        print(f"  {name:12} {bar} {prob*100:5.1f}%")
    
    print("=" * 70)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # Ejemplo predeterminado: Binary Search
        print("\n📝 Ejemplo: Binary Search")
        print_analysis(loops=1, recursion=False, nested_depth=2)
        
        print("\n📝 Ejemplo: Merge Sort")
        print_analysis(loops=1, recursion=True, nested_depth=2)
        
        print("\n📝 Ejemplo: Bubble Sort")
        print_analysis(loops=2, recursion=False, nested_depth=2)
        
        print("\n📝 Ejemplo: Fibonacci Recursivo")
        print_analysis(loops=0, recursion=True, nested_depth=3)
    
    else:
        # Argumentos de línea de comandos: loops recursion nested_depth
        try:
            loops = int(sys.argv[1])
            recursion = sys.argv[2].lower() in ['true', '1', 'yes', 'si']
            nested_depth = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            
            print_analysis(loops, recursion, nested_depth)
        except Exception as e:
            print(f"Error: {e}")
            print("Uso: python analyze_simple.py [loops] [recursion] [nested_depth]")
            print("Ej: python analyze_simple.py 1 true 2")
