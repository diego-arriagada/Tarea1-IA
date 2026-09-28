import heapq
from mapa import obtener_vecinos
from costos import CAPACIDAD_MAXIMA, costo_congestion
from algoritmos.comun import reconstruir_ruta, manhattan


def astar(mapa, inicio, salida, fuego=None, ocupacion=None):
    ocupacion = ocupacion or {}
    frontera = [(manhattan(inicio, salida), 0.0, inicio)]
    g = {inicio: 0.0}
    padres = {}
    while frontera:
        _, costo_actual, actual = heapq.heappop(frontera)
        if costo_actual != g.get(actual):
            continue
        if actual == salida:
            return reconstruir_ruta(padres, inicio, salida)
        for vecino in obtener_vecinos(mapa, actual, fuego):
            n = ocupacion.get(vecino, 0)
            if vecino != salida and n >= CAPACIDAD_MAXIMA:
                continue
            nuevo_g = costo_actual + costo_congestion(n + 1)
            if nuevo_g < g.get(vecino, float('inf')):
                g[vecino] = nuevo_g
                padres[vecino] = actual
                f = nuevo_g + manhattan(vecino, salida)
                heapq.heappush(frontera, (f, nuevo_g, vecino))
    return None
