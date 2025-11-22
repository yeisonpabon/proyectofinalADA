package search

import "math"

// FindClosestElement encuentra el elemento más cercano a target
// Complejidad: O(log n) usando búsqueda binaria
func FindClosestElement(arr []int, target int) int {
	if len(arr) == 0 {
		return -1
	}
	
	if len(arr) == 1 {
		return arr[0]
	}
	
	left := 0
	right := len(arr) - 1
	
	// Caso especial: target fuera del rango
	if target <= arr[left] {
		return arr[left]
	}
	if target >= arr[right] {
		return arr[right]
	}
	
	// Búsqueda binaria del rango donde está target
	for left < right {
		mid := left + (right-left)/2
		
		if arr[mid] == target {
			return arr[mid]
		}
		
		if target < arr[mid] {
			if mid > 0 && target > arr[mid-1] {
				return getClosest(arr[mid-1], arr[mid], target)
			}
			right = mid
		} else {
			if mid < len(arr)-1 && target < arr[mid+1] {
				return getClosest(arr[mid], arr[mid+1], target)
			}
			left = mid + 1
		}
	}
	
	return arr[left]
}

func getClosest(val1, val2, target int) int {
	if math.Abs(float64(target-val1)) <= math.Abs(float64(target-val2)) {
		return val1
	}
	return val2
}
