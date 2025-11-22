# 🎓 Sistema de Análisis de Complejidad Computacional

**Proyecto Final - Análisis y Diseño de Algoritmos (ADA)**

Un sistema completo para **clasificar, analizar y predecir la complejidad computacional** de algoritmos usando técnicas de análisis formal y aprendizaje automático.

---

## 🎯 Objetivo

Construir un sistema funcional que demuestre la intersección entre:
- **Redes neuronales** implementadas desde cero (sin Keras/PyTorch/TensorFlow)
- **Análisis algorítmico riguroso** (Big-O, recurrencias, Método Maestro)
- **Estructuras de datos eficientes** (heaps, BST, hash maps)

---

## 📁 Estructura del Proyecto

```
proyectofinalADA/
├── README.md                      # Este archivo
├── requirements.txt               # Dependencias
├── train_model.py                 # Script principal de entrenamiento
├── proyecto.py                    # Entry point (futuro)
│
├── data/                          # Dataset de algoritmos Go
│   ├── algorithms/
│   │   ├── search/               # Algoritmos de búsqueda
│   │   ├── sort/                 # Algoritmos de ordenamiento
│   │   └── graph/                # Algoritmos de grafos
│   ├── dataset.json              # Metadatos del dataset
│   └── complexity_labels.json    # Definición de clases
│
├── src/                          # Código fuente modular
│   ├── neural_network/           # MLP desde cero
│   │   ├── mlp.py               # Arquitectura completa
│   │   ├── layers.py            # Capas densas y activaciones
│   │   ├── losses.py            # Cross-entropy
│   │   ├── optimizers.py        # SGD, mini-batch SGD
│   │   └── initializers.py      # Xavier, He
│   │
│   ├── data_processing/          # Extracción de features
│   │   └── feature_extractor.py # TF-IDF + contadores sintácticos
│   │
│   ├── algorithms/               # Módulos algorítmicos (Fase 2)
│   ├── data_structures/          # Estructuras eficientes (Fase 3)
│   ├── baselines/                # Modelos de comparación (Fase 4)
│   └── visualization/            # GUI (Fase 4)
│
├── tests/                        # Pruebas unitarias
│   └── test_mlp.py              # Tests del MLP
│
├── experiments/                  # Resultados
│   ├── models/                  # Pesos entrenados (.npz)
│   ├── logs/                    # Métricas de entrenamiento
│   └── figures/                 # Gráficas generadas
│
└── notebooks/                    # Documentación ejecutable (futuro)
```

---

## 🚀 Instalación y Configuración

### 1. Requisitos

- **Python 3.8+**
- **Git** (para clonar el repositorio)

### 2. Clonar el Repositorio

```bash
git clone https://github.com/yeisonpabon/proyectofinalADA.git
cd proyectofinalADA
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Dependencias principales:**
- `numpy`: Álgebra lineal para MLP
- `matplotlib`: Visualización de resultados
- `seaborn`: Gráficas estadísticas

---

## 📊 Dataset

El sistema incluye **10 algoritmos Go** representativos de diferentes complejidades:

| Algoritmo | Complejidad | Clase | Tipo |
|-----------|-------------|-------|------|
| Acceso a Array | O(1) | 0 | Constante |
| Búsqueda Binaria | O(log n) | 1 | Logarítmico |
| Búsqueda Lineal | O(n) | 2 | Lineal |
| DFS/BFS | O(n) | 2 | Lineal |
| Merge Sort | O(n log n) | 3 | Linearítmico |
| Quick Sort | O(n log n) | 3 | Linearítmico |
| Bubble Sort | O(n²) | 4 | Cuadrático |
| Selection Sort | O(n²) | 4 | Cuadrático |
| Fibonacci Recursivo | O(2^n) | 5 | Exponencial |

### Features Extraídas

**1. TF-IDF (Term Frequency - Inverse Document Frequency)**
- Tokens de palabras clave Go (`func`, `for`, `if`, `return`, etc.)
- Top 200 tokens más discriminativos

**2. Features Sintácticas**
- Número de loops (`for`)
- Profundidad de anidamiento
- Presencia de recursión
- Uso de estructuras de datos (`map`, `slice`)
- Número de condiciones (`if`, `else`)
- Número de líneas de código

---

## 🧠 Arquitectura del MLP

### Configuración

```
Input (56 features)
    ↓
