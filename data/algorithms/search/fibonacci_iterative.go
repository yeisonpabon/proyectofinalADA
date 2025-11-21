package main

// Fibonacci Iterativo
// Complejidad: O(n) - Lineal
// Usa programación dinámica

func fibonacciIterative(n int) int {
	if n <= 1 {
		return n
	}
	
	a, b := 0, 1
	
	for i := 2; i <= n; i++ {
		a, b = b, a+b
	}
	
	return b
}
