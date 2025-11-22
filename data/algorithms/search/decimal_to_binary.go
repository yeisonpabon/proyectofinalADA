package main

// Conversión de decimal a binario (O(log n))
func decimalToBinary(n int) []int {
	if n == 0 {
		return []int{0}
	}
	
	binary := []int{}
	for n > 0 {
		binary = append([]int{n % 2}, binary...)
		n /= 2
	}
	return binary
}
