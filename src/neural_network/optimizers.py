"""
Optimizadores para entrenamiento de redes neuronales.

Implementa SGD y mini-batch SGD desde cero.

Complejidad:
- SGD: O(P) donde P = número total de parámetros
- Mini-batch SGD: O(P) por batch
"""

import numpy as np


class Optimizer:
    """Clase base para optimizadores."""
    
    def __init__(self, learning_rate=0.01):
        """
        Args:
            learning_rate (float): Tasa de aprendizaje
        """
        self.learning_rate = learning_rate
    
    def update(self, params, gradients):
        """
        Actualiza parámetros usando gradientes.
        
        Args:
            params (dict): Diccionario de parámetros
            gradients (dict): Diccionario de gradientes
        """
        raise NotImplementedError("Debe implementarse en subclases")


class SGD(Optimizer):
    """
    Stochastic Gradient Descent (SGD).
    
    Regla de actualización:
    θ_new = θ_old - η * ∇L(θ)
    
    Donde:
    - θ: parámetros (pesos, sesgos)
    - η: learning rate
    - ∇L: gradiente de la función de pérdida
    
    Complejidad: O(P) por actualización
    donde P = número total de parámetros
    
    Propiedades:
    - Simple y efectivo
    - Puede escapar mínimos locales (naturaleza estocástica)
    - Convergencia ruidosa pero eventualmente converge
    
    Hiperparámetros:
    - learning_rate: Muy importante
      * Muy grande → oscilaciones, divergencia
      * Muy pequeño → convergencia lenta
      * Típico: 0.001 - 0.1
    """
    
    def __init__(self, learning_rate=0.01):
        """
        Inicializa SGD.
        
        Args:
            learning_rate (float): Tasa de aprendizaje (η)
        """
        super().__init__(learning_rate)
    
    def update(self, layers):
        """
        Actualiza parámetros de todas las capas.
        
        Para cada parámetro θ:
        θ = θ - η * dθ
        
        Complejidad: O(P) donde P = Σ(n_i * m_i) para todas las capas
        
        Args:
            layers (list): Lista de capas con atributos W, b, dW, db
        """
        for layer in layers:
            if hasattr(layer, 'W') and hasattr(layer, 'dW'):
                layer.W -= self.learning_rate * layer.dW
                layer.b -= self.learning_rate * layer.db


class MiniBatchSGD(Optimizer):
    """
    Mini-Batch Stochastic Gradient Descent.
    
    Actualización:
    θ_new = θ_old - η * (1/B) * Σ ∇L_i(θ)
    
    Donde:
    - B: batch size
    - ∇L_i: gradiente del ejemplo i
    
    Diferencia con SGD:
    - SGD: batch_size = 1 (un ejemplo a la vez)
    - Mini-batch: batch_size = B (B ejemplos promediados)
    - Batch GD: batch_size = N (todo el dataset)
    
    Ventajas de mini-batch:
    1. Más estable que SGD puro (gradientes promediados)
    2. Más rápido que batch completo
    3. Aprovecha vectorización (eficiencia GPU/CPU)
    4. Mejor generalización que batch completo
    
    Complejidad por época:
    O((N/B) * P) donde:
    - N: tamaño dataset
    - B: batch size
    - P: número de parámetros
    
    Trade-offs batch size:
    - B pequeño (16-32): Más ruidoso, mejor generalización, más iteraciones
    - B grande (256-512): Más estable, peor generalización, menos iteraciones
    - Típico: 32, 64, 128
    """
    
    def __init__(self, learning_rate=0.01, batch_size=32):
        """
        Inicializa Mini-Batch SGD.
        
        Args:
            learning_rate (float): Tasa de aprendizaje
            batch_size (int): Tamaño del mini-batch
        """
        super().__init__(learning_rate)
        self.batch_size = batch_size
    
    def update(self, layers):
        """
        Actualiza parámetros usando gradientes de mini-batch.
        
        Los gradientes ya están promediados en el backward pass,
        por lo que solo aplicamos learning rate.
        
        Complejidad: O(P) por llamada
        
        Args:
            layers (list): Lista de capas con parámetros y gradientes
        """
        for layer in layers:
            if hasattr(layer, 'W') and hasattr(layer, 'dW'):
                layer.W -= self.learning_rate * layer.dW
                layer.b -= self.learning_rate * layer.db


class SGDMomentum(Optimizer):
    """
    SGD with Momentum.
    
    Actualización:
    v_t = β * v_{t-1} + η * ∇L(θ)
    θ_new = θ_old - v_t
    
    Donde:
    - v: velocidad (acumulación de gradientes)
    - β: momentum (típicamente 0.9)
    
    Ventajas:
    - Acelera convergencia en direcciones consistentes
    - Reduce oscilaciones en direcciones de alta curvatura
    - Ayuda a escapar mínimos locales superficiales
    
    Complejidad: O(P) + O(P) almacenamiento para velocidades
    """
    
    def __init__(self, learning_rate=0.01, momentum=0.9):
        """
        Inicializa SGD con momentum.
        
        Args:
            learning_rate (float): Tasa de aprendizaje
            momentum (float): Factor de momentum β ∈ [0,1]
        """
        super().__init__(learning_rate)
        self.momentum = momentum
        self.velocities = {}  # Diccionario de velocidades por capa
    
    def update(self, layers):
        """
        Actualiza parámetros con momentum.
        
        Complejidad: O(P)
        
        Args:
            layers (list): Lista de capas
        """
        for i, layer in enumerate(layers):
            if hasattr(layer, 'W') and hasattr(layer, 'dW'):
                # Inicializar velocidades si no existen
                if i not in self.velocities:
                    self.velocities[i] = {
                        'vW': np.zeros_like(layer.W),
                        'vb': np.zeros_like(layer.b)
                    }
                
                # Actualizar velocidades
                self.velocities[i]['vW'] = (
                    self.momentum * self.velocities[i]['vW'] + 
                    self.learning_rate * layer.dW
                )
                self.velocities[i]['vb'] = (
                    self.momentum * self.velocities[i]['vb'] + 
                    self.learning_rate * layer.db
                )
                
                # Actualizar parámetros
                layer.W -= self.velocities[i]['vW']
                layer.b -= self.velocities[i]['vb']
