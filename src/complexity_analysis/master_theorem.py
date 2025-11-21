"""
Master Theorem - Clasificador Automático de Complejidad

Implementa el Master Theorem para resolver relaciones de recurrencia
de la forma T(n) = aT(n/b) + f(n).

Teorema Maestro (3 Casos):
    Sea T(n) = aT(n/b) + f(n) donde a ≥ 1, b > 1, f(n) asintóticamente positiva.
    
    Definir: c = log_b(a)
    
    Caso 1: Si f(n) = O(n^(c-ε)) para ε > 0
        => T(n) = Θ(n^c)
    
    Caso 2: Si f(n) = Θ(n^c)
        => T(n) = Θ(n^c * log n)
    
    Caso 3: Si f(n) = Ω(n^(c+ε)) para ε > 0 y a*f(n/b) ≤ k*f(n) para k < 1
        => T(n) = Θ(f(n))

Referencias:
    - Cormen et al. (2009). "Introduction to Algorithms", Chapter 4.5
    - Leighton, F. T. (1996). "Notes on Better Master Theorems for Divide-and-Conquer Recurrences"
"""

import math
import re
from typing import Optional, Tuple, Dict
from dataclasses import dataclass
from enum import Enum


class MasterTheoremCase(Enum):
    """Casos del Master Theorem."""
    CASE_1 = 1  # f(n) más pequeña => T(n) = Θ(n^c)
    CASE_2 = 2  # f(n) igual => T(n) = Θ(n^c log n)
    CASE_3 = 3  # f(n) más grande => T(n) = Θ(f(n))
    NOT_APPLICABLE = 0  # No aplica Master Theorem


@dataclass
class MasterTheoremResult:
    """
    Resultado del análisis con Master Theorem.
    
    Atributos:
        case: Caso aplicado (1, 2, 3, o 0 si no aplica)
        complexity: Complejidad resultante (ej: "O(n log n)")
        explanation: Explicación detallada del análisis
        c_value: Valor de c = log_b(a)
        comparison: Comparación entre f(n) y n^c
        confidence: Confianza en el resultado (0.0 - 1.0)
    """
    case: MasterTheoremCase
    complexity: str
    explanation: str
    c_value: float
    comparison: str
    confidence: float


