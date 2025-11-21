"""
Complexity Plotter - Visualizador de Complejidades Temporales

Genera gráficos comparativos de diferentes complejidades algorítmicas.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk


class ComplexityPlotter:
    """
    Visualizador de complejidades algorítmicas.
    
    Genera gráficos comparativos de O(1), O(log n), O(n), O(n log n), O(n²), O(2^n).
    """
    
    def __init__(self, parent_frame):
        """
        Inicializa el plotter.
        
        Args:
            parent_frame: Frame padre de tkinter
        """
        self.parent = parent_frame
        self.figure = None
        self.canvas = None
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea interfaz de usuario."""
        # Frame para controles
        control_frame = ttk.LabelFrame(self.parent, text="Opciones de Visualización", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Rango de n
        range_frame = ttk.Frame(control_frame)
        range_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(range_frame, text="Rango n:").pack(side=tk.LEFT, padx=5)
        
        self.n_min = tk.IntVar(value=1)
        ttk.Entry(range_frame, textvariable=self.n_min, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(range_frame, text="hasta").pack(side=tk.LEFT, padx=5)
        
        self.n_max = tk.IntVar(value=20)
        ttk.Entry(range_frame, textvariable=self.n_max, width=10).pack(side=tk.LEFT, padx=5)
        
        # Checkboxes
        check_frame = ttk.Frame(control_frame)
        check_frame.pack(fill=tk.X, pady=5)
        
        self.complexities = {
            "O(1)": tk.BooleanVar(value=True),
            "O(log n)": tk.BooleanVar(value=True),
            "O(n)": tk.BooleanVar(value=True),
            "O(n log n)": tk.BooleanVar(value=True),
            "O(n²)": tk.BooleanVar(value=True),
            "O(2^n)": tk.BooleanVar(value=False)  # Desactivado por defecto
        }
        
        for comp, var in self.complexities.items():
            ttk.Checkbutton(check_frame, text=comp, variable=var).pack(side=tk.LEFT, padx=10)
        
        # Botón graficar
        ttk.Button(control_frame, text="📊 Generar Gráfico", 
                  command=self.plot, style="Accent.TButton").pack(pady=10)
        
        # Frame para gráfico
        self.plot_frame = ttk.Frame(self.parent)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Generar gráfico inicial
        self.plot()
    
    def plot(self):
        """Genera gráfico de complejidades."""
        # Limpiar gráfico anterior
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        # Obtener rango
        n_min = max(1, self.n_min.get())
        n_max = max(n_min + 1, self.n_max.get())
        
        # Generar valores de n
        n = np.linspace(n_min, n_max, 100)
        
        # Crear figura
        self.figure = Figure(figsize=(10, 6), dpi=100)
        ax = self.figure.add_subplot(111)
        
        # Colores
        colors = {
            "O(1)": "#2ecc71",
            "O(log n)": "#3498db",
            "O(n)": "#9b59b6",
            "O(n log n)": "#e74c3c",
            "O(n²)": "#e67e22",
            "O(2^n)": "#c0392b"
        }
        
        # Graficar complejidades seleccionadas
        plotted = False
        
        if self.complexities["O(1)"].get():
            ax.plot(n, np.ones_like(n), label="O(1)", color=colors["O(1)"], linewidth=2)
            plotted = True
        
        if self.complexities["O(log n)"].get():
            ax.plot(n, np.log2(n + 1), label="O(log n)", color=colors["O(log n)"], linewidth=2)
            plotted = True
        
        if self.complexities["O(n)"].get():
            ax.plot(n, n, label="O(n)", color=colors["O(n)"], linewidth=2)
            plotted = True
        
        if self.complexities["O(n log n)"].get():
            ax.plot(n, n * np.log2(n + 1), label="O(n log n)", color=colors["O(n log n)"], linewidth=2)
            plotted = True
        
        if self.complexities["O(n²)"].get():
            ax.plot(n, n**2, label="O(n²)", color=colors["O(n²)"], linewidth=2)
            plotted = True
        
        if self.complexities["O(2^n)"].get() and n_max <= 20:  # Limitar para evitar overflow
            n_limited = n[n <= 20]
            ax.plot(n_limited, 2**n_limited, label="O(2^n)", color=colors["O(2^n)"], linewidth=2)
            plotted = True
        elif self.complexities["O(2^n)"].get():
            ax.text(0.5, 0.5, "O(2^n) requiere n ≤ 20", 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14, color='red')
        
        if not plotted:
            ax.text(0.5, 0.5, "Selecciona al menos una complejidad", 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
        
        # Configurar gráfico
        ax.set_xlabel("Tamaño de entrada (n)", fontsize=12)
        ax.set_ylabel("Tiempo de ejecución", fontsize=12)
        ax.set_title("Comparación de Complejidades Temporales", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left', fontsize=10)
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def create_complexity_comparison(parent):
    """
    Crea panel de comparación de complejidades.
    
    Args:
        parent: Frame padre
    
    Returns:
        ComplexityPlotter instance
    """
    return ComplexityPlotter(parent)


if __name__ == '__main__':
    # Demo standalone
    root = tk.Tk()
    root.title("Complexity Plotter Demo")
    root.geometry("900x700")
    
    plotter = ComplexityPlotter(root)
    
    root.mainloop()
