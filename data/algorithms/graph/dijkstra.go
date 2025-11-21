package main

// Dijkstra
// Complejidad: O(n²) con matriz de adyacencia
// O((V+E) log V) con heap

func dijkstra(graph [][]int, src int) []int {
	n := len(graph)
	dist := make([]int, n)
	visited := make([]bool, n)
	
	for i := range dist {
		dist[i] = int(^uint(0) >> 1) // Max int
	}
	dist[src] = 0
	
	for count := 0; count < n-1; count++ {
		u := minDistance(dist, visited)
		visited[u] = true
		
		for v := 0; v < n; v++ {
			if !visited[v] && graph[u][v] != 0 && 
			   dist[u] != int(^uint(0)>>1) && 
			   dist[u]+graph[u][v] < dist[v] {
				dist[v] = dist[u] + graph[u][v]
			}
		}
	}
	
	return dist
}

func minDistance(dist []int, visited []bool) int {
	min := int(^uint(0) >> 1)
	minIndex := -1
	
	for v := 0; v < len(dist); v++ {
		if !visited[v] && dist[v] <= min {
			min = dist[v]
			minIndex = v
		}
	}
	
	return minIndex
}
