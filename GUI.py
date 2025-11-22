#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejecutor de GUI - Inicia la interfaz gráfica
Ejecuta este archivo para ver la ventana en tu pantalla
"""

import os
import sys
import io

# Configurar encoding UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Agregar ruta del proyecto
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("\n" + "=" * 70)
print("SISTEMA DE ANÁLISIS DE COMPLEJIDAD COMPUTACIONAL")
print("=" * 70)
print("\nCargando interfaz gráfica...\n")

try:
    from src.gui.main_window import MainWindow
    
    print("✓ Módulos cargados correctamente")
    print("✓ Iniciando ventana principal...\n")
    
    app = MainWindow()
    app.run()
    
except Exception as e:
    print(f"\n❌ Error al iniciar la GUI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
