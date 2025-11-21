package main

// Acceso a elemento de array
// Complejidad: O(1) - Constante
// No hay loops ni recursión

func getElement(arr []int, index int) int {
	if index >= 0 && index < len(arr) {
		return arr[index]
	}
	return -1
}
