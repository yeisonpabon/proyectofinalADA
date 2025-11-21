package main

// Factorial Recursivo
// Complejidad: O(n) - Lineal
// Recurrencia: T(n) = T(n-1) + O(1)

func factorialRecursive(n int) int {
	if n <= 1 {
		return 1
	}
	return n * factorialRecursive(n-1)
}
