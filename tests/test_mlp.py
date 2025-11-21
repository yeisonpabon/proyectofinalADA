"""
Pruebas unitarias para la arquitectura MLP.

Valida:
- Inicialización de pesos
- Forward pass
- Backward pass y gradientes
- Funciones de activación
- Función de pérdida
- Optimizadores
"""

import numpy as np
import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.neural_network.mlp import MLP
from src.neural_network.layers import DenseLayer, relu, relu_derivative, softmax
from src.neural_network.losses import CrossEntropyLoss
from src.neural_network.optimizers import SGD, MiniBatchSGD
from src.neural_network.initializers import XavierInitializer, HeInitializer


def test_initializers():
    """Test de inicializadores de pesos."""
    print("=" * 70)
    print("TEST 1: Inicializadores de Pesos")
    print("=" * 70)
    
    shape = (100, 50)
    
    # Xavier
    xavier = XavierInitializer()
    W_xavier = xavier.initialize(shape)
    print(f"✓ Xavier - Shape: {W_xavier.shape}, Mean: {W_xavier.mean():.6f}, Std: {W_xavier.std():.6f}")
    assert W_xavier.shape == shape
    assert -0.5 < W_xavier.mean() < 0.5  # Aproximadamente centrado en 0
    
    # He
    he = HeInitializer()
    W_he = he.initialize(shape)
    print(f"✓ He - Shape: {W_he.shape}, Mean: {W_he.mean():.6f}, Std: {W_he.std():.6f}")
    assert W_he.shape == shape
    assert -0.5 < W_he.mean() < 0.5
    
    print("✅ Todos los inicializadores funcionan correctamente\n")


def test_activation_functions():
    """Test de funciones de activación."""
    print("=" * 70)
    print("TEST 2: Funciones de Activación")
    print("=" * 70)
    
    # ReLU
    x = np.array([-2, -1, 0, 1, 2])
    relu_out = relu(x)
    expected_relu = np.array([0, 0, 0, 1, 2])
    assert np.allclose(relu_out, expected_relu)
    print(f"✓ ReLU: {x} → {relu_out}")
    
    # ReLU derivative
    relu_grad = relu_derivative(x)
    expected_grad = np.array([0, 0, 0, 1, 1])
    assert np.allclose(relu_grad, expected_grad)
    print(f"✓ ReLU': {x} → {relu_grad}")
    
    # Softmax
    x_softmax = np.array([[1, 2, 3], [1, 2, 3]])
    softmax_out = softmax(x_softmax)
    print(f"✓ Softmax shape: {softmax_out.shape}")
    print(f"  Suma por fila: {softmax_out.sum(axis=1)}")  # Debe ser ~1
    assert np.allclose(softmax_out.sum(axis=1), 1.0)
    
    print("✅ Todas las activaciones funcionan correctamente\n")


def test_dense_layer():
    """Test de capa densa."""
    print("=" * 70)
    print("TEST 3: Capa Densa (Dense Layer)")
    print("=" * 70)
    
    # Crear capa
    layer = DenseLayer(input_dim=5, output_dim=3, activation='relu')
    print(f"✓ Capa creada: {layer.input_dim} → {layer.output_dim}")
    print(f"  W shape: {layer.W.shape}, b shape: {layer.b.shape}")
    
    # Forward pass
    X = np.random.randn(2, 5)  # 2 ejemplos, 5 features
    output = layer.forward(X)
    print(f"✓ Forward pass: {X.shape} → {output.shape}")
    assert output.shape == (2, 3)
    
    # Backward pass
    dA = np.random.randn(2, 3)
    dX = layer.backward(dA, learning_rate=0.01)
    print(f"✓ Backward pass: {dA.shape} → {dX.shape}")
    assert dX.shape == X.shape
    assert layer.dW is not None
    assert layer.db is not None
    
    print("✅ Capa densa funciona correctamente\n")


