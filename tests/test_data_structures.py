"""
Suite de pruebas para estructuras de datos.

Prueba MinHeap, MaxHeap, AVLTree, HashTable y Trie.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_structures.min_heap import MinHeap
from src.data_structures.max_heap import MaxHeap
from src.data_structures.avl_tree import AVLTree
from src.data_structures.hash_table import HashTable
from src.data_structures.trie import Trie


def test_min_heap():
    """Prueba MinHeap."""
    print("=== Test MinHeap ===")
    
    from src.data_structures.min_heap import HeapElement
    
    heap = MinHeap()
    
    # Test inserción
    for val in [5, 3, 7, 1, 9, 2]:
        heap.insert(val)
    
    min_val, _ = heap.peek()
    assert min_val == 1, "peek() debe retornar mínimo"
    assert heap.size() == 6, "size() debe ser 6"
    
    # Test extracción ordenada
    extracted = []
    while not heap.is_empty():
        val, _ = heap.extract_min()
        extracted.append(val)
    
    assert extracted == [1, 2, 3, 5, 7, 9], "Debe extraer en orden ascendente"
    
    # Test heapify
    heap2 = MinHeap()
    heap2.heapify([9, 5, 7, 3, 1, 8])
    min_val2, _ = heap2.peek()
    assert min_val2 == 1, "heapify debe crear heap válido"
    
    print("✅ MinHeap: PASSED")


def test_max_heap():
    """Prueba MaxHeap."""
    print("\n=== Test MaxHeap ===")
    
    heap = MaxHeap()
    
    # Test inserción
    for val in [5, 3, 7, 1, 9, 2]:
        heap.insert(val)
    
    max_val, _ = heap.peek()
    assert max_val == 9, "peek() debe retornar máximo"
    assert heap.size() == 6, "size() debe ser 6"
    
    # Test extracción ordenada
    extracted = []
    while not heap.is_empty():
        val, _ = heap.extract_max()
        extracted.append(val)
    
    assert extracted == [9, 7, 5, 3, 2, 1], "Debe extraer en orden descendente"
    
    # Test heapify
    heap2 = MaxHeap()
    heap2.heapify([9, 5, 7, 3, 1, 8])
    max_val2, _ = heap2.peek()
    assert max_val2 == 9, "heapify debe crear heap válido"
    
    print("✅ MaxHeap: PASSED")


def test_avl_tree():
    """Prueba AVLTree."""
    print("\n=== Test AVLTree ===")
    
    tree = AVLTree()
    
    # Test inserción
    values = [10, 20, 30, 40, 50, 25]
    for val in values:
        tree.insert(val)
    
    assert tree.size() == 6, "size() debe ser 6"
    assert tree.search(25) is not None, "search(25) debe encontrar el valor"
    assert tree.search(100) is None, "search(100) no debe encontrar nada"
    
    # Test inorder (debe estar ordenado)
    inorder = tree.inorder()
    assert inorder == [10, 20, 25, 30, 40, 50], "inorder debe estar ordenado"
    
    # Test balance
    assert tree.is_balanced(), "Árbol debe estar balanceado"
    
    # Test eliminación
    tree.delete(25)
    assert tree.search(25) is None, "25 debe estar eliminado"
    assert tree.is_balanced(), "Debe permanecer balanceado tras delete"
    
    print("✅ AVLTree: PASSED")


def test_hash_table():
    """Prueba HashTable."""
    print("\n=== Test HashTable ===")
    
    ht = HashTable(capacity=4)
    
    # Test inserción
    ht.insert("key1", 100)
    ht.insert("key2", 200)
    ht.insert("key3", 300)
    
    assert ht.search("key1") == 100, "search('key1') debe retornar 100"
    assert ht.search("key2") == 200, "search('key2') debe retornar 200"
    assert ht.size() == 3, "size() debe ser 3"
    
    # Test actualización
    ht.insert("key1", 150)
    assert ht.search("key1") == 150, "update debe cambiar valor"
    
    # Test eliminación
    assert ht.delete("key2"), "delete('key2') debe retornar True"
    assert ht.search("key2") is None, "key2 no debe existir"
    assert ht.size() == 2, "size() debe ser 2"
    
    # Test rehashing (insertar muchos elementos)
    for i in range(20):
        ht.insert(f"k{i}", i)
    
    stats = ht.get_statistics()
    assert stats["rehashes"] > 0, "Debe haber rehashing"
    
    print("✅ HashTable: PASSED")


def test_trie():
    """Prueba Trie."""
    print("\n=== Test Trie ===")
    
    trie = Trie()
    
    # Test inserción
    words = ["hello", "help", "world", "word", "war"]
    for word in words:
        trie.insert(word)
    
    assert trie.size() == 5, "size() debe ser 5"
    
    # Test búsqueda
    assert trie.search("hello"), "search('hello') debe ser True"
    assert trie.search("help"), "search('help') debe ser True"
    assert not trie.search("hell"), "search('hell') debe ser False"
    
    # Test prefijos
    assert trie.starts_with("hel"), "starts_with('hel') debe ser True"
    assert trie.starts_with("wor"), "starts_with('wor') debe ser True"
    assert not trie.starts_with("xyz"), "starts_with('xyz') debe ser False"
    
    # Test autocompletado
    suggestions = trie.get_all_words("wo")
    assert "word" in suggestions and "world" in suggestions, "Debe sugerir word y world"
    
    # Test eliminación
    trie.delete("hello")
    assert not trie.search("hello"), "hello debe estar eliminado"
    assert trie.search("help"), "help debe seguir existiendo"
    
    print("✅ Trie: PASSED")


def test_complexity_properties():
    """Prueba propiedades de complejidad."""
    print("\n=== Test Propiedades de Complejidad ===")
    
    from src.data_structures.min_heap import HeapElement
    
    # MinHeap: O(log n) insert
    heap = MinHeap()
    for i in range(100):
        heap.insert(i)
    
    min_val, _ = heap.peek()
    assert min_val == 0, "Mínimo debe ser 0"
    
    # AVL: O(log n) height
    tree = AVLTree()
    for i in range(100):
        tree.insert(i)
    
    height = tree.height()
    max_height = 1.44 * (100).bit_length()  # Límite teórico AVL
    assert height <= max_height, f"Altura {height} debe ser ≤ {max_height}"
    
    # HashTable: O(1) average
    ht = HashTable()
    for i in range(1000):
        ht.insert(f"key{i}", i)
    
    stats = ht.get_statistics()
    assert stats["load_factor"] < 0.8, "Load factor debe ser < 0.8"
    
    # Trie: O(m) search
    trie = Trie()
    trie.insert("a" * 1000)  # Palabra muy larga
    assert trie.search("a" * 1000), "Debe encontrar palabra larga"
    
    print("✅ Propiedades de Complejidad: PASSED")


def test_edge_cases():
    """Prueba casos límite."""
    print("\n=== Test Casos Límite ===")
    
    # MinHeap vacío
    heap = MinHeap()
    try:
        heap.peek()
        assert False, "peek() en heap vacío debe lanzar IndexError"
    except IndexError:
        pass  # Comportamiento esperado
    
    # AVL con un elemento
    tree = AVLTree()
    tree.insert(42)
    assert tree.search(42) is not None, "Debe encontrar único elemento"
    tree.delete(42)
    assert tree.size() == 0, "Árbol debe estar vacío"
    
    # HashTable con colisiones
    ht = HashTable(capacity=2)
    ht.insert("key1", 1)
    ht.insert("key2", 2)
    ht.insert("key3", 3)
    assert ht.search("key1") == 1, "Debe manejar colisiones"
    
    # Trie con palabras vacías
    trie = Trie()
    trie.insert("")
    assert trie.search("") == False, "Palabra vacía no debe insertarse"
    
    # Trie con prefijo que es palabra completa
    trie.insert("test")
    trie.insert("testing")
    assert trie.search("test"), "'test' debe existir"
    assert trie.search("testing"), "'testing' debe existir"
    
    print("✅ Casos Límite: PASSED")


def run_all_tests():
    """Ejecuta todos los tests."""
    print("=" * 50)
    print("SUITE DE PRUEBAS - ESTRUCTURAS DE DATOS")
    print("=" * 50)
    
    try:
        test_min_heap()
        test_max_heap()
        test_avl_tree()
        test_hash_table()
        test_trie()
        test_complexity_properties()
        test_edge_cases()
        
        print("\n" + "=" * 50)
        print("✅ TODAS LAS PRUEBAS PASARON")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n❌ FALLÓ: {e}")
        raise


if __name__ == '__main__':
    run_all_tests()
