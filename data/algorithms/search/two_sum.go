package main

// Two Sum Problem - O(n²)
func twoSum(arr []int, target int) []int {
	n := len(arr)
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			if arr[i]+arr[j] == target {
				return []int{i, j}
			}
		}
	}
	return []int{-1, -1}
}
