package search

// SearchInfiniteArray busca en array infinito (o muy grande)
// Complejidad: O(log n) - encontrar rango exponencialmente y luego binary search
func SearchInfiniteArray(arr []int, target int) int {
	// Encontrar rango exponencialmente
	left := 0
	right := 1
	
	// Expandir hasta encontrar un rango que contenga target
	for arr[right] < target {
		left = right
		right = right * 2
	}
	
	// Búsqueda binaria en el rango encontrado
	return binarySearchRange(arr, left, right, target)
}

func binarySearchRange(arr []int, left, right, target int) int {
	for left <= right {
		mid := left + (right-left)/2
		
		if arr[mid] == target {
			return mid
		} else if arr[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}
	
	return -1
}
