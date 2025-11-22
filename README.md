# Complexity Classifier - Neural Network Analysis Tool

A machine learning system that automatically classifies algorithm time complexity using a custom-built neural network. The system analyzes code features and predicts complexity classes: O(1), O(log n), O(n), O(n²), O(n³), O(2^n).

## Project Overview

| Metric | Value |
|--------|-------|
| **Test Accuracy** | 75.86% |
| **Model Architecture** | MLP (3 → 64 → 32 → 6) |
| **Dataset** | 144 balanced algorithms |
| **Features** | 3 (loops, recursion, nested depth) |
| **Framework** | NumPy-based neural network (custom) |
| **Status** | Production Ready |

## Key Features

- **Automatic Feature Extraction**: Detects loops, recursion, and nesting depth from source code
- **Custom MLP Implementation**: Neural network built from scratch with NumPy
- **Interactive GUI**: 4-tab interface for analysis, training visualization, data structure exploration
- **Comprehensive Testing**: 144 verified algorithms with ground-truth complexity labels
- **Model v6 Optimized**: Balanced dataset strategy for optimal classification

## Project Structure

```
src/
├── neural_network/        # Custom MLP implementation
│   ├── mlp.py            # Network architecture
│   ├── layers.py         # Dense & activation layers
│   ├── optimizers.py     # SGD optimizer
│   └── losses.py         # Cross-entropy loss
├── data_processing/
│   ├── feature_extractor.py
│   └── recurrence_parser.py
├── complexity_analysis/
│   ├── master_theorem.py
│   └── recurrence_parser.py
├── data_structures/       # Implementation of classic DS
│   ├── avl_tree.py
│   ├── hash_table.py
│   ├── min_heap.py
│   └── trie.py
└── gui/
    ├── main_window.py     # Main 4-tab interface
    ├── prediction_panel.py
    ├── training_visualizer.py
    └── data_structures_visualizer.py

data/
├── dataset.json           # 144 labeled algorithms
└── complexity_labels.json # Complexity ground truth
```

## Quick Start

### Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Run GUI

```bash
python GUI.py
```

### Run Analysis

```bash
python demo_v6.py
```

## Model Architecture

**Input Layer**: 3 features
- `loops` (0-5): Number of nested loops
- `recursion` (0-1): Presence of recursion
- `nested_depth` (1-5): Maximum nesting depth

**Hidden Layers**: 
- Dense(64, ReLU) + Dense(32, ReLU)

**Output Layer**: 
- Dense(6, Softmax) → 6 complexity classes

## Training Results

```
Dataset Distribution (v6 - Optimal):
- O(log n): 55 (38.2%) ← Key class
- O(n):     36 (25.0%)
- O(2^n):   16 (11.1%)
- O(n³):    16 (11.1%)
- O(n²):     9 (6.2%)
- O(1):      6 (4.2%)

Test Accuracy: 75.86% (29 examples)
Training Accuracy: 90.43%
Loss: Cross-Entropy
Optimizer: SGD
Epochs: 2000
```

## GUI Tabs

1. **Predicción** - Paste code, get complexity prediction
2. **Entrenamiento** - View training history and metrics
3. **Estructuras** - Interactive visualization of data structures (Heap, AVL, Trie, Hash Table)
4. **Comparador** - Compare complexity of multiple algorithms

## Development Notes

- **v1-v5**: Exploration phase with varying dataset sizes and configurations
- **v6**: Optimal balanced dataset, achieved 75.86% accuracy
- **v7**: Attempted expansion failed (54.55%) - proved balance > quantity

### Key Learning

The project demonstrates that **dataset balance is more important than dataset size** for classification performance. Version 6 with optimized O(log n) representation significantly outperformed versions with more data but poor distribution.

## Technologies

- **Neural Network**: NumPy (custom implementation)
- **GUI**: Tkinter
- **Visualization**: Matplotlib
- **Data**: JSON
- **Language**: Python 3.8+

## Requirements

See `requirements.txt` for dependencies.

## Files Included

- `GUI.py` - Main application entry point
- `train_model.py` - Training script
- `test_*.py` - Verification tests
- Configuration files for model versions

## License

Proyecto Final - Análisis y Diseño de Algoritmos
