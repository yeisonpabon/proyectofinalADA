"""
Multi-Layer Perceptron (MLP) implementado desde cero.

Arquitectura modular que combina capas densas, activaciones,
función de pérdida y optimizador para clasificación de complejidad.

Complejidad entrenamiento por época:
O((N/B) * Σ(n_i * m_i)) donde:
- N: tamaño dataset
- B: batch size
- n_i, m_i: dimensiones de cada capa

Memoria: O(Σ(n_i * m_i) + B * max(m_i))
"""

import numpy as np
from .layers import DenseLayer
from .losses import CrossEntropyLoss
from .optimizers import MiniBatchSGD
from .initializers import HeInitializer


class MLP:
    """
    Multi-Layer Perceptron para clasificación multiclase.
    
    Arquitectura típica:
    Input(d) → Dense(h1, ReLU) → Dense(h2, ReLU) → Dense(C, Softmax)
    
    Donde:
    - d: dimensión de features
    - h1, h2: neuronas en capas ocultas
    - C: número de clases
    
    Proceso de entrenamiento:
    1. Forward pass: X → ŷ
    2. Calcular loss: L(ŷ, y)
    3. Backward pass: ∇L → gradientes
    4. Actualizar pesos: θ -= η * ∇θ
    
    Derivación de complejidad:
    Forward pass para batch de tamaño B:
    - Capa 1: O(B * d * h1)
    - Capa 2: O(B * h1 * h2)
    - Capa 3: O(B * h2 * C)
    Total: O(B * (d*h1 + h1*h2 + h2*C))
    
    Backward pass: Misma complejidad (regla de la cadena)
    
    Época completa: O((N/B) * complejidad_forward)
    """
    
    def __init__(self, input_dim, hidden_dims, num_classes, 
                 learning_rate=0.01, batch_size=32):
        """
        Inicializa el MLP.
        
        Args:
            input_dim (int): Dimensión de entrada (features)
            hidden_dims (list): Lista de dimensiones de capas ocultas
                               Ejemplo: [128, 64] para 2 capas ocultas
            num_classes (int): Número de clases de salida
            learning_rate (float): Tasa de aprendizaje
            batch_size (int): Tamaño de mini-batch
            
        Ejemplo:
            mlp = MLP(
                input_dim=300,      # 300 features del código Go
                hidden_dims=[128, 64],  # 2 capas ocultas
                num_classes=7,      # 7 clases de complejidad
                learning_rate=0.01,
                batch_size=32
            )
        """
        self.input_dim = input_dim
        self.hidden_dims = hidden_dims
        self.num_classes = num_classes
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        
        # Construir arquitectura
        self.layers = []
        self._build_network()
        
        # Función de pérdida
        self.loss_fn = CrossEntropyLoss()
        
        # Optimizador
        self.optimizer = MiniBatchSGD(
            learning_rate=learning_rate,
            batch_size=batch_size
        )
        
        # Historial de entrenamiento
        self.history = {
            'train_loss': [],
            'train_accuracy': [],
            'val_loss': [],
            'val_accuracy': []
        }
    
    def _build_network(self):
        """
        Construye la arquitectura de la red.
        
        Estructura:
        - Capas ocultas: ReLU activation
        - Capa final: Softmax para clasificación
        
        Complejidad: O(L) donde L = número de capas
        """
        initializer = HeInitializer()
        
        # Primera capa oculta
        prev_dim = self.input_dim
        for hidden_dim in self.hidden_dims:
            layer = DenseLayer(
                input_dim=prev_dim,
                output_dim=hidden_dim,
                activation='relu',
                initializer=initializer
            )
            self.layers.append(layer)
            prev_dim = hidden_dim
        
        # Capa de salida con softmax
        output_layer = DenseLayer(
            input_dim=prev_dim,
            output_dim=self.num_classes,
            activation='softmax',
            initializer=initializer
        )
        self.layers.append(output_layer)
    
    def forward(self, X):
        """
        Forward pass a través de todas las capas.
        
        Complejidad: O(B * Σ(n_i * m_i)) para todas las capas
        
        Args:
            X (np.ndarray): Entrada de forma (batch_size, input_dim)
        
        Returns:
            np.ndarray: Probabilidades de forma (batch_size, num_classes)
            
        Ejemplo:
            X = np.random.randn(32, 300)  # 32 ejemplos, 300 features
            probs = mlp.forward(X)         # (32, 7) probabilidades
        """
        output = X
        for layer in self.layers:
            output = layer.forward(output)
        return output
    
    def backward(self, y_pred, y_true):
        """
        Backward pass (backpropagation) a través de todas las capas.
        
        Aplica la regla de la cadena desde la salida hasta la entrada:
        
        dL/dθ_i = dL/dy * dy/dθ_i
        
        Complejidad: O(B * Σ(n_i * m_i))
        
        Args:
            y_pred (np.ndarray): Predicciones (batch_size, num_classes)
            y_true (np.ndarray): Etiquetas verdaderas (batch_size,)
        """
        # Gradiente de la pérdida respecto a la salida
        dA = self.loss_fn.gradient(y_pred, y_true)
        
        # Propagar gradiente hacia atrás a través de las capas
        for layer in reversed(self.layers):
            dA = layer.backward(dA, self.learning_rate)
    
    def fit(self, X_train, y_train, X_val=None, y_val=None, 
            epochs=500, verbose=True):
        """
        Entrena el MLP usando mini-batch SGD.
        
        Algoritmo:
        Para cada época:
            1. Mezclar datos (shuffle)
            2. Para cada mini-batch:
                a. Forward pass
                b. Calcular loss
                c. Backward pass
                d. Actualizar pesos
            3. Evaluar en validación
            4. Guardar métricas
        
        Complejidad por época:
        O((N/B) * L * B * max(n_i * m_i)) = O(N * L * max(n_i * m_i))
        donde L = número de capas
        
        Complejidad total: O(E * N * L * max(n_i * m_i))
        donde E = número de épocas (500 mínimo)
        
        Args:
            X_train (np.ndarray): Datos de entrenamiento (N, input_dim)
            y_train (np.ndarray): Etiquetas de entrenamiento (N,)
            X_val (np.ndarray): Datos de validación (opcional)
            y_val (np.ndarray): Etiquetas de validación (opcional)
            epochs (int): Número de épocas (mínimo 500)
            verbose (bool): Mostrar progreso
            
        Returns:
            dict: Historial con pérdidas y precisiones
            
        Ejemplo:
            history = mlp.fit(
                X_train, y_train,
                X_val, y_val,
                epochs=500,
                verbose=True
            )
        """
        n_samples = X_train.shape[0]
        n_batches = max(1, n_samples // self.batch_size)  # Al menos 1 batch
        effective_batch_size = min(self.batch_size, n_samples)
        
        print(f"Iniciando entrenamiento:")
        print(f"  - Muestras: {n_samples}")
        print(f"  - Batch size: {effective_batch_size}")
        print(f"  - Batches por época: {n_batches}")
        print(f"  - Épocas: {epochs}")
        print(f"  - Learning rate: {self.learning_rate}")
        print(f"  - Arquitectura: {self.input_dim} → {' → '.join(map(str, self.hidden_dims))} → {self.num_classes}")
        print("-" * 70)
        
        for epoch in range(epochs):
            # Shuffle de datos al inicio de cada época
            indices = np.random.permutation(n_samples)
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]
            
            # Entrenamiento por mini-batches
            epoch_loss = 0.0
            for batch_idx in range(n_batches):
                # Obtener mini-batch
                start_idx = batch_idx * effective_batch_size
                end_idx = min(start_idx + effective_batch_size, n_samples)
                X_batch = X_shuffled[start_idx:end_idx]
                y_batch = y_shuffled[start_idx:end_idx]
                
                # Forward pass
                y_pred = self.forward(X_batch)
                
                # Calcular pérdida
                batch_loss = self.loss_fn.compute(y_pred, y_batch)
                epoch_loss += batch_loss
                
                # Backward pass
                self.backward(y_pred, y_batch)
            
            # Promediar pérdida de la época
            avg_loss = epoch_loss / n_batches
            self.history['train_loss'].append(avg_loss)
            
            # Calcular precisión en entrenamiento
            train_acc = self.evaluate(X_train, y_train)
            self.history['train_accuracy'].append(train_acc)
            
            # Evaluar en validación si está disponible
            if X_val is not None and y_val is not None:
                val_loss = self.loss_fn.compute(self.forward(X_val), y_val)
                val_acc = self.evaluate(X_val, y_val)
                self.history['val_loss'].append(val_loss)
                self.history['val_accuracy'].append(val_acc)
            
            # Mostrar progreso
            if verbose and (epoch + 1) % 50 == 0:
                msg = f"Época {epoch+1}/{epochs} - Loss: {avg_loss:.4f} - Acc: {train_acc:.4f}"
                if X_val is not None:
                    msg += f" - Val Loss: {val_loss:.4f} - Val Acc: {val_acc:.4f}"
                print(msg)
        
        print("-" * 70)
        print(f"Entrenamiento completado!")
        print(f"  - Loss final: {self.history['train_loss'][-1]:.4f}")
        print(f"  - Precisión final: {self.history['train_accuracy'][-1]:.4f}")
        
        return self.history
    
    def predict(self, X):
        """
        Predice clases para nuevos datos.
        
        Complejidad: O(B * Σ(n_i * m_i))
        
        Args:
            X (np.ndarray): Datos de entrada (batch_size, input_dim)
        
        Returns:
            np.ndarray: Índices de clase predichos (batch_size,)
            
        Ejemplo:
            predictions = mlp.predict(X_test)
        """
        probs = self.forward(X)
        return np.argmax(probs, axis=1)
    
    def predict_proba(self, X):
        """
        Predice probabilidades para cada clase.
        
        Args:
            X (np.ndarray): Datos de entrada (batch_size, input_dim)
        
        Returns:
            np.ndarray: Probabilidades (batch_size, num_classes)
        """
        return self.forward(X)
    
    def evaluate(self, X, y):
        """
        Evalúa precisión del modelo.
        
        Complejidad: O(N * Σ(n_i * m_i))
        
        Args:
            X (np.ndarray): Datos de entrada (N, input_dim)
            y (np.ndarray): Etiquetas verdaderas (N,)
        
        Returns:
            float: Precisión (accuracy) en [0, 1]
        """
        predictions = self.predict(X)
        accuracy = np.mean(predictions == y)
        return accuracy
    
    def save_weights(self, filepath):
        """
        Guarda los pesos del modelo.
        
        Args:
            filepath (str): Ruta donde guardar (formato .npz)
        """
        weights = {}
        for i, layer in enumerate(self.layers):
            params = layer.get_params()
            weights[f'layer_{i}_W'] = params['W']
            weights[f'layer_{i}_b'] = params['b']
        
        np.savez(filepath, **weights)
        print(f"Modelo guardado en: {filepath}")
    
    def load_weights(self, filepath):
        """
        Carga los pesos del modelo.
        
        Args:
            filepath (str): Ruta del archivo .npz
        """
        weights = np.load(filepath)
        
        for i, layer in enumerate(self.layers):
            params = {
                'W': weights[f'layer_{i}_W'],
                'b': weights[f'layer_{i}_b']
            }
            layer.set_params(params)
        
        print(f"Modelo cargado desde: {filepath}")
    
    def get_architecture_summary(self):
        """
        Retorna resumen de la arquitectura.
        
        Returns:
            str: Descripción de la arquitectura
        """
        summary = "Arquitectura del MLP:\n"
        summary += "=" * 60 + "\n"
        
        total_params = 0
        prev_dim = self.input_dim
        
        summary += f"Input: {self.input_dim} features\n"
        summary += "-" * 60 + "\n"
        
        for i, layer in enumerate(self.layers):
            n_params = layer.W.size + layer.b.size
            total_params += n_params
            
            summary += f"Capa {i+1}: {layer.input_dim} → {layer.output_dim}"
            summary += f" (Activación: {layer.activation_name})\n"
            summary += f"  Parámetros: {n_params:,}\n"
            summary += "-" * 60 + "\n"
        
        summary += f"Total de parámetros: {total_params:,}\n"
        summary += "=" * 60 + "\n"
        
        return summary
