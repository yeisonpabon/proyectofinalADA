package search

// BitonicSearch busca en array bitónico (crece y decrece)
// Complejidad: O(log n) - dos búsquedas binarias
func BitonicSearch(arr []int, target int) int {
	n := len(arr)
	if n == 0 {
		return -1
	}
	
	// Encontrar el punto máximo (pico)
	peak := findPeak(arr, 0, n-1)
	
	// Buscar en la parte creciente
	result := binarySearchAsc(arr, 0, peak, target)
	if result != -1 {
		return result
	}
	
	// Buscar en la parte decreciente
	return binarySearchDesc(arr, peak+1, n-1, target)
}

func findPeak(arr []int, left, right int) int {
	for left < right {
		mid := left + (right-left)/2
		
		if arr[mid] < arr[mid+1] {
			left = mid + 1
		} else {
			right = mid
		}
	}
	return left
}

func binarySearchAsc(arr []int, left, right, target int) int {
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

func binarySearchDesc(arr []int, left, right, target int) int {
	for left <= right {
		mid := left + (right-left)/2
		
		if arr[mid] == target {
			return mid
		} else if arr[mid] > target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}
	return -1
}
