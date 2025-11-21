"""
Funciones de activación y capa densa (fully connected).

Implementaciones desde cero con derivadas analíticas para backpropagation.

Complejidades:
- ReLU: O(n) tiempo, O(1) espacio adicional
- Softmax: O(n) tiempo, O(n) espacio para exponenciales
- DenseLayer forward: O(b*n*m) donde b=batch_size, n=input_dim, m=output_dim
- DenseLayer backward: O(b*n*m) para gradientes
"""

import numpy as np


# =============================================================================
# FUNCIONES DE ACTIVACIÓN
# =============================================================================

def relu(x):
    """
    ReLU (Rectified Linear Unit).
    
    f(x) = max(0, x)
    
    Complejidad: O(n) donde n = número de elementos
    
    Ventajas:
    - No sufre vanishing gradient (gradiente = 1 si x > 0)
    - Computacionalmente eficiente
    - Convergencia rápida en práctica
    
    Desventajas:
    - "Dying ReLU" si x << 0 (neurona muerta)
    
    Args:
        x (np.ndarray): Entrada de cualquier forma
        
    Returns:
        np.ndarray: max(0, x) elemento por elemento
    """
    return np.maximum(0, x)


def relu_derivative(x):
    """
    Derivada de ReLU.
    
    f'(x) = 1 si x > 0, 0 si x <= 0
    
    Complejidad: O(n)
    
    Args:
        x (np.ndarray): Entrada original (pre-activación)
        
    Returns:
        np.ndarray: Gradiente (1 o 0)
    """
    return (x > 0).astype(float)


def softmax(x):
    """
    Función Softmax para clasificación multiclase.
    
    f(x_i) = exp(x_i) / Σ exp(x_j)
    
    Complejidad: O(n*C) donde C = número de clases
    
    Propiedades:
    - Σ softmax(x) = 1 (distribución de probabilidad)
    - 0 < softmax(x_i) < 1
    - Diferenciable
    
    Truco numérico: softmax(x - max(x)) para estabilidad
    Previene overflow en exp(x) si x muy grande
    
    Args:
        x (np.ndarray): Logits de forma (batch_size, num_classes)
        
    Returns:
        np.ndarray: Probabilidades de forma (batch_size, num_classes)
    """
    # Estabilidad numérica: restar max por fila
    x_shifted = x - np.max(x, axis=1, keepdims=True)
    exp_x = np.exp(x_shifted)
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


def softmax_derivative(softmax_output):
    """
    Derivada de Softmax (simplificada para uso con cross-entropy).
    
    Cuando se usa con cross-entropy, la derivada combinada es:
    ∂L/∂z = softmax(z) - y_true
    
    Esta función retorna la identidad porque la derivación
    completa se maneja en la función de pérdida.
    
    Args:
        softmax_output (np.ndarray): Salida de softmax
        
    Returns:
        np.ndarray: Mismo tamaño que entrada
    """
    return softmax_output


# =============================================================================
# CAPA DENSA (FULLY CONNECTED)
# =============================================================================

