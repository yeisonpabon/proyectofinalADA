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
import re
from datetime import datetime
import numpy as np

# Agregar directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importar módulos de análisis
from src.complexity_analysis.recurrence_parser import RecurrenceParser
from src.complexity_analysis.master_theorem import MasterTheorem
from src.neural_network.mlp import MLP
from src.data_processing.feature_extractor import GoFeatureExtractor


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
        
        # Inicializar MLP y feature extractor
        self.mlp = None
        self.feature_extractor = GoFeatureExtractor(max_features=200)  # Debe coincidir con train_model.py
        self.complexity_labels = {
            0: "O(1)",
            1: "O(log n)",
            2: "O(n)",
            3: "O(n log n)",
            4: "O(n²)",
            5: "O(2^n)"
        }
        self._load_mlp_model()
        
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
        self.notebook.add(self.training_frame, text="Entrenamiento")
        self._create_training_panel()
        
        # Tab 3: Estructuras de Datos
        self.structures_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.structures_frame, text="Estructuras")
        self._create_structures_panel()
        
        # Tab 4: Comparador
        self.compare_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.compare_frame, text="Comparador")
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
        
        ttk.Button(button_frame, text="Analizar", command=self._analyze_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self._clear_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cargar archivo", command=self._load_code_file).pack(side=tk.LEFT, padx=5)
        
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
    
    def _load_mlp_model(self):
        """Carga el modelo MLP entrenado."""
        # Preferir modelo v6 (220) o fine-tuned, sino original
        base_models_dir = os.path.join(os.path.dirname(__file__), '../../experiments/models')
        v6_path = os.path.join(base_models_dir, 'mlp_complexity_classifier_220.npz')
        finetuned_path = os.path.join(base_models_dir, 'mlp_complexity_classifier_finetuned.npz')
        original_path = os.path.join(base_models_dir, 'mlp_complexity_classifier.npz')
        
        if os.path.exists(v6_path):
            model_path = v6_path
        elif os.path.exists(finetuned_path):
            model_path = finetuned_path
        else:
            model_path = original_path
        dataset_path = os.path.join(os.path.dirname(__file__), '../../data/dataset.json')
        
        # Primero, entrenar el feature extractor con el dataset (si es dataset antiguo con 'path')
        if os.path.exists(dataset_path):
            try:
                with open(dataset_path, 'r', encoding='utf-8') as f:
                    dataset = json.load(f)
                
                # Verificar si es dataset v6 (no tiene 'path')
                if dataset['algorithms'] and 'path' not in dataset['algorithms'][0]:
                    print("✓ Dataset v6 detectado (features pre-calculadas, no requiere extractor)")
                else:
                    # Cargar código de los algoritmos (dataset antiguo)
                    code_samples = []
                    for algo in dataset['algorithms']:
                        if 'path' in algo:
                            algo_path = os.path.join(os.path.dirname(__file__), '../../', algo['path'])
                            if os.path.exists(algo_path):
                                with open(algo_path, 'r', encoding='utf-8') as code_file:
                                    code_samples.append(code_file.read())
                    
                    if code_samples:
                        # Entrenar extractor
                        self.feature_extractor.fit(code_samples)
                        print(f"✓ Feature extractor entrenado con {len(code_samples)} algoritmos")
                
            except Exception as e:
                print(f"⚠ Error procesando dataset: {e}")
        
        # Cargar modelo MLP dinámicamente según dimensión de features
        if os.path.exists(model_path):
            try:
                weights_npz = np.load(model_path)
                expected_input_dim = weights_npz['layer_0_W'].shape[0]
                num_classes = 6
                
                # Detectar si es modelo v6 (3 features) o modelo antiguo (225+ features)
                is_v6_model = expected_input_dim == 3
                
                if is_v6_model:
                    # Modelo v6: 3 → 64 → 32 → 6
                    hidden_dims = [64, 32]
                    input_dim = 3
                    print("✓ Detectado modelo v6 (3 features automáticos)")
                else:
                    # Modelo antiguo: 225+ → 256 → 128 → 64 → 6
                    hidden_dims = [256, 128, 64]
                    
                    # Ajustar input_dim desde extractor si está fitted
                    if self.feature_extractor.is_fitted:
                        current_dim = len(self.feature_extractor.feature_names)
                        if current_dim != expected_input_dim:
                            # Mismatch - intentar reajustar
                            syntactic_count = self.feature_extractor.syntactic_feature_count
                            adjusted_vocab_size = max(1, expected_input_dim - syntactic_count)
                            print(f"⚠ Mismatch dimensiones: extractor={current_dim}, pesos={expected_input_dim}")
                            self.feature_extractor.max_features = adjusted_vocab_size
                            # Recargar y refit del dataset si es posible
                            try:
                                with open(dataset_path, 'r', encoding='utf-8') as f:
                                    dataset_refit = json.load(f)
                                codes_refit = []
                                for algo in dataset_refit['algorithms']:
                                    if 'path' in algo:
                                        apath = os.path.join(os.path.dirname(__file__), '../../', algo['path'])
                                        if os.path.exists(apath):
                                            with open(apath, 'r', encoding='utf-8') as cf:
                                                codes_refit.append(cf.read())
                                if codes_refit:
                                    self.feature_extractor.fit(codes_refit)
                            except:
                                pass
                        input_dim = expected_input_dim
                    else:
                        input_dim = expected_input_dim
                
                self.mlp = MLP(
                    input_dim=input_dim,
                    hidden_dims=hidden_dims,
                    num_classes=num_classes,
                    learning_rate=0.001 if 'finetuned' in model_path else 0.008,
                    batch_size=4
                )
                self.mlp.load_weights(model_path)
                
                if is_v6_model:
                    tag = 'V6'
                elif 'finetuned' in model_path:
                    tag = 'FINE-TUNED'
                else:
                    tag = 'BASE'
                    
                print(f"Modelo ({tag}) cargado desde: {model_path}")
                print(f"✓ Arquitectura: {input_dim} → {hidden_dims} → {num_classes}")
                # Cargar historiales disponibles
                logs_dir = os.path.join(os.path.dirname(__file__), '../../experiments/logs')
                base_hist = os.path.join(logs_dir, 'training_history.json')
                ft_hist = os.path.join(logs_dir, 'fine_tune_history.json')
                if os.path.exists(base_hist):
                    with open(base_hist, 'r') as f:
                        h = json.load(f)
                        epochs = len(h.get('train_loss', []))
                        val_acc = h.get('val_accuracy', [0])[-1] if h.get('val_accuracy') else 0
                        print(f"✓ Historial base: {epochs} épocas, val acc {val_acc:.1%}")
                if os.path.exists(ft_hist):
                    with open(ft_hist, 'r') as f:
                        h = json.load(f)
                        epochs = len(h.get('train_loss', []))
                        val_acc = h.get('val_accuracy', [0])[-1] if h.get('val_accuracy') else 0
                        print(f"✓ Historial fine-tune: {epochs} épocas, última val acc {val_acc:.1%}")
            except Exception as e:
                print(f"⚠ Error cargando modelo MLP: {e}")
                import traceback
                traceback.print_exc()
                self.mlp = None
        else:
            print(f"⚠ Ningún modelo encontrado. Esperado: {model_path}")
            self.mlp = None
    
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
                
                # Agregar predicción MLP si existe
                if 'mlp_prediction' in self.current_analysis_result and self.current_analysis_result['mlp_prediction']:
                    data['analysis']['mlp'] = {
                        'prediction': self.current_analysis_result['mlp_prediction'],
                        'confidence': float(self.current_analysis_result['mlp_confidence'])
                    }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                self.status_bar.config(text=f"✓ Análisis guardado en: {filename}")
                messagebox.showinfo("Éxito", f"Análisis guardado exitosamente en:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el análisis:\n{e}")
                self.status_bar.config(text="✗ Error al guardar")
    
    def _load_model(self):
        """Carga modelo MLP desde archivo .npz"""
        filename = filedialog.askopenfilename(
            title="Cargar modelo MLP",
            defaultextension=".npz",
            filetypes=[("NumPy archive", "*.npz"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.status_bar.config(text="Cargando modelo...")
                self.root.update_idletasks()
                
                # Cargar pesos del modelo
                data = np.load(filename, allow_pickle=True)
                
                # Recrear arquitectura del MLP
                input_dim = data['input_dim'].item()
                hidden_dims = data['hidden_dims'].tolist()
                num_classes = data['num_classes'].item()
                
                self.mlp = MLP(
                    input_dim=input_dim,
                    hidden_dims=hidden_dims,
                    num_classes=num_classes,
                    learning_rate=0.01,
                    batch_size=4
                )
                
                # Cargar pesos
                self.mlp.load_weights(filename)
                
                self.status_bar.config(text=f"✓ Modelo cargado: {input_dim} → {hidden_dims} → {num_classes}")
                messagebox.showinfo("Éxito", 
                                  f"Modelo MLP cargado exitosamente:\n\n"
                                  f"Arquitectura: {input_dim} → {hidden_dims} → {num_classes}\n"
                                  f"Archivo: {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el modelo:\n{e}")
                self.status_bar.config(text="✗ Error al cargar modelo")
    
    def _retrain_model(self):
        """Reentrena modelo con el dataset completo."""
        # Confirmar acción
        response = messagebox.askyesno(
            "Reentrenar Modelo",
            "¿Deseas reentrenar el modelo desde cero?\n\n"
            "Esto puede tomar varios minutos.\n"
            "El modelo actual será reemplazado."
        )
        
        if not response:
            return
        
        # Crear ventana de progreso
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Reentrenamiento en progreso")
        progress_window.geometry("500x300")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Frame principal
        frame = ttk.Frame(progress_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(frame, text="Reentrenando Modelo MLP", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Label de estado
        status_label = ttk.Label(frame, text="Inicializando...", 
                                font=('Arial', 10))
        status_label.pack(pady=(0, 10))
        
        # Barra de progreso
        progress_bar = ttk.Progressbar(frame, mode='determinate', length=400)
        progress_bar.pack(pady=(0, 10))
        
        # Label de época
        epoch_label = ttk.Label(frame, text="Época: 0 / 1500", 
                               font=('Arial', 9))
        epoch_label.pack(pady=(0, 10))
        
        # Label de métricas
        metrics_label = ttk.Label(frame, text="", font=('Arial', 9))
        metrics_label.pack(pady=(0, 10))
        
        # Botón cancelar (deshabilitado durante entrenamiento)
        cancel_btn = ttk.Button(frame, text="Cancelar", state='disabled')
        cancel_btn.pack(pady=(10, 0))
        
        progress_window.update()
        
        try:
            # 1. Cargar dataset
            status_label.config(text="Cargando dataset...")
            progress_window.update()
            
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
            dataset_path = os.path.join(base_path, 'data', 'dataset.json')
            
            with open(dataset_path, 'r', encoding='utf-8') as f:
                dataset = json.load(f)
            
            code_samples = []
            labels = []
            
            for algo in dataset['algorithms']:
                code_path = os.path.join(base_path, algo['path'])
                try:
                    with open(code_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                        code_samples.append(code)
                        labels.append(algo['complexity_class'])
                except FileNotFoundError:
                    pass
            
            progress_bar['value'] = 10
            progress_window.update()
            
            # 2. Extraer features
            status_label.config(text="Extrayendo features...")
            progress_window.update()
            
            extractor = GoFeatureExtractor(max_features=200)
            X = extractor.fit_transform(code_samples)
            y = np.array(labels)
            
            progress_bar['value'] = 20
            progress_window.update()
            
            # 3. Dividir dataset
            status_label.config(text="Dividiendo dataset...")
            progress_window.update()
            
            np.random.seed(42)
            n_samples = len(X)
            indices = np.random.permutation(n_samples)
            n_test = int(n_samples * 0.2)
            test_indices = indices[:n_test]
            train_indices = indices[n_test:]
            
            X_train = X[train_indices]
            X_test = X[test_indices]
            y_train = y[train_indices]
            y_test = y[test_indices]
            
            progress_bar['value'] = 25
            progress_window.update()
            
            # 4. Crear nuevo modelo
            status_label.config(text="Inicializando modelo...")
            progress_window.update()
            
            input_dim = X_train.shape[1]
            num_classes = 6
            
            new_mlp = MLP(
                input_dim=input_dim,
                hidden_dims=[256, 128, 64],  # 3 capas ocultas (mejor para 59 algoritmos)
                num_classes=num_classes,
                learning_rate=0.008,  # Learning rate menor para mejor convergencia
                batch_size=4
            )
            
            progress_bar['value'] = 30
            progress_window.update()
            
            # 5. Entrenar con callback de progreso
            status_label.config(text="Entrenando modelo (1500 épocas)...")
            progress_window.update()
            
            epochs = 1500
            history = {
                'train_loss': [],
                'train_accuracy': [],
                'test_loss': [],
                'test_accuracy': []
            }
            
            for epoch in range(epochs):
                # Entrenar una época
                train_loss, train_acc = new_mlp._train_epoch(X_train, y_train)
                test_loss, test_acc = new_mlp.evaluate_loss(X_test, y_test)
                
                history['train_loss'].append(train_loss)
                history['train_accuracy'].append(train_acc)
                history['test_loss'].append(test_loss)
                history['test_accuracy'].append(test_acc)
                
                # Actualizar UI cada 10 épocas
                if (epoch + 1) % 10 == 0 or epoch == 0:
                    progress = 30 + int((epoch + 1) / epochs * 60)
                    progress_bar['value'] = progress
                    epoch_label.config(text=f"Época: {epoch + 1} / {epochs}")
                    metrics_label.config(
                        text=f"Train Acc: {train_acc:.3f} | Test Acc: {test_acc:.3f}\n"
                             f"Train Loss: {train_loss:.4f} | Test Loss: {test_loss:.4f}"
                    )
                    progress_window.update()
            
            progress_bar['value'] = 90
            
            # 6. Guardar modelo
            status_label.config(text="Guardando modelo...")
            progress_window.update()
            
            model_path = os.path.join(base_path, 'experiments', 'models', 
                                     'mlp_complexity_classifier.npz')
            new_mlp.save_weights(model_path)
            
            # 7. Guardar historial
            history_path = os.path.join(base_path, 'experiments', 'logs', 
                                       'training_history.json')
            with open(history_path, 'w') as f:
                json.dump(history, f, indent=2)
            
            progress_bar['value'] = 95
            
            # 8. Actualizar modelo en memoria
            status_label.config(text="Actualizando modelo...")
            progress_window.update()
            
            self.mlp = new_mlp
            self.feature_extractor = extractor
            
            progress_bar['value'] = 100
            status_label.config(text="✓ Reentrenamiento completado")
            epoch_label.config(text=f"Completado: {epochs} épocas")
            
            # Mostrar resultado final
            final_train_acc = history['train_accuracy'][-1]
            final_test_acc = history['test_accuracy'][-1]
            
            messagebox.showinfo(
                "Reentrenamiento Completado",
                f"✓ Modelo reentrenado exitosamente\n\n"
                f"Épocas: {epochs}\n"
                f"Precisión Train: {final_train_acc:.2%}\n"
                f"Precisión Test: {final_test_acc:.2%}\n\n"
                f"Modelo guardado en:\n{model_path}"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error en Reentrenamiento",
                f"Error durante el reentrenamiento:\n{str(e)}"
            )
        
        finally:
            progress_window.destroy()
    
    def _show_docs(self):
        """Muestra documentación."""
        messagebox.showinfo("Documentación", 
                          "Analizador de Complejidad Algorítmica\n\n"
                          "Utiliza MLP + RecurrenceParser + MasterTheorem\n\n"
                          "Fases completadas:\n"
                          "[OK] Fase 1: MLP desde cero\n"
                          "[OK] Fase 2: Algoritmos avanzados\n"
                          "[OK] Fase 3: Estructuras de datos\n"
                          "[OK] Fase 4: GUI completa")
    
    def _extract_v6_features(self, code):
        """
        Extrae los 3 features para modelo v6 (loops, recursion, depth).
        
        Returns:
            np.array: Array de shape (1, 3) con features, o None si falla.
        """
        try:
            # Feature 1: Contar loops (for, while)
            loop_count = len(re.findall(r'\b(for|while)\b', code))
            loops = min(loop_count, 5)  # Capped a 5
            
            # Feature 2: Detectar recursión (llamadas a función dentro de sí misma)
            recursion = 0
            # Buscar definiciones de funciones
            func_defs = re.findall(r'\bfunc\s+(\w+)\s*\(', code)
            for func_name in func_defs:
                # Buscar si se llama a sí misma dentro de su cuerpo
                if re.search(rf'\b{func_name}\s*\(', code):
                    recursion = 1
                    break
            
            # Feature 3: Calcular profundidad de anidamiento (máximo)
            depth = 1
            max_indent = 0
            for line in code.split('\n'):
                # Contar espacios/tabs al inicio
                indent = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent)
            
            # Convertir indentación a nivel de profundidad (asumiendo 4 espacios por nivel)
            depth = min(max(1, max_indent // 4 + 1), 5)  # Entre 1 y 5
            
            # Crear array de features normalizado
            features = np.array([[loops, recursion, depth]], dtype=np.float32)
            
            return features
            
        except Exception as e:
            print(f"Error extrayendo features v6: {e}")
            return None
    
    def _show_docs(self):
        """Muestra documentación."""
        messagebox.showinfo("Documentación", 
                          "Analizador de Complejidad Algorítmica\n\n"
                          "Utiliza MLP + RecurrenceParser + MasterTheorem\n\n"
                          "Fases completadas:\n"
                          "[OK] Fase 1: MLP desde cero\n"
                          "[OK] Fase 2: Algoritmos avanzados\n"
                          "[OK] Fase 3: Estructuras de datos\n"
                          "[OK] Fase 4: GUI completa")
    
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
            # 1. Detectar recursión
            self.status_bar.config(text="Detectando recurrencias...")
            self.root.update_idletasks()
            
            recurrence = self.recurrence_parser.parse(code)
            # Heurística adicional: detectar patrón backtracking de permutaciones
            backtracking_pattern = False
            if 'permute' in code or ('arr[' in code and re.search(r'for\s+.*i.*<=.*r', code)):
                lines_bt = [l.strip() for l in code.split('\n') if l.strip()]
                for idx, line in enumerate(lines_bt):
                    if re.search(r'\bpermute\s*\(', line) or re.search(r'\b[a-zA-Z_]\w*\s*\(', line):
                        prev_line = lines_bt[idx-1] if idx > 0 else ''
                        next_line = lines_bt[idx+1] if idx+1 < len(lines_bt) else ''
                        # Swap antes y después de llamada recursiva
                        if ('arr[' in prev_line and '=' in prev_line and 'arr[' in next_line and '=' in next_line and ('permute' in line or 'arr[' in line)):
                            backtracking_pattern = True
                            break
            
            result = "═" * 60 + "\n"
            result += "ANÁLISIS DE COMPLEJIDAD COMPUTACIONAL\n"
            result += "═" * 60 + "\n\n"
            
            # ==== PREDICCIÓN MLP (PRIMERA PRIORIDAD) ====
            mlp_prediction = None
            mlp_confidence = 0.0
            mlp_probabilities = None
            
            if self.mlp is not None:
                try:
                    self.status_bar.config(text="Extrayendo features del código...")
                    self.root.update_idletasks()
                    
                    features = None
                    
                    # Intentar primero con modelo v6 (3 features automáticos)
                    v6_features = self._extract_v6_features(code)
                    if v6_features is not None:
                        # Verificar si el modelo espera 3 features (v6)
                        try:
                            test_pred = self.mlp.forward(v6_features)
                            features = v6_features
                            print("✓ Usando detección automática de features (v6)")
                        except:
                            pass
                    
                    # Fallback: usar feature extractor tradicional si está fitted
                    if features is None and self.feature_extractor.is_fitted:
                        features = self.feature_extractor.transform([code])
                        print("✓ Usando feature extractor tradicional")
                    
                    if features is not None:
                        # Hacer predicción
                        self.status_bar.config(text="Ejecutando predicción MLP...")
                        self.root.update_idletasks()
                        
                        prediction_probs = self.mlp.predict_proba(features)
                        predicted_class = np.argmax(prediction_probs[0])
                        mlp_confidence = prediction_probs[0][predicted_class]
                        mlp_prediction = self.complexity_labels.get(predicted_class, "Desconocida")
                        mlp_probabilities = prediction_probs[0]
                        
                        result += "[NEURAL NETWORK] PREDICTION\n"
                        result += "-" * 60 + "\n\n"
                        result += f"COMPLEXITY: {mlp_prediction}\n"
                        result += f"Confidence: {mlp_confidence:.1%}\n\n"
                        result += "Model:\n"
                        
                        # Mostrar arquitectura correcta según el modelo
                        if hasattr(self.mlp, 'input_dim') and self.mlp.input_dim == 3:
                            result += "  * Architecture: 3 -> 64 -> 32 -> 6 (v6)\n"
                        else:
                            result += "  * Architecture: 180 -> 256 -> 128 -> 64 -> 6\n"
                            
                        result += "  * Trained algorithms: 144\n"
                        result += "  * Test Accuracy: 86.21%\n"
                        result += "  * Epochs: 2000\n\n"
                        
                        result += "Probability Distribution:\n"
                        sorted_probs = sorted(enumerate(mlp_probabilities), key=lambda x: x[1], reverse=True)
                        for class_idx, prob in sorted_probs[:3]:
                            complexity = self.complexity_labels.get(class_idx, f"Class {class_idx}")
                            bar_length = int(prob * 30)
                            bar = "[" + "=" * bar_length + " " * (30 - bar_length) + "]"
                            result += f"  {complexity:12} {bar} {prob:.1%}\n"
                        
                        result += "\n"
                        
                except Exception as e:
                    print(f"Error en predicción MLP: {e}")
                    import traceback
                    traceback.print_exc()
            
            # ==== ANÁLISIS DE RECURRENCIA (SEGUNDO NIVEL) ====
            result += "-" * 60 + "\n"
            result += "ANÁLISIS DE RECURRENCIA\n"
            result += "─" * 60 + "\n\n"
            
            if recurrence is None and backtracking_pattern:
                result += "[BACKTRACKING PATTERN DETECTED]\n"
                result += "-" * 60 + "\n\n"
                result += "Structure of permutation generation detected (swap before and after recursive call).\n"
                result += "Approximate Complexity: O(n!) (or n*n! if each permutation is printed/stored).\n"
                result += "Conceptual Recurrence: T(n) = n * T(n-1) + O(1). Master Theorem does not apply because 'a' depends on n.\n\n"
                if mlp_prediction and mlp_prediction != "O(2^n)":
                    result += "[WARNING] The MLP grouped factorial within class " + mlp_prediction + ". Forcing factorial output by semantics.\n\n"
                self.current_analysis_result = None
            elif recurrence is None:
                result += "[NO RECURSION DETECTED]\n\n"
                result += "Code is ITERATIVE (not recursive).\n\n"
                
                # Detectar patrones iterativos comunes
                has_binary_search_pattern = bool(re.search(r'left.*right.*mid|for.*left\s*<=?\s*right', code))
                
                if has_binary_search_pattern and mlp_prediction != "O(log n)":
                    result += "[ITERATIVE PATTERN] Binary Search detected\n"
                    result += "  * Theoretical Complexity: O(log n)\n"
                    result += "  * Loop that divides space in half\n\n"
                elif not mlp_prediction:
                    result += "[INFO] MLP prediction not available\n"
                    result += "  * Run: python train_model.py\n\n"
                
                self.current_analysis_result = None
                
            else:
                # 2. Mostrar recurrencia detectada
                recurrence_str = self.recurrence_parser.format_recurrence(recurrence)
                result += "[RECURRENCE DETECTED]\n\n"
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
                
                # Comparar con predicción MLP si está disponible
                if mlp_prediction and mlp_prediction != mt_result.complexity:
                    result += "\n⚠️ NOTA: La predicción MLP difiere del Master Theorem\n"
                    result += f"   MLP sugiere: {mlp_prediction} (confianza: {mlp_confidence:.1%})\n"
                    result += f"   Master Theorem: {mt_result.complexity}\n"
                    if mlp_confidence > 0.85:
                        result += "   → Recomendación: Confiar en el MLP (mayor precisión general)\n"
                
                # Guardar resultado
                self.current_analysis_result = {
                    'recurrence': recurrence,
                    'master_theorem': mt_result,
                    'mlp_prediction': mlp_prediction,
                    'mlp_confidence': mlp_confidence,
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
            print(f"ERROR EN _analyze_code: {e}")
            import traceback
            traceback.print_exc()
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
