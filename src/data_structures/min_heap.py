"""
Min Heap - Estructura de Datos de Prioridad Mínima

Implementación de Min Heap (montículo mínimo) con operaciones eficientes.
Usado para hard mining en entrenamiento de redes neuronales.

Complejidad:
    - insert(x): O(log n) - Insertar elemento
    - extract_min(): O(log n) - Extraer mínimo
    - peek(): O(1) - Ver mínimo sin extraer
    - heapify(arr): O(n) - Construir heap desde array
    - decrease_key(i, val): O(log n) - Decrementar valor

Hard Mining:
    El Min Heap se usa para mantener los ejemplos más difíciles (mayor loss)
    durante el entrenamiento, permitiendo focalizar en muestras problemáticas.

Referencias:
    - Cormen et al. (2009). "Introduction to Algorithms", Chapter 6
    - Williams, J. W. J. (1964). "Algorithm 232: Heapsort"
"""

import numpy as np
from typing import List, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class HeapElement:
    """
    Elemento del heap con valor y datos asociados.
    
    Atributos:
        value: Valor de prioridad (menor = mayor prioridad en Min Heap)
        data: Datos asociados (ej: índice de muestra, pérdida, etc.)
    """
    value: float
    data: Any = None
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __le__(self, other):
        return self.value <= other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __repr__(self):
        return f"HeapElement({self.value}, {self.data})"


