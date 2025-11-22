package search

// FindMissingNumber encuentra el número faltante en secuencia con búsqueda binaria
// Complejidad: O(log n) - array de 0 a n con un número faltante
func FindMissingNumber(arr []int) int {
	n := len(arr)
	left := 0
	right := n - 1
	
	// Caso especial: falta el primer elemento
	if arr[0] != 0 {
		return 0
	}
	
	// Caso especial: falta el último elemento
	if arr[n-1] != n {
		return n
	}
	
	// Búsqueda binaria
	for left <= right {
		mid := left + (right-left)/2
		
		// El elemento en mid está en su posición correcta
		if arr[mid] == mid {
			left = mid + 1
		} else {
			// Verificar si el número faltante está justo antes de mid
			if mid == 0 || arr[mid-1] == mid-1 {
				return mid
			}
			right = mid - 1
		}
	}
	
	return -1
}
