package main

// Binary Search in Rotated Array - O(log n)
// Busca en un array rotado ordenado
func binarySearchRotated(arr []int, target int) int {
	left, right := 0, len(arr)-1
	
	for left <= right {
		mid := left + (right-left)/2
		
		if arr[mid] == target {
			return mid
		}
		
		// Determinar qué lado está ordenado
		if arr[left] <= arr[mid] {
			// Lado izquierdo está ordenado
			if arr[left] <= target && target < arr[mid] {
				right = mid - 1
			} else {
				left = mid + 1
			}
		} else {
			// Lado derecho está ordenado
			if arr[mid] < target && target <= arr[right] {
				left = mid + 1
			} else {
				right = mid - 1
			}
		}
	}
	
	return -1
}
