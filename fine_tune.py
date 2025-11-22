"""
Fine-tuning incremental del modelo MLP existente con early stopping y menor learning rate.

Objetivos:
- Cargar dataset y extractor (mismas features que entrenamiento principal)
- Cargar pesos previos del modelo base
- Reducir learning rate y aplicar input dropout ligero para mejor generalización
- Early stopping basado en val_loss con paciencia configurable
- Reportar métricas específicas de la clase O(log n): precision, recall, F1

Uso:
    python fine_tune.py --epochs 400 --patience 30 --lr 0.001 --dropout 0.1

"""

import os
import json
import argparse
import numpy as np
from pathlib import Path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.neural_network.mlp import MLP
from src.data_processing.feature_extractor import GoFeatureExtractor


def load_dataset(dataset_path, base_path):
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    code_samples, labels = [], []
    for algo in dataset['algorithms']:
        code_path = os.path.join(base_path, algo['path'])
        try:
            with open(code_path, 'r', encoding='utf-8') as cf:
                code_samples.append(cf.read())
                labels.append(algo['complexity_class'])
        except FileNotFoundError:
            pass
    return code_samples, np.array(labels)


def split_dataset(X, y, test_size=0.2, seed=2025):
    np.random.seed(seed)
    idx = np.random.permutation(len(X))
    n_test = int(len(X) * test_size)
    test_idx = idx[:n_test]
    train_idx = idx[n_test:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


def apply_input_dropout(X_batch, rate):
    if rate <= 0:
        return X_batch
    mask = (np.random.rand(*X_batch.shape) >= rate).astype(X_batch.dtype)
    # Escalar para mantener magnitud esperada
    return X_batch * mask / (1 - rate)


def class_metrics(y_true, y_pred, target_class):
    tp = np.sum((y_pred == target_class) & (y_true == target_class))
    fp = np.sum((y_pred == target_class) & (y_true != target_class))
    fn = np.sum((y_pred != target_class) & (y_true == target_class))
    precision = tp / (tp + fp + 1e-9)
    recall = tp / (tp + fn + 1e-9)
    f1 = 2 * precision * recall / (precision + recall + 1e-9)
    return precision, recall, f1, tp, fp, fn


def confusion_matrix(y_true, y_pred, num_classes):
    cm = np.zeros((num_classes, num_classes), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1
    return cm


def fine_tune(args):
    base_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_path, 'data', 'dataset.json')
    labels_path = os.path.join(base_path, 'data', 'complexity_labels.json')
    model_path = os.path.join(base_path, 'experiments', 'models', 'mlp_complexity_classifier.npz')

    with open(labels_path, 'r', encoding='utf-8') as f:
        complexity_data = json.load(f)
        complexity_labels = {c['class_id']: c for c in complexity_data['complexity_classes']}
    num_classes = len(complexity_labels)

    code_samples, labels = load_dataset(dataset_path, base_path)
    extractor = GoFeatureExtractor(max_features=200)
    X = extractor.fit_transform(code_samples)

    X_train, X_val, y_train, y_val = split_dataset(X, labels, test_size=0.2, seed=args.seed)

    # Model with lower LR
    mlp = MLP(
        input_dim=X_train.shape[1],
        hidden_dims=[256, 128, 64],
        num_classes=num_classes,
        learning_rate=args.lr,
        batch_size=args.batch_size
    )
    # Load previous weights if available
    if os.path.exists(model_path):
        mlp.load_weights(model_path)
    else:
        print('No se encontraron pesos previos, se entrenará desde cero.')

    print('\nINICIO FINE-TUNE')
    print(f'Epochs objetivo: {args.epochs}, Patience: {args.patience}, LR: {args.lr}, Dropout entrada: {args.dropout}')

    best_val_loss = float('inf')
    best_weights = None
    patience_counter = 0

    history = {
        'train_loss': [], 'train_accuracy': [],
        'val_loss': [], 'val_accuracy': []
    }

    for epoch in range(1, args.epochs + 1):
        # Shuffle
        indices = np.random.permutation(len(X_train))
        X_train_sh = X_train[indices]
        y_train_sh = y_train[indices]

        # Mini-batch loop
        n_batches = max(1, len(X_train_sh) // mlp.batch_size)
        epoch_loss = 0.0
        for b in range(n_batches):
            start = b * mlp.batch_size
            end = min(start + mlp.batch_size, len(X_train_sh))
            X_batch = X_train_sh[start:end]
            y_batch = y_train_sh[start:end]
            # Apply input dropout
            X_batch_dp = apply_input_dropout(X_batch, args.dropout)
            y_pred = mlp.forward(X_batch_dp)
            batch_loss = mlp.loss_fn.compute(y_pred, y_batch)
            epoch_loss += batch_loss
            mlp.backward(y_pred, y_batch)

        avg_loss = epoch_loss / n_batches
        train_acc = mlp.evaluate(X_train, y_train)
        val_loss = mlp.loss_fn.compute(mlp.forward(X_val), y_val)
        val_acc = mlp.evaluate(X_val, y_val)

        history['train_loss'].append(avg_loss)
        history['train_accuracy'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_accuracy'].append(val_acc)

        improved = val_loss + args.min_delta < best_val_loss
        if improved:
            best_val_loss = val_loss
            patience_counter = 0
            # Snapshot weights
            best_weights = [layer.get_params() for layer in mlp.layers]
        else:
            patience_counter += 1

        if epoch % 25 == 0 or epoch == 1:
            print(f'Epoch {epoch:4d} | TrainLoss {avg_loss:.4f} Acc {train_acc:.3f} | ValLoss {val_loss:.4f} Acc {val_acc:.3f} | Patience {patience_counter}')

        if patience_counter >= args.patience:
            print(f'>> Early stopping disparado en epoch {epoch}. Mejor val_loss {best_val_loss:.4f}')
            break

    # Restore best weights
    if best_weights is not None:
        for layer, params in zip(mlp.layers, best_weights):
            layer.set_params(params)

    # Final evaluation
    y_pred_val = mlp.predict(X_val)
    overall_acc = np.mean(y_pred_val == y_val)
    precision, recall, f1, tp, fp, fn = class_metrics(y_val, y_pred_val, target_class=1)  # Clase log

    print('\nRESULTADOS FINE-TUNE')
    print(f'Accuracy global val: {overall_acc:.4f}')
    print(f'Clase O(log n) -> Precision: {precision:.4f} Recall: {recall:.4f} F1: {f1:.4f} (TP={tp}, FP={fp}, FN={fn})')

    cm = confusion_matrix(y_val, y_pred_val, num_classes)
    print('\nConfusion Matrix (rows=real, cols=pred):')
    for i in range(num_classes):
        print(' '.join(f'{cm[i,j]:3d}' for j in range(num_classes)))

    # Guardar nuevo modelo si mejora
    fine_tuned_path = os.path.join(base_path, 'experiments', 'models', 'mlp_complexity_classifier_finetuned.npz')
    mlp.save_weights(fine_tuned_path)
    print(f'Pesos fine-tuned guardados en: {fine_tuned_path}')

    # Guardar historial
    log_path = os.path.join(base_path, 'experiments', 'logs', 'fine_tune_history.json')
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)
    print(f'Historial fine-tune guardado en: {log_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fine-tuning incremental del MLP')
    parser.add_argument('--epochs', type=int, default=400)
    parser.add_argument('--patience', type=int, default=40)
    parser.add_argument('--min_delta', type=float, default=0.0005)
    parser.add_argument('--lr', type=float, default=0.001)
    parser.add_argument('--batch_size', type=int, default=8)
    parser.add_argument('--dropout', type=float, default=0.1)
    parser.add_argument('--seed', type=int, default=2025)
    args = parser.parse_args()
    fine_tune(args)
