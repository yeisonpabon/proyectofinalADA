package main

// Calcula a^n usando exponenciación binaria (O(log n))
func fastPower(a, n int) int {
	result := 1
	base := a
	exp := n

	for exp > 0 {
		if exp%2 == 1 {
			result *= base
		}
		base *= base
		exp /= 2
	}

	return result
}
