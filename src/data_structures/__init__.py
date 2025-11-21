"""
Estructuras de Datos - Fase 3

Implementaciones de estructuras de datos fundamentales con análisis de complejidad.
"""

from .min_heap import MinHeap, HardMiningHeap
from .max_heap import MaxHeap
from .avl_tree import AVLTree
from .hash_table import HashTable
from .trie import Trie

__all__ = [
    'MinHeap',
    'HardMiningHeap',
    'MaxHeap',
    'AVLTree',
    'HashTable',
    'Trie'
]
