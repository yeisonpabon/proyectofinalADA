package main

// Fibonacci recursivo (ineficiente)
// Complejidad: O(2^n) - Exponencial
// Recurrencia: T(n) = T(n-1) + T(n-2) + O(1)

func fibonacci(n int) int {
	if n <= 1 {
		return n
	}
	
	return fibonacci(n-1) + fibonacci(n-2)
}
