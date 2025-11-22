#!/usr/bin/env python3
"""
Script para agregar 20 algoritmos reales O(n) al dataset
"""
import json

# Cargar dataset actual
with open('data/dataset.json', 'r') as f:
    data = json.load(f)

# Nuevos algoritmos reales (todos O(n))
new_algorithms = [
    {
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
        "source": "user_provided"
    },
    {
        "name": "Sum",
        "code": """func Sum(arr []int) int {
	s := 0
	for _, v := range arr {
		s += v
	}
	return s
}""",
        "complexity": "O(n)",
        "source": "user_provided"
    },
    {
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
        "source": "user_provided"
    },
    {
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
        "source": "user_provided"
    },
    {
        "name": "Average",
        "code": """func Average(arr []int) float64 {
	if len(arr) == 0 { return 0 }
	sum := 0
	for _, v := range arr { sum += v }
	return float64(sum) / float64(len(arr))
}""",
        "complexity": "O(n)",
        "source": "user_provided"
    },
    {
        "name": "CountOccurrences",
        "code": """func CountOccurrences(arr []int, target int) int {
	c := 0
	for _, v := range arr {
		if v == target { c++ }
	}
	return c
}""",
        "complexity": "O(n)",
        "source": "user_provided"
    },
    {
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
        "source": "user_provided"
    },
    {
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
        "source": "user_provided"
    },
    {
        "name": "CopyArr",
        "code": """func CopyArr(arr []int) []int {
	res := make([]int, len(arr))
	for i, v := range arr {
		res[i] = v
	}
	return res
}""",
        "complexity": "O(n)",
        "source": "user_provided"
    },
    {
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
        "source": "user_provided"
    },
    {
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
        "source": "user_provided"
    },
    {
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
        "source": "user_provided"
    },
    {
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
        "source": "user_provided"
    },
    {
        "name": "CharFrequency",
        "code": """func CharFrequency(s string) map[rune]int {
	freq := make(map[rune]int)
	for _, ch := range s {
		freq[ch]++
	}
	return freq
}""",
        "complexity": "O(n)",
        "source": "user_provided"
    },
    {
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
        "source": "user_provided"
    },
    {
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
        "source": "user_provided"
    },
    {
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
        "source": "user_provided"
    },
    {
        "name": "CountUnique",
        "code": """func CountUnique(arr []int) int {
	seen := make(map[int]struct{})
	for _, v := range arr {
		seen[v] = struct{}{}
	}
	return len(seen)
}""",
        "complexity": "O(n)",
        "source": "user_provided"
    },
    {
        "name": "Intersection",
        "code": """func Intersection(a, b []int) []int {
	seen := make(map[int]bool)
	for _, v := range a { seen[v] = true }
	res := []int{}
	for _, v := range b {
		if seen[v] {
			res = append(res, v)
			seen[v] = false // evitar repetidos
		}
	}
	return res
}""",
        "complexity": "O(n)",
        "source": "user_provided"
    },
    {
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
        "source": "user_provided"
    },
]

# Agregar nuevos algoritmos
data['algorithms'].extend(new_algorithms)

# Guardar dataset actualizado
with open('data/dataset.json', 'w') as f:
    json.dump(data, f, indent=2)

# Estadísticas
from collections import Counter
complexities = [a['complexity'] for a in data['algorithms']]
dist = Counter(complexities)

print("=" * 60)
print("DATASET ACTUALIZADO")
print("=" * 60)
print(f"\nTotal algoritmos: {len(data['algorithms'])}")
print(f"Nuevos agregados: {len(new_algorithms)}")
print(f"\nDistribución de complejidades:")
for comp, count in sorted(dist.items()):
    pct = (count / len(data['algorithms'])) * 100
    print(f"  {comp:10s}: {count:3d} ({pct:5.1f}%)")

print(f"\nDataset guardado: data/dataset.json")