Dense Layer 1: 56 → 128 (ReLU)
    ↓
Dense Layer 2: 128 → 64 (ReLU)
    ↓
Dense Layer 3: 64 → 6 (Softmax)
    ↓
Output (6 clases de complejidad)
```

**Parámetros totales:** 15,942

### Detalles de Implementación

- **Inicialización:** He (optimizada para ReLU)
- **Función de pérdida:** Cross-Entropy
- **Optimizador:** Mini-Batch SGD (batch_size=4)
- **Learning rate:** 0.01
- **Épocas:** 500 (mínimo requerido)

---

## 🎓 Ejecución

### 1. Ejecutar Pruebas Unitarias

```bash
python tests/test_mlp.py
```

**Tests incluidos:**
- ✅ Inicializadores (Xavier, He)
- ✅ Funciones de activación (ReLU, Softmax)
- ✅ Capa densa (forward/backward pass)
- ✅ Función de pérdida (Cross-Entropy)
- ✅ MLP completo (forward pass)
- ✅ Entrenamiento
- ✅ Verificación numérica de gradientes
- ✅ Guardado y carga de modelo

### 2. Entrenar el Modelo

```bash
python train_model.py
```

**Proceso de entrenamiento:**
1. Carga dataset de 10 algoritmos Go
2. Extrae features (TF-IDF + sintácticas)
3. Divide en train (80%) y test (20%)
4. Entrena MLP por 500 épocas
5. Evalúa y guarda resultados
6. Genera gráficas de pérdida/precisión

**Salida esperada:**
```
Iniciando entrenamiento:
  - Muestras: 8
  - Batch size: 4
  - Batches por época: 2
  - Épocas: 500
  - Learning rate: 0.01
  - Arquitectura: 56 → 128 → 64 → 6

Época 500/500 - Loss: 0.2125 - Acc: 1.0000 - Val Loss: 5.2614 - Val Acc: 0.5000

✓ Precisión final (train): 1.0000
✓ Precisión final (test): 0.5000
```

### 3. Resultados Generados

Después del entrenamiento, se crean:

**Modelo entrenado:**
```
experiments/models/mlp_complexity_classifier.npz
```

**Historial de entrenamiento:**
```
experiments/logs/training_history.json
```

**Gráficas:**
```
experiments/figures/training_history.png
```

---

## 📈 Análisis de Complejidad

### Complejidad Temporal del Sistema

#### 1. Extracción de Features
- **Tokenización:** O(L) donde L = longitud del código
- **TF-IDF:** O(N·M) donde N = documentos, M = vocabulario
- **Features sintácticas:** O(L)
- **Total:** O(N·L·M)

#### 2. Forward Pass (MLP)
Para un batch de tamaño B:
- **Capa 1:** O(B · 56 · 128) = O(7,168B)
- **Capa 2:** O(B · 128 · 64) = O(8,192B)
- **Capa 3:** O(B · 64 · 6) = O(384B)
- **Total:** O(B · 15,744)

#### 3. Backward Pass
- **Misma complejidad que forward:** O(B · 15,744)

#### 4. Entrenamiento Completo
Para E épocas con N ejemplos:
- **Épocas:** O(E · (N/B) · P)
- donde P = número de parámetros (15,942)
- **Con E=500, N=8, B=4:** O(500 · 2 · 15,942) = O(15,942,000)

### Complejidad Espacial
- **Parámetros del modelo:** O(15,942)
- **Activaciones (batch):** O(B · 128) = O(512)
- **Gradientes:** O(15,942)
- **Total:** O(15,942)

---

## 🔬 Derivaciones Matemáticas

### 1. Backpropagation

Para una capa densa:

**Forward:**
```
z = W·x + b
a = σ(z)
```

**Backward (regla de la cadena):**
```
dL/dW = x^T · dZ
dL/db = sum(dZ)
dL/dx = dZ · W^T

