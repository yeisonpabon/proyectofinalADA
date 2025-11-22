package main

// Peak Element Binary Search - O(log n)
// Encuentra un elemento pico (mayor que sus vecinos)
func peakElementSearch(arr []int) int {
	left, right := 0, len(arr)-1
	
	for left < right {
		mid := left + (right-left)/2
		
		if arr[mid] < arr[mid+1] {
			// Pico está a la derecha
			left = mid + 1
		} else {
			// Pico está a la izquierda o es mid
			right = mid
		}
	}
	
	return left
}
