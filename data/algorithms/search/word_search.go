package main

import "fmt"

// Word Search (backtracking): O(N * 3^L) exponencial
// Busca palabra en matriz usando backtracking
func wordSearch(board [][]byte, word string, row int, col int, idx int) bool {
	if idx == len(word) {
		return true
	}

	if row < 0 || row >= len(board) || col < 0 || col >= len(board[0]) ||
		board[row][col] != word[idx] || board[row][col] == '#' {
		return false
	}

	temp := board[row][col]
	board[row][col] = '#' // Marcar visitado

	found := wordSearch(board, word, row+1, col, idx+1) ||
		wordSearch(board, word, row-1, col, idx+1) ||
		wordSearch(board, word, row, col+1, idx+1) ||
		wordSearch(board, word, row, col-1, idx+1)

	board[row][col] = temp // Backtrack
	return found
}

func main() {
	board := [][]byte{
		{'A', 'B', 'C', 'E'},
		{'S', 'F', 'C', 'S'},
		{'A', 'D', 'E', 'E'},
	}
	word := "ABCCED"
	fmt.Println("Palabra encontrada:", wordSearch(board, word, 0, 0, 0))
}
