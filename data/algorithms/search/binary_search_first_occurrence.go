package main

// Binary Search First Occurrence - O(log n)
// Encuentra la primera ocurrencia de target
func binarySearchFirstOccurrence(arr []int, target int) int {
	left, right := 0, len(arr)-1
	result := -1
	
	for left <= right {
		mid := left + (right-left)/2
		
		if arr[mid] == target {
			result = mid
			right = mid - 1  // Continuar buscando a la izquierda
		} else if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}
	
	return result
}
