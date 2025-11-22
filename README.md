# Computational Complexity Classifier

Automatic classification of algorithm computational complexity using formal analysis and neural networks.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Launch GUI
python GUI.py
```

Or double-click `ejecutar_gui.bat` (Windows).

## Features

- **Multi-method Analysis**: Recurrence detection, Master Theorem, iterative analysis
- **Neural Network**: MLP trained on 74 Go algorithms
- **GUI Interface**: Real-time prediction and visualization
- **Data Structures**: Interactive AVL, Heap, Hash Table, and Trie visualizations

## Supported Complexity Classes

| Class | Example |
|-------|---------|
| O(1) | Array access |
| O(log n) | Binary search |
| O(n) | Linear search |
| O(n log n) | Merge sort |
| O(n²) | Bubble sort |
| O(2^n) | Fibonacci recursive |

## Architecture

```
src/
├── gui/                    # Tkinter interface
├── neural_network/         # MLP implementation from scratch
├── data_processing/        # Feature extraction
├── complexity_analysis/    # Recurrence parser & Master Theorem
├── data_structures/        # AVL, Heap, Hash Table, Trie
└── algorithms/             # Selection algorithms

data/
├── dataset.json            # 74 algorithm metadata
├── complexity_labels.json  # Class definitions
└── algorithms/             # Go source code

experiments/
├── models/                 # Trained MLP weights
├── logs/                   # Training history
└── figures/                # Visualizations
```

## Model Performance

- **Test Accuracy**: 93.33% (14/15 examples)
- **Per-class Precision**: 
  - O(1): 100% | O(log n): 100% | O(n): 100%
  - O(n²): 100% | O(2^n): 75%

## Training

To retrain the model (2000 epochs):

```bash
python train_model.py
```

## Tools

Diagnostic and analysis scripts available in `tools/`:

```bash
python tools/test_model_loading.py        # Validate model
python tools/precision_por_complejidad.py # Precision analysis
```

See `tools/README.md` for details.

## Requirements

- Python 3.8+
- NumPy, Matplotlib, scikit-learn

See `requirements.txt` for full list.

## File Structure

```
proyectofinalADA/
├── GUI.py                  # Main entry point
├── train_model.py          # Model training
├── ejecutar_gui.bat        # Windows launcher
├── requirements.txt        # Dependencies
├── README.md              # This file
│
├── src/                    # Source code
├── data/                   # Dataset
├── experiments/            # Models & logs
├── tests/                  # Unit tests
└── tools/                  # Diagnostic tools
```

## License

Academic Project
