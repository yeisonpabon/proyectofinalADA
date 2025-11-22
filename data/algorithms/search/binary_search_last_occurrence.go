package main

// Binary Search Last Occurrence - O(log n)
// Encuentra la última ocurrencia de target
func binarySearchLastOccurrence(arr []int, target int) int {
	left, right := 0, len(arr)-1
	result := -1
	
	for left <= right {
		mid := left + (right-left)/2
		
		if arr[mid] == target {
			result = mid
			left = mid + 1  // Continuar buscando a la derecha
		} else if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}
	
	return result
}
