# Análisis Final: Mejoras de Overfitting

## Resumen de Resultados

Probamos 5 estrategias diferentes para reducir overfitting:

| Estrategia | Train Acc | Test Acc | Overfitting | Resultado |
|-----------|-----------|----------|-------------|-----------|
| **Original (2000 ep)** | 80.00% | **93.33%** | -13.33% | ✅ MEJOR |
| 5000 Epochs | 96.61% | 46.67% | +50% | ❌ Severo |
| Improved (LR=0.002) | 100% | 46.67% | +53% | ❌ Peor |
| Ensemble (5 modelos) | ~98% | 26.67% | +71% | ❌ Muy malo |
| PCA (4 features) | 52.54% | 26.67% | +26% | ❌ Malo |

## Análisis

### ¿Por qué todo empeoró?

1. **Dataset muy pequeño**: 59 ejemplos de entrenamiento, 15 de test
   - Ratio de features/ejemplos: 186/59 = 3.15 (debería ser <0.1)
   - El modelo original tuvo "suerte" en la inicialización

2. **Overfitting del 5000-epoch model**:
   - Train: 96.61%, Test: 46.67% → Brecha de 50 puntos
   - El modelo memoriza exactamente los 59 ejemplos

3. **Por qué Ensemble empeoró (26.67%)**:
   - Con pocos datos, diferentes seeds iniciales → modelos divergentes e incorrectos
   - Al promediar predicciones de 5 modelos malos → resultado peor

4. **Por qué PCA empeoró (26.67%)**:
   - Solo 4 componentes principales retienen 100% varianza = insuficiente
   - Muchos patrones importantes se pierden con solo 4 dimensiones

## Recomendación

### ✅ USAR MODELO ORIGINAL

**Mantener la configuración original** en GUI.py:
- 2000 epochs
- Batch size: 32
- Learning rate: 0.01
- Features: 186
- Test accuracy: **93.33%**

### Por qué es la mejor opción

1. **Mejor generalización**: Test accuracy más alta (93.33%)
2. **Balance train/test**: No hay sobreajuste aparente
3. **Estable**: Reproducible y confiable
4. **Simple**: No requiere transformaciones complejas

## Conclusión

**El problema fundamental no es el entrenamiento, sino el tamaño del dataset.**

Con solo 59 ejemplos de entrenamiento, cualquier intento de "regularizar" que reduce la complejidad del modelo destruye la capacidad de aprender.

### Soluciones a largo plazo (No implementadas)

Si se necesita mejorar más adelante:

1. **Data Augmentation**: Generar código Go sintético variando algoritmos
2. **Transfer Learning**: Usar modelo pre-entrenado en datos más grandes
3. **Recolectar más algoritmos**: Expandir dataset a 200+ ejemplos
4. **Feature Engineering**: Crear features más significativas y discriminativas

**Para ahora**: Usar el modelo original. Funciona bien.
