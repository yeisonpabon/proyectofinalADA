package main

// Power Set - O(2^n)
func powerSet(arr []int) [][]int {
	result := [][]int{}
	generateSubsets(arr, 0, []int{}, &result)
	return result
}

func generateSubsets(arr []int, index int, current []int, result *[][]int) {
	if index == len(arr) {
		subset := make([]int, len(current))
		copy(subset, current)
		*result = append(*result, subset)
		return
	}
	
	// No incluir elemento actual
	generateSubsets(arr, index+1, current, result)
	
	// Incluir elemento actual
	generateSubsets(arr, index+1, append(current, arr[index]), result)
}