donde: dZ = dA · σ'(z)
```

### 2. Cross-Entropy + Softmax

**Simplificación especial:**

Para softmax + cross-entropy, la derivada combinada es elegante:

```
∂L/∂z = softmax(z) - y_true
```

**Derivación:**
```
L = -Σ y_true · log(softmax(z))

∂L/∂z_i = softmax(z_i) - y_true_i
```

### 3. Método Maestro (Ejemplos del Dataset)

#### Merge Sort
```
T(n) = 2T(n/2) + Θ(n)

a = 2, b = 2, f(n) = Θ(n)
n^(log_b(a)) = n^(log_2(2)) = n

Como f(n) = Θ(n^(log_b(a))):
→ Caso 2 del Método Maestro
→ T(n) = Θ(n log n)
```

#### Búsqueda Binaria
```
T(n) = T(n/2) + Θ(1)

a = 1, b = 2, f(n) = Θ(1)
n^(log_b(a)) = n^0 = 1

Como f(n) = Θ(n^(log_b(a))):
→ Caso 2 del Método Maestro
→ T(n) = Θ(log n)
```

---

## 📝 Próximas Fases

### Fase 2: Módulos Algorítmicos
- [ ] Implementar Quickselect
- [ ] Top-k con heap vs sort
- [ ] Análisis de recurrencias
- [ ] Hard mining con estructuras

### Fase 3: Estructuras de Datos
- [ ] Min-heap para ejemplos difíciles
- [ ] Batch queue eficiente
- [ ] Loss tracker con hash map

### Fase 4: Baseline y Evaluación
- [ ] Implementar k-NN classifier
- [ ] Clasificador basado en reglas
- [ ] Comparación experimental
- [ ] GUI interactiva (Tkinter)

---

## 🧪 Testing

El proyecto incluye una suite completa de pruebas unitarias:

```bash
python tests/test_mlp.py
```

**Cobertura de tests:**
- Inicializadores de pesos (Xavier, He)
- Funciones de activación (ReLU, Softmax)
- Capas densas (forward/backward)
- Función de pérdida (Cross-Entropy)
- Optimizadores (SGD, Mini-Batch SGD)
- MLP completo
- Verificación numérica de gradientes
- Guardado y carga de modelos

---

## 📚 Referencias

### Papers y Teoría
- Rumelhart et al. (1986) - "Learning representations by back-propagating errors"
- Glorot & Bengio (2010) - "Understanding the difficulty of training deep feedforward neural networks"
- He et al. (2015) - "Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet"

### Análisis de Algoritmos
- Cormen et al. - "Introduction to Algorithms" (CLRS)
- Método Maestro para recurrencias

---

## 👥 Autor

**Proyecto Final - Análisis y Diseño de Algoritmos**
- Repositorio: [github.com/yeisonpabon/proyectofinalADA](https://github.com/yeisonpabon/proyectofinalADA)

---

## 📄 Licencia

Este proyecto es de carácter académico y educativo.

---

## 🤝 Contribuciones

Este es un proyecto académico. Para sugerencias o mejoras, por favor abrir un issue en el repositorio.

---

## ⚠️ Notas Importantes

1. **Dataset pequeño:** El modelo actual usa solo 10 algoritmos. Para producción, se recomienda expandir a 100+ ejemplos.

2. **Overfitting:** Con precisión 100% en train y 50% en test, hay overfitting. Soluciones:
   - Aumentar dataset
   - Agregar dropout
   - Regularización L2

3. **Prohibiciones respetadas:** No se usaron frameworks de deep learning (Keras, PyTorch, TensorFlow). Solo NumPy para álgebra lineal.

---

**¡Sistema funcional y listo para demostración académica!** ✅
