package main

// Algoritmo de Euclides para calcular GCD (O(log n))
func gcd(a, b int) int {
	for b != 0 {
		temp := b
		b = a % b
		a = temp
	}
	return a
}
