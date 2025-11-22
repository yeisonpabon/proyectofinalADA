package main

// Búsqueda en árbol binario (O(log n) en árbol balanceado)
type TreeNode struct {
	val   int
	left  *TreeNode
	right *TreeNode
}

func searchBST(root *TreeNode, target int) *TreeNode {
	current := root
	
	for current != nil {
		if current.val == target {
			return current
		} else if target < current.val {
			current = current.left
		} else {
			current = current.right
		}
	}
	
	return nil
}
