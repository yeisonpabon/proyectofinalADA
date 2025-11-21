package main

// Exponential Search
// Complejidad: O(log n)
// Busca por potencias de 2, luego binary search

func exponentialSearch(arr []int, target int) int {
	n := len(arr)
	
	if n == 0 {
		return -1
	}
	
	if arr[0] == target {
		return 0
	}
	
	// Encontrar rango
	i := 1
	for i < n && arr[i] <= target {
		i *= 2
	}
	
	// Binary search en el rango
	return binarySearchRange(arr, target, i/2, min(i, n-1))
}

func binarySearchRange(arr []int, target int, left int, right int) int {
	for left <= right {
		mid := left + (right-left)/2
		
		if arr[mid] == target {
			return mid
		}
		
		if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}
	
	return -1
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
