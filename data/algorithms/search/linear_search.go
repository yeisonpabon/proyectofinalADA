package main

// Búsqueda lineal en un slice
// Complejidad: O(n)
// Recurrencia: No aplica (iterativo)

func linearSearch(arr []int, target int) int {
	for i := 0; i < len(arr); i++ {
		if arr[i] == target {
			return i
		}
	}
	return -1
}
