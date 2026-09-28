# Tarea 1 IA - Escape de la Torre

Simulación de evacuación de varios agentes en una grilla con congestión y fuego.

## Integrantes

- Diego Arriagada

## Algoritmos

- BFS
- UCS
- Greedy Best First Search
- A*
- Algoritmo genético

Para Greedy y A* se usa distancia Manhattan.

## Mapa

Los mapas usan estos caracteres:

- `#`: muro
- `.`: espacio libre
- `P`: posición inicial de un agente
- `S`: salida
- `F`: foco inicial de fuego

Cada casilla admite como máximo 4 agentes. El costo por congestión es:

`C(n) = 1 + (n - 1)^2`

El fuego se propaga cada 3 turnos. Un agente vuelve a calcular su ruta desde donde está cuando el fuego bloquea la ruta, cuando las próximas casillas están congestionadas, cuando lleva dos turnos sin poder avanzar o cuando no tiene ruta.

## Ejecución

Ejemplo:

```bash
python main.py --mapa mapas/mapa1_cuello.txt --algoritmo bfs --semilla 42 --verbose
```

Los algoritmos disponibles son `bfs`, `ucs`, `greedy`, `astar` y `genetico`.

## Benchmark

Para ejecutar 80 pruebas por combinación:

```bash
python benchmark.py --iteraciones 80
```

Para las 200 iteraciones esperadas:

```bash
python benchmark.py --iteraciones 200
```

Los resultados quedan en:

- `resultados/benchmark.csv`
- `resultados/benchmark_resumen.csv`

El resumen contiene la tasa de supervivencia y la media, desviación estándar, mínimo y máximo del tiempo de despeje. El tiempo de despeje es el turno en que sale el último sobreviviente, por eso las corridas donde nadie sobrevive no se consideran en esas estadísticas (se indica cuántas fueron). Todos los algoritmos se prueban con las mismas semillas en cada mapa.

## Archivos principales

- `main.py`: ejecuta una simulación.
- `simulacion.py`: controla turnos, movimiento, congestión, fuego y replanificación.
- `mapa.py`: lectura y operaciones del mapa.
- `agente.py`: estado de cada agente.
- `benchmark.py`: ejecuta las pruebas repetidas.
- `algoritmos/`: implementaciones de los cinco algoritmos.

## Uso de IA generativa

Se utilizó IA generativa como apoyo durante el desarrollo y revisión del proyecto. El código fue revisado antes de la entrega.
