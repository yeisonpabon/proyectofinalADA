package main

// Merge Sort
// Complejidad: O(n log n)
// Recurrencia: T(n) = 2T(n/2) + O(n)

func mergeSort(arr []int) []int {
	if len(arr) <= 1 {
		return arr
	}
	
	mid := len(arr) / 2
	left := mergeSort(arr[:mid])
	right := mergeSort(arr[mid:])
	
	return merge(left, right)
}

func merge(left []int, right []int) []int {
	result := make([]int, 0)
	i, j := 0, 0
	
	for i < len(left) && j < len(right) {
		if left[i] <= right[j] {
			result = append(result, left[i])
			i++
		} else {
			result = append(result, right[j])
			j++
		}
	}
	
	result = append(result, left[i:]...)
	result = append(result, right[j:]...)
	
	return result
}
