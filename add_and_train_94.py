#!/usr/bin/env python3
"""
Agregar 20 algoritmos reales al dataset con código completo
Luego entrenar el modelo con el dataset expandido
"""
import json
import sys
sys.path.insert(0, 'src')

# Nuevos algoritmos reales (todos O(n))
new_algorithms = [
    {
        "id": "linear_search_real",
        "name": "LinearSearch",
        "code": """func LinearSearch(arr []int, target int) int {
	for i, v := range arr {
		if v == target {
			return i
		}
	}
	return -1
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Búsqueda lineal en un arreglo",
        "source": "user_provided"
    },
    {
        "id": "sum_array_real",
        "name": "Sum",
        "code": """func Sum(arr []int) int {
	s := 0
	for _, v := range arr {
		s += v
	}
	return s
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Suma de todos los elementos",
        "source": "user_provided"
    },
    {
        "id": "max_element_real",
        "name": "Max",
        "code": """func Max(arr []int) int {
	if len(arr) == 0 { return 0 }
	m := arr[0]
	for _, v := range arr[1:] {
		if v > m { m = v }
	}
	return m
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Encontrar elemento máximo",
        "source": "user_provided"
    },
    {
        "id": "min_element_real",
        "name": "Min",
        "code": """func Min(arr []int) int {
	if len(arr) == 0 { return 0 }
	m := arr[0]
	for _, v := range arr[1:] {
		if v < m { m = v }
	}
	return m
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Encontrar elemento mínimo",
        "source": "user_provided"
    },
    {
        "id": "average_real",
        "name": "Average",
        "code": """func Average(arr []int) float64 {
	if len(arr) == 0 { return 0 }
	sum := 0
	for _, v := range arr { sum += v }
	return float64(sum) / float64(len(arr))
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Calcular promedio de elementos",
        "source": "user_provided"
    },
    {
        "id": "count_occurrences_real",
        "name": "CountOccurrences",
        "code": """func CountOccurrences(arr []int, target int) int {
	c := 0
	for _, v := range arr {
		if v == target { c++ }
	}
	return c
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Contar ocurrencias de un valor",
        "source": "user_provided"
    },
    {
        "id": "is_sorted_real",
        "name": "IsSorted",
        "code": """func IsSorted(arr []int) bool {
	for i := 1; i < len(arr); i++ {
		if arr[i] < arr[i-1] {
			return false
		}
	}
	return true
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Verificar si arreglo está ordenado",
        "source": "user_provided"
    },
    {
        "id": "reverse_array_real",
        "name": "Reverse",
        "code": """func Reverse(arr []int) []int {
	n := len(arr)
	res := make([]int, n)
	for i := 0; i < n; i++ {
		res[i] = arr[n-1-i]
	}
	return res
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Invertir un arreglo",
        "source": "user_provided"
    },
    {
        "id": "copy_array_real",
        "name": "CopyArr",
        "code": """func CopyArr(arr []int) []int {
	res := make([]int, len(arr))
	for i, v := range arr {
		res[i] = v
	}
	return res
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Copiar un arreglo",
        "source": "user_provided"
    },
    {
        "id": "filter_even_real",
        "name": "FilterEven",
        "code": """func FilterEven(arr []int) []int {
	res := []int{}
	for _, v := range arr {
		if v%2 == 0 {
			res = append(res, v)
		}
	}
	return res
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Filtrar números pares",
        "source": "user_provided"
    },
    {
        "id": "remove_first_real",
        "name": "RemoveFirst",
        "code": """func RemoveFirst(arr []int, target int) []int {
	res := []int{}
	removed := false
	for _, v := range arr {
		if v == target && !removed {
			removed = true
			continue
		}
		res = append(res, v)
	}
	return res
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Eliminar primera ocurrencia",
        "source": "user_provided"
    },
    {
        "id": "prefix_sums_real",
        "name": "PrefixSums",
        "code": """func PrefixSums(arr []int) []int {
	res := make([]int, len(arr))
	sum := 0
	for i, v := range arr {
		sum += v
		res[i] = sum
	}
	return res
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Calcular sumas acumuladas",
        "source": "user_provided"
    },
    {
        "id": "first_duplicate_real",
        "name": "FirstDuplicate",
        "code": """func FirstDuplicate(arr []int) (int, bool) {
	seen := make(map[int]bool)
	for _, v := range arr {
		if seen[v] {
			return v, true
		}
		seen[v] = true
	}
	return 0, false
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Encontrar primer duplicado",
        "source": "user_provided"
    },
    {
        "id": "char_frequency_real",
        "name": "CharFrequency",
        "code": """func CharFrequency(s string) map[rune]int {
	freq := make(map[rune]int)
	for _, ch := range s {
		freq[ch]++
	}
	return freq
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Frecuencia de caracteres",
        "source": "user_provided"
    },
    {
        "id": "is_palindrome_real",
        "name": "IsPalindrome",
        "code": """func IsPalindrome(s string) bool {
	r := []rune(s)
	i, j := 0, len(r)-1
	for i < j {
		if r[i] != r[j] { return false }
		i++; j--
	}
	return true
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Verificar si es palíndromo",
        "source": "user_provided"
    },
    {
        "id": "rotate_left_real",
        "name": "RotateLeft",
        "code": """func RotateLeft(arr []int, k int) []int {
	n := len(arr)
	if n == 0 { return arr }
	k %= n
	res := make([]int, 0, n)
	for i := k; i < n; i++ { res = append(res, arr[i]) }
	for i := 0; i < k; i++ { res = append(res, arr[i]) }
	return res
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Rotar arreglo a la izquierda",
        "source": "user_provided"
    },
    {
        "id": "merge_sorted_real",
        "name": "MergeSorted",
        "code": """func MergeSorted(a, b []int) []int {
	res := make([]int, 0, len(a)+len(b))
	i, j := 0, 0
	for i < len(a) && j < len(b) {
		if a[i] <= b[j] { res = append(res, a[i]); i++ } 
		else { res = append(res, b[j]); j++ }
	}
	for i < len(a) { res = append(res, a[i]); i++ }
	for j < len(b) { res = append(res, b[j]); j++ }
	return res
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Merge de arreglos ordenados",
        "source": "user_provided"
    },
    {
        "id": "count_unique_real",
        "name": "CountUnique",
        "code": """func CountUnique(arr []int) int {
	seen := make(map[int]struct{})
	for _, v := range arr {
		seen[v] = struct{}{}
	}
	return len(seen)
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Contar valores únicos",
        "source": "user_provided"
    },
    {
        "id": "intersection_real",
        "name": "Intersection",
        "code": """func Intersection(a, b []int) []int {
	seen := make(map[int]bool)
	for _, v := range a { seen[v] = true }
	res := []int{}
	for _, v := range b {
		if seen[v] {
			res = append(res, v)
			seen[v] = false
		}
	}
	return res
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Intersección de dos arreglos",
        "source": "user_provided"
    },
    {
        "id": "two_sum_real",
        "name": "TwoSum",
        "code": """func TwoSum(arr []int, target int) (int, int, bool) {
	pos := make(map[int]int)
	for i, v := range arr {
		if j, ok := pos[target-v]; ok {
			return j, i, true
		}
		pos[v] = i
	}
	return 0, 0, false
}""",
        "complexity": "O(n)",
        "complexity_class": 2,
        "description": "Encontrar dos números que sumen target",
        "source": "user_provided"
    }
]

print("=" * 60)
print("AGREGAR ALGORITMOS Y ENTRENAR")
print("=" * 60)

# Cargar dataset original
print("\nCargando dataset original...")
with open('data/dataset.json', 'r') as f:
    data = json.load(f)

print(f"Algoritmos originales: {len(data['algorithms'])}")

# Agregar nuevos algoritmos
data['algorithms'].extend(new_algorithms)
print(f"Nuevos algoritmos: {len(new_algorithms)}")
print(f"Total: {len(data['algorithms'])}")

# Guardar dataset actualizado
with open('data/dataset.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✓ Dataset actualizado guardado")

# Ahora entrenar
print("\n" + "=" * 60)
print("ENTRENAMIENTO")
print("=" * 60)

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from neural_network.mlp import MLP

# Extraer código y etiquetas
codes = [algo.get('code', f"Algorithm: {algo['name']}") for algo in data['algorithms']]
labels = [algo['complexity'] for algo in data['algorithms']]

# Crear mapeo
unique_classes = sorted(set(labels))
class_to_idx = {cls: idx for idx, cls in enumerate(unique_classes)}
idx_to_class = {idx: cls for cls, idx in class_to_idx.items()}

print(f"\nClases: {unique_classes}")

# TF-IDF
print("Extrayendo features TF-IDF...")
vectorizer = TfidfVectorizer(max_features=225, ngram_range=(1, 2), max_df=0.9, min_df=1)
X = vectorizer.fit_transform(codes).toarray()
y = np.array([class_to_idx[label] for label in labels])

print(f"Features shape: {X.shape}")

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train: {len(X_train)}, Test: {len(X_test)}")

# Entrenar
print("\nEntrenando modelo...")
mlp = MLP(
    input_dim=225,
    hidden_dims=[256, 128, 64],
    num_classes=len(unique_classes),
    learning_rate=0.01,
    batch_size=32
)

history = mlp.fit(X_train, y_train, epochs=2000, verbose=True)

# Resultados
train_pred = mlp.predict(X_train)
test_pred = mlp.predict(X_test)

train_acc = (train_pred == y_train).mean() * 100
test_acc = (test_pred == y_test).mean() * 100

print(f"\n{'='*60}")
print(f"Training Accuracy: {train_acc:.2f}%")
print(f"Test Accuracy: {test_acc:.2f}%")
print(f"{'='*60}")

# Guardar
mlp.save_weights('experiments/models/mlp_complexity_classifier_114.npz')
print("\n✓ Modelo guardado: mlp_complexity_classifier_114.npz")

# Historial
history_dict = {
    'train_loss': [float(x) for x in history['train_loss']],
    'train_accuracy': [float(x) for x in history['train_accuracy']],
    'val_loss': [float(x) for x in history['val_loss']],
    'val_accuracy': [float(x) for x in history['val_accuracy']],
    'test_accuracy': test_acc,
    'dataset_size': len(data['algorithms'])
}

with open('experiments/logs/training_history_114.json', 'w') as f:
    json.dump(history_dict, f, indent=2)

print("✓ Historial guardado: training_history_114.json")
