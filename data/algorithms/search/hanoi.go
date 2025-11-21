package main

// Torres de Hanoi
// Complejidad: O(2^n) - Exponencial
// Recurrencia: T(n) = 2T(n-1) + O(1)

func hanoi(n int, from string, to string, aux string) {
	if n == 1 {
		return
	}
	
	hanoi(n-1, from, aux, to)
	hanoi(n-1, aux, to, from)
}
