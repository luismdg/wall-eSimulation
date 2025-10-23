# ForkLifts Simulation
Este proyecto simula el comportamiento de montacargas (`lifters`) que recolectan basura en un entorno gráfico utilizando Python y Pygame + OpenGL.

## Requisitos de instalación
Antes de ejecutar el simulador, asegúrate de tener instaladas las siguientes bibliotecas de Python:

```bash
pip install pygame PyOpenGL PyOpenGL_accelerate numpy pyyaml
```
⚠️ Si estás usando un entorno virtual (como venv o conda), activa el entorno antes de instalar.

## Ejecución del simulador
Para correr la simulación, usa el siguiente comando desde la raíz del proyecto:

```bash
python Main.py Simulacion --lifters 10 --Basuras 10 --Delta 0.001
```

## Parámetros
--lifters: número de montacargas en la simulación.
--Basuras: cantidad total de objetos basura a recolectar.
--Delta: intervalo de tiempo entre actualizaciones (en segundos).
