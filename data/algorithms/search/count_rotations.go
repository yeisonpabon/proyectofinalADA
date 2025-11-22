package search

// CountRotations cuenta cuántas veces se rotó un array ordenado
// Complejidad: O(log n) - encuentra el índice del elemento mínimo
func CountRotations(arr []int) int {
	n := len(arr)
	if n == 0 {
		return 0
	}
	
	left := 0
	right := n - 1
	
	// Array no rotado
	if arr[left] <= arr[right] {
		return 0
	}
	
	// Búsqueda binaria del punto de rotación
	for left <= right {
		mid := left + (right-left)/2
		
		// Siguiente elemento en forma circular
		next := (mid + 1) % n
		prev := (mid + n - 1) % n
		
		// El elemento más pequeño será menor que sus vecinos
		if arr[mid] <= arr[next] && arr[mid] <= arr[prev] {
			return mid
		}
		
		// Decidir qué mitad buscar
		if arr[mid] <= arr[right] {
			right = mid - 1
		} else if arr[mid] >= arr[left] {
			left = mid + 1
		}
	}
	
	return 0
}
