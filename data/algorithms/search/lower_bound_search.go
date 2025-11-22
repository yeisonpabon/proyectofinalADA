package main

// Lower Bound Binary Search - O(log n)
// Encuentra el primer elemento >= target
func lowerBound(arr []int, target int) int {
	left, right := 0, len(arr)
	
	for left < right {
		mid := left + (right-left)/2
		
		if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid
		}
	}
	
	return left
}
