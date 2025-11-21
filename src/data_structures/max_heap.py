"""
Max Heap - Estructura de Datos de Prioridad Máxima

Implementación de Max Heap (montículo máximo) simétrica a Min Heap.

Complejidad:
    - insert(x): O(log n)
    - extract_max(): O(log n)
    - peek(): O(1)
    - heapify(arr): O(n)

Referencias:
    - Cormen et al. (2009). "Introduction to Algorithms", Chapter 6
"""

import numpy as np
from typing import List, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class HeapElement:
    """Elemento del heap con valor y datos asociados."""
    value: float
    data: Any = None
    
    def __lt__(self, other):
        return self.value > other.value  # Invertido para Max Heap
    
    def __le__(self, other):
        return self.value >= other.value
    
    def __gt__(self, other):
        return self.value < other.value
    
    def __repr__(self):
        return f"HeapElement({self.value}, {self.data})"


class MaxHeap:
    """
    Max Heap - Cola de prioridad máxima.
    
    Propiedades:
        - Cada nodo es mayor o igual que sus hijos
        - Raíz contiene el máximo elemento
    """
    
    def __init__(self, capacity: Optional[int] = None):
        """Inicializa Max Heap vacío."""
        self.heap: List[HeapElement] = []
        self.capacity = capacity
        self.operation_count = 0
    
    def size(self) -> int:
        """Retorna el número de elementos."""
        return len(self.heap)
    
    def is_empty(self) -> bool:
        """Verifica si está vacío."""
        return len(self.heap) == 0
    
    def is_full(self) -> bool:
        """Verifica si está lleno."""
        if self.capacity is None:
            return False
        return len(self.heap) >= self.capacity
    
    def _parent(self, i: int) -> int:
        return (i - 1) // 2
    
    def _left_child(self, i: int) -> int:
        return 2 * i + 1
    
    def _right_child(self, i: int) -> int:
        return 2 * i + 2
    
    def _swap(self, i: int, j: int):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.operation_count += 1
    
    def _bubble_up(self, i: int):
        """Restaura propiedad subiendo elemento. O(log n)"""
        while i > 0:
            parent = self._parent(i)
            self.operation_count += 1
            
            # Comparación por valor: hijo > padre
            if self.heap[i].value > self.heap[parent].value:
                self._swap(i, parent)
                i = parent
            else:
                break
    
    def _bubble_down(self, i: int):
        """Restaura propiedad bajando elemento. O(log n)"""
        n = len(self.heap)
        
        while True:
            largest = i
            left = self._left_child(i)
            right = self._right_child(i)
            
            if left < n:
                self.operation_count += 1
                # Comparación por valor
                if self.heap[left].value > self.heap[largest].value:
                    largest = left
            
            if right < n:
                self.operation_count += 1
                # Comparación por valor
                if self.heap[right].value > self.heap[largest].value:
                    largest = right
            
            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break
    
    def insert(self, value: float, data: Any = None):
        """Inserta elemento. O(log n)"""
        if self.is_full():
            raise ValueError("Heap lleno")
        
        element = HeapElement(value, data)
        self.heap.append(element)
        self._bubble_up(len(self.heap) - 1)
    
    def extract_max(self) -> Tuple[float, Any]:
        """Extrae y retorna el máximo. O(log n)"""
        if self.is_empty():
            raise IndexError("extract_max() en heap vacío")
        
        max_element = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        
        if not self.is_empty():
            self._bubble_down(0)
        
        return max_element.value, max_element.data
    
    def peek(self) -> Tuple[float, Any]:
        """Retorna el máximo sin extraerlo. O(1)"""
        if self.is_empty():
            raise IndexError("peek() en heap vacío")
        
        max_element = self.heap[0]
        return max_element.value, max_element.data
    
    def heapify(self, arr: List[float]):
        """Construye heap desde array. O(n)"""
        self.heap = [HeapElement(val) for val in arr]
        self.operation_count = 0
        
        n = len(self.heap)
        for i in range(n // 2 - 1, -1, -1):
            self._bubble_down(i)
    
    def increase_key(self, i: int, new_value: float):
        """Aumenta el valor de un elemento. O(log n)"""
        if i >= len(self.heap):
            raise IndexError("Índice fuera de rango")
        
        if new_value < self.heap[i].value:
            raise ValueError("Nuevo valor debe ser mayor")
        
        self.heap[i].value = new_value
        self._bubble_up(i)
    
    def get_sorted(self) -> List[float]:
        """Retorna elementos ordenados descendentemente. O(n log n)"""
        result = []
        while not self.is_empty():
            value, _ = self.extract_max()
            result.append(value)
        return result
    
    def __repr__(self) -> str:
        values = [elem.value for elem in self.heap]
        return f"MaxHeap({values})"


if __name__ == '__main__':
    # Demo rápida
    heap = MaxHeap()
    for val in [5, 3, 7, 1, 9, 2]:
        heap.insert(val)
    
    print(f"Max Heap: {heap}")
    print(f"Máximo: {heap.peek()[0]}")
    
    print("Extrayendo en orden descendente:")
    while not heap.is_empty():
        val, _ = heap.extract_max()
        print(f"  {val}")
