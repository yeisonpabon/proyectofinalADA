"""
Data Structures Visualizer - Visualizador de Estructuras de Datos

Visualiza MinHeap, MaxHeap, AVL Tree, Hash Table y Trie con animaciones interactivas.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import sys
import os

# Agregar path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class DataStructuresVisualizer:
    """Visualizador interactivo de estructuras de datos."""
    
    def __init__(self, parent_frame):
        """
        Inicializa visualizador.
        
        Args:
            parent_frame: Frame padre
        """
        self.parent = parent_frame
        self.current_structure = None
        self.figure = None
        self.canvas = None
        
        # Importar estructuras
        try:
            from src.data_structures import MinHeap, MaxHeap, AVLTree, HashTable, Trie
            self.MinHeap = MinHeap
            self.MaxHeap = MaxHeap
            self.AVLTree = AVLTree
            self.HashTable = HashTable
            self.Trie = Trie
        except ImportError as e:
            print(f"Error importando estructuras: {e}")
            self.MinHeap = None
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea interfaz de usuario."""
        # Frame de control
        control_frame = ttk.LabelFrame(self.parent, text="Controles", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Selector de estructura
        selector_frame = ttk.Frame(control_frame)
        selector_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(selector_frame, text="Estructura:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.structure_var = tk.StringVar(value="MinHeap")
        structures = ["MinHeap", "MaxHeap", "AVL Tree", "Hash Table", "Trie"]
        ttk.Combobox(selector_frame, textvariable=self.structure_var, 
                    values=structures, state="readonly", width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(selector_frame, text="🔄 Visualizar", 
                  command=self.visualize).pack(side=tk.LEFT, padx=5)
        
        # Controles de datos
        data_frame = ttk.Frame(control_frame)
        data_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(data_frame, text="Datos (separados por comas):").pack(side=tk.LEFT, padx=5)
        
        self.data_entry = ttk.Entry(data_frame, width=40)
        self.data_entry.pack(side=tk.LEFT, padx=5)
        self.data_entry.insert(0, "50,30,70,20,40,60,80")
        
        ttk.Button(data_frame, text="➕ Insertar", 
                  command=self.insert_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(data_frame, text="🗑️ Limpiar", 
                  command=self.clear_structure).pack(side=tk.LEFT, padx=5)
        
        # Frame para visualización
        self.viz_frame = ttk.Frame(self.parent)
        self.viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel de información
        self.info_frame = ttk.LabelFrame(self.parent, text="Información", padding=10)
        self.info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.info_text = tk.Text(self.info_frame, height=4, wrap=tk.WORD, 
                                font=("Consolas", 9), state=tk.DISABLED)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Visualizar estructura inicial
        self.visualize()
    
    def visualize(self):
        """Visualiza estructura seleccionada."""
        structure = self.structure_var.get()
        
        if structure == "MinHeap":
            self._visualize_heap(is_min=True)
        elif structure == "MaxHeap":
            self._visualize_heap(is_min=False)
        elif structure == "AVL Tree":
            self._visualize_avl_tree()
        elif structure == "Hash Table":
            self._visualize_hash_table()
        elif structure == "Trie":
            self._visualize_trie()
    
    def insert_data(self):
        """Inserta datos en la estructura actual."""
        data_str = self.data_entry.get().strip()
        if not data_str:
            messagebox.showwarning("Advertencia", "Ingresa datos para insertar")
            return
        
        try:
            # Parsear datos
            if self.structure_var.get() == "Trie":
                data = [word.strip() for word in data_str.split(',')]
            else:
                data = [int(x.strip()) for x in data_str.split(',')]
            
            # Insertar en estructura
            structure_type = self.structure_var.get()
            
            if structure_type == "MinHeap":
                if not self.current_structure:
                    self.current_structure = self.MinHeap()
                for val in data:
                    self.current_structure.insert(val)
            
            elif structure_type == "MaxHeap":
                if not self.current_structure:
                    self.current_structure = self.MaxHeap()
                for val in data:
                    self.current_structure.insert(val)
            
            elif structure_type == "AVL Tree":
                if not self.current_structure:
                    self.current_structure = self.AVLTree()
                for val in data:
                    self.current_structure.insert(val)
            
            elif structure_type == "Hash Table":
                if not self.current_structure:
                    self.current_structure = self.HashTable()
                for val in data:
                    self.current_structure.insert(f"key{val}", val)
            
            elif structure_type == "Trie":
                if not self.current_structure:
                    self.current_structure = self.Trie()
                for word in data:
                    self.current_structure.insert(word)
            
            # Visualizar
            self.visualize()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error insertando datos:\n{str(e)}")
    
    def clear_structure(self):
        """Limpia estructura actual."""
        self.current_structure = None
        self.visualize()
    
    def _visualize_heap(self, is_min=True):
        """Visualiza MinHeap o MaxHeap."""
        # Limpiar canvas anterior
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        # Crear figura
        self.figure = Figure(figsize=(10, 6), dpi=100)
        ax = self.figure.add_subplot(111)
        
        if self.current_structure and self.current_structure.size() > 0:
            # Obtener datos del heap
            heap_data = [elem.value for elem in self.current_structure.heap]
            
            # Dibujar árbol binario
            self._draw_binary_tree(ax, heap_data, is_min)
            
            # Actualizar info
            info = f"Tipo: {'MinHeap' if is_min else 'MaxHeap'}\n"
            info += f"Elementos: {len(heap_data)}\n"
            info += f"Raíz: {heap_data[0] if heap_data else 'N/A'}\n"
            info += f"Array: {heap_data[:10]}{'...' if len(heap_data) > 10 else ''}"
            
        else:
            ax.text(0.5, 0.5, f"{'MinHeap' if is_min else 'MaxHeap'} vacío\n\nInserta datos para visualizar", 
                   ha='center', va='center', transform=ax.transAxes, 
                   fontsize=14, color='gray')
            info = f"Tipo: {'MinHeap' if is_min else 'MaxHeap'}\nElementos: 0"
        
        ax.set_title(f"{'Min' if is_min else 'Max'} Heap - Visualización", 
                    fontsize=14, fontweight='bold')
        ax.axis('off')
        
        # Mostrar canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Actualizar info
        self._update_info(info)
    
    def _draw_binary_tree(self, ax, data, is_min=True):
        """Dibuja árbol binario (heap)."""
        if not data:
            return
        
        n = len(data)
        levels = int(np.log2(n)) + 1
        
        # Calcular posiciones
        positions = {}
        
        def calculate_position(index, level, left, right):
            if index >= n:
                return
            
            x = (left + right) / 2
            y = levels - level
            positions[index] = (x, y)
            
            # Hijos
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            
            if left_child < n:
                calculate_position(left_child, level + 1, left, x)
            if right_child < n:
                calculate_position(right_child, level + 1, x, right)
        
        calculate_position(0, 0, 0, 2**levels)
        
        # Dibujar aristas
        for i in range(n):
            left_child = 2 * i + 1
            right_child = 2 * i + 2
            
            if left_child < n:
                x1, y1 = positions[i]
                x2, y2 = positions[left_child]
                ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.3, linewidth=1)
            
            if right_child < n:
                x1, y1 = positions[i]
                x2, y2 = positions[right_child]
                ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.3, linewidth=1)
        
        # Dibujar nodos
        for i, val in enumerate(data):
            x, y = positions[i]
            
            # Color según nivel
            if i == 0:
                color = '#e74c3c' if not is_min else '#3498db'
            else:
                color = '#ecf0f1'
            
            circle = plt.Circle((x, y), 0.3, color=color, ec='black', linewidth=2, zorder=10)
            ax.add_patch(circle)
            ax.text(x, y, str(val), ha='center', va='center', 
                   fontsize=10, fontweight='bold', zorder=11)
        
        ax.set_xlim(-1, 2**levels + 1)
        ax.set_ylim(-0.5, levels + 0.5)
        ax.set_aspect('equal')
    
    def _visualize_avl_tree(self):
        """Visualiza AVL Tree."""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        self.figure = Figure(figsize=(10, 6), dpi=100)
        ax = self.figure.add_subplot(111)
        
        if self.current_structure and self.current_structure.size() > 0:
            # Dibujar árbol AVL
            self._draw_avl_tree(ax, self.current_structure.root)
            
            info = f"Tipo: AVL Tree\n"
            info += f"Elementos: {self.current_structure.size()}\n"
            info += f"Altura: {self.current_structure.height()}\n"
            info += f"Balanceado: {'✅' if self.current_structure.is_balanced() else '❌'}"
        else:
            ax.text(0.5, 0.5, "AVL Tree vacío\n\nInserta datos para visualizar", 
                   ha='center', va='center', transform=ax.transAxes, 
                   fontsize=14, color='gray')
            info = "Tipo: AVL Tree\nElementos: 0"
        
        ax.set_title("AVL Tree - Auto-Balanceado", fontsize=14, fontweight='bold')
        ax.axis('off')
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self._update_info(info)
    
    def _draw_avl_tree(self, ax, node, x=0, y=0, dx=2):
        """Dibuja árbol AVL recursivamente."""
        if node is None:
            return
        
        # Dibujar nodo actual
        circle = plt.Circle((x, y), 0.25, color='#2ecc71', ec='black', linewidth=2, zorder=10)
        ax.add_patch(circle)
        ax.text(x, y, str(node.key), ha='center', va='center', 
               fontsize=9, fontweight='bold', zorder=11)
        
        # Balance factor (pequeño)
        balance = self._get_balance(node)
        ax.text(x + 0.35, y + 0.15, f"{balance:+d}", ha='center', va='center',
               fontsize=7, color='red' if abs(balance) > 1 else 'green', zorder=11)
        
        # Hijo izquierdo
        if node.left:
            x_left = x - dx
            y_left = y - 1
            ax.plot([x, x_left], [y, y_left], 'k-', alpha=0.5, linewidth=1.5)
            self._draw_avl_tree(ax, node.left, x_left, y_left, dx * 0.6)
        
        # Hijo derecho
        if node.right:
            x_right = x + dx
            y_right = y - 1
            ax.plot([x, x_right], [y, y_right], 'k-', alpha=0.5, linewidth=1.5)
            self._draw_avl_tree(ax, node.right, x_right, y_right, dx * 0.6)
        
        ax.set_aspect('equal')
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 1)
    
    def _get_balance(self, node):
        """Calcula balance factor de nodo AVL."""
        if node is None:
            return 0
        left_h = node.left.height if node.left else -1
        right_h = node.right.height if node.right else -1
        return left_h - right_h
    
    def _visualize_hash_table(self):
        """Visualiza Hash Table."""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        self.figure = Figure(figsize=(10, 6), dpi=100)
        ax = self.figure.add_subplot(111)
        
        if self.current_structure and self.current_structure.size() > 0:
            # Dibujar tabla hash
            capacity = self.current_structure.capacity
            buckets = self.current_structure.table
            
            # Dibujar buckets
            for i in range(min(capacity, 16)):  # Limitar a 16 buckets visibles
                y = i
                
                # Bucket box
                rect = mpatches.Rectangle((0, y - 0.4), 1, 0.8, 
                                         linewidth=2, edgecolor='black', 
                                         facecolor='#ecf0f1')
                ax.add_patch(rect)
                ax.text(0.5, y, f"[{i}]", ha='center', va='center', 
                       fontsize=9, fontweight='bold')
                
                # Cadena (chaining)
                if buckets[i]:
                    chain = buckets[i]
                    x = 2
                    node = chain
                    while node:
                        # Nodo de cadena
                        rect = mpatches.Rectangle((x, y - 0.3), 1.5, 0.6,
                                                 linewidth=1, edgecolor='blue',
                                                 facecolor='#3498db', alpha=0.7)
                        ax.add_patch(rect)
                        ax.text(x + 0.75, y, f"{node.key}:{node.value}", 
                               ha='center', va='center', fontsize=8, color='white')
                        
                        # Flecha
                        if node.next:
                            ax.arrow(x + 1.5, y, 0.3, 0, head_width=0.2, 
                                   head_length=0.1, fc='black', ec='black')
                        
                        node = node.next
                        x += 2
            
            stats = self.current_structure.get_statistics()
            info = f"Tipo: Hash Table (Chaining)\n"
            info += f"Elementos: {stats['size']}\n"
            info += f"Capacidad: {stats['capacity']}\n"
            info += f"Load Factor: {stats['load_factor']:.2f}\n"
            info += f"Colisiones: {stats['collisions']}"
            
        else:
            ax.text(0.5, 0.5, "Hash Table vacía\n\nInserta datos para visualizar", 
                   ha='center', va='center', transform=ax.transAxes, 
                   fontsize=14, color='gray')
            info = "Tipo: Hash Table\nElementos: 0"
        
        ax.set_title("Hash Table - Chaining", fontsize=14, fontweight='bold')
        ax.set_xlim(-0.5, 10)
        ax.set_ylim(-1, 16)
        ax.axis('off')
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self._update_info(info)
    
    def _visualize_trie(self):
        """Visualiza Trie."""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        self.figure = Figure(figsize=(10, 6), dpi=100)
        ax = self.figure.add_subplot(111)
        
        if self.current_structure and self.current_structure.size() > 0:
            # Dibujar trie (simplificado)
            words = self.current_structure.get_all_words("")
            
            # Mostrar palabras en árbol simple
            y = 0
            for word in words[:15]:  # Limitar a 15 palabras
                ax.text(0, y, word, fontsize=11, family='monospace')
                
                # Línea de separación
                ax.plot([0, len(word) * 0.15], [y - 0.2, y - 0.2], 
                       'k-', alpha=0.2, linewidth=0.5)
                y -= 0.5
            
            if len(words) > 15:
                ax.text(0, y, f"... y {len(words) - 15} más", 
                       fontsize=10, style='italic', color='gray')
            
            info = f"Tipo: Trie (Prefix Tree)\n"
            info += f"Palabras: {self.current_structure.size()}\n"
            info += f"Nodos: {self.current_structure.node_count}\n"
            info += f"Primeras: {', '.join(words[:5])}"
        else:
            ax.text(0.5, 0.5, "Trie vacío\n\nInserta palabras separadas por comas", 
                   ha='center', va='center', transform=ax.transAxes, 
                   fontsize=14, color='gray')
            info = "Tipo: Trie\nPalabras: 0"
        
        ax.set_title("Trie - Árbol de Prefijos", fontsize=14, fontweight='bold')
        ax.set_xlim(-0.5, 5)
        ax.set_ylim(-8, 1)
        ax.axis('off')
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self._update_info(info)
    
    def _update_info(self, text):
        """Actualiza panel de información."""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", text)
        self.info_text.config(state=tk.DISABLED)


if __name__ == '__main__':
    # Demo standalone
    root = tk.Tk()
    root.title("Data Structures Visualizer Demo")
    root.geometry("1000x800")
    
    visualizer = DataStructuresVisualizer(root)
    
    root.mainloop()
