"""
Analizador Automático de Recurrencias

Detecta y clasifica relaciones de recurrencia en código Go.
Identifica patrones como T(n) = aT(n/b) + f(n) mediante análisis del AST.

Características:
    - Parser de código Go para detectar recursión
    - Conteo de llamadas recursivas (parámetro 'a')
    - Detección de división del problema (parámetro 'b')
    - Identificación de trabajo no recursivo f(n)
    - Clasificación de complejidad de f(n) por loops

Referencias:
    - Cormen et al. (2009). "Introduction to Algorithms", Chapter 4
    - Sedgewick & Wayne (2011). "Algorithms", 4th Edition
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class RecurrenceRelation:
    """
    Representa una relación de recurrencia T(n) = a*T(n/b) + f(n).
    
    Atributos:
        a: Número de subproblemas (llamadas recursivas)
        b: Factor de reducción del problema (n/b tamaño de cada subproblema)
        f_n: Complejidad del trabajo no recursivo (ej: "O(n)", "O(1)", "O(n^2)")
        confidence: Confianza en la detección (0.0 - 1.0)
        recursive_calls: Líneas con llamadas recursivas encontradas
        loop_depth: Profundidad máxima de loops anidados
        division_pattern: Patrón detectado (divide-by-2, divide-by-3, etc.)
    """
    a: int
    b: int
    f_n: str
    confidence: float
    recursive_calls: List[str]
    loop_depth: int
    division_pattern: str


class RecurrenceParser:
    """
    Parser automático de recurrencias en código Go.
    
    Analiza código fuente Go para detectar:
        1. Llamadas recursivas (parámetro 'a')
        2. Divisiones del problema (parámetro 'b')
        3. Trabajo no recursivo (función f(n))
    """
    
    def __init__(self):
        """Inicializa el parser de recurrencias."""
        self.debug = False
    
    def parse(self, code: str, function_name: Optional[str] = None) -> Optional[RecurrenceRelation]:
        """
        Analiza código Go y detecta relación de recurrencia.
        
        Args:
            code: Código fuente Go
            function_name: Nombre de la función a analizar (None = detectar automáticamente)
        
        Returns:
            RecurrenceRelation si se detecta, None si no hay recursión
        
        Examples:
            >>> parser = RecurrenceParser()
            >>> code = '''
            ... func binarySearch(arr []int, target int, left int, right int) int {
            ...     if left > right {
            ...         return -1
            ...     }
            ...     mid := left + (right - left) / 2
            ...     if arr[mid] == target {
            ...         return mid
            ...     } else if arr[mid] < target {
            ...         return binarySearch(arr, target, mid+1, right)
            ...     } else {
            ...         return binarySearch(arr, target, left, mid-1)
            ...     }
            ... }
            ... '''
            >>> result = parser.parse(code)
            >>> print(f"T(n) = {result.a}T(n/{result.b}) + {result.f_n}")
            T(n) = 1T(n/2) + O(1)
        """
        if function_name is None:
            function_name = self._extract_function_name(code)
        
        if function_name is None:
            return None
        
        # 1. Detectar llamadas recursivas
        recursive_calls = self._find_recursive_calls(code, function_name)
        
        # DEBUG: Imprimir lo que se encontró
        if self.debug:
            print(f"DEBUG: Función '{function_name}' - Llamadas encontradas: {len(recursive_calls)}")
            for call in recursive_calls:
                print(f"  - {call}")
        
        # VALIDACIÓN ESTRICTA: NO hay recursión si no hay llamadas recursivas REALES
        if len(recursive_calls) == 0:
            return None  # No hay recursión
        
        # 2. VALIDACIÓN ADICIONAL: Si hay loops, muy probablemente NO es recursivo
        has_loops = bool(re.search(r'\bfor\b', code))
        
        if has_loops:
            # Si tiene loops Y las "llamadas recursivas" no tienen 'return' delante,
            # probablemente sea un falso positivo
            real_recursive_calls = [call for call in recursive_calls if 'return' in call.lower()]
            
            if len(real_recursive_calls) == 0:
                # No hay llamadas recursivas reales (con return)
                return None
            
            # Actualizar con solo las llamadas reales
            recursive_calls = real_recursive_calls
        
        # Si después de validaciones no hay llamadas, retornar None
        if len(recursive_calls) == 0:
            return None
        
        # 2. Contar llamadas recursivas (parámetro 'a')
        a = len(recursive_calls)
        
        # 3. Detectar división del problema (parámetro 'b')
        b, division_pattern, confidence_b = self._detect_division(code, recursive_calls)
        
        # 4. Analizar trabajo no recursivo (función f(n))
        loop_depth = self._count_loop_depth(code)
        f_n = self._classify_fn_complexity(code, loop_depth)
        
        # 5. Calcular confianza general
        confidence = self._calculate_confidence(a, b, confidence_b, recursive_calls)
        
        return RecurrenceRelation(
            a=a,
            b=b,
            f_n=f_n,
            confidence=confidence,
            recursive_calls=recursive_calls,
            loop_depth=loop_depth,
            division_pattern=division_pattern
        )
    
    def _extract_function_name(self, code: str) -> Optional[str]:
        """
        Extrae el nombre de la primera función en el código.
        
        Args:
            code: Código Go
        
        Returns:
            Nombre de la función o None
        """
        match = re.search(r'func\s+(\w+)\s*\(', code)
        return match.group(1) if match else None
    
    def _find_recursive_calls(self, code: str, function_name: str) -> List[str]:
        """
        Encuentra todas las llamadas recursivas en el código.
        
        Args:
            code: Código Go
            function_name: Nombre de la función
        
        Returns:
            Lista de líneas con llamadas recursivas
        """
        recursive_calls = []
        
        # Buscar llamadas a la misma función
        pattern = rf'\b{function_name}\s*\('
        
        # IMPORTANTE: Solo considerar líneas que NO estén en contexto de definición
        in_function = False
        function_def_line = 0
        
        lines = code.split('\n')
        for i, line in enumerate(lines):
            # Detectar definición de la función
            if re.match(r'\s*func\s+' + function_name, line):
                in_function = True
                function_def_line = i
                continue
            
            # Solo buscar llamadas DESPUÉS de la definición
            if in_function and i > function_def_line:
                # Verificar que NO sea solo el nombre de la función en un comentario
                stripped = line.strip()
                if stripped.startswith('//'):
                    continue
                    
                if re.search(pattern, line):
                    # Verificar contexto: permitir llamada dentro de bucle aunque no tenga 'return'
                    is_real = any(keyword in line for keyword in ['return', '=', ':=', 'go '])
                    # Patrones de backtracking (swap antes/después) indican llamada real
                    # Ej: arr[l], arr[i] = arr[i], arr[l]; permute(...); arr[l], arr[i] = arr[i], arr[l]
                    backtracking_context = False
                    if i+1 < len(lines):
                        next_line = lines[i+1].strip()
                        prev_line = lines[i-1].strip() if i > 0 else ''
                        if ('arr[' in prev_line and 'arr[' in next_line and '=' in prev_line and '=' in next_line):
                            backtracking_context = True
                    # Si línea está dentro de un for y sólo contiene la llamada recursiva, aceptarla
                    loop_context = any('for' in lines[j] for j in range(max(0, i-3), i+1))
                    stripped = line.strip()
                    just_call = re.match(rf'^({function_name})\s*\(', stripped) is not None
                    if is_real or (loop_context and just_call) or backtracking_context:
                        recursive_calls.append(line.strip())
        
        return recursive_calls
    
    def _detect_division(self, code: str, recursive_calls: List[str]) -> Tuple[int, str, float]:
        """
        Detecta el factor de división del problema (parámetro 'b').
        
        Busca patrones como:
            - n/2, mid, (right-left)/2  -> b=2
            - n/3  -> b=3
            - n-1  -> b=1 (recurrencia lineal)
        
        Args:
            code: Código Go
            recursive_calls: Líneas con llamadas recursivas
        
        Returns:
            Tupla (b, patrón, confianza)
        """
        # Patrones comunes de división
        patterns = [
            (r'/\s*2\b', 2, 'divide-by-2', 0.9),
            (r'mid', 2, 'midpoint', 0.85),
            (r'\(right\s*-\s*left\)\s*/\s*2', 2, 'binary-partition', 0.9),
            (r'/\s*3\b', 3, 'divide-by-3', 0.9),
            (r'-\s*1\b', 1, 'decrement', 0.8),
            (r'\+\s*1\b', 1, 'increment', 0.7),
        ]
        
        # Buscar en todo el código
        full_code = '\n'.join(recursive_calls)
        
        for pattern, b, name, confidence in patterns:
            if re.search(pattern, full_code):
                return b, name, confidence
        
        # Por defecto: asumimos división por 2 (caso común)
        return 2, 'assumed-binary', 0.5
    
    def _count_loop_depth(self, code: str) -> int:
        """
        Cuenta la profundidad máxima de loops anidados.
        
        Args:
            code: Código Go
        
        Returns:
            Profundidad máxima de anidamiento
        """
        max_depth = 0
        current_depth = 0
        
        for line in code.split('\n'):
            # Detectar inicio de loop
            if re.search(r'\bfor\b', line):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            
            # Detectar fin de bloque (simplificado)
            if line.strip() == '}' and current_depth > 0:
                # Verificar si cierra un for
                # (simplificación: asumimos que cada } cierra un bloque)
                pass  # En un parser real usaríamos contador de llaves
        
        return max_depth
    
    def _classify_fn_complexity(self, code: str, loop_depth: int) -> str:
        """
        Clasifica la complejidad del trabajo no recursivo f(n).
        
        Heurísticas:
            - 0 loops: O(1)
            - 1 loop: O(n)
            - 2 loops anidados: O(n²)
            - 3 loops anidados: O(n³)
        
        Args:
            code: Código Go
            loop_depth: Profundidad de loops
        
        Returns:
            Complejidad estimada (ej: "O(1)", "O(n)", "O(n²)")
        """
        if loop_depth == 0:
            return "O(1)"
        elif loop_depth == 1:
            return "O(n)"
        elif loop_depth == 2:
            return "O(n²)"
        elif loop_depth == 3:
            return "O(n³)"
        else:
            return f"O(n^{loop_depth})"
    
    def _calculate_confidence(self, a: int, b: int, confidence_b: float, 
                             recursive_calls: List[str]) -> float:
        """
        Calcula confianza general en el análisis.
        
        Args:
            a: Número de llamadas recursivas
            b: Factor de división
            confidence_b: Confianza en detección de b
            recursive_calls: Llamadas recursivas encontradas
        
        Returns:
            Confianza (0.0 - 1.0)
        """
        # Factores de confianza
        confidence = confidence_b
        
        # Penalizar si hay demasiadas llamadas recursivas
        if a > 4:
            confidence *= 0.7
        
        # Penalizar si no detectamos división clara
        if b == 1:
            confidence *= 0.6
        
        return min(max(confidence, 0.0), 1.0)
    
    def format_recurrence(self, relation: RecurrenceRelation) -> str:
        """
        Formatea la relación de recurrencia como string matemático.
        
        Args:
            relation: Relación de recurrencia
        
        Returns:
            String formateado (ej: "T(n) = 2T(n/2) + O(n)")
        """
        return f"T(n) = {relation.a}T(n/{relation.b}) + {relation.f_n}"
    
    def analyze_file(self, filepath: str) -> Optional[RecurrenceRelation]:
        """
        Analiza un archivo Go completo.
        
        Args:
            filepath: Ruta al archivo .go
        
        Returns:
            RecurrenceRelation o None
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        return self.parse(code)


