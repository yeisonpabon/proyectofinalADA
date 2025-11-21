package main

// Interpolation Search
// Complejidad: O(log log n) promedio, O(n) peor caso
// Mejor que binary search para datos uniformemente distribuidos

func interpolationSearch(arr []int, target int) int {
	low := 0
	high := len(arr) - 1
	
	for low <= high && target >= arr[low] && target <= arr[high] {
		if low == high {
			if arr[low] == target {
				return low
			}
			return -1
		}
		
		pos := low + ((target-arr[low])*(high-low))/(arr[high]-arr[low])
		
		if arr[pos] == target {
			return pos
		}
		
		if arr[pos] < target {
			low = pos + 1
		} else {
			high = pos - 1
		}
	}
	
	return -1
}
