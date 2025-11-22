package main

import "fmt"

// Rat in a Maze: O(2^(n^2)) exponencial
// Encuentra camino en laberinto usando backtracking
func solveMaze(maze [][]int, x int, y int, sol [][]int, n int) bool {
	if x == n-1 && y == n-1 && maze[x][y] == 1 {
		sol[x][y] = 1
		return true
	}

	if x >= 0 && x < n && y >= 0 && y < n && maze[x][y] == 1 {
		sol[x][y] = 1

		// Mover derecha
		if solveMaze(maze, x+1, y, sol, n) {
			return true
		}
		// Mover abajo
		if solveMaze(maze, x, y+1, sol, n) {
			return true
		}

		sol[x][y] = 0 // Backtrack
		return false
	}
	return false
}

func main() {
	maze := [][]int{
		{1, 0, 0, 0},
		{1, 1, 0, 1},
		{0, 1, 0, 0},
		{1, 1, 1, 1},
	}
	n := len(maze)
	sol := make([][]int, n)
	for i := range sol {
		sol[i] = make([]int, n)
	}
	if solveMaze(maze, 0, 0, sol, n) {
		fmt.Println("Solución encontrada")
	}
}
