"""
Sistema Integrado de Análisis de Complejidad - Fase 2

Combina:
    1. Parser automático de recurrencias
    2. Master Theorem para clasificación
    3. MLP para predicción empírica
    4. Comparación de resultados

Uso:
    python analyze_complexity.py <archivo.go>
"""

import os
import sys
import argparse
from pathlib import Path

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.complexity_analysis.recurrence_parser import RecurrenceParser
from src.complexity_analysis.master_theorem import MasterTheorem
from src.data_processing.feature_extractor import GoFeatureExtractor
from src.neural_network.mlp import MLP


class ComplexityAnalyzer:
    """
    Analizador integrado de complejidad algorítmica.
    
    Combina análisis teórico (Master Theorem) con predicción empírica (MLP).
    """
    
    def __init__(self, mlp_model_path: str):
        """
        Inicializa el analizador.
        
        Args:
            mlp_model_path: Ruta al modelo MLP entrenado
        """
        self.parser = RecurrenceParser()
        self.master_theorem = MasterTheorem()
        self.extractor = GoFeatureExtractor()
        
        # Cargar modelo MLP
        self.mlp = MLP(
            input_dim=118,  # Ajustar según features
            hidden_dims=[128, 64],
            num_classes=6,
            learning_rate=0.01,
            batch_size=4
        )
        
        if os.path.exists(mlp_model_path):
            self.mlp.load_weights(mlp_model_path)
            print(f"✓ Modelo MLP cargado desde: {mlp_model_path}")
        else:
            print(f"⚠ Advertencia: No se encontró modelo en {mlp_model_path}")
        
        # Mapeo de clases
        self.complexity_map = {
            0: "O(1)",
            1: "O(log n)",
            2: "O(n)",
            3: "O(n log n)",
            4: "O(n²)",
            5: "O(2^n)"
        }
    
    def analyze_file(self, filepath: str) -> dict:
        """
        Analiza un archivo Go completo.
        
        Args:
            filepath: Ruta al archivo .go
        
        Returns:
            Diccionario con resultados del análisis
        """
        print("=" * 70)
        print(f"ANÁLISIS DE COMPLEJIDAD: {os.path.basename(filepath)}")
        print("=" * 70)
        print()
        
        # Leer código
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 1. Análisis de recurrencia
        print("1. ANÁLISIS DE RECURRENCIA")
        print("-" * 70)
        recurrence = self.parser.parse(code)
        
        if recurrence is None:
            print("No se detectó recursión")
            recurrence_result = None
        else:
            recurrence_str = self.parser.format_recurrence(recurrence)
            print(f"Recurrencia: {recurrence_str}")
            print(f"  a (subproblemas): {recurrence.a}")
            print(f"  b (división): {recurrence.b} ({recurrence.division_pattern})")
            print(f"  f(n): {recurrence.f_n}")
            print(f"  Confianza: {recurrence.confidence:.1%}")
            recurrence_result = recurrence
        
        print()
        
        # 2. Master Theorem
        print("2. MASTER THEOREM")
        print("-" * 70)
        
        if recurrence_result is not None:
            mt_result = self.master_theorem.solve(
                recurrence.a,
                recurrence.b,
                recurrence.f_n
            )
            
            print(f"Caso: {mt_result.case.name}")
            print(f"c = log_{recurrence.b}({recurrence.a}) = {mt_result.c_value:.3f}")
            print(f"Complejidad teórica: {mt_result.complexity}")
            print(f"Confianza: {mt_result.confidence:.1%}")
            print()
            print("Explicación:")
            print(mt_result.explanation)
        else:
            print("No se puede aplicar Master Theorem (sin recursión detectada)")
            mt_result = None
        
        print()
        
        # 3. Predicción MLP
        print("3. PREDICCIÓN CON MLP")
        print("-" * 70)
        
        try:
            # Extraer features (necesita ajustar extractor primero)
            # Por ahora, hacer predicción directa si tenemos modelo
            print("⚠ Predicción MLP requiere extractor entrenado")
            mlp_result = None
        except Exception as e:
            print(f"Error en predicción MLP: {e}")
            mlp_result = None
        
        print()
        
        # 4. Resumen comparativo
        print("4. RESUMEN COMPARATIVO")
        print("-" * 70)
        
        results = {
            'file': filepath,
            'recurrence': recurrence_result,
            'master_theorem': mt_result,
            'mlp_prediction': mlp_result
        }
        
        if mt_result:
            print(f"Complejidad (Master Theorem): {mt_result.complexity}")
        
        if mlp_result:
            print(f"Complejidad (MLP): {mlp_result}")
        
        print()
        print("=" * 70)
        
        return results
    
    def analyze_dataset(self, dataset_dir: str):
        """
        Analiza todos los algoritmos en el dataset.
        
        Args:
            dataset_dir: Directorio con algoritmos Go
        """
        print("=" * 70)
        print("ANÁLISIS MASIVO DEL DATASET")
        print("=" * 70)
        print()
        
        # Buscar archivos .go
        go_files = list(Path(dataset_dir).rglob("*.go"))
        
        print(f"Encontrados {len(go_files)} archivos .go")
        print()
        
        results = []
        
        for filepath in go_files:
            result = self.analyze_file(str(filepath))
            results.append(result)
            print()
        
        # Resumen estadístico
        print("=" * 70)
        print("ESTADÍSTICAS GENERALES")
        print("=" * 70)
        
        with_recurrence = sum(1 for r in results if r['recurrence'] is not None)
        print(f"Algoritmos con recursión detectada: {with_recurrence}/{len(results)}")
        
        if with_recurrence > 0:
            master_applicable = sum(
                1 for r in results 
                if r['master_theorem'] and r['master_theorem'].case.value != 0
            )
            print(f"Master Theorem aplicable: {master_applicable}/{with_recurrence}")
        
        print()


def main():
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(
        description="Análisis integrado de complejidad algorítmica (Fase 2)"
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='Archivo Go a analizar (opcional, usa dataset si no se especifica)'
    )
    
    parser.add_argument(
        '--model',
        default='experiments/models/mlp_complexity_classifier.npz',
        help='Ruta al modelo MLP entrenado'
    )
    
    parser.add_argument(
        '--dataset',
        default='data/algorithms',
        help='Directorio con dataset de algoritmos'
    )
    
    args = parser.parse_args()
    
    # Inicializar analizador
    base_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_path, args.model)
    
    analyzer = ComplexityAnalyzer(model_path)
    
    if args.file:
        # Analizar archivo único
        analyzer.analyze_file(args.file)
    else:
        # Analizar dataset completo
        dataset_path = os.path.join(base_path, args.dataset)
        analyzer.analyze_dataset(dataset_path)


if __name__ == '__main__':
    main()
