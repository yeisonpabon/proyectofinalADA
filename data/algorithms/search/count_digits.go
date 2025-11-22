package main

// Cuenta dígitos de un número (O(log n))
func countDigits(n int) int {
	if n == 0 {
		return 1
	}
	
	count := 0
	for n > 0 {
		count++
		n /= 10
	}
	return count
}
