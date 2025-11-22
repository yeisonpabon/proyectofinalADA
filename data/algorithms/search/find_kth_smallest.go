package search

// FindKthSmallest encuentra el k-ésimo elemento más pequeño usando búsqueda binaria
// Complejidad: O(log n) promedio con particionamiento
func FindKthSmallest(arr []int, k int) int {
	if k < 1 || k > len(arr) {
		return -1
	}
	
	return quickSelect(arr, 0, len(arr)-1, k-1)
}

func quickSelect(arr []int, left, right, k int) int {
	if left == right {
		return arr[left]
	}
	
	pivotIndex := partition(arr, left, right)
	
	if k == pivotIndex {
		return arr[k]
	} else if k < pivotIndex {
		return quickSelect(arr, left, pivotIndex-1, k)
	} else {
		return quickSelect(arr, pivotIndex+1, right, k)
	}
}

func partition(arr []int, left, right int) int {
	pivot := arr[right]
	i := left
	
	for j := left; j < right; j++ {
		if arr[j] <= pivot {
			arr[i], arr[j] = arr[j], arr[i]
			i++
		}
	}
	
	arr[i], arr[right] = arr[right], arr[i]
	return i
}
