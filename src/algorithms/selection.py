"""
Quickselect - Algoritmo de Selección Rápida

Implementación del algoritmo Quickselect para encontrar el k-ésimo elemento más pequeño
en un array sin necesidad de ordenar completamente.

Complejidad:
    - Mejor caso: O(n)
    - Caso promedio: O(n)
    - Peor caso: O(n²) [cuando el pivote siempre es el peor posible]

Comparación con Quicksort:
    - Quicksort ordena completamente: O(n log n) promedio
    - Quickselect solo encuentra k-ésimo: O(n) promedio
    - Ambos usan particionamiento similar pero Quickselect solo procesa un lado

Referencias:
    - Hoare, C.A.R. (1961). "Algorithm 65: Find". Communications of the ACM
    - Cormen et al. (2009). "Introduction to Algorithms", Chapter 9
"""

import random
import numpy as np
from typing import List, Union, Optional, Tuple


class Quickselect:
    """
    Clase Quickselect para encontrar el k-ésimo elemento más pequeño.
    
    Implementa:
        - Quickselect determinista (pivote aleatorio)
        - Quickselect con mediana de medianas (O(n) garantizado)
        - Análisis de complejidad con conteo de operaciones
        - Comparación con ordenamiento completo
    """
    
    def __init__(self, strategy: str = 'random'):
        """
        Inicializa Quickselect con estrategia de selección de pivote.
        
        Args:
            strategy (str): 'random' (aleatorio) o 'median_of_medians' (determinista)
        
        Raises:
            ValueError: Si la estrategia no es válida
        """
        if strategy not in ['random', 'median_of_medians']:
            raise ValueError(f"Estrategia inválida: {strategy}")
        
        self.strategy = strategy
        self.comparisons = 0  # Contador de comparaciones
        self.swaps = 0        # Contador de intercambios
        self.recursive_calls = 0  # Contador de llamadas recursivas
    
    def find_kth(self, arr: Union[List, np.ndarray], k: int) -> Union[int, float]:
        """
        Encuentra el k-ésimo elemento más pequeño (1-indexed).
        
        Args:
            arr: Array de números
            k: Posición del elemento buscado (1 = mínimo, n = máximo)
        
        Returns:
            El k-ésimo elemento más pequeño
        
        Raises:
            ValueError: Si k está fuera de rango
            
        Examples:
            >>> qs = Quickselect()
            >>> arr = [3, 2, 1, 5, 4]
            >>> qs.find_kth(arr, 3)  # 3er más pequeño
            3
            >>> qs.find_kth(arr, 1)  # Mínimo
            1
            >>> qs.find_kth(arr, 5)  # Máximo
            5
        """
        if not isinstance(arr, (list, np.ndarray)):
            raise TypeError("arr debe ser lista o numpy array")
        
        arr_copy = np.array(arr, dtype=float)
        n = len(arr_copy)
        
        if k < 1 or k > n:
            raise ValueError(f"k={k} debe estar entre 1 y {n}")
        
        # Reiniciar contadores
        self.comparisons = 0
        self.swaps = 0
        self.recursive_calls = 0
        
        # Quickselect usa índices 0-based internamente
        result = self._quickselect(arr_copy, 0, n - 1, k - 1)
        
        return result
    
    def _quickselect(self, arr: np.ndarray, left: int, right: int, k: int) -> float:
        """
        Implementación recursiva de Quickselect.
        
        Args:
            arr: Array de trabajo (modificado in-place)
            left: Índice izquierdo del rango
            right: Índice derecho del rango
            k: Índice del elemento buscado (0-based)
        
        Returns:
            El k-ésimo elemento
        """
        self.recursive_calls += 1
        
        # Caso base: un solo elemento
        if left == right:
            return arr[left]
        
        # Particionar array
        pivot_index = self._partition(arr, left, right)
        
        # Comparar posición del pivote con k
        self.comparisons += 1
        
        if k == pivot_index:
            # Encontrado!
            return arr[k]
        elif k < pivot_index:
            # Buscar en mitad izquierda
            return self._quickselect(arr, left, pivot_index - 1, k)
        else:
            # Buscar en mitad derecha
            return self._quickselect(arr, pivot_index + 1, right, k)
    
    def _partition(self, arr: np.ndarray, left: int, right: int) -> int:
        """
        Particiona el array alrededor de un pivote.
        
        Algoritmo de Hoare: elementos menores al pivote van a la izquierda,
        mayores van a la derecha.
        
        Args:
            arr: Array a particionar (modificado in-place)
            left: Índice inicial
            right: Índice final
        
        Returns:
            Índice final del pivote
        """
        # Seleccionar pivote según estrategia
        if self.strategy == 'random':
            pivot_index = random.randint(left, right)
        else:  # median_of_medians
            pivot_index = self._median_of_medians(arr, left, right)
        
        # Mover pivote al final
        arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
        self.swaps += 1
        
        pivot_value = arr[right]
        store_index = left
        
        # Particionar
        for i in range(left, right):
            self.comparisons += 1
            if arr[i] < pivot_value:
                arr[i], arr[store_index] = arr[store_index], arr[i]
                self.swaps += 1
                store_index += 1
        
        # Colocar pivote en su posición final
        arr[store_index], arr[right] = arr[right], arr[store_index]
        self.swaps += 1
        
        return store_index
    
    def _median_of_medians(self, arr: np.ndarray, left: int, right: int) -> int:
        """
        Encuentra la mediana de medianas para garantizar O(n) en el peor caso.
        
        Algoritmo:
        1. Dividir array en grupos de 5
        2. Encontrar mediana de cada grupo
        3. Recursivamente encontrar mediana de medianas
        
        Args:
            arr: Array
            left: Índice inicial
            right: Índice final
        
        Returns:
            Índice de la mediana de medianas
        """
        n = right - left + 1
        
        # Caso base: pocos elementos
        if n <= 5:
            # Ordenar y tomar mediana
            sub_arr = sorted(arr[left:right+1])
            median = sub_arr[n // 2]
            # Buscar índice de la mediana
            for i in range(left, right + 1):
                if arr[i] == median:
                    return i
        
        # Dividir en grupos de 5 y encontrar medianas
        medians = []
        i = left
        while i <= right:
            sub_right = min(i + 4, right)
            sub_arr = sorted(arr[i:sub_right+1])
            median = sub_arr[len(sub_arr) // 2]
            medians.append(median)
            i += 5
        
        # Recursivamente encontrar mediana de medianas
        medians_arr = np.array(medians)
        median_of_medians = self._quickselect(
            medians_arr, 0, len(medians_arr) - 1, len(medians_arr) // 2
        )
        
        # Buscar índice en array original
        for i in range(left, right + 1):
            if arr[i] == median_of_medians:
                return i
        
        return left
    
    def find_median(self, arr: Union[List, np.ndarray]) -> float:
        """
        Encuentra la mediana del array en O(n) promedio.
        
        Args:
            arr: Array de números
        
        Returns:
            Mediana (promedio de los dos centrales si n es par)
        
        Examples:
            >>> qs = Quickselect()
            >>> qs.find_median([3, 1, 2, 5, 4])
            3.0
            >>> qs.find_median([4, 1, 3, 2])
            2.5
        """
        n = len(arr)
        
        if n % 2 == 1:
            # Impar: elemento central
            return self.find_kth(arr, n // 2 + 1)
        else:
            # Par: promedio de dos centrales
            lower = self.find_kth(arr, n // 2)
            upper = self.find_kth(arr, n // 2 + 1)
            return (lower + upper) / 2
    
    def find_min(self, arr: Union[List, np.ndarray]) -> Union[int, float]:
        """
        Encuentra el mínimo usando Quickselect (k=1).
        
        Args:
            arr: Array de números
        
        Returns:
            Elemento mínimo
        """
        return self.find_kth(arr, 1)
    
    def find_max(self, arr: Union[List, np.ndarray]) -> Union[int, float]:
        """
        Encuentra el máximo usando Quickselect (k=n).
        
        Args:
            arr: Array de números
        
        Returns:
            Elemento máximo
        """
        return self.find_kth(arr, len(arr))
    
    def get_statistics(self) -> dict:
        """
        Obtiene estadísticas de la última ejecución.
        
        Returns:
            Diccionario con contadores de operaciones
        """
        return {
            'comparisons': self.comparisons,
            'swaps': self.swaps,
            'recursive_calls': self.recursive_calls,
            'total_operations': self.comparisons + self.swaps
        }
    
    def compare_with_sorting(self, arr: Union[List, np.ndarray], k: int) -> Tuple[float, dict]:
        """
        Compara Quickselect con ordenamiento completo.
        
        Args:
            arr: Array de números
            k: Posición del elemento buscado
        
        Returns:
            Tupla (resultado, comparación) donde comparación contiene:
                - quickselect_ops: operaciones de Quickselect
                - sorting_ops: operaciones estimadas de ordenamiento
                - speedup: factor de aceleración
        """
        # Quickselect
        result = self.find_kth(arr, k)
        qs_stats = self.get_statistics()
        
        # Estimación de ordenamiento (Merge Sort: O(n log n))
        n = len(arr)
        estimated_sorting_ops = n * np.log2(n) if n > 0 else 0
        
        speedup = estimated_sorting_ops / max(qs_stats['total_operations'], 1)
        
        comparison = {
            'quickselect_ops': qs_stats['total_operations'],
            'sorting_ops_estimated': int(estimated_sorting_ops),
            'speedup': speedup,
            'complexity_ratio': f"O(n) vs O(n log n)",
            'quickselect_details': qs_stats
        }
        
        return result, comparison


def demo_quickselect():
    """
    Demostración de Quickselect con análisis comparativo.
    """
    print("=" * 70)
    print("DEMOSTRACIÓN DE QUICKSELECT - FASE 2")
    print("=" * 70)
    print()
    
    # Ejemplo 1: Array pequeño
    print("Ejemplo 1: Array [3, 7, 2, 9, 1, 5, 8, 4, 6]")
    print("-" * 70)
    arr = [3, 7, 2, 9, 1, 5, 8, 4, 6]
    qs = Quickselect(strategy='random')
    
    # Encontrar varios elementos
    for k in [1, 3, 5, 9]:
        result = qs.find_kth(arr, k)
        stats = qs.get_statistics()
        print(f"k={k}: {result} | Comparaciones: {stats['comparisons']} | "
              f"Intercambios: {stats['swaps']} | Llamadas: {stats['recursive_calls']}")
    
    print()
    
    # Ejemplo 2: Comparación con ordenamiento
    print("Ejemplo 2: Comparación Quickselect vs Ordenamiento Completo")
    print("-" * 70)
    sizes = [10, 100, 1000, 10000]
    
    for n in sizes:
        arr = np.random.randint(1, 1000, n)
        k = n // 2  # Buscar mediana
        
        result, comparison = qs.compare_with_sorting(arr, k)
        
        print(f"n={n:5d} | k={k:5d} | "
              f"Quickselect: {comparison['quickselect_ops']:6d} ops | "
              f"Sort (est): {comparison['sorting_ops_estimated']:6d} ops | "
              f"Speedup: {comparison['speedup']:.2f}x")
    
    print()
    
    # Ejemplo 3: Mediana
    print("Ejemplo 3: Encontrar Mediana")
    print("-" * 70)
    arr1 = [1, 3, 5, 7, 9]
    arr2 = [2, 4, 6, 8]
    
    print(f"Array impar {arr1}")
    median1 = qs.find_median(arr1)
    print(f"  Mediana: {median1}")
    print(f"  Operaciones: {qs.get_statistics()['total_operations']}")
    
    print(f"\nArray par {arr2}")
    median2 = qs.find_median(arr2)
    print(f"  Mediana: {median2}")
    print(f"  Operaciones: {qs.get_statistics()['total_operations']}")
    
    print()
    
    # Ejemplo 4: Min y Max
    print("Ejemplo 4: Encontrar Mínimo y Máximo")
    print("-" * 70)
    arr = [15, 3, 8, 23, 1, 42, 7, 19]
    print(f"Array: {arr}")
    print(f"  Mínimo: {qs.find_min(arr)} | Ops: {qs.get_statistics()['total_operations']}")
    print(f"  Máximo: {qs.find_max(arr)} | Ops: {qs.get_statistics()['total_operations']}")
    
    print()
    print("=" * 70)
    print("ANÁLISIS DE COMPLEJIDAD")
    print("=" * 70)
    print()
    print("Quickselect:")
    print("  • Mejor caso: O(n) - partición siempre equilibrada")
    print("  • Caso promedio: O(n) - con pivote aleatorio")
    print("  • Peor caso: O(n²) - pivote siempre el peor")
    print("  • Con mediana de medianas: O(n) garantizado")
    print()
    print("Comparación con Quicksort:")
    print("  • Quicksort: O(n log n) promedio (ordena todo)")
    print("  • Quickselect: O(n) promedio (solo k-ésimo)")
    print("  • Ventaja: ~log n más rápido para un elemento")
    print()
    print("Casos de uso:")
    print("  • Encontrar mediana sin ordenar")
    print("  • Top-k elementos")
    print("  • Percentiles en estadísticas")
    print("  • Selección de pivote en algoritmos")
    print()


if __name__ == '__main__':
    demo_quickselect()
