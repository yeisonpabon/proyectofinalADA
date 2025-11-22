package main

import "fmt"

// Calcula a^n en O(log n)
func fastPower(a, n int) int {
    result := 1
    base := a
    exp := n

    for exp > 0 { // Se repite log(n) veces
        if exp%2 == 1 {
            result *= base
        }
        base *= base
        exp /= 2 // divide entre 2 -> por eso es O(log n)
    }

    return result
}

func main() {
    fmt.Println(fastPower(3, 10)) // 3^10 = 59049
}
