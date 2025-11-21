package main

// N-Queens Problem - O(n!)
func solveNQueens(n int) [][]string {
	result := [][]string{}
	board := make([][]string, n)
	for i := range board {
		board[i] = make([]string, n)
		for j := range board[i] {
			board[i][j] = "."
		}
	}
	
	backtrack(board, 0, &result)
	return result
}

func backtrack(board [][]string, row int, result *[][]string) {
	if row == len(board) {
		solution := make([]string, len(board))
		for i := range board {
			solution[i] = ""
			for j := range board[i] {
				solution[i] += board[i][j]
			}
		}
		*result = append(*result, solution)
		return
	}
	
	for col := 0; col < len(board); col++ {
		if isValid(board, row, col) {
			board[row][col] = "Q"
			backtrack(board, row+1, result)
			board[row][col] = "."
		}
	}
}

func isValid(board [][]string, row int, col int) bool {
	// Verificar columna
	for i := 0; i < row; i++ {
		if board[i][col] == "Q" {
			return false
		}
	}
	
	// Verificar diagonal izquierda
	for i, j := row-1, col-1; i >= 0 && j >= 0; i, j = i-1, j-1 {
		if board[i][j] == "Q" {
			return false
		}
	}
	
	// Verificar diagonal derecha
	for i, j := row-1, col+1; i >= 0 && j < len(board); i, j = i-1, j+1 {
		if board[i][j] == "Q" {
			return false
		}
	}
	
	return true
}
