package main

// Búsqueda binaria recursiva
// Complejidad: O(log n)
// Recurrencia: T(n) = T(n/2) + O(1)

func binarySearch(arr []int, target int, left int, right int) int {
	if left > right {
		return -1
	}
	
	mid := left + (right-left)/2
	
	if arr[mid] == target {
		return mid
	}
	
	if arr[mid] > target {
		return binarySearch(arr, target, left, mid-1)
	}
	
	return binarySearch(arr, target, mid+1, right)
}
