"""
Trie - Árbol de Prefijos para Búsqueda de Cadenas

Implementación de Trie (árbol digital) para búsqueda eficiente de palabras.

Complejidad:
    - insert(word): O(m) donde m = longitud de palabra
    - search(word): O(m)
    - starts_with(prefix): O(m)
    - delete(word): O(m)

Aplicaciones:
    - Autocompletado
    - Diccionarios
    - Corrección ortográfica
    - Búsqueda de prefijos

Referencias:
    - Fredkin, E. (1960). "Trie memory"
    - Knuth, D. (1998). "The Art of Computer Programming", Vol 3
"""

from typing import Optional, List, Dict


class TrieNode:
    """Nodo del Trie."""
    
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False
        self.word_count: int = 0  # Número de palabras que terminan aquí
    
    def __repr__(self):
        return f"TrieNode(children={len(self.children)}, is_end={self.is_end_of_word})"


class Trie:
    """
    Trie - Árbol de prefijos para búsqueda de cadenas.
    
    Almacena palabras de forma que prefijos comunes comparten nodos.
    """
    
    def __init__(self):
        """Inicializa Trie vacío."""
        self.root = TrieNode()
        self.word_count = 0
        self.node_count = 1  # Raíz
    
    def insert(self, word: str):
        """
        Inserta palabra en el Trie. O(m) donde m = len(word)
        
        Args:
            word: Palabra a insertar
        
        Examples:
            >>> trie = Trie()
            >>> trie.insert("hello")
            >>> trie.insert("world")
            >>> trie.search("hello")
            True
        """
        if not word:
            return
        
        node = self.root
        
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
                self.node_count += 1
            
            node = node.children[char]
        
        # Marcar fin de palabra
        if not node.is_end_of_word:
            self.word_count += 1
        
        node.is_end_of_word = True
        node.word_count += 1
    
    def search(self, word: str) -> bool:
        """
        Busca palabra exacta en el Trie. O(m)
        
        Args:
            word: Palabra a buscar
        
        Returns:
            True si la palabra existe, False en caso contrario
        
        Examples:
            >>> trie = Trie()
            >>> trie.insert("hello")
            >>> trie.search("hello")
            True
            >>> trie.search("hell")
            False
        """
        node = self._search_node(word)
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix: str) -> bool:
        """
        Verifica si existe alguna palabra con el prefijo dado. O(m)
        
        Args:
            prefix: Prefijo a buscar
        
        Returns:
            True si existe al menos una palabra con ese prefijo
        
        Examples:
            >>> trie = Trie()
            >>> trie.insert("hello")
            >>> trie.starts_with("hel")
            True
            >>> trie.starts_with("world")
            False
        """
        return self._search_node(prefix) is not None
    
    def _search_node(self, word: str) -> Optional[TrieNode]:
        """
        Busca nodo correspondiente a una palabra/prefijo.
        
        Args:
            word: Palabra o prefijo
        
        Returns:
            Nodo si existe, None en caso contrario
        """
        if not word:
            return self.root
        
        node = self.root
        
        for char in word.lower():
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def delete(self, word: str) -> bool:
        """
        Elimina palabra del Trie. O(m)
        
        Args:
            word: Palabra a eliminar
        
        Returns:
            True si se eliminó, False si no existía
        
        Examples:
            >>> trie = Trie()
            >>> trie.insert("hello")
            >>> trie.delete("hello")
            True
            >>> trie.search("hello")
            False
        """
        if not word:
            return False
        
        return self._delete_recursive(self.root, word.lower(), 0)
    
    def _delete_recursive(self, node: TrieNode, word: str, index: int) -> bool:
        """Eliminación recursiva."""
        if index == len(word):
            # Fin de la palabra
            if not node.is_end_of_word:
                return False
            
            node.is_end_of_word = False
            node.word_count = 0
            self.word_count -= 1
            
            # Retornar True si el nodo no tiene hijos (puede eliminarse)
            return len(node.children) == 0
        
        char = word[index]
        
        if char not in node.children:
            return False
        
        child_node = node.children[char]
        should_delete_child = self._delete_recursive(child_node, word, index + 1)
        
        # Eliminar hijo si es necesario
        if should_delete_child:
            del node.children[char]
            self.node_count -= 1
            
            # Retornar True si este nodo tampoco es fin de palabra y no tiene hijos
            return not node.is_end_of_word and len(node.children) == 0
        
        return False
    
    def get_all_words(self, prefix: str = "") -> List[str]:
        """
        Retorna todas las palabras con el prefijo dado.
        
        Args:
            prefix: Prefijo (vacío = todas las palabras)
        
        Returns:
            Lista de palabras
        
        Examples:
            >>> trie = Trie()
            >>> trie.insert("hello")
            >>> trie.insert("help")
            >>> trie.insert("world")
            >>> trie.get_all_words("hel")
            ['hello', 'help']
        """
        result = []
        node = self._search_node(prefix)
        
        if node is None:
            return result
        
        self._collect_words(node, prefix.lower(), result)
        return sorted(result)
    
    def _collect_words(self, node: TrieNode, current_word: str, result: List[str]):
        """Recolecta palabras recursivamente."""
        if node.is_end_of_word:
            result.append(current_word)
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, current_word + char, result)
    
    def autocomplete(self, prefix: str, limit: int = 10) -> List[str]:
        """
        Autocompletado: retorna hasta 'limit' palabras con el prefijo.
        
        Args:
            prefix: Prefijo a buscar
            limit: Número máximo de sugerencias
        
        Returns:
            Lista de sugerencias
        """
        all_words = self.get_all_words(prefix)
        return all_words[:limit]
    
    def count_words_with_prefix(self, prefix: str) -> int:
        """
        Cuenta palabras con el prefijo dado.
        
        Args:
            prefix: Prefijo
        
        Returns:
            Número de palabras
        """
        return len(self.get_all_words(prefix))
    
    def size(self) -> int:
        """Retorna número de palabras únicas."""
        return self.word_count
    
    def node_count_total(self) -> int:
        """Retorna número total de nodos."""
        return self.node_count
    
    def __repr__(self):
        return f"Trie(words={self.word_count}, nodes={self.node_count})"


if __name__ == '__main__':
    # Demo
    trie = Trie()
    
    words = ["hello", "help", "world", "word", "war", "hello"]
    
    print("Insertando palabras:")
    for word in words:
        trie.insert(word)
        print(f"  {word}")
    
    print(f"\nTrie: {trie}")
    
    print("\nBúsquedas:")
    print(f"  search('hello'): {trie.search('hello')}")
    print(f"  search('hell'): {trie.search('hell')}")
    print(f"  starts_with('hel'): {trie.starts_with('hel')}")
    print(f"  starts_with('wor'): {trie.starts_with('wor')}")
    
    print(f"\nAutocompletado 'wo': {trie.autocomplete('wo')}")
    print(f"Todas las palabras con 'hel': {trie.get_all_words('hel')}")