class MinHeap:
    """
    Min Heap - Cola de prioridad mínima.
    
    Propiedades:
        - Árbol binario completo
        - Cada nodo es menor o igual que sus hijos
        - Raíz contiene el mínimo elemento
        - Representado como array: hijo_izq(i) = 2i+1, hijo_der(i) = 2i+2
    """
    
    def __init__(self, capacity: Optional[int] = None):
        """
        Inicializa Min Heap vacío.
        
        Args:
            capacity: Capacidad máxima (None = ilimitado)
        """
        self.heap: List[HeapElement] = []
        self.capacity = capacity
        self.operation_count = 0  # Contador de operaciones
    
    def size(self) -> int:
        """Retorna el número de elementos en el heap."""
        return len(self.heap)
    
    def is_empty(self) -> bool:
        """Verifica si el heap está vacío."""
        return len(self.heap) == 0
    
    def is_full(self) -> bool:
        """Verifica si el heap está lleno (si tiene capacidad)."""
        if self.capacity is None:
            return False
        return len(self.heap) >= self.capacity
    
    def _parent(self, i: int) -> int:
        """Retorna índice del padre."""
        return (i - 1) // 2
    
    def _left_child(self, i: int) -> int:
        """Retorna índice del hijo izquierdo."""
        return 2 * i + 1
    
    def _right_child(self, i: int) -> int:
        """Retorna índice del hijo derecho."""
        return 2 * i + 2
    
    def _swap(self, i: int, j: int):
        """Intercambia dos elementos."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.operation_count += 1
    
    def _bubble_up(self, i: int):
        """
        Restaura propiedad del heap subiendo elemento.
        
        Usado después de insert para mantener invariante.
        Complejidad: O(log n)
        
        Args:
            i: Índice del elemento a subir
        """
        while i > 0:
            parent = self._parent(i)
            self.operation_count += 1
            
            if self.heap[i] < self.heap[parent]:
                self._swap(i, parent)
                i = parent
            else:
                break
    
    def _bubble_down(self, i: int):
        """
        Restaura propiedad del heap bajando elemento.
        
        Usado después de extract_min para mantener invariante.
        Complejidad: O(log n)
        
        Args:
            i: Índice del elemento a bajar
        """
        n = len(self.heap)
        
        while True:
            smallest = i
            left = self._left_child(i)
            right = self._right_child(i)
            
            # Comparar con hijo izquierdo
            if left < n:
                self.operation_count += 1
                if self.heap[left] < self.heap[smallest]:
                    smallest = left
            
            # Comparar con hijo derecho
            if right < n:
                self.operation_count += 1
                if self.heap[right] < self.heap[smallest]:
                    smallest = right
            
            # Si el más pequeño no es el nodo actual, intercambiar
            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break
    
    def insert(self, value: float, data: Any = None):
        """
        Inserta elemento en el heap.
        
        Complejidad: O(log n)
        
        Args:
            value: Valor de prioridad
            data: Datos asociados
        
        Raises:
            ValueError: Si el heap está lleno
        
        Examples:
            >>> heap = MinHeap()
            >>> heap.insert(5)
            >>> heap.insert(3)
            >>> heap.insert(7)
            >>> heap.peek()
            3
        """
        if self.is_full():
            raise ValueError("Heap lleno")
        
        # Agregar al final
        element = HeapElement(value, data)
        self.heap.append(element)
        
        # Restaurar propiedad del heap
        self._bubble_up(len(self.heap) - 1)
    
    def extract_min(self) -> Tuple[float, Any]:
        """
        Extrae y retorna el elemento mínimo.
        
        Complejidad: O(log n)
        
        Returns:
            Tupla (valor, datos)
        
        Raises:
            IndexError: Si el heap está vacío
        
        Examples:
            >>> heap = MinHeap()
            >>> heap.insert(5)
            >>> heap.insert(3)
            >>> heap.extract_min()
            (3, None)
        """
        if self.is_empty():
            raise IndexError("extract_min() en heap vacío")
        
        # Guardar mínimo
        min_element = self.heap[0]
        
        # Mover último elemento a la raíz
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        
        # Restaurar propiedad si no está vacío
        if not self.is_empty():
            self._bubble_down(0)
        
        return min_element.value, min_element.data
    
    def peek(self) -> Tuple[float, Any]:
        """
        Retorna el elemento mínimo sin extraerlo.
        
        Complejidad: O(1)
        
        Returns:
            Tupla (valor, datos)
        
        Raises:
            IndexError: Si el heap está vacío
        """
        if self.is_empty():
            raise IndexError("peek() en heap vacío")
        
        min_element = self.heap[0]
        return min_element.value, min_element.data
    
    def heapify(self, arr: List[float]):
        """
        Construye heap desde array desordenado.
        
        Algoritmo de Floyd: O(n) en lugar de O(n log n)
        
        Args:
            arr: Lista de valores
        
        Examples:
            >>> heap = MinHeap()
            >>> heap.heapify([5, 3, 7, 1, 9, 2])
            >>> heap.peek()
            1
        """
        self.heap = [HeapElement(val) for val in arr]
        self.operation_count = 0
        
        # Comenzar desde último nodo interno
        n = len(self.heap)
        for i in range(n // 2 - 1, -1, -1):
            self._bubble_down(i)
    
    def decrease_key(self, i: int, new_value: float):
        """
        Disminuye el valor de un elemento.
        
        Complejidad: O(log n)
        
        Args:
            i: Índice del elemento
            new_value: Nuevo valor (debe ser menor)
        
        Raises:
            ValueError: Si el nuevo valor es mayor
            IndexError: Si el índice está fuera de rango
        """
        if i >= len(self.heap):
            raise IndexError("Índice fuera de rango")
        
        if new_value > self.heap[i].value:
            raise ValueError("Nuevo valor debe ser menor")
        
        self.heap[i].value = new_value
        self._bubble_up(i)
    
    def get_sorted(self) -> List[float]:
        """
        Retorna elementos ordenados (destruye el heap).
        
        Complejidad: O(n log n)
        
        Returns:
            Lista ordenada de valores
        """
        result = []
        while not self.is_empty():
            value, _ = self.extract_min()
            result.append(value)
        return result
    
    def get_operation_count(self) -> int:
        """Retorna el número de operaciones realizadas."""
        return self.operation_count
    
    def reset_operation_count(self):
        """Reinicia el contador de operaciones."""
        self.operation_count = 0
    
    def __repr__(self) -> str:
        """Representación del heap."""
        values = [elem.value for elem in self.heap]
        return f"MinHeap({values})"


class HardMiningHeap:
    """
    Min Heap especializado para Hard Mining en entrenamiento de ML.
    
    Mantiene los ejemplos con mayor pérdida (loss) para focalizar
    el entrenamiento en muestras difíciles.
    """
    
    def __init__(self, capacity: int, strategy: str = 'loss'):
        """
        Inicializa heap para hard mining.
        
        Args:
            capacity: Número máximo de ejemplos difíciles a mantener
            strategy: 'loss' (mayor pérdida) o 'confidence' (menor confianza)
        """
        self.heap = MinHeap(capacity=capacity)
        self.strategy = strategy
        self.sample_count = 0
    
    def add_sample(self, sample_idx: int, loss: float, confidence: float = None):
        """
        Agrega muestra al heap de ejemplos difíciles.
        
        Args:
            sample_idx: Índice de la muestra
            loss: Pérdida de la muestra
            confidence: Confianza de la predicción
        """
        self.sample_count += 1
        
        # Determinar prioridad según estrategia
        if self.strategy == 'loss':
            # Invertir para que mayor loss = menor valor (más prioritario)
            priority = -loss
        else:  # confidence
            priority = confidence if confidence is not None else -loss
        
        data = {
            'sample_idx': sample_idx,
            'loss': loss,
            'confidence': confidence
        }
        
        # Si el heap está lleno, comparar con el mínimo
        if self.heap.is_full():
            min_priority, _ = self.heap.peek()
            
            # Solo agregar si es más difícil que el mínimo
            if priority < min_priority:
                self.heap.extract_min()
                self.heap.insert(priority, data)
        else:
            self.heap.insert(priority, data)
    
    def get_hard_samples(self) -> List[dict]:
        """
        Retorna lista de muestras difíciles ordenadas por dificultad.
        
        Returns:
            Lista de diccionarios con información de las muestras
        """
        samples = []
        temp_heap = MinHeap()
        
        # Extraer todos los elementos
        while not self.heap.is_empty():
            priority, data = self.heap.extract_min()
            samples.append(data)
            temp_heap.insert(priority, data)
        
        # Restaurar heap original
        while not temp_heap.is_empty():
            priority, data = temp_heap.extract_min()
            self.heap.insert(priority, data)
        
        # Ordenar por dificultad (mayor pérdida primero)
        samples.sort(key=lambda x: x['loss'], reverse=True)
        
        return samples
    
    def get_statistics(self) -> dict:
        """Retorna estadísticas del hard mining."""
        hard_samples = self.get_hard_samples()
        
        if not hard_samples:
            return {
                'num_hard_samples': 0,
                'total_samples': self.sample_count,
                'avg_loss': 0.0,
                'max_loss': 0.0,
                'min_loss': 0.0
            }
        
        losses = [s['loss'] for s in hard_samples]
        
        return {
            'num_hard_samples': len(hard_samples),
            'total_samples': self.sample_count,
            'avg_loss': np.mean(losses),
            'max_loss': np.max(losses),
            'min_loss': np.min(losses),
            'hard_sample_indices': [s['sample_idx'] for s in hard_samples]
        }


def demo_min_heap():
    """
    Demostración de Min Heap con análisis de complejidad.
    """
    print("=" * 70)
    print("MIN HEAP - ESTRUCTURA DE DATOS - FASE 3")
    print("=" * 70)
    print()
    
    # Ejemplo 1: Operaciones básicas
    print("Ejemplo 1: Operaciones Básicas")
    print("-" * 70)
    heap = MinHeap()
    
    values = [5, 3, 7, 1, 9, 2, 8, 4, 6]
    print(f"Insertando: {values}")
    
    for val in values:
        heap.insert(val)
        print(f"  Insertado {val} | Mínimo actual: {heap.peek()[0]}")
    
    print(f"\nHeap: {heap}")
    print(f"Operaciones realizadas: {heap.get_operation_count()}")
    print()
    
    # Extraer elementos
    print("Extrayendo elementos (orden ascendente):")
    extracted = []
    while not heap.is_empty():
        val, _ = heap.extract_min()
        extracted.append(val)
        print(f"  Extraído: {val}")
    
    print(f"Secuencia ordenada: {extracted}")
    print()
    
    # Ejemplo 2: Heapify
    print("Ejemplo 2: Heapify (Construcción O(n))")
    print("-" * 70)
    arr = [15, 3, 8, 23, 1, 42, 7, 19, 11, 5]
    print(f"Array original: {arr}")
    
    heap2 = MinHeap()
    heap2.heapify(arr)
    
    print(f"Heap construido: {heap2}")
    print(f"Mínimo: {heap2.peek()[0]}")
    print(f"Operaciones: {heap2.get_operation_count()}")
    print()
    
    # Ejemplo 3: Hard Mining
    print("Ejemplo 3: Hard Mining para Machine Learning")
    print("-" * 70)
    hard_heap = HardMiningHeap(capacity=5, strategy='loss')
    
    # Simular muestras con diferentes pérdidas
    samples = [
        (0, 0.1),   # Muestra fácil
        (1, 2.5),   # Muestra difícil
        (2, 0.3),   # Fácil
        (3, 3.2),   # Muy difícil
        (4, 0.2),   # Fácil
        (5, 1.8),   # Difícil
        (6, 0.5),   # Media
        (7, 4.1),   # Muy difícil
        (8, 0.4),   # Media
        (9, 2.9),   # Difícil
    ]
    
    print("Agregando muestras:")
    for idx, loss in samples:
        hard_heap.add_sample(idx, loss)
        print(f"  Muestra {idx} | Loss: {loss:.2f}")
    
    print()
    print("Top 5 muestras más difíciles:")
    hard_samples = hard_heap.get_hard_samples()
    for i, sample in enumerate(hard_samples, 1):
        print(f"  {i}. Muestra {sample['sample_idx']} | Loss: {sample['loss']:.2f}")
    
    print()
    stats = hard_heap.get_statistics()
    print("Estadísticas:")
    print(f"  Total muestras procesadas: {stats['total_samples']}")
    print(f"  Muestras difíciles guardadas: {stats['num_hard_samples']}")
    print(f"  Pérdida promedio (hard): {stats['avg_loss']:.3f}")
    print(f"  Pérdida máxima: {stats['max_loss']:.3f}")
    print()
    
    # Ejemplo 4: Análisis de complejidad
    print("Ejemplo 4: Análisis de Complejidad")
    print("-" * 70)
    sizes = [10, 100, 1000, 10000]
    
    print("Operaciones vs Tamaño:")
    for n in sizes:
        arr = list(np.random.randint(1, 1000, n))
        heap_test = MinHeap()
        heap_test.heapify(arr)
        ops_heapify = heap_test.get_operation_count()
        
        # Extraer todos
        heap_test.reset_operation_count()
        while not heap_test.is_empty():
            heap_test.extract_min()
        ops_extract = heap_test.get_operation_count()
        
        print(f"n={n:5d} | Heapify: {ops_heapify:6d} ops (~O(n)) | "
              f"n extracciones: {ops_extract:6d} ops (~O(n log n))")
    
    print()
    print("=" * 70)
    print("COMPLEJIDAD RESUMEN")
    print("=" * 70)
    print("insert(x):        O(log n)")
    print("extract_min():    O(log n)")
    print("peek():           O(1)")
    print("heapify(arr):     O(n)")
    print("decrease_key():   O(log n)")
    print()


if __name__ == '__main__':
    demo_min_heap()
