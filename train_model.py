"""
Script de entrenamiento del MLP para clasificación de complejidad.

Integra:
- Carga de dataset de algoritmos Go
- Extracción de features (TF-IDF + sintácticas)
- Entrenamiento de MLP (500+ épocas)
- Evaluación y visualización
- Guardado de modelo

Uso:
    python train_model.py
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Importar módulos del proyecto
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.neural_network.mlp import MLP
from src.data_processing.feature_extractor import GoFeatureExtractor


def load_dataset(dataset_path, base_path):
    """
    Carga el dataset de algoritmos Go.
    
    Args:
        dataset_path (str): Ruta al archivo dataset.json
        base_path (str): Ruta base del proyecto
        
    Returns:
        tuple: (code_samples, labels, metadata)
    """
    print("=" * 70)
    print("CARGANDO DATASET")
    print("=" * 70)
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    code_samples = []
    labels = []
    metadata = []
    
    for algo in dataset['algorithms']:
        # Leer archivo de código Go
        code_path = os.path.join(base_path, algo['path'])
        
        try:
            with open(code_path, 'r', encoding='utf-8') as f:
                code = f.read()
                code_samples.append(code)
                labels.append(algo['complexity_class'])
                metadata.append({
                    'id': algo['id'],
                    'name': algo['name'],
                    'complexity': algo['complexity'],
                    'recurrence': algo['recurrence']
                })
                print(f"✓ {algo['name']:30} -> {algo['complexity']:10} (Clase {algo['complexity_class']})")
        except FileNotFoundError:
            print(f"✗ Archivo no encontrado: {code_path}")
    
    print(f"\n✓ Total de algoritmos cargados: {len(code_samples)}")
    
    return code_samples, np.array(labels), metadata


def split_dataset(X, y, test_size=0.2, random_seed=777):
    """
    Divide el dataset en entrenamiento y prueba.
    
    Args:
        X (np.ndarray): Features
        y (np.ndarray): Labels
        test_size (float): Proporción para test
        random_seed (int): Semilla aleatoria
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    np.random.seed(random_seed)
    n_samples = len(X)
    indices = np.random.permutation(n_samples)
    
    n_test = int(n_samples * test_size)
    test_indices = indices[:n_test]
    train_indices = indices[n_test:]
    
    X_train = X[train_indices]
    X_test = X[test_indices]
    y_train = y[train_indices]
    y_test = y[test_indices]
    
    return X_train, X_test, y_train, y_test


