package main

// Matriz Multiplicación
// Complejidad: O(n³) - Cúbico
// Tres loops anidados para multiplicación de matrices

func matrixMultiplication(A [][]int, B [][]int) [][]int {
	n := len(A)
	m := len(B[0])
	p := len(B)
	
	result := make([][]int, n)
	for i := range result {
		result[i] = make([]int, m)
	}
	
	for i := 0; i < n; i++ {
		for j := 0; j < m; j++ {
			for k := 0; k < p; k++ {
				result[i][j] += A[i][k] * B[k][j]
			}
		}
	}
	
	return result
}
