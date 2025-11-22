package main

// Square Root Binary Search - O(log n)
// Calcula raíz cuadrada usando búsqueda binaria
func sqrtBinarySearch(n int) int {
	if n < 2 {
		return n
	}
	
	left, right := 1, n
	result := 0
	
	for left <= right {
		mid := left + (right-left)/2
		
		if mid <= n/mid {
			result = mid
			left = mid + 1
		} else {
			right = mid - 1
		}
	}
	
	return result
}
