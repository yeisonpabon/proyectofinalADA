#!/usr/bin/env python3
"""
Agregar 20 algoritmos O(n log n) al dataset (134 → 154)
Luego entrenar el modelo
"""
import json
import sys
sys.path.insert(0, 'src')

# Nuevos algoritmos O(n log n)
new_algorithms_nlogn = [
    {
        "id": "merge_sort_recursive_nlogn",
        "name": "MergeSort",
        "code": """func MergeSort(arr []int) []int {
	if len(arr) <= 1 { return arr }
	mid := len(arr) / 2
	left := MergeSort(arr[:mid])
	right := MergeSort(arr[mid:])
	return merge(left, right)
}

func merge(a, b []int) []int {
	i, j := 0, 0
	res := make([]int, 0, len(a)+len(b))
	for i < len(a) && j < len(b) {
		if a[i] <= b[j] {
			res = append(res, a[i]); i++
		} else {
			res = append(res, b[j]); j++
		}
	}
	res = append(res, a[i:]...)
	res = append(res, b[j:]...)
	return res
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Merge Sort recursivo",
        "source": "user_provided"
    },
    {
        "id": "merge_sort_iterative_nlogn",
        "name": "MergeSortIter",
        "code": """func MergeSortIter(arr []int) []int {
	n := len(arr)
	res := make([]int, n)
	copy(res, arr)

	for size := 1; size < n; size *= 2 {
		for left := 0; left < n; left += 2 * size {
			mid := min(left+size, n)
			right := min(left+2*size, n)
			tmp := merge(res[left:mid], res[mid:right])
			copy(res[left:right], tmp)
		}
	}
	return res
}

func min(a, b int) int {
	if a < b { return a }
	return b
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Merge Sort iterativo bottom-up",
        "source": "user_provided"
    },
    {
        "id": "quick_sort_nlogn",
        "name": "QuickSort",
        "code": """func QuickSort(arr []int, l, r int) {
	if l >= r { return }
	p := partition(arr, l, r)
	QuickSort(arr, l, p-1)
	QuickSort(arr, p+1, r)
}

func partition(arr []int, l, r int) int {
	pivot := arr[r]
	i := l
	for j := l; j < r; j++ {
		if arr[j] < pivot {
			arr[i], arr[j] = arr[j], arr[i]
			i++
		}
	}
	arr[i], arr[r] = arr[r], arr[i]
	return i
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Quick Sort promedio O(n log n)",
        "source": "user_provided"
    },
    {
        "id": "heap_sort_nlogn",
        "name": "HeapSort",
        "code": """func HeapSort(arr []int) {
	n := len(arr)

	for i := n/2 - 1; i >= 0; i-- {
		heapify(arr, n, i)
	}
	for i := n - 1; i > 0; i-- {
		arr[0], arr[i] = arr[i], arr[0]
		heapify(arr, i, 0)
	}
}

func heapify(arr []int, n, i int) {
	l, r := 2*i+1, 2*i+2
	largest := i
	if l < n && arr[l] > arr[largest] { largest = l }
	if r < n && arr[r] > arr[largest] { largest = r }
	if largest != i {
		arr[i], arr[largest] = arr[largest], arr[i]
		heapify(arr, n, largest)
	}
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Heap Sort",
        "source": "user_provided"
    },
    {
        "id": "sort_ints_library_nlogn",
        "name": "SortIntsLibrary",
        "code": """import "sort"

func SortIntsLibrary(arr []int) {
	sort.Ints(arr) // O(n log n)
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Ordenar con librería sort.Ints",
        "source": "user_provided"
    },
    {
        "id": "sort_strings_library_nlogn",
        "name": "SortStringsLibrary",
        "code": """import "sort"

func SortStringsLibrary(arr []string) {
	sort.Strings(arr) // O(n log n)
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Ordenar strings con librería",
        "source": "user_provided"
    },
    {
        "id": "kth_smallest_nlogn",
        "name": "KthSmallest",
        "code": """import "sort"

func KthSmallest(arr []int, k int) int {
	sort.Ints(arr)
	return arr[k-1]
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Encontrar k-ésimo menor",
        "source": "user_provided"
    },
    {
        "id": "median_nlogn",
        "name": "Median",
        "code": """import "sort"

func Median(arr []int) float64 {
	sort.Ints(arr)
	n := len(arr)
	if n%2 == 1 { return float64(arr[n/2]) }
	return float64(arr[n/2-1]+arr[n/2]) / 2.0
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Calcular mediana ordenando",
        "source": "user_provided"
    },
    {
        "id": "unique_sorted_nlogn",
        "name": "UniqueSorted",
        "code": """import "sort"

func UniqueSorted(arr []int) []int {
	if len(arr) == 0 { return arr }
	sort.Ints(arr)
	res := []int{arr[0]}
	for i := 1; i < len(arr); i++ {
		if arr[i] != arr[i-1] {
			res = append(res, arr[i])
		}
	}
	return res
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Eliminar duplicados ordenando",
        "source": "user_provided"
    },
    {
        "id": "intersection_sort_nlogn",
        "name": "IntersectionSort",
        "code": """import "sort"

func IntersectionSort(a, b []int) []int {
	sort.Ints(a)
	sort.Ints(b)
	i, j := 0, 0
	res := []int{}
	for i < len(a) && j < len(b) {
		if a[i] == b[j] {
			res = append(res, a[i]); i++; j++
		} else if a[i] < b[j] {
			i++
		} else {
			j++
		}
	}
	return res
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Intersección ordenando ambas listas",
        "source": "user_provided"
    },
    {
        "id": "union_sort_nlogn",
        "name": "UnionSort",
        "code": """import "sort"

func UnionSort(a, b []int) []int {
	sort.Ints(a)
	sort.Ints(b)
	i, j := 0, 0
	res := []int{}
	for i < len(a) && j < len(b) {
		if a[i] == b[j] {
			res = append(res, a[i]); i++; j++
		} else if a[i] < b[j] {
			res = append(res, a[i]); i++
		} else {
			res = append(res, b[j]); j++
		}
	}
	res = append(res, a[i:]...)
	res = append(res, b[j:]...)
	return res
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Unión de dos listas ordenadas",
        "source": "user_provided"
    },
    {
        "id": "balanced_bst_nlogn",
        "name": "BuildBalancedBST",
        "code": """type Node struct {
	Val int
	Left, Right *Node
}

func BuildBalancedBST(sorted []int) *Node {
	if len(sorted) == 0 { return nil }
	mid := len(sorted)/2
	root := &Node{Val: sorted[mid]}
	root.Left = BuildBalancedBST(sorted[:mid])
	root.Right = BuildBalancedBST(sorted[mid+1:])
	return root
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Construir BST balanceado",
        "source": "user_provided"
    },
    {
        "id": "insert_many_balanced_tree_nlogn",
        "name": "InsertManyBalancedTree",
        "code": """func InsertManyBalancedTree(values []int) {
	var tree BalancedTree
	for _, v := range values { // n veces
		tree.Insert(v) // log n
	}
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Insertar n elementos en árbol balanceado",
        "source": "user_provided"
    },
    {
        "id": "sort_binary_queries_nlogn",
        "name": "SortAndBinaryQueries",
        "code": """import "sort"

func SortAndBinaryQueries(arr []int, queries []int) []bool {
	sort.Ints(arr) // n log n
	res := make([]bool, len(queries))
	for i, q := range queries { // m veces
		idx := sort.SearchInts(arr, q) // log n
		res[i] = idx < len(arr) && arr[idx] == q
	}
	return res
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Ordenar y buscar binaria",
        "source": "user_provided"
    },
    {
        "id": "count_inversions_nlogn",
        "name": "CountInversions",
        "code": """func CountInversions(arr []int) int {
	_, inv := sortCount(arr)
	return inv
}

func sortCount(arr []int) ([]int, int) {
	if len(arr) <= 1 { return arr, 0 }
	mid := len(arr)/2
	left, invL := sortCount(arr[:mid])
	right, invR := sortCount(arr[mid:])
	merged, invM := mergeCount(left, right)
	return merged, invL+invR+invM
}

func mergeCount(a, b []int) ([]int, int) {
	i, j, inv := 0, 0, 0
	res := []int{}
	for i < len(a) && j < len(b) {
		if a[i] <= b[j] {
			res = append(res, a[i]); i++
		} else {
			res = append(res, b[j]); j++
			inv += len(a) - i
		}
	}
	res = append(res, a[i:]...)
	res = append(res, b[j:]...)
	return res, inv
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Contar inversiones con merge sort",
        "source": "user_provided"
    },
    {
        "id": "top_k_heap_nlogn",
        "name": "TopK",
        "code": """import "container/heap"

type MinHeap []int
func (h MinHeap) Len() int { return len(h) }
func (h MinHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h MinHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *MinHeap) Push(x any) { *h = append(*h, x.(int)) }
func (h *MinHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

func TopK(arr []int, k int) []int {
	h := &MinHeap{}
	heap.Init(h)
	for _, v := range arr {
		heap.Push(h, v)
		if h.Len() > k {
			heap.Pop(h)
		}
	}
	res := make([]int, h.Len())
	for i := len(res)-1; i >= 0; i-- {
		res[i] = heap.Pop(h).(int)
	}
	return res
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Top-K usando heap",
        "source": "user_provided"
    },
    {
        "id": "sort_pairs_nlogn",
        "name": "SortPairs",
        "code": """import "sort"

type Pair struct{ A, B int }

func SortPairs(pairs []Pair) {
	sort.Slice(pairs, func(i, j int) bool {
		return pairs[i].A < pairs[j].A
	}) // O(n log n)
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Ordenar pares por primer elemento",
        "source": "user_provided"
    },
    {
        "id": "canonical_anagrams_nlogn",
        "name": "Canonical",
        "code": """import "sort"

func Canonical(word string) string {
	r := []rune(word)
	sort.Slice(r, func(i, j int) bool { return r[i] < r[j] })
	return string(r)
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Forma canónica para anagramas",
        "source": "user_provided"
    },
    {
        "id": "dijkstra_sparse_nlogn",
        "name": "DijkstraSparse",
        "code": """func DijkstraSparse(graph [][]Edge, start int) []int {
	// usando prioridad (heap) => cada pop/push log V
	// total O(E log V)
	return nil
}

type Edge struct{ To, W int }""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Dijkstra con heap (sparse graph)",
        "source": "user_provided"
    },
    {
        "id": "heapify_extract_nlogn",
        "name": "HeapifyAndExtract",
        "code": """import "container/heap"

func HeapifyAndExtract(arr []int) []int {
	h := MinHeap(arr)
	heap.Init(&h) // O(n)
	res := []int{}
	for h.Len() > 0 { // n veces
		res = append(res, heap.Pop(&h).(int)) // log n
	}
	return res
}""",
        "complexity": "O(n log n)",
        "complexity_class": 3,
        "description": "Heapificar y extraer todo",
        "source": "user_provided"
    }
]

print("=" * 70)
print("AGREGAR 20 ALGORITMOS O(n log n) Y ENTRENAR")
print("=" * 70)

# Cargar dataset actual (134 algoritmos)
print("\nCargando dataset actual...")
with open('data/dataset.json', 'r') as f:
    data = json.load(f)

print(f"Algoritmos actuales: {len(data['algorithms'])}")

# Agregar nuevos
data['algorithms'].extend(new_algorithms_nlogn)
print(f"Nuevos algoritmos O(n log n): {len(new_algorithms_nlogn)}")
print(f"Total: {len(data['algorithms'])}")

# Guardar
with open('data/dataset.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✓ Dataset actualizado")

# Entrenar
print("\n" + "=" * 70)
print("ENTRENAMIENTO CON 154 ALGORITMOS")
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
mlp.save_weights('experiments/models/mlp_complexity_classifier_154.npz')
print("\n✓ Modelo guardado: mlp_complexity_classifier_154.npz")

# Historial
history_dict = {
    'train_loss': [float(x) for x in history['train_loss']],
    'train_accuracy': [float(x) for x in history['train_accuracy']],
    'val_loss': [float(x) for x in history['val_loss']],
    'val_accuracy': [float(x) for x in history['val_accuracy']],
    'test_accuracy': test_acc,
    'dataset_size': len(data['algorithms'])
}

with open('experiments/logs/training_history_154.json', 'w') as f:
    json.dump(history_dict, f, indent=2)

print("✓ Historial guardado: training_history_154.json")
