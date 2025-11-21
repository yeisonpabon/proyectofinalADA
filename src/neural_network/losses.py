"""
Funciones de pérdida (loss functions) para clasificación.

Implementa cross-entropy con derivadas analíticas para backpropagation.

Complejidad:
- Cross-entropy: O(b*C) donde b=batch_size, C=num_classes
- Gradiente: O(b*C)
"""

import numpy as np


class Loss:
    """Clase base para funciones de pérdida."""
    
    def compute(self, y_pred, y_true):
        """
        Calcula la pérdida.
        
        Args:
            y_pred (np.ndarray): Predicciones
            y_true (np.ndarray): Etiquetas verdaderas
            
        Returns:
            float: Valor de pérdida
        """
        raise NotImplementedError("Debe implementarse en subclases")
    
    def gradient(self, y_pred, y_true):
        """
        Calcula el gradiente de la pérdida.
        
        Args:
            y_pred (np.ndarray): Predicciones
            y_true (np.ndarray): Etiquetas verdaderas
            
        Returns:
            np.ndarray: Gradiente
        """
        raise NotImplementedError("Debe implementarse en subclases")


class CrossEntropyLoss(Loss):
    """
    Cross-Entropy Loss para clasificación multiclase.
    
    Fórmula:
    L = -1/N * Σ Σ y_true[i,c] * log(y_pred[i,c])
    
    Donde:
    - N = batch_size
    - C = num_classes
    - y_true = one-hot encoding de etiquetas
    - y_pred = probabilidades softmax
    
    Derivación de complejidad:
    - Cálculo de log: O(N*C)
    - Suma sobre clases: O(N*C)
    - Total: O(N*C)
    
    Propiedades:
    - Convexa (único mínimo global)
    - Penaliza fuertemente predicciones confiadas incorrectas
    - Derivada combinada con softmax: y_pred - y_true (simplificación elegante)
    
    Derivación matemática de la derivada:
    Para softmax + cross-entropy:
    
    L = -Σ y_true * log(softmax(z))
    
    ∂L/∂z_i = softmax(z_i) - y_true_i
    
    Esta es una propiedad especial de esta combinación.
    """
    
    def __init__(self, epsilon=1e-15):
        """
        Args:
            epsilon (float): Pequeño valor para estabilidad numérica
                           Previene log(0) = -inf
        """
        self.epsilon = epsilon
    
    def compute(self, y_pred, y_true):
        """
        Calcula cross-entropy loss.
        
        Complejidad: O(batch_size * num_classes)
        
        Args:
            y_pred (np.ndarray): Probabilidades predichas (batch_size, num_classes)
                               Salida de softmax, valores en [0,1]
            y_true (np.ndarray): Etiquetas one-hot (batch_size, num_classes)
                               o índices de clase (batch_size,)
        
        Returns:
            float: Pérdida promedio sobre el batch
            
        Ejemplo:
            y_true = [0, 2, 1]  # Índices de clase
            y_pred = [[0.7, 0.2, 0.1],
                      [0.1, 0.3, 0.6],
                      [0.2, 0.5, 0.3]]
            
            Loss = -1/3 * (log(0.7) + log(0.6) + log(0.5))
                 ≈ 0.567
        """
        batch_size = y_pred.shape[0]
        
        # Clip predictions para estabilidad numérica
        # Previene log(0) y log(1) exactos
        y_pred_clipped = np.clip(y_pred, self.epsilon, 1 - self.epsilon)
        
        # Convertir índices a one-hot si es necesario
        if y_true.ndim == 1:
            y_true_one_hot = np.zeros_like(y_pred)
            y_true_one_hot[np.arange(batch_size), y_true] = 1
        else:
            y_true_one_hot = y_true
        
        # Cross-entropy: -Σ y_true * log(y_pred)
        # Suma sobre todas las clases y ejemplos
        loss = -np.sum(y_true_one_hot * np.log(y_pred_clipped)) / batch_size
        
        return loss
    
    def gradient(self, y_pred, y_true):
        """
        Calcula gradiente de cross-entropy respecto a predicciones.
        
        Para softmax + cross-entropy:
        ∂L/∂z = (y_pred - y_true) / batch_size
        
        Esta simplificación es una propiedad matemática especial.
        
        Complejidad: O(batch_size * num_classes)
        
        Args:
            y_pred (np.ndarray): Probabilidades predichas (batch_size, num_classes)
            y_true (np.ndarray): Etiquetas one-hot o índices
        
        Returns:
            np.ndarray: Gradiente de forma (batch_size, num_classes)
            
        Ejemplo:
            y_true = [0, 2, 1]
            y_pred = [[0.7, 0.2, 0.1],
                      [0.1, 0.3, 0.6],
                      [0.2, 0.5, 0.3]]
            
            Gradiente = [[0.7-1, 0.2-0, 0.1-0],     [[-0.3, 0.2, 0.1],
                         [0.1-0, 0.3-0, 0.6-1],  =   [0.1, 0.3, -0.4],
                         [0.2-0, 0.5-1, 0.3-0]]      [0.2, -0.5, 0.3]]
        """
        batch_size = y_pred.shape[0]
        
        # Convertir índices a one-hot si es necesario
        if y_true.ndim == 1:
            y_true_one_hot = np.zeros_like(y_pred)
            y_true_one_hot[np.arange(batch_size), y_true] = 1
        else:
            y_true_one_hot = y_true
        
        # Gradiente: (y_pred - y_true) / N
        # División por N para promedio sobre batch
        gradient = (y_pred - y_true_one_hot) / batch_size
        
        return gradient


class MSELoss(Loss):
    """
    Mean Squared Error para regresión (incluido por completitud).
    
    Fórmula:
    L = 1/(2N) * Σ (y_pred - y_true)²
    
    Derivada:
    ∂L/∂y_pred = (y_pred - y_true) / N
    
    Uso: Regresión, no recomendado para clasificación
    """
    
    def compute(self, y_pred, y_true):
        """
        Calcula MSE loss.
        
        Complejidad: O(N) donde N = número de elementos
        
        Args:
            y_pred (np.ndarray): Predicciones
            y_true (np.ndarray): Valores verdaderos
        
        Returns:
            float: Pérdida MSE promedio
        """
        return np.mean((y_pred - y_true) ** 2)
    
    def gradient(self, y_pred, y_true):
        """
        Calcula gradiente de MSE.
        
        Complejidad: O(N)
        
        Args:
            y_pred (np.ndarray): Predicciones
            y_true (np.ndarray): Valores verdaderos
        
        Returns:
            np.ndarray: Gradiente
        """
        batch_size = y_pred.shape[0]
        return 2 * (y_pred - y_true) / batch_size