class MasterTheorem:
    """
    Clasificador automático usando el Master Theorem.
    
    Resuelve recurrencias T(n) = aT(n/b) + f(n) y determina
    la complejidad asintótica resultante.
    """
    
    def __init__(self, epsilon: float = 0.1):
        """
        Inicializa el analizador del Master Theorem.
        
        Args:
            epsilon: Umbral para comparaciones (usado en Caso 1 y 3)
        """
        self.epsilon = epsilon
    
    def solve(self, a: int, b: int, f_n: str) -> MasterTheoremResult:
        """
        Resuelve la recurrencia T(n) = aT(n/b) + f(n) usando Master Theorem.
        
        Args:
            a: Número de subproblemas
            b: Factor de división
            f_n: Complejidad del trabajo no recursivo (ej: "O(1)", "O(n)", "O(n²)")
        
        Returns:
            MasterTheoremResult con análisis completo
        
        Examples:
            >>> mt = MasterTheorem()
            >>> result = mt.solve(2, 2, "O(n)")
            >>> print(result.complexity)
            O(n log n)
            >>> print(result.case)
            MasterTheoremCase.CASE_2
        """
        # Validar parámetros
        if a < 1 or b <= 1:
            return MasterTheoremResult(
                case=MasterTheoremCase.NOT_APPLICABLE,
                complexity="No determinada",
                explanation="Master Theorem requiere a ≥ 1 y b > 1",
                c_value=0,
                comparison="",
                confidence=0.0
            )
        
        # Calcular c = log_b(a)
        c = math.log(a) / math.log(b)
        
        # Parsear f(n) para obtener su exponente
        f_exponent = self._parse_fn_exponent(f_n)
        
        # Comparar f(n) con n^c
        case, comparison = self._determine_case(f_exponent, c)
        
        # Generar resultado
        complexity = self._compute_complexity(case, c, f_n)
        explanation = self._generate_explanation(case, a, b, c, f_n, f_exponent)
        confidence = self._compute_confidence(case, a, b, f_exponent)
        
        return MasterTheoremResult(
            case=case,
            complexity=complexity,
            explanation=explanation,
            c_value=c,
            comparison=comparison,
            confidence=confidence
        )
    
    def _parse_fn_exponent(self, f_n: str) -> float:
        """
        Extrae el exponente de f(n).
        
        Soporta:
            - O(1) -> 0
            - O(log n) -> 0 (considerado menor que cualquier potencia)
            - O(n) -> 1
            - O(n²) o O(n^2) -> 2
            - O(n³) o O(n^3) -> 3
        
        Args:
            f_n: String de complejidad
        
        Returns:
            Exponente detectado
        """
        f_n_lower = f_n.lower()
        
        # O(1) -> exponente 0
        if '1' in f_n_lower or 'const' in f_n_lower:
            return 0.0
        
        # O(log n) -> -0.5 (menor que cualquier potencia positiva)
        if 'log' in f_n_lower:
            return -0.5
        
        # O(n log n) -> especial
        if 'n' in f_n_lower and 'log' in f_n_lower:
            return 1.1  # Ligeramente mayor que n
        
        # O(n^k)
        match = re.search(r'n\s*[\^]\s*(\d+)', f_n_lower)
        if match:
            return float(match.group(1))
        
        # O(n²), O(n³), etc.
        if '²' in f_n or 'n2' in f_n_lower or 'n**2' in f_n_lower:
            return 2.0
        if '³' in f_n or 'n3' in f_n_lower or 'n**3' in f_n_lower:
            return 3.0
        
        # O(n) simple
        if 'n' in f_n_lower:
            return 1.0
        
        # Por defecto
        return 0.0
    
    def _determine_case(self, f_exponent: float, c: float) -> Tuple[MasterTheoremCase, str]:
        """
        Determina cuál caso del Master Theorem aplica.
        
        Args:
            f_exponent: Exponente de f(n)
            c: Valor de log_b(a)
        
        Returns:
            Tupla (caso, comparación textual)
        """
        diff = f_exponent - c
        
        if diff < -self.epsilon:
            # f(n) = O(n^(c-ε))  =>  Caso 1
            comparison = f"f(n) = O(n^{f_exponent:.2f}) < O(n^{c:.2f})"
            return MasterTheoremCase.CASE_1, comparison
        
        elif abs(diff) <= self.epsilon:
            # f(n) = Θ(n^c)  =>  Caso 2
            comparison = f"f(n) = Θ(n^{c:.2f})"
            return MasterTheoremCase.CASE_2, comparison
        
        else:
            # f(n) = Ω(n^(c+ε))  =>  Caso 3
            comparison = f"f(n) = Ω(n^{f_exponent:.2f}) > Ω(n^{c:.2f})"
            return MasterTheoremCase.CASE_3, comparison
    
    def _compute_complexity(self, case: MasterTheoremCase, c: float, f_n: str) -> str:
        """
        Calcula la complejidad resultante según el caso.
        
        Args:
            case: Caso del Master Theorem
            c: Valor de log_b(a)
            f_n: Complejidad original de f(n)
        
        Returns:
            Complejidad resultante (ej: "O(n log n)")
        """
        if case == MasterTheoremCase.CASE_1:
            # T(n) = Θ(n^c)
            if abs(c - round(c)) < 0.01:
                exponent = int(round(c))
            else:
                exponent = f"{c:.2f}"
            
            if c == 0:
                return "O(1)"
            elif c == 1:
                return "O(n)"
            elif c == 2:
                return "O(n²)"
            else:
                return f"O(n^{exponent})"
        
        elif case == MasterTheoremCase.CASE_2:
            # T(n) = Θ(n^c * log n)
            if c == 0:
                return "O(log n)"
            elif c == 1:
                return "O(n log n)"
            elif c == 2:
                return "O(n² log n)"
            else:
                return f"O(n^{c:.2f} log n)"
        
        elif case == MasterTheoremCase.CASE_3:
            # T(n) = Θ(f(n))
            return f_n
        
        else:
            return "No determinada"
    
    def _generate_explanation(self, case: MasterTheoremCase, a: int, b: int, 
                             c: float, f_n: str, f_exponent: float) -> str:
        """
        Genera explicación detallada del análisis.
        
        Args:
            case: Caso aplicado
            a, b: Parámetros de la recurrencia
            c: Valor de log_b(a)
            f_n: Complejidad de f(n)
            f_exponent: Exponente de f(n)
        
        Returns:
            Explicación textual
        """
        base_explanation = (
            f"Recurrencia: T(n) = {a}T(n/{b}) + {f_n}\n"
            f"c = log_{b}({a}) = {c:.3f}\n"
        )
        
        if case == MasterTheoremCase.CASE_1:
            return (
                base_explanation +
                f"Caso 1: f(n) = O(n^{f_exponent:.2f}) < O(n^{c:.3f})\n"
                f"El trabajo recursivo domina.\n"
                f"Resultado: T(n) = Θ(n^{c:.3f})"
            )
        
        elif case == MasterTheoremCase.CASE_2:
            return (
                base_explanation +
                f"Caso 2: f(n) = Θ(n^{c:.3f})\n"
                f"Trabajo recursivo y no recursivo balanceados.\n"
                f"Resultado: T(n) = Θ(n^{c:.3f} * log n)"
            )
        
        elif case == MasterTheoremCase.CASE_3:
            return (
                base_explanation +
                f"Caso 3: f(n) = Ω(n^{f_exponent:.2f}) > Ω(n^{c:.3f})\n"
                f"El trabajo no recursivo domina.\n"
                f"Resultado: T(n) = Θ(f(n)) = {f_n}"
            )
        
        else:
            return base_explanation + "Master Theorem no aplica."
    
    def _compute_confidence(self, case: MasterTheoremCase, a: int, b: int, 
                           f_exponent: float) -> float:
        """
        Calcula confianza en el resultado.
        
        Args:
            case: Caso aplicado
            a, b: Parámetros de la recurrencia
            f_exponent: Exponente de f(n)
        
        Returns:
            Confianza (0.0 - 1.0)
        """
        confidence = 1.0
        
        # Penalizar si no se puede aplicar Master Theorem
        if case == MasterTheoremCase.NOT_APPLICABLE:
            return 0.0
        
        # Penalizar si a o b son muy grandes (menos típico)
        if a > 8 or b > 4:
            confidence *= 0.8
        
        # Penalizar si f_exponent es estimado (log n)
        if f_exponent < 0:
            confidence *= 0.7
        
        return confidence


