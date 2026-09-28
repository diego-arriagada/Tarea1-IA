from collections import deque
from mapa import obtener_vecinos
from algoritmos.comun import reconstruir_ruta


def bfs(mapa, inicio, salida, fuego=None, ocupacion=None):
    cola = deque([inicio])
    visitados = {inicio}
    padres = {}
    while cola:
        actual = cola.popleft()
        if actual == salida:
            return reconstruir_ruta(padres, inicio, salida)
        for vecino in obtener_vecinos(mapa, actual, fuego):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                cola.append(vecino)
    return None
