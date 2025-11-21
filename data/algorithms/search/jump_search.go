package main

// Jump Search
// Complejidad: O(√n)
// Saltos de tamaño √n seguidos de búsqueda lineal

import "math"

func jumpSearch(arr []int, target int) int {
	n := len(arr)
	step := int(math.Sqrt(float64(n)))
	prev := 0
	
	// Saltar hasta encontrar rango
	for arr[min(step, n)-1] < target {
		prev = step
		step += int(math.Sqrt(float64(n)))
		if prev >= n {
			return -1
		}
	}
	
	// Búsqueda lineal en el rango
	for arr[prev] < target {
		prev++
		if prev == min(step, n) {
			return -1
		}
	}
	
	if arr[prev] == target {
		return prev
	}
	
	return -1
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
