package main

// Is Power of Two
// Complejidad: O(1) - Constante
// Operación bit a bit

func isPowerOfTwo(n int) bool {
	if n <= 0 {
		return false
	}
	return (n & (n - 1)) == 0
}
