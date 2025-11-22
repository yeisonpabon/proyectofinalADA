package main

import "fmt"

// Graph Coloring: O(m^n) exponencial
// Asigna colores a vértices usando backtracking
func graphColoring(graph [][]int, m int, color []int, v int) bool {
	n := len(graph)
	if v == n {
		return true
	}

	for c := 1; c <= m; c++ {
		if isSafe(graph, color, v, c) {
			color[v] = c
			if graphColoring(graph, m, color, v+1) {
				return true
			}
			color[v] = 0 // Backtrack
		}
	}
	return false
}

func isSafe(graph [][]int, color []int, v int, c int) bool {
	for i := 0; i < len(graph); i++ {
		if graph[v][i] == 1 && color[i] == c {
			return false
		}
	}
	return true
}

func main() {
	graph := [][]int{
		{0, 1, 1, 1},
		{1, 0, 1, 0},
		{1, 1, 0, 1},
		{1, 0, 1, 0},
	}
	m := 3
	color := make([]int, len(graph))
	if graphColoring(graph, m, color, 0) {
		fmt.Println("Colores asignados:", color)
	}
}
