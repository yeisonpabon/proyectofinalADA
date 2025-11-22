"""
Training Visualizer - Visualizador de Métricas de Entrenamiento

Muestra gráficos de loss, accuracy, y confusion matrix del entrenamiento del MLP.
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
import os


class TrainingVisualizer:
    """Visualizador de métricas de entrenamiento."""
    
    def __init__(self, parent_frame):
        """
        Inicializa visualizador.
        
        Args:
            parent_frame: Frame padre
        """
        self.parent = parent_frame
        self.history = None
        
        self._load_training_history()
        self._create_ui()
    
    def _load_training_history(self):
        """Carga historial de entrenamiento."""
        try:
            # Buscar en la ubicación correcta
            history_path = os.path.join(os.path.dirname(__file__), 
                                       '../../experiments/logs/training_history.json')
            
            if os.path.exists(history_path):
                with open(history_path, 'r') as f:
                    self.history = json.load(f)
                print(f"✓ Historial de entrenamiento cargado: {len(self.history.get('train_loss', []))} épocas")
            else:
                print(f"⚠ No se encontró historial en: {history_path}")
                print("  Usando datos de ejemplo para demostración")
                self.history = self._generate_dummy_history()
        except Exception as e:
            print(f"⚠ Error cargando historial: {e}")
            self.history = self._generate_dummy_history()
    
    def _generate_dummy_history(self):
        """Genera historial dummy para demostración."""
        epochs = 50
        train_loss = 3.0 * np.exp(-np.linspace(0, 3, epochs)) + 0.1 * np.random.rand(epochs)
        test_loss = 3.2 * np.exp(-np.linspace(0, 2.8, epochs)) + 0.15 * np.random.rand(epochs)
        train_acc = 1 - 0.9 * np.exp(-np.linspace(0, 3, epochs)) - 0.05 * np.random.rand(epochs)
        test_acc = 1 - 0.92 * np.exp(-np.linspace(0, 2.7, epochs)) - 0.07 * np.random.rand(epochs)
        
        return {
            'train_loss': train_loss.tolist(),
            'val_loss': test_loss.tolist(),
            'train_accuracy': train_acc.tolist(),
            'val_accuracy': test_acc.tolist(),
            'epochs': epochs
        }
    
    def _create_ui(self):
        """Crea interfaz."""
        # Título
        title = ttk.Label(self.parent, text="Métricas de Entrenamiento", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Frame de métricas
        metrics_frame = ttk.LabelFrame(self.parent, text="Resumen", padding=10)
        metrics_frame.pack(fill=tk.X, padx=10, pady=5)
        
        if self.history:
            epochs = len(self.history.get('train_loss', []))
            final_train_acc = self.history['train_accuracy'][-1] if self.history.get('train_accuracy') else 0
            final_test_acc = self.history['val_accuracy'][-1] if self.history.get('val_accuracy') else 0
            final_train_loss = self.history['train_loss'][-1] if self.history.get('train_loss') else 0
            final_test_loss = self.history['val_loss'][-1] if self.history.get('val_loss') else 0
            
            info_text = f"""
Épocas entrenadas: {epochs}
Train Accuracy: {final_train_acc:.2%}
Test Accuracy: {final_test_acc:.2%}
Train Loss: {final_train_loss:.4f}
Test Loss: {final_test_loss:.4f}
            """
            ttk.Label(metrics_frame, text=info_text, font=("Consolas", 10)).pack()
        
        # Notebook para gráficos
        notebook = ttk.Notebook(self.parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Loss
        loss_frame = ttk.Frame(notebook)
        notebook.add(loss_frame, text="📉 Loss")
        self._create_loss_plot(loss_frame)
        
        # Tab 2: Accuracy
        acc_frame = ttk.Frame(notebook)
        notebook.add(acc_frame, text="📈 Accuracy")
        self._create_accuracy_plot(acc_frame)
        
        # Tab 3: Confusion Matrix (placeholder)
        conf_frame = ttk.Frame(notebook)
        notebook.add(conf_frame, text="🔢 Confusion Matrix")
        self._create_confusion_matrix(conf_frame)
    
    def _create_loss_plot(self, parent):
        """Crea gráfico de pérdida."""
        figure = Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        
        if self.history and self.history['train_loss']:
            epochs = range(1, len(self.history['train_loss']) + 1)
            
            ax.plot(epochs, self.history['train_loss'], 'b-', label='Train Loss', linewidth=2)
            ax.plot(epochs, self.history['val_loss'], 'r--', label='Val Loss', linewidth=2)
            
            ax.set_xlabel('Época', fontsize=12)
            ax.set_ylabel('Pérdida', fontsize=12)
            ax.set_title('Evolución de la Pérdida Durante el Entrenamiento', fontsize=13, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'No hay datos de entrenamiento disponibles', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
        
        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _create_accuracy_plot(self, parent):
        """Crea gráfico de precisión."""
        figure = Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        
        if self.history and self.history['train_accuracy']:
            epochs = range(1, len(self.history['train_accuracy']) + 1)
            
            ax.plot(epochs, [a * 100 for a in self.history['train_accuracy']], 
                   'g-', label='Train Accuracy', linewidth=2)
            ax.plot(epochs, [a * 100 for a in self.history['val_accuracy']], 
                   'm--', label='Val Accuracy', linewidth=2)
            
            ax.set_xlabel('Época', fontsize=12)
            ax.set_ylabel('Precisión (%)', fontsize=12)
            ax.set_title('Evolución de la Precisión Durante el Entrenamiento', fontsize=13, fontweight='bold')
            ax.set_ylim([0, 105])
            ax.legend()
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'No hay datos de entrenamiento disponibles', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
        
        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _create_confusion_matrix(self, parent):
        """Crea matriz de confusión."""
        # Matriz de confusión dummy
        cm = np.array([
            [15, 1, 0, 0, 0, 0],
            [2, 18, 1, 0, 0, 0],
            [0, 1, 14, 2, 0, 0],
            [0, 0, 1, 19, 1, 0],
            [0, 0, 0, 2, 16, 2],
            [0, 0, 0, 0, 1, 3]
        ])
        
        labels = ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)', 'O(n²)', 'O(2^n)']
        
        figure = Figure(figsize=(7, 6), dpi=100)
        ax = figure.add_subplot(111)
        
        im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        ax.figure.colorbar(im, ax=ax)
        
        ax.set(xticks=np.arange(cm.shape[1]),
              yticks=np.arange(cm.shape[0]),
              xticklabels=labels, yticklabels=labels,
              ylabel='Clase Real',
              xlabel='Clase Predicha',
              title='Matriz de Confusión (Ejemplo)')
        
        # Rotar labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Agregar valores
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], 'd'),
                       ha="center", va="center",
                       color="white" if cm[i, j] > thresh else "black")
        
        figure.tight_layout()
        
        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


if __name__ == '__main__':
    # Demo standalone
    root = tk.Tk()
    root.title("Training Visualizer Demo")
    root.geometry("900x700")
    
    visualizer = TrainingVisualizer(root)
    
    root.mainloop()
