package main

// Ternary Search - O(log n)
func ternarySearch(arr []int, target int, left int, right int) int {
	if right >= left {
		mid1 := left + (right-left)/3
		mid2 := right - (right-left)/3

		if arr[mid1] == target {
			return mid1
		}
		if arr[mid2] == target {
			return mid2
		}

		if target < arr[mid1] {
			return ternarySearch(arr, target, left, mid1-1)
		} else if target > arr[mid2] {
			return ternarySearch(arr, target, mid2+1, right)
		} else {
			return ternarySearch(arr, target, mid1+1, mid2-1)
		}
	}
	return -1
}
