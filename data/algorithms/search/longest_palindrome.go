package main

// Longest Palindrome - O(n²)
func longestPalindrome(s string) string {
	if len(s) < 1 {
		return ""
	}
	
	start := 0
	maxLen := 1
	
	for i := 0; i < len(s); i++ {
		for j := i; j < len(s); j++ {
			if isPalindrome(s, i, j) && j-i+1 > maxLen {
				start = i
				maxLen = j - i + 1
			}
		}
	}
	
	return s[start : start+maxLen]
}

func isPalindrome(s string, left int, right int) bool {
	for left < right {
		if s[left] != s[right] {
			return false
		}
		left++
		right--
	}
	return true
}
