package main

import "fmt"

// Generar paréntesis válidos: O(4^n / sqrt(n)) ~ exponencial
// Backtracking con poda
func generateParenthesis(n int, open int, close int, current string, result *[]string) {
	if len(current) == 2*n {
		*result = append(*result, current)
		return
	}

	if open < n {
		generateParenthesis(n, open+1, close, current+"(", result)
	}
	if close < open {
		generateParenthesis(n, open, close+1, current+")", result)
	}
}

func main() {
	n := 3
	var result []string
	generateParenthesis(n, 0, 0, "", &result)
	fmt.Println("Paréntesis válidos:", result)
}
