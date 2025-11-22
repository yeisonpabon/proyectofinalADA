"""
Extractor de features para código Go.

Convierte código fuente Go en vectores numéricos usando:
1. TF-IDF (Term Frequency - Inverse Document Frequency)
2. Bag-of-Words
3. Contadores sintácticos (loops, recursión, estructuras)

Complejidad:
- TF-IDF: O(N*M) donde N=documentos, M=vocabulario
- Contadores: O(L) donde L=líneas de código
"""

import re
import numpy as np
from collections import Counter, defaultdict
import math


class GoFeatureExtractor:
    """
    Extractor de features para clasificación de complejidad de código Go.
    
    Features extraídas:
    1. TF-IDF de tokens (palabras clave, identificadores)
    2. Bag-of-Words de patrones sintácticos
    3. Contadores de estructuras:
       - Loops (for, while)
       - Recursión (llamadas a sí mismo)
       - Profundidad de anidamiento
       - Estructuras de datos (map, slice, array)
    """
    
    def __init__(self, max_features=300):
        """
        Inicializa el extractor.
        
        Args:
            max_features (int): Número máximo de features TF-IDF
        """
        self.max_features = max_features
        self.vocabulary = {}  # Mapeo token -> índice
        self.idf = {}  # IDF por token
        self.feature_names = []  # Nombres de todas las features
        self.is_fitted = False
    
    def _tokenize_go(self, code):
        """
        Tokeniza código Go.
        
        Extrae:
        - Palabras clave Go (func, for, if, return, etc.)
        - Identificadores
        - Operadores
        
        Complejidad: O(L) donde L = longitud del código
        
        Args:
            code (str): Código Go
            
        Returns:
            list: Lista de tokens
        """
        # Eliminar comentarios
        code = re.sub(r'//.*?\n', ' ', code)
        code = re.sub(r'/\*.*?\*/', ' ', code, flags=re.DOTALL)
        
        # Palabras clave Go importantes
        go_keywords = {
            'func', 'for', 'if', 'else', 'return', 'package', 'import',
            'var', 'const', 'type', 'struct', 'interface', 'map', 'slice',
            'range', 'break', 'continue', 'switch', 'case', 'default',
            'go', 'defer', 'select', 'chan', 'make', 'new', 'append'
        }
        
        # Tokenizar
        # Patrón: palabra completa o símbolo
        # Incluir también operador de módulo '%' en la tokenización
        tokens = re.findall(r'\b\w+\b|[<>=!+\-*/%]', code.lower())
        
        # Filtrar tokens relevantes
        filtered_tokens = []
        for token in tokens:
            # Mantener keywords
            if token in go_keywords:
                filtered_tokens.append(token)
            # Mantener identificadores significativos (no números)
            elif token.isalpha() and len(token) > 1:
                filtered_tokens.append(token)
        
        return filtered_tokens
    
    def _extract_syntactic_features(self, code):
        """
        Extrae features sintácticas del código Go.
        
        Features:
        1. Número de loops (for)
        2. Profundidad máxima de anidamiento
        3. Presencia de recursión (detectada por nombre de función)
        4. Número de llamadas a funciones
        5. Uso de estructuras de datos (map, slice, array)
        6. Número de condiciones (if, else)
        
        Complejidad: O(L) donde L = líneas de código
        
        Args:
            code (str): Código Go
            
        Returns:
            dict: Diccionario de features sintácticas
        """
        features = {}
        
        # Contar loops
        features['num_for_loops'] = len(re.findall(r'\bfor\b', code))
        
        # Contar condiciones
        features['num_if'] = len(re.findall(r'\bif\b', code))
        features['num_else'] = len(re.findall(r'\belse\b', code))
        
        # Detectar recursión (heurística: función se llama a sí misma)
        func_names = re.findall(r'func\s+(\w+)\s*\(', code)
        features['has_recursion'] = 0
        if func_names:
            func_name = func_names[0]  # Primera función
            # Buscar llamadas a la misma función
            pattern = rf'\b{func_name}\s*\('
            calls = re.findall(pattern, code)
            features['has_recursion'] = 1 if len(calls) > 1 else 0
        
        # Profundidad de anidamiento (contar llaves)
        max_depth = 0
        current_depth = 0
        for char in code:
            if char == '{':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char == '}':
                current_depth -= 1
        features['max_nesting_depth'] = max_depth
        
        # Estructuras de datos
        features['uses_map'] = 1 if re.search(r'\bmap\s*\[', code) else 0
        features['uses_slice'] = 1 if re.search(r'\[\]', code) else 0
        features['uses_make'] = 1 if re.search(r'\bmake\s*\(', code) else 0
        features['uses_append'] = 1 if re.search(r'\bappend\s*\(', code) else 0
        
        # Número de returns (puede indicar casos base en recursión)
        features['num_returns'] = len(re.findall(r'\breturn\b', code))
        
        # Número de líneas de código (sin contar vacías)
        lines = [l.strip() for l in code.split('\n') if l.strip()]
        features['num_lines'] = len(lines)
        
        # ===== NUEVAS FEATURES PARA DETECTAR O(log n) =====
        
        # 1. Patrón de división binaria (mid, /2, left+right)
        features['has_binary_division'] = 0
        binary_patterns = [
            r'mid\s*:?=\s*\(?left\s*\+\s*right\)?.*?[/]',  # mid = (left+right)/2
            r'mid\s*:?=\s*left\s*\+\s*\(.*?right.*?left.*?\)\s*/\s*2',  # mid = left + (right-left)/2
            r'/\s*2(?!\*)',  # división por 2 (no seguida de *)
            r'>>\s*1',  # bit shift (equivalente a /2)
        ]
        for pattern in binary_patterns:
            if re.search(pattern, code):
                features['has_binary_division'] = 1
                break
        
        # 2. Actualización de left/right (búsqueda binaria)
        features['has_binary_search_update'] = 0
        if re.search(r'left\s*=\s*mid', code) and re.search(r'right\s*=\s*mid', code):
            features['has_binary_search_update'] = 1
        
        # 3. Patrón logarítmico: loop que divide el rango
        features['has_logarithmic_loop'] = 0
        # Detectar: while/for con condición left <= right y división de rango
        if re.search(r'for\s+.*?left\s*<=?\s*right', code) and features['has_binary_division']:
            features['has_logarithmic_loop'] = 1
        
        # 4. Recursión con división del problema (T(n/2), T(n/3))
        features['has_divide_conquer_recursion'] = 0
        if features['has_recursion'] and features['has_binary_division']:
            features['has_divide_conquer_recursion'] = 1
        
        # 5. Patrón de búsqueda: comparaciones con mid
        features['has_mid_comparison'] = 0
        if re.search(r'arr\s*\[.*?mid.*?\]', code) or re.search(r'matrix\s*\[.*?mid.*?\]', code):
            features['has_mid_comparison'] = 1
        
        # 6. Variables típicas de búsqueda binaria (left, right, mid)
        features['has_binary_search_vars'] = 0
        has_left = bool(re.search(r'\bleft\b', code))
        has_right = bool(re.search(r'\bright\b', code))
        has_mid = bool(re.search(r'\bmid\b', code))
        if has_left and has_right and has_mid:
            features['has_binary_search_vars'] = 1
        
        # 7. Patrón de búsqueda exponencial (duplicación: *2, <<1)
        features['has_exponential_search'] = 0
        if re.search(r'\*\s*2(?!\.)|\<\<\s*1', code):  # *2 o <<1
            features['has_exponential_search'] = 1
        
        # 8. Ratio de profundidad vs líneas (bajo = posible log)
        if features['num_lines'] > 0:
            features['depth_to_lines_ratio'] = features['max_nesting_depth'] / features['num_lines']
        else:
            features['depth_to_lines_ratio'] = 0

        # === NUEVAS FEATURES PARA PATRONES LOGARÍTMICOS NO BINARIOS (Euclides, conteo dígitos, etc.) ===

        # 9. Uso de operador módulo dentro de un loop (típico en gcd, fast power, conversión base)
        features['has_modulo_in_loop'] = 0
        if re.search(r'for\s+.*?{[\s\S]*?%[\s\S]*?}', code):
            features['has_modulo_in_loop'] = 1

        # 10. Patrón de reducción (a, b = b, a % b) o asignaciones similares con módulo encadenado
        features['has_gcd_swap_pattern'] = 0
        gcd_patterns = [
            r'\b[a-zA-Z_]\w*\s*,\s*[a-zA-Z_]\w*\s*=\s*[a-zA-Z_]\w*\s*,\s*[a-zA-Z_]\w*\s*%\s*[a-zA-Z_]\w*',
            r'\b[a-zA-Z_]\w*\s*=\s*[a-zA-Z_]\w*\s*%\s*[a-zA-Z_]\w*'
        ]
        for pattern in gcd_patterns:
            if re.search(pattern, code):
                features['has_gcd_swap_pattern'] = 1
                break

        # 11. Loop con condición basada en variable que se reduce por división/módulo (b != 0, n > 0)
        features['has_loop_variable_reduction'] = 0
        # Detectar variable control que aparece en condición del for y luego se reasigna con / o %
        loop_conditions = re.findall(r'for\s+([^\{]*){', code)
        for cond in loop_conditions:
            # Extraer posibles variables en condición
            vars_in_cond = re.findall(r'\b([a-zA-Z_]\w*)\b', cond)
            for var in vars_in_cond:
                # Buscar reasignaciones de la variable con / o % dentro del cuerpo
                pattern_div = rf'{var}\s*=\s*{var}\s*/\s*\d+'
                pattern_mod = rf'{var}\s*=\s*{var}\s*%\s*\d+'
                if re.search(pattern_div, code) or re.search(pattern_mod, code):
                    features['has_loop_variable_reduction'] = 1
                    break
            if features['has_loop_variable_reduction']:
                break

        # 12. Conteo de divisiones por base 10 (n /= 10, n = n/10) para detectar log base distinto
        features['has_division_by_10_loop'] = 0
        if re.search(r'for\s+.*?{[\s\S]*?(?:/\s*10)', code):
            features['has_division_by_10_loop'] = 1

        # 13. Conversión repetida mediante division y módulo (decimal a binario/base)
        features['has_division_mod_conversion'] = 0
        if features['has_modulo_in_loop'] and (features['has_binary_division'] or features['has_division_by_10_loop']):
            features['has_division_mod_conversion'] = 1

        # 14. Señal compuesta de posible log: cualquier patrón de reducción + loop
        reduction_signals = [
            features['has_binary_division'],
            features['has_modulo_in_loop'],
            features['has_loop_variable_reduction'],
            features['has_division_by_10_loop'],
            features['has_gcd_swap_pattern']
        ]
        features['has_any_log_reduction_pattern'] = 1 if any(reduction_signals) else 0
        
        return features
    
    def _compute_tf(self, tokens):
        """
        Calcula Term Frequency.
        
        TF(t, d) = (Número de veces que t aparece en d) / (Total de términos en d)
        
        Complejidad: O(n) donde n = número de tokens
        
        Args:
            tokens (list): Lista de tokens
            
        Returns:
            dict: TF por token
        """
        tf = Counter(tokens)
        total = len(tokens)
        return {token: count / total for token, count in tf.items()}
    
    def _compute_idf(self, documents_tokens):
        """
        Calcula Inverse Document Frequency.
        
        IDF(t) = log(N / df(t))
        
        donde:
        - N = número total de documentos
        - df(t) = número de documentos que contienen t
        
        Complejidad: O(N*M) donde N=docs, M=vocabulario promedio
        
        Args:
            documents_tokens (list): Lista de listas de tokens
            
        Returns:
            dict: IDF por token
        """
        N = len(documents_tokens)
        df = defaultdict(int)
        
        # Contar en cuántos documentos aparece cada token
        for tokens in documents_tokens:
            unique_tokens = set(tokens)
            for token in unique_tokens:
                df[token] += 1
        
        # Calcular IDF
        idf = {}
        for token, count in df.items():
            idf[token] = math.log(N / count)
        
        return idf
    
    def fit(self, code_samples):
        """
        Ajusta el extractor a un conjunto de código.
        
        Construye:
        1. Vocabulario (top max_features tokens)
        2. IDF para cada token
        
        Complejidad: O(N*L*M) donde N=muestras, L=longitud, M=vocabulario
        
        Args:
            code_samples (list): Lista de strings de código Go
        """
        print(f"Ajustando extractor de features con {len(code_samples)} muestras...")
        
        # Tokenizar todos los documentos
        all_tokens = []
        for code in code_samples:
            tokens = self._tokenize_go(code)
            all_tokens.append(tokens)
        
        # Calcular IDF
        self.idf = self._compute_idf(all_tokens)
        
        # Construir vocabulario (top max_features por IDF)
        # Tokens con IDF alto son más discriminativos
        sorted_tokens = sorted(self.idf.items(), key=lambda x: x[1], reverse=True)
        top_tokens = sorted_tokens[:self.max_features]
        
        self.vocabulary = {token: idx for idx, (token, _) in enumerate(top_tokens)}
        
        # Nombres de features
        self.feature_names = list(self.vocabulary.keys())
        
        # Añadir nombres de features sintácticas
        syntactic_features = self._extract_syntactic_features(code_samples[0])
        self.feature_names.extend(syntactic_features.keys())
        
        self.is_fitted = True
        
        print(f"[OK] Vocabulario: {len(self.vocabulary)} tokens")
        print(f"✓ Total features: {len(self.feature_names)}")
        print(f"✓ Top 10 tokens: {list(self.vocabulary.keys())[:10]}")
    
    def transform(self, code_samples):
        """
        Transforma código Go en vectores de features.
        
        Vector final:
        [TF-IDF features] + [Syntactic features]
        
        Complejidad: O(N*L*V) donde N=muestras, L=longitud, V=vocabulario
        
        Args:
            code_samples (list): Lista de strings de código Go
            
        Returns:
            np.ndarray: Matriz (N, D) donde D = número de features
        """
        if not self.is_fitted:
            raise ValueError("Extractor no ajustado. Llamar fit() primero.")
        
        features_matrix = []
        
        for code in code_samples:
            # 1. TF-IDF features
            tokens = self._tokenize_go(code)
            tf = self._compute_tf(tokens)
            
            # Calcular TF-IDF para vocabulario conocido
            tfidf_vector = np.zeros(len(self.vocabulary))
            for token, idx in self.vocabulary.items():
                if token in tf:
                    tfidf_vector[idx] = tf[token] * self.idf.get(token, 0)
            
            # 2. Syntactic features
            syntactic = self._extract_syntactic_features(code)
            syntactic_vector = np.array([syntactic[key] for key in syntactic.keys()])
            
            # Concatenar
            full_vector = np.concatenate([tfidf_vector, syntactic_vector])
            features_matrix.append(full_vector)
        
        return np.array(features_matrix)
    
    def fit_transform(self, code_samples):
        """
        Ajusta y transforma en un solo paso.
        
        Args:
            code_samples (list): Lista de strings de código Go
            
        Returns:
            np.ndarray: Matriz de features
        """
        self.fit(code_samples)
        return self.transform(code_samples)
    
    def get_feature_importance(self, feature_vector):
        """
        Retorna las features más importantes para un vector dado.
        
        Args:
            feature_vector (np.ndarray): Vector de features
            
        Returns:
            list: Lista de tuplas (nombre_feature, valor) ordenadas
        """
        if len(feature_vector) != len(self.feature_names):
            raise ValueError(f"Vector de features tiene longitud incorrecta")
        
        importance = [(name, val) for name, val in zip(self.feature_names, feature_vector)]
        importance.sort(key=lambda x: abs(x[1]), reverse=True)
        
        return importance[:10]  # Top 10