class DenseLayer:
    """
    Capa densa (fully connected) con activación opcional.
    
    Operación: y = activation(W @ x + b)
    
    Parámetros:
    - W: Pesos de forma (input_dim, output_dim)
    - b: Sesgos de forma (output_dim,)
    
    Complejidad temporal:
    - Forward: O(batch_size * input_dim * output_dim)
    - Backward: O(batch_size * input_dim * output_dim)
    
    Complejidad espacial:
    - Parámetros: O(input_dim * output_dim)
    - Activaciones: O(batch_size * output_dim)
    - Gradientes: O(input_dim * output_dim) + O(output_dim)
    """
    
    def __init__(self, input_dim, output_dim, activation='relu', initializer=None):
        """
        Inicializa la capa densa.
        
        Args:
            input_dim (int): Dimensión de entrada
            output_dim (int): Dimensión de salida (número de neuronas)
            activation (str): 'relu', 'softmax', o None
            initializer (Initializer): Objeto inicializador de pesos
        """
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.activation_name = activation
        
        # Inicializar pesos
        if initializer is None:
            from .initializers import HeInitializer
            initializer = HeInitializer()
        
        self.W = initializer.initialize((input_dim, output_dim))
        self.b = np.zeros((1, output_dim))
        
        # Seleccionar función de activación
        if activation == 'relu':
            self.activation = relu
            self.activation_derivative = relu_derivative
        elif activation == 'softmax':
            self.activation = softmax
            self.activation_derivative = softmax_derivative
        elif activation is None:
            self.activation = lambda x: x
            self.activation_derivative = lambda x: np.ones_like(x)
        else:
            raise ValueError(f"Activación desconocida: {activation}")
        
        # Cache para backpropagation
        self.input_cache = None
        self.z_cache = None  # Pre-activación
        self.output_cache = None  # Post-activación
        
        # Gradientes acumulados
        self.dW = None
        self.db = None
    
    def forward(self, X):
        """
        Forward pass de la capa.
        
        Operaciones:
        1. z = X @ W + b     [O(b*n*m)]
        2. a = activation(z) [O(b*m)]
        
        Args:
            X (np.ndarray): Entrada de forma (batch_size, input_dim)
            
        Returns:
            np.ndarray: Salida de forma (batch_size, output_dim)
        """
        self.input_cache = X
        
        # Producto matriz-matriz: O(batch_size * input_dim * output_dim)
        self.z_cache = X @ self.W + self.b
        
        # Activación: O(batch_size * output_dim)
        self.output_cache = self.activation(self.z_cache)
        
        return self.output_cache
    
    def backward(self, dA, learning_rate=0.01):
        """
        Backward pass de la capa.
        
        Calcula gradientes usando la regla de la cadena:
        dL/dW = X^T @ dZ
        dL/db = sum(dZ, axis=0)
        dL/dX = dZ @ W^T
        
        donde dZ = dA * activation'(z)
        
        Complejidad: O(batch_size * input_dim * output_dim)
        
        Args:
            dA (np.ndarray): Gradiente desde capa siguiente (batch_size, output_dim)
            learning_rate (float): Tasa de aprendizaje para actualización
            
        Returns:
            np.ndarray: Gradiente para capa anterior (batch_size, input_dim)
        """
        batch_size = self.input_cache.shape[0]
        
        # Gradiente a través de la activación
        if self.activation_name == 'softmax':
            # Para softmax + cross-entropy, dA ya incluye la derivada
            dZ = dA
        else:
            dZ = dA * self.activation_derivative(self.z_cache)
        
        # Gradientes de los parámetros
        # dW = X^T @ dZ / batch_size
        self.dW = (self.input_cache.T @ dZ) / batch_size
        
        # db = sum(dZ) / batch_size
        self.db = np.sum(dZ, axis=0, keepdims=True) / batch_size
        
        # Gradiente para capa anterior
        # dX = dZ @ W^T
        dX = dZ @ self.W.T
        
        # Actualizar pesos (SGD simple)
        self.W -= learning_rate * self.dW
        self.b -= learning_rate * self.db
        
        return dX
    
    def get_params(self):
        """
        Retorna diccionario con parámetros de la capa.
        
        Returns:
            dict: {'W': pesos, 'b': sesgos}
        """
        return {'W': self.W.copy(), 'b': self.b.copy()}
    
    def set_params(self, params):
        """
        Establece parámetros de la capa.
        
        Args:
            params (dict): {'W': pesos, 'b': sesgos}
        """
        self.W = params['W'].copy()
        self.b = params['b'].copy()
    
    def get_gradients(self):
        """
        Retorna diccionario con gradientes calculados.
        
        Returns:
            dict: {'dW': gradiente pesos, 'db': gradiente sesgos}
        """
        return {'dW': self.dW.copy(), 'db': self.db.copy()}
