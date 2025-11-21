package main

// Karatsuba Multiplication - O(n^1.58)
func karatsubaMultiply(x int, y int) int {
	if x < 10 || y < 10 {
		return x * y
	}

	n := max(numDigits(x), numDigits(y))
	m := n / 2

	high1 := x / pow10(m)
	low1 := x % pow10(m)
	high2 := y / pow10(m)
	low2 := y % pow10(m)

	z0 := karatsubaMultiply(low1, low2)
	z1 := karatsubaMultiply(low1+high1, low2+high2)
	z2 := karatsubaMultiply(high1, high2)

	return z2*pow10(2*m) + (z1-z2-z0)*pow10(m) + z0
}

func numDigits(n int) int {
	if n == 0 {
		return 1
	}
	count := 0
	for n > 0 {
		n /= 10
		count++
	}
	return count
}

func pow10(exp int) int {
	result := 1
	for i := 0; i < exp; i++ {
		result *= 10
	}
	return result
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
