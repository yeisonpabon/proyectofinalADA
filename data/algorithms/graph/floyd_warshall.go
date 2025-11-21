package main

// Floyd-Warshall
// Complejidad: O(n³) - Cúbico
// Tres loops anidados para caminos más cortos

func floydWarshall(graph [][]int) [][]int {
	n := len(graph)
	dist := make([][]int, n)
	
	for i := range dist {
		dist[i] = make([]int, n)
		copy(dist[i], graph[i])
	}
	
	for k := 0; k < n; k++ {
		for i := 0; i < n; i++ {
			for j := 0; j < n; j++ {
				if dist[i][k]+dist[k][j] < dist[i][j] {
					dist[i][j] = dist[i][k] + dist[k][j]
				}
			}
		}
	}
	
	return dist
}