def demo_master_theorem():
    """
    Demostración del Master Theorem con ejemplos clásicos.
    """
    print("=" * 70)
    print("MASTER THEOREM - CLASIFICADOR AUTOMÁTICO - FASE 2")
    print("=" * 70)
    print()
    
    mt = MasterTheorem()
    
    # Ejemplos clásicos
    examples = [
        ("Binary Search", 1, 2, "O(1)"),
        ("Merge Sort", 2, 2, "O(n)"),
        ("Quicksort (promedio)", 2, 2, "O(n)"),
        ("Multiplicación Strassen", 7, 2, "O(n²)"),
        ("Búsqueda en árbol binario", 2, 2, "O(1)"),
        ("Karatsuba", 3, 2, "O(n)"),
        ("Fibonacci recursivo", 2, 1, "O(1)"),  # No aplica (b=1)
    ]
    
    for name, a, b, f_n in examples:
        print(f"{name}")
        print("-" * 70)
        print(f"T(n) = {a}T(n/{b}) + {f_n}")
        
        result = mt.solve(a, b, f_n)
        
        print(f"\nCaso: {result.case.name}")
        print(f"c = log_{b}({a}) = {result.c_value:.3f}")
        print(f"Comparación: {result.comparison}")
        print(f"Complejidad: {result.complexity}")
        print(f"Confianza: {result.confidence:.1%}")
        print()
    
    print("=" * 70)
    print("RESUMEN DE LOS 3 CASOS")
    print("=" * 70)
    print()
    print("Dado T(n) = aT(n/b) + f(n), con c = log_b(a):")
    print()
    print("Caso 1: f(n) = O(n^(c-ε))")
    print("  -> Trabajo recursivo domina")
    print("  -> T(n) = Θ(n^c)")
    print()
    print("Caso 2: f(n) = Θ(n^c)")
    print("  -> Trabajo balanceado")
    print("  -> T(n) = Θ(n^c * log n)")
    print()
    print("Caso 3: f(n) = Ω(n^(c+ε))")
    print("  -> Trabajo no recursivo domina")
    print("  -> T(n) = Θ(f(n))")
    print()


if __name__ == '__main__':
    demo_master_theorem()
