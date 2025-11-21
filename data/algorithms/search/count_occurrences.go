package main

// Count Occurrences - O(n)
func countOccurrences(arr []int, target int) int {
	count := 0
	for i := 0; i < len(arr); i++ {
		if arr[i] == target {
			count++
		}
	}
	return count
}