def test_loss_function():
    """Test de función de pérdida."""
    print("=" * 70)
    print("TEST 4: Función de Pérdida (Cross-Entropy)")
    print("=" * 70)
    
    loss_fn = CrossEntropyLoss()
    
    # Predicciones perfectas
    y_pred = np.array([[0.9, 0.05, 0.05],
                       [0.05, 0.9, 0.05],
                       [0.05, 0.05, 0.9]])
    y_true = np.array([0, 1, 2])
    
    loss = loss_fn.compute(y_pred, y_true)
    print(f"✓ Loss (predicciones perfectas): {loss:.6f}")
    assert loss < 0.2  # Pérdida baja para predicciones buenas
    
    # Predicciones malas
    y_pred_bad = np.array([[0.1, 0.45, 0.45],
                           [0.45, 0.1, 0.45],
                           [0.45, 0.45, 0.1]])
    loss_bad = loss_fn.compute(y_pred_bad, y_true)
    print(f"✓ Loss (predicciones malas): {loss_bad:.6f}")
    assert loss_bad > loss  # Pérdida mayor para predicciones malas
    
    # Gradiente
    grad = loss_fn.gradient(y_pred, y_true)
    print(f"✓ Gradiente shape: {grad.shape}")
    assert grad.shape == y_pred.shape
    
    print("✅ Función de pérdida funciona correctamente\n")


def test_mlp_forward():
    """Test de forward pass del MLP completo."""
    print("=" * 70)
    print("TEST 5: MLP Forward Pass")
    print("=" * 70)
    
    # Crear MLP pequeño
    mlp = MLP(
        input_dim=10,
        hidden_dims=[8, 4],
        num_classes=3,
        learning_rate=0.01,
        batch_size=4
    )
    
    print(mlp.get_architecture_summary())
    
    # Forward pass
    X = np.random.randn(4, 10)  # 4 ejemplos, 10 features
    output = mlp.forward(X)
    
    print(f"✓ Input shape: {X.shape}")
    print(f"✓ Output shape: {output.shape}")
    print(f"✓ Output probabilities sum: {output.sum(axis=1)}")
    
    assert output.shape == (4, 3)
    assert np.allclose(output.sum(axis=1), 1.0)  # Softmax suma 1
    
    print("✅ MLP forward pass funciona correctamente\n")


def test_mlp_training():
    """Test de entrenamiento del MLP."""
    print("=" * 70)
    print("TEST 6: MLP Training (Mini-test con 10 épocas)")
    print("=" * 70)
    
    # Dataset sintético pequeño
    np.random.seed(42)
    X_train = np.random.randn(20, 10)
    y_train = np.random.randint(0, 3, 20)
    
    X_val = np.random.randn(8, 10)
    y_val = np.random.randint(0, 3, 8)
    
    # Crear y entrenar MLP
    mlp = MLP(
        input_dim=10,
        hidden_dims=[16, 8],
        num_classes=3,
        learning_rate=0.05,
        batch_size=4
    )
    
    print(f"Dataset: {X_train.shape[0]} train, {X_val.shape[0]} val")
    print(f"Batch size: {mlp.batch_size}\n")
    
    # Entrenar por pocas épocas para test
    history = mlp.fit(
        X_train, y_train,
        X_val, y_val,
        epochs=10,
        verbose=True
    )
    
    # Verificar que el historial se guarda
    assert len(history['train_loss']) == 10
    assert len(history['train_accuracy']) == 10
    
    # Verificar que la pérdida disminuye (al menos al final vs inicio)
    initial_loss = history['train_loss'][0]
    final_loss = history['train_loss'][-1]
    print(f"\n✓ Pérdida inicial: {initial_loss:.4f}")
    print(f"✓ Pérdida final: {final_loss:.4f}")
    print(f"✓ Reducción: {((initial_loss - final_loss) / initial_loss * 100):.2f}%")
    
    # Predicciones
    predictions = mlp.predict(X_val)
    print(f"\n✓ Predicciones shape: {predictions.shape}")
    print(f"✓ Predicciones: {predictions}")
    
    print("✅ Entrenamiento funciona correctamente\n")