def plot_training_history(history, save_path):
    """
    Grafica el historial de entrenamiento.
    
    Args:
        history (dict): Historial con pérdidas y precisiones
        save_path (str): Ruta para guardar la figura
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Pérdida
    ax1.plot(history['train_loss'], label='Train Loss', linewidth=2)
    if 'val_loss' in history and len(history['val_loss']) > 0:
        ax1.plot(history['val_loss'], label='Val Loss', linewidth=2)
    ax1.set_xlabel('Época', fontsize=12)
    ax1.set_ylabel('Pérdida (Cross-Entropy)', fontsize=12)
    ax1.set_title('Evolución de la Pérdida', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Precisión
    ax2.plot(history['train_accuracy'], label='Train Accuracy', linewidth=2, color='green')
    if 'val_accuracy' in history and len(history['val_accuracy']) > 0:
        ax2.plot(history['val_accuracy'], label='Val Accuracy', linewidth=2, color='orange')
    ax2.set_xlabel('Época', fontsize=12)
    ax2.set_ylabel('Precisión', fontsize=12)
    ax2.set_title('Evolución de la Precisión', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0, 1])
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfica guardada en: {save_path}")
    plt.close()


def evaluate_model(mlp, X_test, y_test, metadata, complexity_labels):
    """
    Evalúa el modelo y muestra resultados detallados.
    
    Args:
        mlp (MLP): Modelo entrenado
        X_test (np.ndarray): Features de test
        y_test (np.ndarray): Labels de test
        metadata (list): Metadatos de los ejemplos
        complexity_labels (dict): Mapeo de clases
    """
    print("\n" + "=" * 70)
    print("EVALUACIÓN DEL MODELO")
    print("=" * 70)
    
    predictions = mlp.predict(X_test)
    probabilities = mlp.predict_proba(X_test)
    
    accuracy = np.mean(predictions == y_test)
    print(f"\n✓ Precisión en test: {accuracy:.4f} ({accuracy*100:.2f}%)\n")
    
    print("Predicciones detalladas:")
    print("-" * 70)
    
    for i, (pred, true, probs) in enumerate(zip(predictions, y_test, probabilities)):
        correct = "✓" if pred == true else "✗"
        confidence = probs[pred] * 100
        
        pred_label = complexity_labels[pred]['notation']
        true_label = complexity_labels[true]['notation']
        
        print(f"{correct} Ejemplo {i+1}:")
        print(f"   Predicción: {pred_label} (confianza: {confidence:.1f}%)")
        print(f"   Real: {true_label}")
        print()


def main():
    """Función principal de entrenamiento."""
    
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "SISTEMA DE CLASIFICACIÓN DE COMPLEJIDAD COMPUTACIONAL" + " " * 5 + "║")
    print("║" + " " * 20 + "Entrenamiento del Modelo MLP" + " " * 20 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    
    # Rutas
    base_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_path, 'data', 'dataset.json')
    labels_path = os.path.join(base_path, 'data', 'complexity_labels.json')
    
    # Crear directorios de salida si no existen
    os.makedirs(os.path.join(base_path, 'experiments', 'models'), exist_ok=True)
    os.makedirs(os.path.join(base_path, 'experiments', 'figures'), exist_ok=True)
    os.makedirs(os.path.join(base_path, 'experiments', 'logs'), exist_ok=True)
    
    # Cargar etiquetas de complejidad
    with open(labels_path, 'r', encoding='utf-8') as f:
        complexity_data = json.load(f)
        complexity_labels = {c['class_id']: c for c in complexity_data['complexity_classes']}
    
    print(f"Clases de complejidad:")
    for class_id, label in complexity_labels.items():
        print(f"  {class_id}: {label['notation']} - {label['name']}")
    print()
    
    # 1. Cargar dataset
    code_samples, labels, metadata = load_dataset(dataset_path, base_path)
    
    # 2. Extraer features
    print("\n" + "=" * 70)
    print("EXTRACCIÓN DE FEATURES")
    print("=" * 70)
    
    extractor = GoFeatureExtractor(max_features=200)  # Más features TF-IDF
    X = extractor.fit_transform(code_samples)
    
    print(f"✓ Shape de features: {X.shape}")
    print(f"✓ Dimensión por ejemplo: {X.shape[1]}")
    
    # Mostrar features de un ejemplo
    print(f"\nTop features del primer algoritmo:")
    importance = extractor.get_feature_importance(X[0])
    for name, value in importance[:5]:
        print(f"  {name}: {value:.4f}")
    
    # 3. Dividir dataset
    print("\n" + "=" * 70)
    print("DIVISIÓN DEL DATASET")
    print("=" * 70)
    
    X_train, X_test, y_train, y_test = split_dataset(X, labels, test_size=0.2)
    
    print(f"✓ Training set: {X_train.shape[0]} ejemplos")
    print(f"✓ Test set: {X_test.shape[0]} ejemplos")
    print(f"✓ Clases en training: {np.unique(y_train)}")
    
    # 4. Crear y entrenar modelo
    print("\n" + "=" * 70)
    print("CONFIGURACIÓN DEL MODELO")
    print("=" * 70)
    
    num_classes = len(complexity_labels)
    input_dim = X_train.shape[1]
    
    mlp = MLP(
        input_dim=input_dim,
        hidden_dims=[256, 128, 64],  # 3 capas ocultas (mejor para 64 algoritmos)
        num_classes=num_classes,
        learning_rate=0.005,  # Learning rate menor para mejor generalización
        batch_size=8  # Batch más grande para dataset de 64 algoritmos
    )
    
    print(mlp.get_architecture_summary())
    
    # 5. Entrenar (2000 épocas - FASE 4 MEJORADA)
    print("\n" + "=" * 70)
    print("ENTRENAMIENTO (2000 ÉPOCAS - FASE 4 MEJORADA)")
    print("=" * 70)
    print()
    
    history = mlp.fit(
        X_train, y_train,
        X_val=X_test, y_val=y_test,
        epochs=2000,  # 2000 épocas totales (Fase 4 mejorada con 64 algoritmos)
        verbose=True
    )
    
    # 6. Evaluar modelo
    evaluate_model(mlp, X_test, y_test, metadata, complexity_labels)
    
    # 7. Guardar modelo
    model_path = os.path.join(base_path, 'experiments', 'models', 'mlp_complexity_classifier.npz')
    mlp.save_weights(model_path)
    
    # 8. Guardar historial
    history_path = os.path.join(base_path, 'experiments', 'logs', 'training_history.json')
    with open(history_path, 'w') as f:
        # Convertir arrays a listas para JSON
        history_json = {k: [float(v) for v in vals] for k, vals in history.items()}
        json.dump(history_json, f, indent=2)
    print(f"✓ Historial guardado en: {history_path}")
    
    # 9. Graficar resultados
    figure_path = os.path.join(base_path, 'experiments', 'figures', 'training_history.png')
    plot_training_history(history, figure_path)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    print(f"✓ Épocas completadas: {len(history['train_loss'])}")
    print(f"✓ Pérdida final (train): {history['train_loss'][-1]:.4f}")
    print(f"✓ Precisión final (train): {history['train_accuracy'][-1]:.4f}")
    print(f"✓ Pérdida final (test): {history['val_loss'][-1]:.4f}")
    print(f"✓ Precisión final (test): {history['val_accuracy'][-1]:.4f}")
    print(f"✓ Modelo guardado en: {model_path}")
    print("\n" + "=" * 70)
    print("¡ENTRENAMIENTO COMPLETADO CON ÉXITO!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
