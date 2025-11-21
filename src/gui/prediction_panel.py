"""
Prediction Panel - Panel de Predicción con Integración Real

Integra MLP + RecurrenceParser + MasterTheorem para análisis completo.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import json
import os


class PredictionPanel:
    """Panel de predicción con análisis completo."""
    
    def __init__(self, parent_frame):
        """
        Inicializa panel de predicción.
        
        Args:
            parent_frame: Frame padre de tkinter
        """
        self.parent = parent_frame
        self.mlp = None
        self.recurrence_parser = None
        self.master_theorem = None
        
        self._load_models()
        self._create_ui()
    
    def _load_models(self):
        """Carga modelos entrenados."""
        try:
            # Cargar MLP
            import sys
            sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
            
            from src.ml.mlp import MLP
            from src.complexity_analysis.recurrence_parser import RecurrenceParser
            from src.complexity_analysis.master_theorem import MasterTheorem
            
            # Cargar modelo entrenado
            model_path = os.path.join(os.path.dirname(__file__), '../../models/best_mlp_model.json')
            if os.path.exists(model_path):
                self.mlp = MLP.load(model_path)
            
            self.recurrence_parser = RecurrenceParser()
            self.master_theorem = MasterTheorem()
            
        except Exception as e:
            print(f"Error cargando modelos: {e}")
    
    def _create_ui(self):
        """Crea interfaz de usuario."""
        # Frame principal dividido
        main_paned = ttk.PanedWindow(self.parent, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel izquierdo: código
        left_frame = ttk.LabelFrame(main_paned, text="Código de Entrada", padding=10)
        main_paned.add(left_frame, weight=1)
        
        self._create_code_editor(left_frame)
        
        # Panel derecho: resultados
        right_frame = ttk.LabelFrame(main_paned, text="Resultados del Análisis", padding=10)
        main_paned.add(right_frame, weight=1)
        
        self._create_results_panel(right_frame)
    
    def _create_code_editor(self, parent):
        """Crea editor de código."""
        # Área de texto
        text_container = ttk.Frame(parent)
        text_container.pack(fill=tk.BOTH, expand=True)
        
        # Text widget con scrollbars usando pack
        y_scroll = ttk.Scrollbar(text_container, orient=tk.VERTICAL)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scroll = ttk.Scrollbar(text_container, orient=tk.HORIZONTAL)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.code_text = tk.Text(text_container, wrap=tk.NONE, font=("Consolas", 10),
                                bg="#1e1e1e", fg="#d4d4d4", insertbackground="white",
                                yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        y_scroll.config(command=self.code_text.yview)
        x_scroll.config(command=self.code_text.xview)
        
        # Texto de ejemplo
        example_code = """package main

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
}"""
        self.code_text.insert("1.0", example_code)
        
        # Botones de control
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="🔍 Analizar Código", 
                  command=self.analyze_code, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Limpiar", 
                  command=self.clear_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📋 Ejemplo", 
                  command=self.load_example).pack(side=tk.LEFT, padx=5)
    
    def _create_results_panel(self, parent):
        """Crea panel de resultados."""
        # Notebook para diferentes análisis
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Resumen
        summary_frame = ttk.Frame(notebook, padding=10)
        notebook.add(summary_frame, text="📊 Resumen")
        
        self.summary_text = tk.Text(summary_frame, wrap=tk.WORD, font=("Consolas", 10),
                                   state=tk.DISABLED, height=15)
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        
        summary_scroll = ttk.Scrollbar(summary_frame, orient=tk.VERTICAL, 
                                      command=self.summary_text.yview)
        summary_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.summary_text.config(yscrollcommand=summary_scroll.set)
        
        # Tab 2: Recurrencia
        recurrence_frame = ttk.Frame(notebook, padding=10)
        notebook.add(recurrence_frame, text="🔄 Recurrencia")
        
        self.recurrence_text = tk.Text(recurrence_frame, wrap=tk.WORD, font=("Consolas", 10),
                                      state=tk.DISABLED)
        self.recurrence_text.pack(fill=tk.BOTH, expand=True)
        
        # Tab 3: Master Theorem
        master_frame = ttk.Frame(notebook, padding=10)
        notebook.add(master_frame, text="📐 Master Theorem")
        
        self.master_text = tk.Text(master_frame, wrap=tk.WORD, font=("Consolas", 10),
                                  state=tk.DISABLED)
        self.master_text.pack(fill=tk.BOTH, expand=True)
        
        # Tab 4: MLP
        mlp_frame = ttk.Frame(notebook, padding=10)
        notebook.add(mlp_frame, text="🧠 Red Neuronal")
        
        self.mlp_text = tk.Text(mlp_frame, wrap=tk.WORD, font=("Consolas", 10),
                               state=tk.DISABLED)
        self.mlp_text.pack(fill=tk.BOTH, expand=True)
    
    def analyze_code(self):
        """Analiza código con todos los métodos."""
        code = self.code_text.get("1.0", tk.END).strip()
        
        if not code:
            messagebox.showwarning("Advertencia", "Ingresa código para analizar")
            return
        
        # Limpiar resultados anteriores
        self._clear_results()
        
        try:
            # 1. Análisis de recurrencia
            recurrence_result = None
            if self.recurrence_parser:
                recurrence_result = self.recurrence_parser.parse(code)
                self._display_recurrence(recurrence_result)
            
            # 2. Master Theorem
            master_result = None
            if self.master_theorem and recurrence_result and recurrence_result.get('detected'):
                a = recurrence_result.get('a', 1)
                b = recurrence_result.get('b', 1)
                fn_complexity = recurrence_result.get('fn_complexity', 'O(1)')
                
                master_result = self.master_theorem.solve(a, b, fn_complexity)
                self._display_master_theorem(master_result)
            
            # 3. MLP (si está disponible)
            if self.mlp:
                # TODO: Extraer features del código
                # Por ahora, mostrar mensaje
                self._display_mlp_placeholder()
            
            # 4. Resumen
            self._display_summary(recurrence_result, master_result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el análisis:\n{str(e)}")
    
    def _clear_results(self):
        """Limpia resultados previos."""
        for text_widget in [self.summary_text, self.recurrence_text, 
                           self.master_text, self.mlp_text]:
            text_widget.config(state=tk.NORMAL)
            text_widget.delete("1.0", tk.END)
            text_widget.config(state=tk.DISABLED)
    
    def _display_recurrence(self, result):
        """Muestra resultado de análisis de recurrencia."""
        self.recurrence_text.config(state=tk.NORMAL)
        
        if result and result.get('detected'):
            text = "✅ RECURRENCIA DETECTADA\n\n"
            text += f"Forma: T(n) = {result['a']}·T(n/{result['b']}) + {result['fn_complexity']}\n\n"
            text += f"Parámetros:\n"
            text += f"  a = {result['a']} (llamadas recursivas)\n"
            text += f"  b = {result['b']} (división del problema)\n"
            text += f"  f(n) = {result['fn_complexity']} (trabajo adicional)\n\n"
            text += f"Confianza: {result.get('confidence', 0):.1%}\n"
        else:
            text = "❌ No se detectó recurrencia\n\n"
            text += "El código no parece seguir un patrón de divide-y-conquista.\n"
        
        self.recurrence_text.insert("1.0", text)
        self.recurrence_text.config(state=tk.DISABLED)
    
    def _display_master_theorem(self, result):
        """Muestra resultado del Master Theorem."""
        self.master_text.config(state=tk.NORMAL)
        
        if result:
            text = "📐 ANÁLISIS CON MASTER THEOREM\n\n"
            text += f"Caso: {result.get('case', 'N/A')}\n"
            text += f"Complejidad: {result.get('complexity', 'N/A')}\n\n"
            text += f"Explicación:\n{result.get('explanation', 'N/A')}\n\n"
            text += f"Confianza: {result.get('confidence', 0):.1%}\n"
        else:
            text = "❌ Master Theorem no aplicable\n\n"
            text += "La recurrencia no cumple con los requisitos del Master Theorem.\n"
        
        self.master_text.insert("1.0", text)
        self.master_text.config(state=tk.DISABLED)
    
    def _display_mlp_placeholder(self):
        """Muestra placeholder para MLP."""
        self.mlp_text.config(state=tk.NORMAL)
        
        text = "🧠 PREDICCIÓN CON RED NEURONAL\n\n"
        text += "Modelo: MLP (118 → 128 → 64 → 6)\n"
        text += "Entrenamiento: 1000 épocas, 31 algoritmos\n\n"
        text += "⚠️ Integración pendiente\n"
        text += "La extracción de features del código está en desarrollo.\n"
        
        self.mlp_text.insert("1.0", text)
        self.mlp_text.config(state=tk.DISABLED)
    
    def _display_summary(self, recurrence_result, master_result):
        """Muestra resumen del análisis."""
        self.summary_text.config(state=tk.NORMAL)
        
        text = "═" * 50 + "\n"
        text += "RESUMEN DEL ANÁLISIS\n"
        text += "═" * 50 + "\n\n"
        
        # Complejidad final
        if master_result and master_result.get('complexity'):
            complexity = master_result['complexity']
            confidence = master_result.get('confidence', 0)
        elif recurrence_result and recurrence_result.get('detected'):
            complexity = "O(n log n)"  # Default estimate
            confidence = 0.7
        else:
            complexity = "Desconocida"
            confidence = 0.0
        
        text += f"📊 Complejidad Temporal: {complexity}\n"
        text += f"🎯 Confianza: {confidence:.1%}\n\n"
        
        # Métodos utilizados
        text += "Métodos de análisis:\n"
        
        if recurrence_result and recurrence_result.get('detected'):
            text += "  ✅ Análisis de recurrencia\n"
        else:
            text += "  ❌ Análisis de recurrencia\n"
        
        if master_result:
            text += "  ✅ Master Theorem\n"
        else:
            text += "  ❌ Master Theorem\n"
        
        text += "  ⚠️  Red Neuronal (pendiente)\n\n"
        
        # Recomendaciones
        text += "Recomendaciones:\n"
        if confidence > 0.8:
            text += "  • Alta confianza en el resultado\n"
        elif confidence > 0.5:
            text += "  • Confianza moderada, considera análisis manual\n"
        else:
            text += "  • Baja confianza, se recomienda análisis experto\n"
        
        self.summary_text.insert("1.0", text)
        self.summary_text.config(state=tk.DISABLED)
    
    def clear_code(self):
        """Limpia editor de código."""
        self.code_text.delete("1.0", tk.END)
    
    def load_example(self):
        """Carga código de ejemplo."""
        example = """package main

func mergeSort(arr []int) []int {
    if len(arr) <= 1 {
        return arr
    }
    
    mid := len(arr) / 2
    left := mergeSort(arr[:mid])
    right := mergeSort(arr[mid:])
    
    return merge(left, right)
}

func merge(left, right []int) []int {
    result := make([]int, 0, len(left)+len(right))
    i, j := 0, 0
    
    for i < len(left) && j < len(right) {
        if left[i] <= right[j] {
            result = append(result, left[i])
            i++
        } else {
            result = append(result, right[j])
            j++
        }
    }
    
    result = append(result, left[i:]...)
    result = append(result, right[j:]...)
    
    return result
}"""
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", example)
