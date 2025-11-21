"""
Main Window - Ventana Principal de la GUI

Interfaz gráfica con múltiples paneles:
- Predicción de complejidad
- Visualización de entrenamiento
- Estructuras de datos
- Análisis de algoritmos
- Comparador de complejidades
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import json
from datetime import datetime

# Agregar directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importar módulos de análisis
from src.complexity_analysis.recurrence_parser import RecurrenceParser
from src.complexity_analysis.master_theorem import MasterTheorem


class MainWindow:
    """
    Ventana principal de la aplicación.
    
    Usa ttk.Notebook para organizar diferentes paneles en tabs.
    """
    
    def __init__(self):
        """Inicializa ventana principal."""
        self.root = tk.Tk()
        self.root.title("Análisis de Complejidad Algorítmica - ADA Project")
        self.root.geometry("1200x800")
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Inicializar analizadores
        self.recurrence_parser = RecurrenceParser()
        self.master_theorem = MasterTheorem()
        self.current_analysis_result = None
        
        # Crear interfaz
        self._create_menu()
        self._create_notebook()
        self._create_status_bar()
        
    def _create_menu(self):
        """Crea barra de menú."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Abrir código...", command=self._open_file)
        file_menu.add_command(label="Guardar análisis...", command=self._save_analysis)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Modelo
        model_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modelo", menu=model_menu)
        model_menu.add_command(label="Cargar modelo...", command=self._load_model)
        model_menu.add_command(label="Reentrenar", command=self._retrain_model)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Documentación", command=self._show_docs)
        help_menu.add_command(label="Acerca de", command=self._show_about)
    
    def _create_notebook(self):
        """Crea notebook con tabs."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Predicción
        self.prediction_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.prediction_frame, text="📊 Predicción")
        self._create_prediction_panel()
        
        # Tab 2: Entrenamiento
        self.training_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.training_frame, text="📈 Entrenamiento")
        self._create_training_panel()
        
        # Tab 3: Estructuras de Datos
        self.structures_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.structures_frame, text="🌳 Estructuras")
        self._create_structures_panel()
        
        # Tab 4: Comparador
        self.compare_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.compare_frame, text="⚖️ Comparador")
        self._create_compare_panel()
    
    def _create_prediction_panel(self):
        """Panel de predicción de complejidad."""
        # Frame izquierdo: entrada de código
        left_frame = ttk.LabelFrame(self.prediction_frame, text="Código de Entrada")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Área de texto para código
        text_frame = ttk.Frame(left_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        y_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.code_text = tk.Text(text_frame, wrap=tk.NONE, font=("Consolas", 10),
                                yscrollcommand=y_scroll.set)
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scroll.config(command=self.code_text.yview)
        
        # Placeholder
        placeholder = """// Ingresa tu código Go aquí
package main

