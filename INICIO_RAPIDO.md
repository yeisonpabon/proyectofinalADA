# 🚀 GUÍA DE INICIO RÁPIDO

## Sistema de Clasificación de Complejidad Computacional

---

## ⚡ Inicio en 3 Pasos

### 1️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2️⃣ Verificar Instalación

```bash
python proyecto.py --test
```

✅ **Resultado esperado:** Todos los 8 tests pasan

### 3️⃣ Ver Modelo Entrenado

```bash
python proyecto.py --stats
```

---

## 🎯 Comandos Principales

### Entrenar Nuevo Modelo

```bash
python proyecto.py --train
```

**Duración:** ~30 segundos  
**Genera:** Modelo + Historial + Gráficas

### Demostración Interactiva

```bash
python proyecto.py --demo
```

**Funcionalidad:** Clasifica un nuevo algoritmo Go

### Ejecutar Tests

```bash
python proyecto.py --test
```

**Valida:** Forward pass, backprop, gradientes, etc.

### Ver Ayuda

```bash
python proyecto.py
```

o

```bash
python proyecto.py --help
```

---

## 📊 Resultados Actuales

```
✅ Modelo Entrenado: SÍ
✅ Épocas: 500
✅ Train Accuracy: 100%
✅ Test Accuracy: 50%
```

---

## 📁 Archivos Importantes

| Archivo | Descripción |
|---------|-------------|
| `README.md` | Documentación completa |
| `FASE1_COMPLETADA.md` | Resumen de implementación |
| `proyecto.py` | Punto de entrada principal |
| `train_model.py` | Script de entrenamiento |
| `demo.py` | Demostración interactiva |

---

## 🏗️ Estructura

```
proyectofinalADA/
├── src/neural_network/      # MLP desde cero
├── src/data_processing/     # Feature extraction
├── data/algorithms/         # Dataset Go (10 algoritmos)
├── tests/                   # Tests unitarios
└── experiments/             # Modelos y resultados
```

---

## 🆘 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'numpy'`

**Solución:**
```bash
pip install numpy matplotlib seaborn
```

### Error: Modelo no encontrado

**Solución:**
```bash
python proyecto.py --train
```

### Tests fallan

**Verificar instalación:**
```bash
python --version  # Debe ser 3.8+
pip list | grep numpy  # Verificar numpy instalado
```

---

## 📚 Documentación Completa

Ver `README.md` para:
- Análisis de complejidad detallado
- Derivaciones matemáticas
- Arquitectura del MLP
- Features extraídas
- Método Maestro aplicado

---

## ✅ Checklist de Verificación

- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Tests pasan (`python proyecto.py --test`)
- [ ] Modelo entrenado existe (`python proyecto.py --stats`)
- [ ] Demo funciona (`python proyecto.py --demo`)

---

## 🎓 Sistema Académico

Este proyecto cumple con todos los requisitos:

✅ MLP implementado desde cero (sin frameworks)  
✅ Forward pass + Backpropagation  
✅ 500+ épocas de entrenamiento  
✅ Dataset de algoritmos Go  
✅ Análisis de complejidad Big-O  
✅ Tests unitarios comprehensivos  
✅ Documentación completa  

---

## 📞 Contacto

**Repositorio:** [github.com/yeisonpabon/proyectofinalADA](https://github.com/yeisonpabon/proyectofinalADA)

---

**¡Sistema listo para uso! 🎉**
