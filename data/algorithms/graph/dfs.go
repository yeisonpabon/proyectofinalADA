package main

// DFS (Depth-First Search) recursivo
// Complejidad: O(V + E) donde V=vértices, E=aristas
// Recurrencia: T(n) = T(n-1) + O(1) en grafo lineal

func dfs(graph map[int][]int, node int, visited map[int]bool) {
	if visited[node] {
		return
	}
	
	visited[node] = true
	
	for _, neighbor := range graph[node] {
		dfs(graph, neighbor, visited)
	}
}