func binarySearch(arr []int, target int) int {
    left, right := 0, len(arr)-1
    
    for left <= right {
        mid := (left + right) / 2
        if arr[mid] == target {
            return mid
        } else if arr[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }
    return -1
}
"""
        self.code_text.insert("1.0", placeholder)
        
        # Botones
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="🔍 Analizar", command=self._analyze_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Limpiar", command=self._clear_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📂 Cargar archivo", command=self._load_code_file).pack(side=tk.LEFT, padx=5)
        
        # Frame derecho: resultados
        right_frame = ttk.LabelFrame(self.prediction_frame, text="Resultados del Análisis")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Texto de resultados
        self.results_text = tk.Text(right_frame, wrap=tk.WORD, font=("Consolas", 10), state=tk.DISABLED)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        result_scroll = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        result_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=result_scroll.set)
    
    def _create_training_panel(self):
        """Panel de visualización de entrenamiento."""
        try:
            from src.gui.training_visualizer import TrainingVisualizer
            TrainingVisualizer(self.training_frame)
        except Exception as e:
            label = ttk.Label(self.training_frame, text=f"Error cargando visualizador: {e}")
            label.pack(pady=20)
    
    def _create_structures_panel(self):
        """Panel de estructuras de datos."""
        try:
            from src.gui.data_structures_visualizer import DataStructuresVisualizer
            DataStructuresVisualizer(self.structures_frame)
        except Exception as e:
            label = ttk.Label(self.structures_frame, text=f"Error cargando visualizador: {e}")
            label.pack(pady=20)
    
    def _create_compare_panel(self):
        """Panel comparador de complejidades."""
        # Usar ComplexityPlotter
        try:
            from src.gui.complexity_plotter import ComplexityPlotter
            ComplexityPlotter(self.compare_frame)
        except Exception as e:
            # Fallback
            label = ttk.Label(self.compare_frame, text=f"Error cargando plotter: {e}")
            label.pack(pady=20)
    
    def _create_status_bar(self):
        """Crea barra de estado."""
        self.status_bar = ttk.Label(self.root, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Callbacks de menú
    def _open_file(self):
        """Abre archivo de código."""
        filename = filedialog.askopenfilename(
            title="Abrir código",
            filetypes=[("Go files", "*.go"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    code = f.read()
                self.code_text.delete("1.0", tk.END)
                self.code_text.insert("1.0", code)
                self.status_bar.config(text=f"Cargado: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")
    
    def _save_analysis(self):
        """Guarda análisis en archivo JSON."""
        if self.current_analysis_result is None:
            messagebox.showwarning("Advertencia", "No hay análisis para guardar.\nPrimero analiza algún código.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Guardar análisis",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Preparar datos para JSON
                data = {
                    'timestamp': datetime.now().isoformat(),
                    'code': self.current_analysis_result['code'],
                    'analysis': {
                        'recurrence_detected': self.current_analysis_result['recurrence'] is not None,
                    }
                }
                
                if self.current_analysis_result['recurrence']:
                    rec = self.current_analysis_result['recurrence']
                    data['analysis']['recurrence'] = {
                        'formula': self.recurrence_parser.format_recurrence(rec),
                        'a': rec.a,
                        'b': rec.b,
                        'f_n': rec.f_n,
                        'confidence': rec.confidence,
                        'division_pattern': rec.division_pattern
                    }
                    
                    mt = self.current_analysis_result['master_theorem']
                    data['analysis']['master_theorem'] = {
                        'case': mt.case.name,
                        'complexity': mt.complexity,
                        'c_value': mt.c_value,
                        'confidence': mt.confidence,
                        'explanation': mt.explanation
                    }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                self.status_bar.config(text=f"✓ Análisis guardado en: {filename}")
                messagebox.showinfo("Éxito", f"Análisis guardado exitosamente en:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el análisis:\n{e}")
                self.status_bar.config(text="✗ Error al guardar")
    
    def _load_model(self):
        """Carga modelo."""
        messagebox.showinfo("Info", "Función de carga de modelo en desarrollo")
    
    def _retrain_model(self):
        """Reentrena modelo."""
        messagebox.showinfo("Info", "Función de reentrenamiento en desarrollo")
    
    def _show_docs(self):
        """Muestra documentación."""
        messagebox.showinfo("Documentación", 
                          "Analizador de Complejidad Algorítmica\n\n"
                          "Utiliza MLP + RecurrenceParser + MasterTheorem\n\n"
                          "Fases completadas:\n"
                          "✅ Fase 1: MLP desde cero\n"
                          "✅ Fase 2: Algoritmos avanzados\n"
                          "✅ Fase 3: Estructuras de datos\n"
                          "✅ Fase 4: GUI completa")
    
    def _show_about(self):
        """Muestra información."""
        messagebox.showinfo("Acerca de", 
                          "Proyecto Final - Análisis de Algoritmos\n\n"
                          "Versión: 1.0.0\n"
                          "Año: 2025\n\n"
                          "Desarrollado para el curso de\n"
                          "Análisis y Diseño de Algoritmos")
    
    # Callbacks de predicción
    def _analyze_code(self):
        """Analiza código usando RecurrenceParser y MasterTheorem."""
        code = self.code_text.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Advertencia", "Ingresa código para analizar")
            return
        
        self.status_bar.config(text="Analizando código...")
        self.root.update_idletasks()
        
        try:
            # 1. Análisis de recurrencia
            self.status_bar.config(text="Detectando recurrencias...")
            self.root.update_idletasks()
            
            recurrence = self.recurrence_parser.parse(code)
            
            result = "═" * 60 + "\n"
            result += "ANÁLISIS DE COMPLEJIDAD COMPUTACIONAL\n"
            result += "═" * 60 + "\n\n"
            
            if recurrence is None:
                result += "❌ NO SE DETECTÓ RECURSIÓN\n\n"
                result += "El código no parece usar recursión o divide-y-conquista.\n"
                result += "Posible complejidad iterativa: O(n) o mejor.\n\n"
                result += "💡 Tip: El analizador funciona mejor con algoritmos recursivos\n"
                result += "   como Binary Search, Merge Sort, Quicksort, etc.\n"
                
                self.current_analysis_result = None
                
            else:
                # 2. Mostrar recurrencia detectada
                recurrence_str = self.recurrence_parser.format_recurrence(recurrence)
                result += "✅ RECURRENCIA DETECTADA\n\n"
                result += f"Forma matemática:\n"
                result += f"  {recurrence_str}\n\n"
                
                result += f"Parámetros:\n"
                result += f"  • a = {recurrence.a} (llamadas recursivas)\n"
                result += f"  • b = {recurrence.b} (factor de división)\n"
                result += f"  • f(n) = {recurrence.f_n} (trabajo no recursivo)\n\n"
                
                result += f"Detalles:\n"
                result += f"  • Patrón de división: {recurrence.division_pattern}\n"
                result += f"  • Profundidad de loops: {recurrence.loop_depth}\n"
                result += f"  • Confianza de detección: {recurrence.confidence:.1%}\n\n"
                
                # 3. Aplicar Master Theorem
                self.status_bar.config(text="Aplicando Master Theorem...")
                self.root.update_idletasks()
                
                mt_result = self.master_theorem.solve(
                    recurrence.a,
                    recurrence.b,
                    recurrence.f_n
                )
                
                result += "─" * 60 + "\n"
                result += "MASTER THEOREM\n"
                result += "─" * 60 + "\n\n"
                
                result += f"📊 Complejidad Final: {mt_result.complexity}\n\n"
                
                result += f"Análisis:\n"
                result += f"  • Caso: {mt_result.case.name}\n"
                result += f"  • c = log_{recurrence.b}({recurrence.a}) = {mt_result.c_value:.3f}\n"
                result += f"  • {mt_result.comparison}\n\n"
                
                result += f"Explicación:\n"
                for line in mt_result.explanation.split('\n'):
                    result += f"  {line}\n"
                
                result += f"\n  • Confianza: {mt_result.confidence:.1%}\n"
                
                # Guardar resultado
                self.current_analysis_result = {
                    'recurrence': recurrence,
                    'master_theorem': mt_result,
                    'code': code
                }
            
            result += "\n" + "═" * 60 + "\n"
            
            # Mostrar resultado
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert("1.0", result)
            self.results_text.config(state=tk.DISABLED)
            
            self.status_bar.config(text="✓ Análisis completado exitosamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el análisis:\n\n{str(e)}")
            self.status_bar.config(text="✗ Error en el análisis")
    
    def _clear_code(self):
        """Limpia código."""
        self.code_text.delete("1.0", tk.END)
    
    def _load_code_file(self):
        """Carga archivo de código."""
        self._open_file()
    
    # Callbacks de estructuras
    def _visualize_structure(self):
        """Visualiza estructura. (Ya no se usa - DataStructuresVisualizer maneja esto)"""
        pass
    
    # Callbacks de comparador
    def _plot_comparison(self):
        """Grafica comparación. (Ya no se usa - ComplexityPlotter maneja esto)"""
        pass
    
    def run(self):
        """Inicia aplicación."""
        self.root.mainloop()


def main():
    """Punto de entrada principal."""
    app = MainWindow()
    app.run()


if __name__ == '__main__':
    main()
