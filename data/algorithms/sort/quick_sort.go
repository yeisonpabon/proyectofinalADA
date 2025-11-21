package main

// Quick Sort
// Complejidad: O(n log n) promedio, O(n²) peor caso
// Recurrencia: T(n) = 2T(n/2) + O(n)

func quickSort(arr []int, low int, high int) {
	if low < high {
		pi := partition(arr, low, high)
		quickSort(arr, low, pi-1)
		quickSort(arr, pi+1, high)
	}
}

func partition(arr []int, low int, high int) int {
	pivot := arr[high]
	i := low - 1
	
	for j := low; j < high; j++ {
		if arr[j] <= pivot {
			i++
			arr[i], arr[j] = arr[j], arr[i]
		}
	}
	
	arr[i+1], arr[high] = arr[high], arr[i+1]
	return i + 1
}
