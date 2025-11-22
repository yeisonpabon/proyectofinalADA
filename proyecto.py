"""
Sistema de Clasificación de Complejidad Computacional
Proyecto Final - Análisis y Diseño de Algoritmos

Punto de entrada principal del sistema.

Funcionalidades:
1. Entrenar modelo MLP desde cero
2. Ejecutar demo de clasificación
3. Ejecutar tests unitarios
4. Ver estadísticas del modelo

Uso:
    python proyecto.py --train          # Entrenar modelo (500 épocas)
    python proyecto.py --demo           # Demo interactiva
    python proyecto.py --test           # Ejecutar tests
    python proyecto.py --stats          # Estadísticas del modelo
    python proyecto.py --help           # Ayuda
"""

import sys
import os
import argparse


def print_banner():
    """Imprime el banner del proyecto."""
    banner = """
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   SISTEMA DE CLASIFICACIÓN DE COMPLEJIDAD COMPUTACIONAL           ║
║                                                                    ║
║   Proyecto Final - Análisis y Diseño de Algoritmos               ║
║                                                                    ║
║   Características:                                                 ║
║   • MLP implementado desde cero (sin frameworks)                   ║
║   • Clasificación de 6 clases de complejidad                       ║
║   • Dataset de 10 algoritmos Go                                    ║
║   • Entrenamiento de 500+ épocas                                   ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def train_model():
    """Ejecuta el entrenamiento del modelo."""
    print("\n🎯 Iniciando entrenamiento del modelo...\n")
    os.system(f"{sys.executable} train_model.py")


def run_demo():
    """Ejecuta la demostración interactiva."""
    print("\n🎮 Iniciando demostración interactiva...\n")
    os.system(f"{sys.executable} demo.py")

def run_gui():
    """Inicia la interfaz gráfica completa (GUI)."""
    print("\n🖥️ Abriendo interfaz gráfica (GUI)...\n")
    # Llamamos directamente al módulo de la ventana principal
    gui_path = os.path.join('src', 'gui', 'main_window.py')
    if not os.path.exists(gui_path):
        print("⚠️ Archivo de GUI no encontrado en:", gui_path)
        return
    exit_code = os.system(f"{sys.executable} {gui_path}")
    if exit_code != 0:
        print("⚠️ La GUI terminó con código", exit_code)


def run_tests():
    """Ejecuta los tests unitarios."""
    print("\n🧪 Ejecutando suite de tests unitarios...\n")
    os.system(f"{sys.executable} tests/test_mlp.py")


def show_stats():
    """Muestra estadísticas del modelo."""
    import json
    
    print("\n📊 ESTADÍSTICAS DEL MODELO")
    print("=" * 70)
    
    # Verificar si el modelo existe
    # V6 (220) es el MODELO ÓPTIMO con 75.86% accuracy
    model_path = "experiments/models/mlp_complexity_classifier_220.npz"
    if not os.path.exists(model_path):
        print("⚠️  Modelo v6 no encontrado. Ejecuta: python add_and_train_220.py")
        return
    
    # Cargar historial v6
    history_path = "experiments/logs/training_history_220.json"
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            history = json.load(f)
        
        print(f"\n✓ Modelo v6 (ÓPTIMO) encontrado")
        print(f"✓ Épocas completadas: {len(history['train_loss'])}")
        print(f"✓ Algoritmos: 144 (balanceados)")
        print(f"\nMétricas finales:")
        print(f"  • Train Loss:     {history['train_loss'][-1]:.4f}")
        print(f"  • Train Accuracy: {history['train_accuracy'][-1]:.4f} ({history['train_accuracy'][-1]*100:.2f}%)")
        print(f"  • Test Loss:      {history['val_loss'][-1]:.4f}")
        print(f"  • Test Accuracy:  {history['val_accuracy'][-1]:.4f} ({history['val_accuracy'][-1]*100:.2f}%)")
        
        # Mejores épocas
        best_train_epoch = history['train_accuracy'].index(max(history['train_accuracy'])) + 1
        best_test_epoch = history['val_accuracy'].index(max(history['val_accuracy'])) + 1
        
        print(f"\nMejores resultados:")
        print(f"  • Mejor train accuracy: Época {best_train_epoch} ({max(history['train_accuracy'])*100:.2f}%)")
        print(f"  • Mejor test accuracy:  Época {best_test_epoch} ({max(history['val_accuracy'])*100:.2f}%)")
    else:
        print("⚠️  Historial de entrenamiento no encontrado")
    
    print("\n" + "=" * 70 + "\n")


def show_help():
    """Muestra la ayuda del sistema."""
    help_text = """
COMANDOS DISPONIBLES:
--------------------

python proyecto.py --train
    Entrena el modelo MLP desde cero por 500 épocas.
    Genera: modelo entrenado, historial JSON, gráficas.
    Duración: ~30 segundos

python proyecto.py --demo
    Ejecuta una demostración interactiva del sistema.
    Carga el modelo entrenado y clasifica un nuevo algoritmo.

python proyecto.py --test
    Ejecuta la suite completa de tests unitarios.
    Verifica: forward pass, backprop, gradientes, etc.

python proyecto.py --stats
    Muestra estadísticas del modelo entrenado.
    Incluye: épocas, pérdidas, precisiones.

python proyecto.py --help
    Muestra esta ayuda.


ARCHIVOS GENERADOS (V6 ÓPTIMO):
------------------------------

experiments/models/mlp_complexity_classifier_220.npz  - Modelo v6 (75.86%)
experiments/logs/training_history_220.json            - Historial v6
experiments/figures/training_history.png          - Gráficas de entrenamiento


ESTRUCTURA DEL PROYECTO:
-----------------------

src/neural_network/    - MLP implementado desde cero
src/data_processing/   - Extractor de features (TF-IDF)
data/algorithms/       - Dataset de 10 algoritmos Go
tests/                 - Suite de tests unitarios
experiments/           - Modelos y resultados


DOCUMENTACIÓN:
-------------

README.md              - Guía completa del proyecto
FASE1_COMPLETADA.md    - Resumen de implementación
RESUMEN_PROYECTO.txt   - Estado actual del proyecto


SOPORTE:
--------

Repositorio: https://github.com/yeisonpabon/proyectofinalADA
Documentación completa en README.md
"""
    print(help_text)


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="Sistema de Clasificación de Complejidad Computacional",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--train', action='store_true', 
                       help='Entrenar modelo MLP (500 épocas)')
    parser.add_argument('--demo', action='store_true',
                       help='Ejecutar demostración interactiva')
    parser.add_argument('--test', action='store_true',
                       help='Ejecutar tests unitarios')
    parser.add_argument('--stats', action='store_true',
                       help='Mostrar estadísticas del modelo')
    parser.add_argument('--gui', action='store_true',
                       help='Abrir interfaz gráfica (GUI)')
    
    args = parser.parse_args()
    
    # Si no se pasa ningún argumento, mostrar ayuda
    if len(sys.argv) == 1:
        print_banner()
        show_help()
        return
    
    print_banner()
    
    # Ejecutar comando correspondiente
    if args.train:
        train_model()
    elif args.demo:
        run_demo()
    elif args.gui:
        run_gui()
    elif args.test:
        run_tests()
    elif args.stats:
        show_stats()
    else:
        show_help()


if __name__ == "__main__":
    main()
