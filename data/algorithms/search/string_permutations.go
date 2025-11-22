package main

import "fmt"

// Permutaciones de string: O(n!)
// Genera todas las permutaciones de una cadena
func permuteString(s string, l int, r int) {
	if l == r {
		fmt.Println(s)
		return
	}

	runes := []rune(s)
	for i := l; i <= r; i++ {
		// Swap
		runes[l], runes[i] = runes[i], runes[l]
		permuteString(string(runes), l+1, r)
		// Backtrack
		runes[l], runes[i] = runes[i], runes[l]
	}
}

func main() {
	str := "ABC"
	permuteString(str, 0, len(str)-1)
}
