package main

// Suma de Array
// Complejidad: O(n) - Lineal
// Recorre el array una vez

func arraySum(arr []int) int {
	sum := 0
	for _, val := range arr {
		sum += val
	}
	return sum
}
