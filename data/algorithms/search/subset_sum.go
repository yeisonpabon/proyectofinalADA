package main

// Subset Sum (Backtracking)
// Complejidad: O(2^n) - Exponencial
// Genera todos los subconjuntos posibles

func subsetSum(arr []int, target int) bool {
	n := len(arr)
	return subsetSumHelper(arr, n, target)
}

func subsetSumHelper(arr []int, n int, target int) bool {
	if target == 0 {
		return true
	}
	
	if n == 0 {
		return false
	}
	
	// Incluir elemento actual
	if arr[n-1] <= target {
		if subsetSumHelper(arr, n-1, target-arr[n-1]) {
			return true
		}
	}
	
	// No incluir elemento actual
	return subsetSumHelper(arr, n-1, target)
}
