package main

import "fmt"

// Knapsack 0/1 (fuerza bruta): O(2^n)
// Prueba todas las combinaciones de items
func knapsack(weights []int, values []int, capacity int, n int) int {
	if n == 0 || capacity == 0 {
		return 0
	}

	if weights[n-1] > capacity {
		return knapsack(weights, values, capacity, n-1)
	}

	// Incluir o excluir el item actual
	include := values[n-1] + knapsack(weights, values, capacity-weights[n-1], n-1)
	exclude := knapsack(weights, values, capacity, n-1)

	if include > exclude {
		return include
	}
	return exclude
}

func main() {
	values := []int{60, 100, 120}
	weights := []int{10, 20, 30}
	capacity := 50
	n := len(values)
	fmt.Println("Valor máximo:", knapsack(weights, values, capacity, n))
}
