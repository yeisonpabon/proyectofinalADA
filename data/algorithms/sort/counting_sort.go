package main

// Counting Sort
// Complejidad: O(n + k) donde k es el rango de valores
// Lineal cuando k = O(n)

func countingSort(arr []int) []int {
	if len(arr) == 0 {
		return arr
	}
	
	max := arr[0]
	min := arr[0]
	
	for _, val := range arr {
		if val > max {
			max = val
		}
		if val < min {
			min = val
		}
	}
	
	rangeSize := max - min + 1
	count := make([]int, rangeSize)
	output := make([]int, len(arr))
	
	for _, val := range arr {
		count[val-min]++
	}
	
	for i := 1; i < len(count); i++ {
		count[i] += count[i-1]
	}
	
	for i := len(arr) - 1; i >= 0; i-- {
		val := arr[i]
		output[count[val-min]-1] = val
		count[val-min]--
	}
	
	return output
}
