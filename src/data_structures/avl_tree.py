"""
AVL Tree - Árbol Binario de Búsqueda Balanceado

Implementación de AVL Tree con rotaciones automáticas para mantener balance.

Complejidad:
    - insert(x): O(log n) - Garantizado
    - delete(x): O(log n) - Garantizado
    - search(x): O(log n) - Garantizado
    - min/max: O(log n)

Propiedades:
    - BST: izquierdo < nodo < derecho
    - Factor de balance: |altura(izq) - altura(der)| ≤ 1
    - Rotaciones: LL, RR, LR, RL

Referencias:
    - Adelson-Velsky & Landis (1962). "An algorithm for the organization of information"
    - Cormen et al. (2009). "Introduction to Algorithms", Chapter 13
"""

from typing import Optional, List, Tuple
from dataclasses import dataclass


@dataclass
class AVLNode:
    """Nodo del AVL Tree."""
    key: int
    value: any = None
    left: Optional['AVLNode'] = None
    right: Optional['AVLNode'] = None
    height: int = 1
    
    def __repr__(self):
        return f"AVLNode({self.key})"


class AVLTree:
    """
    AVL Tree - Árbol binario de búsqueda auto-balanceado.
    
    Mantiene factor de balance [-1, 0, 1] en cada nodo mediante rotaciones.
    """
    
    def __init__(self):
        """Inicializa AVL Tree vacío."""
        self.root: Optional[AVLNode] = None
        self.size_count = 0
        self.rotation_count = 0
    
    def _height(self, node: Optional[AVLNode]) -> int:
        """Retorna altura del nodo (0 si None)."""
        return node.height if node else 0
    
    def _balance_factor(self, node: AVLNode) -> int:
        """Calcula factor de balance: altura(izq) - altura(der)."""
        return self._height(node.left) - self._height(node.right)
    
    def _update_height(self, node: AVLNode):
        """Actualiza altura del nodo."""
        node.height = 1 + max(self._height(node.left), self._height(node.right))
    
    def _rotate_right(self, z: AVLNode) -> AVLNode:
        """
        Rotación derecha (LL).
        
              z                   y
             / \\                 / \\
            y   T4    -->       x   z
           / \\                /   / \\
          x  T3              T1  T3 T4
         / \\
        T1 T2
        """
        self.rotation_count += 1
        
        y = z.left
        T3 = y.right
        
        # Rotar
        y.right = z
        z.left = T3
        
        # Actualizar alturas
        self._update_height(z)
        self._update_height(y)
        
        return y
    
    def _rotate_left(self, z: AVLNode) -> AVLNode:
        """
        Rotación izquierda (RR).
        
          z                     y
         / \\                   / \\
        T1  y       -->       z   x
           / \\               / \\ / \\
          T2  x            T1 T2 T3 T4
             / \\
            T3 T4
        """
        self.rotation_count += 1
        
        y = z.right
        T2 = y.left
        
        # Rotar
        y.left = z
        z.right = T2
        
        # Actualizar alturas
        self._update_height(z)
        self._update_height(y)
        
        return y
    
    def insert(self, key: int, value: any = None):
        """
        Inserta clave en el árbol. O(log n)
        
        Args:
            key: Clave a insertar
            value: Valor asociado
        """
        self.root = self._insert_recursive(self.root, key, value)
        self.size_count += 1
    
    def _insert_recursive(self, node: Optional[AVLNode], key: int, value: any) -> AVLNode:
        """Inserción recursiva con balanceo."""
        # 1. BST insert normal
        if node is None:
            return AVLNode(key, value)
        
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)
        else:
            # Clave duplicada: actualizar valor
            node.value = value
            return node
        
        # 2. Actualizar altura
        self._update_height(node)
        
        # 3. Obtener factor de balance
        balance = self._balance_factor(node)
        
        # 4. Casos de desbalance
        
        # Caso LL: Rotación derecha simple
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        
        # Caso RR: Rotación izquierda simple
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        
        # Caso LR: Rotación izquierda-derecha
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Caso RL: Rotación derecha-izquierda
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def search(self, key: int) -> Optional[any]:
        """Busca clave en el árbol. O(log n)"""
        node = self._search_node(self.root, key)
        return node.key if node else None
    
    def _search_node(self, node: Optional[AVLNode], key: int) -> Optional[AVLNode]:
        """Búsqueda recursiva."""
        if node is None or node.key == key:
            return node
        
        if key < node.key:
            return self._search_node(node.left, key)
        else:
            return self._search_node(node.right, key)
    
    def delete(self, key: int):
        """Elimina clave del árbol. O(log n)"""
        self.root = self._delete_recursive(self.root, key)
        self.size_count -= 1
    
    def _delete_recursive(self, node: Optional[AVLNode], key: int) -> Optional[AVLNode]:
        """Eliminación recursiva con balanceo."""
        if node is None:
            return node
        
        # 1. BST delete normal
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Nodo a eliminar encontrado
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Nodo con dos hijos: sucesor inorder
            successor = self._min_node(node.right)
            node.key = successor.key
            node.value = successor.value
            node.right = self._delete_recursive(node.right, successor.key)
        
        # 2. Actualizar altura
        self._update_height(node)
        
        # 3. Balancear
        balance = self._balance_factor(node)
        
        # LL
        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)
        
        # LR
        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # RR
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)
        
        # RL
        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _min_node(self, node: AVLNode) -> AVLNode:
        """Encuentra nodo con clave mínima."""
        current = node
        while current.left:
            current = current.left
        return current
    
    def inorder(self) -> List[int]:
        """Recorrido inorder (ordenado). O(n)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[AVLNode], result: List[int]):
        """Recorrido inorder recursivo."""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.key)
            self._inorder_recursive(node.right, result)
    
    def size(self) -> int:
        """Retorna número de nodos."""
        return self.size_count
    
    def height(self) -> int:
        """Retorna altura del árbol."""
        return self._height(self.root)
    
    def is_balanced(self) -> bool:
        """Verifica si el árbol está balanceado."""
        return self._check_balance(self.root)
    
    def _check_balance(self, node: Optional[AVLNode]) -> bool:
        """Verifica balance recursivamente."""
        if node is None:
            return True
        
        balance = self._balance_factor(node)
        if abs(balance) > 1:
            return False
        
        return self._check_balance(node.left) and self._check_balance(node.right)
    
    def __repr__(self):
        return f"AVLTree(size={self.size_count}, height={self.height()})"


if __name__ == '__main__':
    # Demo
    avl = AVLTree()
    
    keys = [10, 20, 30, 40, 50, 25]
    print(f"Insertando: {keys}")
    
    for key in keys:
        avl.insert(key)
        print(f"  Insertado {key} | Altura: {avl.height()} | Rotaciones: {avl.rotation_count}")
    
    print(f"\nInorder: {avl.inorder()}")
    print(f"Balanceado: {avl.is_balanced()}")
