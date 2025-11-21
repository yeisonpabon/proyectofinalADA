"""
Inicializadores de pesos para redes neuronales.

Implementa diferentes estrategias de inicialización:
- Xavier/Glorot: Para activaciones tanh/sigmoid
- He: Para activaciones ReLU
- Uniform: Distribución uniforme básica

Complejidad temporal: O(n*m) donde n,m son dimensiones de la matriz
Complejidad espacial: O(n*m) para almacenar los pesos
"""

import numpy as np


class Initializer:
    """Clase base para inicializadores."""
    
    def initialize(self, shape):
        """
        Inicializa una matriz de pesos.
        
        Args:
            shape (tuple): Dimensiones de la matriz (input_dim, output_dim)
            
        Returns:
            np.ndarray: Matriz de pesos inicializada
        """
        raise NotImplementedError("Debe implementarse en subclases")


class XavierInitializer(Initializer):
    """
    Inicializador Xavier/Glorot.
    
    Fórmula: W ~ U[-√(6/(n_in + n_out)), √(6/(n_in + n_out))]
    
    Derivación:
    - Mantiene varianza constante entre capas
    - Var(W) = 2/(n_in + n_out)
    - Previene vanishing/exploding gradients
    
    Uso: Activaciones tanh, sigmoid, softmax
    """
    
    def initialize(self, shape):
        """
        Inicializa con Xavier.
        
        Complejidad: O(n*m) - generación de n*m números aleatorios
        
        Args:
            shape (tuple): (input_dim, output_dim)
            
        Returns:
            np.ndarray: Matriz shape con valores Xavier
        """
        n_in, n_out = shape
        limit = np.sqrt(6.0 / (n_in + n_out))
        return np.random.uniform(-limit, limit, size=shape)


class HeInitializer(Initializer):
    """
    Inicializador He (Kaiming).
    
    Fórmula: W ~ N(0, √(2/n_in))
    
    Derivación:
    - Diseñado específicamente para ReLU
    - Compensa por neurona "muerta" (50% activaciones = 0)
    - Var(W) = 2/n_in
    
    Uso: Activaciones ReLU, Leaky ReLU
    """
    
    def initialize(self, shape):
        """
        Inicializa con He.
        
        Complejidad: O(n*m) - generación de n*m números aleatorios
        
        Args:
            shape (tuple): (input_dim, output_dim)
            
        Returns:
            np.ndarray: Matriz shape con valores He
        """
        n_in, n_out = shape
        std = np.sqrt(2.0 / n_in)
        return np.random.randn(n_in, n_out) * std


class UniformInitializer(Initializer):
    """
    Inicializador uniforme simple.
    
    Fórmula: W ~ U[-scale, scale]
    
    Uso: Experimentos básicos, debugging
    """
    
    def __init__(self, scale=0.01):
        """
        Args:
            scale (float): Rango de inicialización [-scale, scale]
        """
        self.scale = scale
    
    def initialize(self, shape):
        """
        Inicializa con distribución uniforme.
        
        Complejidad: O(n*m)
        
        Args:
            shape (tuple): (input_dim, output_dim)
            
        Returns:
            np.ndarray: Matriz shape con valores uniformes
        """
        return np.random.uniform(-self.scale, self.scale, size=shape)


class ZeroInitializer(Initializer):
    """
    Inicializador de ceros.
    
    Uso: Biases (sesgos)
    NUNCA usar para pesos (rompe simetría)
    """
    
    def initialize(self, shape):
        """
        Inicializa con ceros.
        
        Complejidad: O(n*m)
        
        Args:
            shape (tuple): Dimensiones
            
        Returns:
            np.ndarray: Matriz de ceros
        """
        return np.zeros(shape)
