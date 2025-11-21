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
        tokens = re.findall(r'\b\w+\b|[<>=!+\-*/]', code.lower())
        
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
        
        print(f"✓ Vocabulario: {len(self.vocabulary)} tokens")
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
