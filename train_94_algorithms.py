#!/usr/bin/env python3
"""
Entrenar modelo con dataset expandido (94 algoritmos: 74 originales + 20 reales)
"""
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import sys
sys.path.insert(0, 'src')
from neural_network.mlp import MLP

# Cargar dataset
print("Cargando dataset expandido...")
with open('data/dataset.json', 'r') as f:
    data = json.load(f)

algorithms = data['algorithms']
print(f"Total algoritmos: {len(algorithms)}")

# Extraer código y etiquetas
codes = [algo['code'] for algo in algorithms]
labels = [algo['complexity'] for algo in algorithms]

# Crear mapeo de complejidades
unique_classes = sorted(set(labels))
class_to_idx = {cls: idx for idx, cls in enumerate(unique_classes)}
idx_to_class = {idx: cls for cls, idx in class_to_idx.items()}

print(f"\nClases: {unique_classes}")
print(f"Total clases: {len(unique_classes)}")

# Extraer features TF-IDF
print("\nExtrayendo features TF-IDF...")
vectorizer = TfidfVectorizer(max_features=225, ngram_range=(1, 2), max_df=0.9, min_df=1)
X = vectorizer.fit_transform(codes).toarray()
y = np.array([class_to_idx[label] for label in labels])

print(f"Features shape: {X.shape}")
print(f"Labels shape: {y.shape}")

# Split train-test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTrain: {X_train.shape[0]} ({len(X_train)/len(X)*100:.1f}%)")
print(f"Test: {X_test.shape[0]} ({len(X_test)/len(X)*100:.1f}%)")

# Distribucion en test
from collections import Counter
test_dist = Counter(y_test)
print(f"\nDistribución en test:")
for cls_idx in sorted(test_dist.keys()):
    count = test_dist[cls_idx]
    cls_name = idx_to_class[cls_idx]
    print(f"  {cls_name:10s}: {count:2d} ({count/len(y_test)*100:5.1f}%)")

# Crear y entrenar modelo
print("\n" + "="*60)
print("ENTRENAMIENTO DEL MODELO")
print("="*60)

mlp = MLP(
    input_dim=225,
    hidden_dims=[256, 128, 64],
    num_classes=len(unique_classes),
    learning_rate=0.01,
    batch_size=32
)

history = mlp.fit(
    X_train, y_train,
    epochs=2000,
    verbose=True,
    validation_split=0.2
)

# Evaluar en test
train_pred = np.argmax(mlp.predict(X_train), axis=1)
test_pred = np.argmax(mlp.predict(X_test), axis=1)

train_acc = (train_pred == y_train).mean() * 100
test_acc = (test_pred == y_test).mean() * 100

print(f"\n{'='*60}")
print("RESULTADOS")
print(f"{'='*60}")
print(f"Training Accuracy: {train_acc:.2f}%")
print(f"Test Accuracy: {test_acc:.2f}%")

# Precisión por clase en test
print(f"\nPrecisión por clase en test:")
for cls_idx in sorted(set(y_test)):
    mask = y_test == cls_idx
    if mask.sum() > 0:
        acc = (test_pred[mask] == y_test[mask]).mean() * 100
        cls_name = idx_to_class[cls_idx]
        print(f"  {cls_name:10s}: {acc:6.2f}% ({mask.sum()} ejemplos)")

# Guardar modelo
print(f"\nGuardando modelo...")
mlp.save('experiments/models/mlp_complexity_classifier_94.npz')

# Guardar historial
import json
history_dict = {
    'train_loss': [float(x) for x in history['train_loss']],
    'train_accuracy': [float(x) for x in history['train_accuracy']],
    'val_loss': [float(x) for x in history['val_loss']],
    'val_accuracy': [float(x) for x in history['val_accuracy']],
    'test_accuracy': test_acc,
    'dataset_size': len(algorithms),
    'training_config': {
        'epochs': 2000,
        'batch_size': 32,
        'learning_rate': 0.01,
        'hidden_dims': [256, 128, 64]
    }
}

with open('experiments/logs/training_history_94.json', 'w') as f:
    json.dump(history_dict, f, indent=2)

print(f"✓ Modelo guardado: experiments/models/mlp_complexity_classifier_94.npz")
print(f"✓ Historial guardado: experiments/logs/training_history_94.json")
