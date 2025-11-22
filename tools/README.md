# 🔧 Tools - Herramientas Auxiliares

Scripts de diagnóstico, análisis y validación. **Opcionales** para desarrollo y debugging.

## 📊 Análisis de Precisión

```bash
python tools/precision_por_complejidad.py
```

Calcula y muestra la precisión del modelo por cada clase de complejidad.

**Salida**: 
- Precisión total
- Breakdown por clase (O(1), O(log n), O(n), etc.)
- Matriz de confusión

---

## 🔍 Diagnóstico del Modelo

```bash
python tools/test_model_loading.py
```

Valida que el modelo MLP carga correctamente y puede hacer predicciones.

**Verifica**:
- ✅ Carga del modelo desde `experiments/models/`
- ✅ Extracción de features
- ✅ Predicciones correctas
- ✅ Dimensiones de entrada/salida

**Útil para**: Debugging si el GUI no funciona correctamente.

---

## 📝 Notas

Estos scripts son para **desarrollo y mantenimiento** interno. No son necesarios para usar el sistema en producción.
