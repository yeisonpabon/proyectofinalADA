package main

// Permutaciones (Backtracking)
// Complejidad: O(n!) - Factorial
// Genera todas las permutaciones

func permutations(arr []int) [][]int {
	result := [][]int{}
	permutationsHelper(arr, 0, &result)
	return result
}

func permutationsHelper(arr []int, start int, result *[][]int) {
	if start == len(arr)-1 {
		temp := make([]int, len(arr))
		copy(temp, arr)
		*result = append(*result, temp)
		return
	}
	
	for i := start; i < len(arr); i++ {
		arr[start], arr[i] = arr[i], arr[start]
		permutationsHelper(arr, start+1, result)
		arr[start], arr[i] = arr[i], arr[start]
	}
}