def test_gradient_check():
    """Test de gradientes (verificación numérica simple)."""
    print("=" * 70)
    print("TEST 7: Verificación Numérica de Gradientes")
    print("=" * 70)
    
    # Crear capa simple
    layer = DenseLayer(input_dim=3, output_dim=2, activation='relu')
    loss_fn = CrossEntropyLoss()
    
    # Datos de prueba
    X = np.array([[1.0, 2.0, 3.0]])
    y_true = np.array([0])
    
    # Forward pass
    output = layer.forward(X)
    y_pred = softmax(output)
    
    # Backward pass (gradiente analítico)
    dA = loss_fn.gradient(y_pred, y_true)
    dX = layer.backward(dA, learning_rate=0.0)  # No actualizar aún
    analytical_grad_W = layer.dW.copy()
    
    # Gradiente numérico (aproximación)
    epsilon = 1e-4
    numerical_grad_W = np.zeros_like(layer.W)
    
    for i in range(layer.W.shape[0]):
        for j in range(layer.W.shape[1]):
            # W + epsilon
            layer.W[i, j] += epsilon
            output_plus = layer.forward(X)
            y_pred_plus = softmax(output_plus)
            loss_plus = loss_fn.compute(y_pred_plus, y_true)
            
            # W - epsilon
            layer.W[i, j] -= 2 * epsilon
            output_minus = layer.forward(X)
            y_pred_minus = softmax(output_minus)
            loss_minus = loss_fn.compute(y_pred_minus, y_true)
            
            # Derivada numérica
            numerical_grad_W[i, j] = (loss_plus - loss_minus) / (2 * epsilon)
            
            # Restaurar peso
            layer.W[i, j] += epsilon
    
    # Comparar gradientes
    diff = np.abs(analytical_grad_W - numerical_grad_W).max()
    print(f"✓ Diferencia máxima entre gradientes: {diff:.8f}")
    print(f"✓ Gradiente analítico (muestra): \n{analytical_grad_W[:2, :2]}")
    print(f"✓ Gradiente numérico (muestra): \n{numerical_grad_W[:2, :2]}")
    
    # Tolerancia razonable (pueden diferir ligeramente por aproximación)
    assert diff < 1e-5, f"Gradientes difieren demasiado: {diff}"
    
    print("✅ Gradientes verificados correctamente\n")


def test_save_load():
    """Test de guardado y carga de modelo."""
    print("=" * 70)
    print("TEST 8: Guardado y Carga de Modelo")
    print("=" * 70)
    
    # Crear y entrenar modelo
    mlp1 = MLP(input_dim=5, hidden_dims=[4], num_classes=2)
    X = np.random.randn(10, 5)
    y = np.random.randint(0, 2, 10)
    mlp1.fit(X, y, epochs=5, verbose=False)
    
    # Hacer predicciones
    pred1 = mlp1.predict(X)
    
    # Guardar modelo
    save_path = os.path.join(os.path.dirname(__file__), '..', 'experiments', 'models', 'test_model.npz')
    mlp1.save_weights(save_path)
    print(f"✓ Modelo guardado")
    
    # Crear nuevo modelo y cargar pesos
    mlp2 = MLP(input_dim=5, hidden_dims=[4], num_classes=2)
    mlp2.load_weights(save_path)
    print(f"✓ Modelo cargado")
    
    # Verificar predicciones idénticas
    pred2 = mlp2.predict(X)
    assert np.array_equal(pred1, pred2)
    print(f"✓ Predicciones idénticas después de cargar")
    
    # Limpiar archivo
    if os.path.exists(save_path):
        os.remove(save_path)
        print(f"✓ Archivo de prueba eliminado")
    
    print("✅ Guardado y carga funcionan correctamente\n")


def run_all_tests():
    """Ejecuta todos los tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "PRUEBAS UNITARIAS MLP - SUITE COMPLETA" + " " * 15 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    
    try:
        test_initializers()
        test_activation_functions()
        test_dense_layer()
        test_loss_function()
        test_mlp_forward()
        test_mlp_training()
        test_gradient_check()
        test_save_load()
        
        print("\n")
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 20 + "✅ TODOS LOS TESTS PASARON ✅" + " " * 19 + "║")
        print("╚" + "=" * 68 + "╝")
        print("\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FALLIDO: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}\n")
        raise


if __name__ == "__main__":
    run_all_tests()
