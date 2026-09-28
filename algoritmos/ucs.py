import heapq
from mapa import obtener_vecinos
from costos import CAPACIDAD_MAXIMA, costo_congestion
from algoritmos.comun import reconstruir_ruta


def ucs(mapa, inicio, salida, fuego=None, ocupacion=None):
    ocupacion = ocupacion or {}
    frontera = [(0.0, inicio)]
    costos = {inicio: 0.0}
    padres = {}
    while frontera:
        costo_actual, actual = heapq.heappop(frontera)
        if costo_actual != costos.get(actual):
            continue
        if actual == salida:
            return reconstruir_ruta(padres, inicio, salida)
        for vecino in obtener_vecinos(mapa, actual, fuego):
            n = ocupacion.get(vecino, 0)
            if vecino != salida and n >= CAPACIDAD_MAXIMA:
                continue
            paso = costo_congestion(n + 1)
            nuevo = costo_actual + paso
            if nuevo < costos.get(vecino, float('inf')):
                costos[vecino] = nuevo
                padres[vecino] = actual
                heapq.heappush(frontera, (nuevo, vecino))
    return None
