package search

// FindFixedPoint encuentra índice donde arr[i] == i usando búsqueda binaria
// Complejidad: O(log n) - array ordenado con elementos distintos
func FindFixedPoint(arr []int) int {
	left := 0
	right := len(arr) - 1
	
	for left <= right {
		mid := left + (right-left)/2
		
		if arr[mid] == mid {
			return mid
		}
		
		// Si arr[mid] > mid, el fixed point está a la izquierda
		if arr[mid] > mid {
			right = mid - 1
		} else {
			// arr[mid] < mid, el fixed point está a la derecha
			left = mid + 1
		}
	}
	
	return -1
}
