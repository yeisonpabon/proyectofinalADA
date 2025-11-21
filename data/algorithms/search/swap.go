package main

// Swap dos elementos
// Complejidad: O(1) - Constante
// Operación atómica

func swap(a *int, b *int) {
	temp := *a
	*a = *b
	*b = temp
}
