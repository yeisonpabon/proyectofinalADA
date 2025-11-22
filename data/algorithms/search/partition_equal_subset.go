package main

import "fmt"

// Partition Equal Subset (fuerza bruta): O(2^n)
// Determina si un array se puede dividir en dos subconjuntos con suma igual
func canPartition(nums []int, n int, sum int, target int) bool {
	if sum == target {
		return true
	}
	if n == 0 || sum > target {
		return false
	}

	// Incluir o excluir el elemento actual
	return canPartition(nums, n-1, sum+nums[n-1], target) ||
		canPartition(nums, n-1, sum, target)
}

func main() {
	nums := []int{1, 5, 11, 5}
	total := 0
	for _, num := range nums {
		total += num
	}
	if total%2 == 0 {
		fmt.Println("Puede particionar:", canPartition(nums, len(nums), 0, total/2))
	} else {
		fmt.Println("No puede particionar (suma impar)")
	}
}
