# Entrenamiento Avanzado del Modelo MLP - 200 Algoritmos

## Estado del Entrenamiento

**Inicio:** Noviembre 21, 2025

### Configuración

```
Epocas:         5000 (incremento de 2.5x respecto a 2000)
Dataset:        200 algoritmos (incremento de 3x respecto a 74)
Batch Size:     16
Learning Rate:  0.005
Arquitectura:   225 -> 256 -> 128 -> 64 -> 6
```

### Dataset Expandido

| Clase | Complejidad | Algoritmos |
|-------|-------------|-----------|
| 0 | O(1) | ~30 |
| 1 | O(log n) | ~30 |
| 2 | O(n) | ~50 |
| 3 | O(n log n) | ~40 |
| 4 | O(n²) | ~40 |
| 5 | O(2^n) | ~10 |

**Total:** 200 algoritmos sintéticos

### Algoritmos Base

Cada algoritmo base tiene múltiples variantes:
- Acceso Directo (const_access)
- Búsqueda Binaria (binary_search)
- Búsqueda Lineal (linear_search)
- Merge Sort (merge_sort)
- Bubble Sort (bubble_sort)
- Fibonacci Recursivo (fibonacci_recursive)
- Y muchos más...

### Proceso de Entrenamiento

1. **Generación de Dataset** (Completado)
   - 200 algoritmos sintéticos generados
   - Código Go válido para cada variante
   - Almacenado en `data/algorithms/generated/`

2. **Extracción de Features** (En Progreso)
   - TF-IDF: 200 tokens
   - Features sintácticas: 25
   - Total: 225 features por algoritmo

3. **Entrenamiento MLP** (Pendiente)
   - 5000 épocas (estimado: 2-4 horas dependiendo del hardware)
   - Mini-batch SGD
   - Validación en test set (20%)

### Modelos Generados

- `experiments/models/mlp_complexity_classifier_200algo.npz`
- `experiments/logs/training_history_5000.json`

### Esperado

- Precisión mejorada gracias a más datos
- Mejor generalización
- Reducción de overfitting
- Cobertura más balanceada en todas las clases

### Monitoreo

Puedes revisar el progreso con:
```bash
Get-Content training_output.log -Tail 20
```

### Beneficios de este Entrenamiento

✅ Dataset 3x más grande (200 vs 74)
✅ Variantes sintéticas de cada algoritmo
✅ 2.5x más épocas para convergencia
✅ Mejor distribución de clases
✅ Mayor capacidad de generalización

---

**Nota:** El entrenamiento está en background. Este proceso es computacionalmente intensivo y puede tomar várias horas.
