package main

import "fmt"

// Letter Combinations: O(4^n) exponencial
// Genera combinaciones de letras del teclado telefónico
var phoneMap = map[byte]string{
	'2': "abc", '3': "def", '4': "ghi", '5': "jkl",
	'6': "mno", '7': "pqrs", '8': "tuv", '9': "wxyz",
}

func letterCombinations(digits string, idx int, current string, result *[]string) {
	if idx == len(digits) {
		if current != "" {
			*result = append(*result, current)
		}
		return
	}

	letters := phoneMap[digits[idx]]
	for i := 0; i < len(letters); i++ {
		letterCombinations(digits, idx+1, current+string(letters[i]), result)
	}
}

func main() {
	digits := "23"
	var result []string
	letterCombinations(digits, 0, "", &result)
	fmt.Println("Combinaciones:", result)
}