def demo_recurrence_parser():
    """
    Demostración del parser de recurrencias.
    """
    print("=" * 70)
    print("ANALIZADOR AUTOMÁTICO DE RECURRENCIAS - FASE 2")
    print("=" * 70)
    print()
    
    parser = RecurrenceParser()
    
    # Ejemplos de código Go
    examples = [
        ("Binary Search (Divide y Conquista)", """
func binarySearch(arr []int, target int, left int, right int) int {
    if left > right {
        return -1
    }
    mid := left + (right - left) / 2
    if arr[mid] == target {
        return mid
    } else if arr[mid] < target {
        return binarySearch(arr, target, mid+1, right)
    } else {
        return binarySearch(arr, target, left, mid-1)
    }
}
        """),
        ("Merge Sort (Divide y Conquista)", """
func mergeSort(arr []int) []int {
    if len(arr) <= 1 {
        return arr
    }
    mid := len(arr) / 2
    left := mergeSort(arr[:mid])
    right := mergeSort(arr[mid:])
    return merge(left, right)
}
        """),
        ("Fibonacci (Recursión Múltiple)", """
func fibonacci(n int) int {
    if n <= 1 {
        return n
    }
    return fibonacci(n-1) + fibonacci(n-2)
}
        """),
        ("Factorial (Recursión Lineal)", """
func factorial(n int) int {
    if n <= 1 {
        return 1
    }
    return n * factorial(n-1)
}
        """),
    ]
    
    for title, code in examples:
        print(f"{title}")
        print("-" * 70)
        
        result = parser.parse(code)
        
        if result is None:
            print("No se detectó recursión")
        else:
            print(f"Recurrencia detectada: {parser.format_recurrence(result)}")
            print(f"  a (subproblemas): {result.a}")
            print(f"  b (división): {result.b} ({result.division_pattern})")
            print(f"  f(n): {result.f_n}")
            print(f"  Confianza: {result.confidence:.2%}")
            print(f"  Llamadas recursivas: {len(result.recursive_calls)}")
        
        print()
    
    print("=" * 70)


if __name__ == '__main__':
    demo_recurrence_parser()
