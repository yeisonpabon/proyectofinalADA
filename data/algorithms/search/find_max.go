package main

// Máximo en Array
// Complejidad: O(n) - Lineal
// Recorre el array para encontrar el máximo

func findMax(arr []int) int {
	if len(arr) == 0 {
		return -1
	}
	
	max := arr[0]
	for i := 1; i < len(arr); i++ {
		if arr[i] > max {
			max = arr[i]
		}
	}
	return max
}
