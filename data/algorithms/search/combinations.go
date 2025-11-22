package main

import "fmt"

// Combinaciones: C(n,k) = O(2^n) en el peor caso
// Genera todas las combinaciones de k elementos de un conjunto
func combinations(arr []int, k int, start int, current []int, result *[][]int) {
	if len(current) == k {
		// Copiar combinación actual
		comb := make([]int, k)
		copy(comb, current)
		*result = append(*result, comb)
		return
	}

	for i := start; i < len(arr); i++ {
		current = append(current, arr[i])
		combinations(arr, k, i+1, current, result)
		current = current[:len(current)-1]
	}
}

func main() {
	arr := []int{1, 2, 3, 4}
	var result [][]int
	combinations(arr, 2, 0, []int{}, &result)
	fmt.Println("Combinaciones:", result)
}
