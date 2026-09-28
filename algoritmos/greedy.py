import heapq
from mapa import obtener_vecinos
from algoritmos.comun import reconstruir_ruta, manhattan


def greedy(mapa, inicio, salida, fuego=None, ocupacion=None):
    frontera = [(manhattan(inicio, salida), inicio)]
    visitados = {inicio}
    padres = {}
    while frontera:
        _, actual = heapq.heappop(frontera)
        if actual == salida:
            return reconstruir_ruta(padres, inicio, salida)
        for vecino in obtener_vecinos(mapa, actual, fuego):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                heapq.heappush(frontera, (manhattan(vecino, salida), vecino))
    return None
