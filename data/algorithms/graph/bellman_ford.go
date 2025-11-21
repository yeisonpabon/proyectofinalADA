package main

// Bellman-Ford
// Complejidad: O(V·E) donde V=vértices, E=aristas
// Dos loops anidados sobre vértices y aristas

type Edge struct {
	src, dest, weight int
}

func bellmanFord(vertices int, edges []Edge, src int) []int {
	dist := make([]int, vertices)
	
	for i := range dist {
		dist[i] = int(^uint(0) >> 1) // Max int
	}
	dist[src] = 0
	
	// Relajar aristas V-1 veces
	for i := 0; i < vertices-1; i++ {
		for _, edge := range edges {
			if dist[edge.src] != int(^uint(0)>>1) && 
			   dist[edge.src]+edge.weight < dist[edge.dest] {
				dist[edge.dest] = dist[edge.src] + edge.weight
			}
		}
	}
	
	return dist
}
