package search

// BinarySearch2D realiza búsqueda binaria en matriz 2D ordenada
// Complejidad: O(log(n*m)) = O(log n + log m)
// La matriz está ordenada por filas y columnas
func BinarySearch2D(matrix [][]int, target int) bool {
	if len(matrix) == 0 || len(matrix[0]) == 0 {
		return false
	}
	
	rows := len(matrix)
	cols := len(matrix[0])
	left := 0
	right := rows*cols - 1
	
	for left <= right {
		mid := left + (right-left)/2
		midValue := matrix[mid/cols][mid%cols]
		
		if midValue == target {
			return true
		} else if midValue < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}
	
	return false
}
