#!/usr/bin/env python3
"""
Agregar 20 algoritmos O(n²) al dataset (114 → 134)
Luego entrenar el modelo
"""
import json
import sys
sys.path.insert(0, 'src')

# Nuevos algoritmos O(n²)
new_algorithms_n2 = [
    {
        "id": "bubble_sort_n2",
        "name": "BubbleSort",
        "code": """func BubbleSort(arr []int) {
	n := len(arr)
	for i := 0; i < n; i++ {
		for j := 0; j < n-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
			}
		}
	}
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Bubble Sort - Ordenamiento de burbuja",
        "source": "user_provided"
    },
    {
        "id": "selection_sort_n2",
        "name": "SelectionSort",
        "code": """func SelectionSort(arr []int) {
	n := len(arr)
	for i := 0; i < n; i++ {
		minIdx := i
		for j := i + 1; j < n; j++ {
			if arr[j] < arr[minIdx] {
				minIdx = j
			}
		}
		arr[i], arr[minIdx] = arr[minIdx], arr[i]
	}
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Selection Sort - Ordenamiento por selección",
        "source": "user_provided"
    },
    {
        "id": "insertion_sort_n2",
        "name": "InsertionSort",
        "code": """func InsertionSort(arr []int) {
	for i := 1; i < len(arr); i++ {
		key := arr[i]
		j := i - 1
		for j >= 0 && arr[j] > key {
			arr[j+1] = arr[j]
			j--
		}
		arr[j+1] = key
	}
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Insertion Sort - Ordenamiento por inserción",
        "source": "user_provided"
    },
    {
        "id": "count_pairs_greater_n2",
        "name": "CountPairsGreater",
        "code": """func CountPairsGreater(arr []int, target int) int {
	n := len(arr)
	count := 0
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if arr[i]+arr[j] > target {
				count++
			}
		}
	}
	return count
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Contar pares con suma mayor a target",
        "source": "user_provided"
    },
    {
        "id": "find_duplicates_n2",
        "name": "FindDuplicates",
        "code": """func FindDuplicates(arr []int) []int {
	n := len(arr)
	dups := []int{}
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if arr[i] == arr[j] {
				dups = append(dups, arr[i])
				break
			}
		}
	}
	return dups
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Encontrar todos los duplicados",
        "source": "user_provided"
    },
    {
        "id": "has_duplicate_n2",
        "name": "HasAnyDuplicate",
        "code": """func HasAnyDuplicate(arr []int) bool {
	n := len(arr)
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if arr[i] == arr[j] {
				return true
			}
		}
	}
	return false
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Verificar si hay algún duplicado",
        "source": "user_provided"
    },
    {
        "id": "identity_matrix_n2",
        "name": "IdentityMatrix",
        "code": """func IdentityMatrix(n int) [][]int {
	m := make([][]int, n)
	for i := 0; i < n; i++ {
		m[i] = make([]int, n)
		for j := 0; j < n; j++ {
			if i == j {
				m[i][j] = 1
			}
		}
	}
	return m
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Crear matriz identidad n×n",
        "source": "user_provided"
    },
    {
        "id": "add_matrices_n2",
        "name": "AddMatrices",
        "code": """func AddMatrices(a, b [][]int) [][]int {
	n := len(a)
	res := make([][]int, n)
	for i := 0; i < n; i++ {
		res[i] = make([]int, n)
		for j := 0; j < n; j++ {
			res[i][j] = a[i][j] + b[i][j]
		}
	}
	return res
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Suma de dos matrices n×n",
        "source": "user_provided"
    },
    {
        "id": "transpose_matrix_n2",
        "name": "Transpose",
        "code": """func Transpose(mat [][]int) [][]int {
	n := len(mat)
	res := make([][]int, n)
	for i := 0; i < n; i++ {
		res[i] = make([]int, n)
		for j := 0; j < n; j++ {
			res[j][i] = mat[i][j]
		}
	}
	return res
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Transpuesta de matriz n×n",
        "source": "user_provided"
    },
    {
        "id": "all_pairs_product_n2",
        "name": "AllPairsProduct",
        "code": """func AllPairsProduct(arr []int) int {
	n := len(arr)
	sum := 0
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			sum += arr[i] * arr[j]
		}
	}
	return sum
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Producto punto de todos con todos",
        "source": "user_provided"
    },
    {
        "id": "all_abs_distances_n2",
        "name": "AllAbsDistances",
        "code": """func AllAbsDistances(arr []int) []int {
	n := len(arr)
	res := make([]int, 0, n*(n-1)/2)
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			d := arr[i] - arr[j]
			if d < 0 { d = -d }
			res = append(res, d)
		}
	}
	return res
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Calcular distancias absolutas entre pares",
        "source": "user_provided"
    },
    {
        "id": "anagram_naive_n2",
        "name": "IsAnagramNaive",
        "code": """func IsAnagramNaive(a, b string) bool {
	ra := []rune(a)
	rb := []rune(b)
	if len(ra) != len(rb) { return false }

	used := make([]bool, len(rb))
	for i := 0; i < len(ra); i++ {
		found := false
		for j := 0; j < len(rb); j++ {
			if !used[j] && ra[i] == rb[j] {
				used[j] = true
				found = true
				break
			}
		}
		if !found { return false }
	}
	return true
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Verificar anagrama (comparación naive)",
        "source": "user_provided"
    },
    {
        "id": "count_inversions_n2",
        "name": "CountInversions",
        "code": """func CountInversions(arr []int) int {
	n := len(arr)
	inv := 0
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if arr[i] > arr[j] {
				inv++
			}
		}
	}
	return inv
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Conteo de inversiones",
        "source": "user_provided"
    },
    {
        "id": "two_sum_naive_n2",
        "name": "TwoSumNaive",
        "code": """func TwoSumNaive(arr []int, target int) bool {
	n := len(arr)
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if arr[i]+arr[j] == target {
				return true
			}
		}
	}
	return false
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "TwoSum naive - Verificar par con suma exacta",
        "source": "user_provided"
    },
    {
        "id": "max_pair_product_n2",
        "name": "MaxPairProduct",
        "code": """func MaxPairProduct(arr []int) int {
	n := len(arr)
	maxP := -1 << 31
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			p := arr[i] * arr[j]
			if p > maxP { maxP = p }
		}
	}
	return maxP
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Encontrar máximo producto de pares",
        "source": "user_provided"
    },
    {
        "id": "adj_matrix_naive_n2",
        "name": "BuildAdjMatrixNaive",
        "code": """type Edge struct{ U, V int }

func BuildAdjMatrixNaive(n int, edges []Edge) [][]int {
	mat := make([][]int, n)
	for i := 0; i < n; i++ {
		mat[i] = make([]int, n)
	}
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			for _, e := range edges {
				if (e.U == i && e.V == j) || (e.U == j && e.V == i) {
					mat[i][j] = 1
					break
				}
			}
		}
	}
	return mat
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Matriz de adyacencia naive",
        "source": "user_provided"
    },
    {
        "id": "intersection_naive_n2",
        "name": "IntersectionNaive",
        "code": """func IntersectionNaive(a, b []int) []int {
	res := []int{}
	for i := 0; i < len(a); i++ {
		for j := 0; j < len(b); j++ {
			if a[i] == b[j] {
				res = append(res, a[i])
				break
			}
		}
	}
	return res
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Intersección de arreglos (naive)",
        "source": "user_provided"
    },
    {
        "id": "mult_table_n2",
        "name": "MultiplicationTable",
        "code": """func MultiplicationTable(n int) [][]int {
	tab := make([][]int, n)
	for i := 0; i < n; i++ {
		tab[i] = make([]int, n)
		for j := 0; j < n; j++ {
			tab[i][j] = (i + 1) * (j + 1)
		}
	}
	return tab
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Tabla de multiplicar n×n",
        "source": "user_provided"
    },
    {
        "id": "count_matches_naive_n2",
        "name": "CountMatchesNaive",
        "code": """func CountMatchesNaive(a, b []int) int {
	matches := 0
	for i := 0; i < len(a); i++ {
		for j := 0; j < len(b); j++ {
			if a[i] == b[j] {
				matches++
			}
		}
	}
	return matches
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Contar coincidencias naive",
        "source": "user_provided"
    },
    {
        "id": "subarray_sums_n2",
        "name": "AllSubarraySums",
        "code": """func AllSubarraySums(arr []int) []int {
	n := len(arr)
	res := []int{}
	for i := 0; i < n; i++ {
		sum := 0
		for j := i; j < n; j++ {
			sum += arr[j]
			res = append(res, sum)
		}
	}
	return res
}""",
        "complexity": "O(n²)",
        "complexity_class": 5,
        "description": "Calcular todas las sumas de subarrays",
        "source": "user_provided"
    }
]

print("=" * 70)
print("AGREGAR 20 ALGORITMOS O(n²) Y ENTRENAR")
print("=" * 70)

# Cargar dataset actual (114 algoritmos)
print("\nCargando dataset actual...")
with open('data/dataset.json', 'r') as f:
    data = json.load(f)

print(f"Algoritmos actuales: {len(data['algorithms'])}")

# Agregar nuevos
data['algorithms'].extend(new_algorithms_n2)
print(f"Nuevos algoritmos O(n²): {len(new_algorithms_n2)}")
print(f"Total: {len(data['algorithms'])}")

# Guardar
with open('data/dataset.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✓ Dataset actualizado")

# Entrenar
print("\n" + "=" * 70)
print("ENTRENAMIENTO CON 134 ALGORITMOS")
print("=" * 70)

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from neural_network.mlp import MLP

# Extraer datos
codes = [algo.get('code', f"Algorithm: {algo['name']}") for algo in data['algorithms']]
labels = [algo['complexity'] for algo in data['algorithms']]

# Mapeo de clases
unique_classes = sorted(set(labels))
class_to_idx = {cls: idx for idx, cls in enumerate(unique_classes)}
idx_to_class = {idx: cls for cls, idx in class_to_idx.items()}

print(f"\nClases: {unique_classes}")

# Verificar distribución
from collections import Counter
dist = Counter(labels)
print(f"\nDistribución:")
for cls in unique_classes:
    count = dist.get(cls, 0)
    pct = (count / len(labels)) * 100
    print(f"  {cls:10s}: {count:3d} ({pct:5.1f}%)")

# TF-IDF
print("\nExtrayendo features...")
vectorizer = TfidfVectorizer(max_features=225, ngram_range=(1, 2), max_df=0.9, min_df=1)
X = vectorizer.fit_transform(codes).toarray()
y = np.array([class_to_idx[label] for label in labels])

print(f"Shape: {X.shape}")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train: {len(X_train)}, Test: {len(X_test)}")

# Entrenar
print("\nEntrenando...")
mlp = MLP(
    input_dim=225,
    hidden_dims=[256, 128, 64],
    num_classes=len(unique_classes),
    learning_rate=0.01,
    batch_size=32
)

history = mlp.fit(X_train, y_train, epochs=2000, verbose=True)

# Evaluar
train_pred = mlp.predict(X_train)
test_pred = mlp.predict(X_test)

train_acc = (train_pred == y_train).mean() * 100
test_acc = (test_pred == y_test).mean() * 100

print(f"\n{'='*70}")
print(f"Training Accuracy: {train_acc:.2f}%")
print(f"Test Accuracy: {test_acc:.2f}%")
print(f"{'='*70}")

# Guardar
mlp.save_weights('experiments/models/mlp_complexity_classifier_134.npz')
print("\n✓ Modelo guardado: mlp_complexity_classifier_134.npz")

# Historial
history_dict = {
    'train_loss': [float(x) for x in history['train_loss']],
    'train_accuracy': [float(x) for x in history['train_accuracy']],
    'val_loss': [float(x) for x in history['val_loss']],
    'val_accuracy': [float(x) for x in history['val_accuracy']],
    'test_accuracy': test_acc,
    'dataset_size': len(data['algorithms'])
}

with open('experiments/logs/training_history_134.json', 'w') as f:
    json.dump(history_dict, f, indent=2)

print("✓ Historial guardado: training_history_134.json")
