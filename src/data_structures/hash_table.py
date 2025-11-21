"""
Hash Table - Tabla de Dispersión con Encadenamiento

Implementación de Hash Table con resolución de colisiones mediante chaining.

Complejidad:
    - insert(key, val): O(1) promedio
    - search(key): O(1) promedio
    - delete(key): O(1) promedio
    - Peor caso: O(n) si todas las claves colisionan

Propiedades:
    - Factor de carga: λ = n/m (elementos/buckets)
    - Rehashing automático cuando λ > 0.75
    - Función hash: división módulo

Referencias:
    - Cormen et al. (2009). "Introduction to Algorithms", Chapter 11
    - Knuth, D. (1998). "The Art of Computer Programming", Vol 3
"""

from typing import Optional, List, Tuple, Any


class HashNode:
    """Nodo para encadenamiento en colisiones."""
    
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.next: Optional['HashNode'] = None
    
    def __repr__(self):
        return f"({self.key}: {self.value})"


class HashTable:
    """
    Hash Table con chaining para resolución de colisiones.
    
    Usa listas enlazadas para manejar colisiones.
    """
    
    def __init__(self, capacity: int = 16):
        """
        Inicializa hash table.
        
        Args:
            capacity: Número inicial de buckets
        """
        self.capacity = capacity
        self.size_count = 0
        self.buckets: List[Optional[HashNode]] = [None] * capacity
        self.collision_count = 0
        self.rehash_count = 0
        self.load_factor_threshold = 0.75
    
    def _hash(self, key: Any) -> int:
        """
        Función hash simple: módulo.
        
        Args:
            key: Clave a hashear
        
        Returns:
            Índice del bucket
        """
        return hash(key) % self.capacity
    
    def _load_factor(self) -> float:
        """Calcula factor de carga actual."""
        return self.size_count / self.capacity
    
    def insert(self, key: Any, value: Any):
        """
        Inserta par clave-valor. O(1) promedio
        
        Args:
            key: Clave
            value: Valor asociado
        """
        # Verificar si necesita rehashing
        if self._load_factor() > self.load_factor_threshold:
            self._rehash()
        
        index = self._hash(key)
        node = self.buckets[index]
        
        # Verificar si la clave ya existe
        current = node
        while current:
            if current.key == key:
                # Actualizar valor existente
                current.value = value
                return
            current = current.next
        
        # Insertar nuevo nodo al inicio de la cadena
        new_node = HashNode(key, value)
        new_node.next = node
        self.buckets[index] = new_node
        self.size_count += 1
        
        # Contar colisión si había nodo previo
        if node is not None:
            self.collision_count += 1
    
    def search(self, key: Any) -> Optional[Any]:
        """
        Busca valor por clave. O(1) promedio
        
        Args:
            key: Clave a buscar
        
        Returns:
            Valor asociado o None
        """
        index = self._hash(key)
        node = self.buckets[index]
        
        while node:
            if node.key == key:
                return node.value
            node = node.next
        
        return None
    
    def delete(self, key: Any) -> bool:
        """
        Elimina clave del hash table. O(1) promedio
        
        Args:
            key: Clave a eliminar
        
        Returns:
            True si se eliminó, False si no existía
        """
        index = self._hash(key)
        node = self.buckets[index]
        prev = None
        
        while node:
            if node.key == key:
                # Eliminar nodo
                if prev:
                    prev.next = node.next
                else:
                    self.buckets[index] = node.next
                
                self.size_count -= 1
                return True
            
            prev = node
            node = node.next
        
        return False
    
    def _rehash(self):
        """
        Rehashing: duplica capacidad y reinserta elementos.
        
        Complejidad: O(n)
        """
        self.rehash_count += 1
        
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size_count = 0
        self.collision_count = 0
        
        # Reinsertar todos los elementos
        for bucket in old_buckets:
            node = bucket
            while node:
                self.insert(node.key, node.value)
                node = node.next
    
    def keys(self) -> List[Any]:
        """Retorna lista de todas las claves. O(n)"""
        result = []
        for bucket in self.buckets:
            node = bucket
            while node:
                result.append(node.key)
                node = node.next
        return result
    
    def values(self) -> List[Any]:
        """Retorna lista de todos los valores. O(n)"""
        result = []
        for bucket in self.buckets:
            node = bucket
            while node:
                result.append(node.value)
                node = node.next
        return result
    
    def items(self) -> List[Tuple[Any, Any]]:
        """Retorna lista de pares (clave, valor). O(n)"""
        result = []
        for bucket in self.buckets:
            node = bucket
            while node:
                result.append((node.key, node.value))
                node = node.next
        return result
    
    def size(self) -> int:
        """Retorna número de elementos."""
        return self.size_count
    
    def get_statistics(self) -> dict:
        """Retorna estadísticas del hash table."""
        # Calcular longitud de cadenas
        chain_lengths = []
        non_empty_buckets = 0
        
        for bucket in self.buckets:
            length = 0
            node = bucket
            while node:
                length += 1
                node = node.next
            
            chain_lengths.append(length)
            if length > 0:
                non_empty_buckets += 1
        
        return {
            'size': self.size_count,
            'capacity': self.capacity,
            'load_factor': self._load_factor(),
            'collisions': self.collision_count,
            'rehashes': self.rehash_count,
            'non_empty_buckets': non_empty_buckets,
            'avg_chain_length': sum(chain_lengths) / len(chain_lengths),
            'max_chain_length': max(chain_lengths)
        }
    
    def __repr__(self):
        return f"HashTable(size={self.size_count}, capacity={self.capacity}, load={self._load_factor():.2f})"


if __name__ == '__main__':
    # Demo
    ht = HashTable(capacity=4)
    
    print("Insertando elementos:")
    for i in range(10):
        ht.insert(f"key{i}", i * 10)
        print(f"  Insertado key{i} | Load factor: {ht._load_factor():.2f} | Rehashes: {ht.rehash_count}")
    
    print(f"\nBuscando key5: {ht.search('key5')}")
    print(f"Estadísticas: {ht.get_statistics()}")
