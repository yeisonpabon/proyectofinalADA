package main

// Heap Sort
// Complejidad: O(n log n)
// Construcción del heap O(n) + n extracciones O(log n)

func heapSort(arr []int) []int {
	n := len(arr)
	
	// Construir max heap
	for i := n/2 - 1; i >= 0; i-- {
		heapify(arr, n, i)
	}
	
	// Extraer elementos del heap
	for i := n - 1; i > 0; i-- {
		arr[0], arr[i] = arr[i], arr[0]
		heapify(arr, i, 0)
	}
	
	return arr
}

func heapify(arr []int, n int, i int) {
	largest := i
	left := 2*i + 1
	right := 2*i + 2
	
	if left < n && arr[left] > arr[largest] {
		largest = left
	}
	
	if right < n && arr[right] > arr[largest] {
		largest = right
	}
	
	if largest != i {
		arr[i], arr[largest] = arr[largest], arr[i]
		heapify(arr, n, largest)
	}
}
