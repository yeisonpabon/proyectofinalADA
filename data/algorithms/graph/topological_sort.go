package main

// Topological Sort (DFS)
// Complejidad: O(V + E) - Lineal en grafos
// DFS con stack para ordenamiento topológico

func topologicalSort(graph map[int][]int, n int) []int {
	visited := make([]bool, n)
	stack := []int{}
	
	var dfsHelper func(int)
	dfsHelper = func(v int) {
		visited[v] = true
		
		for _, neighbor := range graph[v] {
			if !visited[neighbor] {
				dfsHelper(neighbor)
			}
		}
		
		stack = append([]int{v}, stack...)
	}
	
	for i := 0; i < n; i++ {
		if !visited[i] {
			dfsHelper(i)
		}
	}
	
	return stack
}
