import random
from mapa import obtener_vecinos
from algoritmos.comun import manhattan
from costos import CAPACIDAD_MAXIMA, costo_congestion


# Cada individuo es una lista de numeros entre 0 y 1 (claves aleatorias).
# Al decodificar, en cada paso se ordenan los vecinos no visitados por cercania
# a la salida y el gen decide cual se toma. Si el agente queda encerrado,
# retrocede (como DFS). Asi todo individuo termina siendo una ruta valida y el
# GA solo tiene que buscar la combinacion de decisiones con menor costo.
def _decodificar(cromosoma, mapa, inicio, salida, fuego, ocupacion):
    pila = [inicio]
    visitados = {inicio}
    i = 0
    while pila:
        pos = pila[-1]
        if pos == salida:
            return pila
        opciones = [v for v in obtener_vecinos(mapa, pos, fuego)
                    if v not in visitados and (v == salida or ocupacion.get(v, 0) < CAPACIDAD_MAXIMA)]
        if not opciones:
            pila.pop()
            continue
        opciones.sort(key=lambda v: manhattan(v, salida))
        gen = cromosoma[i % len(cromosoma)]
        i += 1
        # gen^2 hace que sea mas probable elegir los vecinos mas cercanos a la salida
        elegido = opciones[min(int(gen * gen * len(opciones)), len(opciones) - 1)]
        visitados.add(elegido)
        pila.append(elegido)
    return None


def _evaluar(cromosoma, mapa, inicio, salida, fuego, ocupacion):
    ruta = _decodificar(cromosoma, mapa, inicio, salida, fuego, ocupacion)
    if ruta is None:
        return float('-inf'), None
    costo = sum(costo_congestion(ocupacion.get(p, 0) + 1) for p in ruta[1:])
    return -costo, ruta


def _torneo(evaluados, rng, k=3):
    return max(rng.sample(evaluados, k), key=lambda x: x[0])[1]


def genetico(mapa, inicio, salida, fuego=None, ocupacion=None, semilla=None,
             poblacion_tam=20, generaciones=30, longitud=None, mutacion=0.1,
             sin_mejora_max=8):
    fuego = fuego or set()
    ocupacion = ocupacion or {}
    rng = random.Random(semilla)
    if inicio == salida:
        return [inicio]
    if longitud is None:
        longitud = max(20, manhattan(inicio, salida) * 2)

    poblacion = [[rng.random() for _ in range(longitud)] for _ in range(poblacion_tam)]
    mejor_ruta = None
    mejor_fit = float('-inf')
    sin_mejora = 0

    for _ in range(generaciones):
        evaluados = []
        mejoro = False
        for crom in poblacion:
            fit, ruta = _evaluar(crom, mapa, inicio, salida, fuego, ocupacion)
            evaluados.append((fit, crom, ruta))
            if fit > mejor_fit:
                mejor_fit, mejor_ruta = fit, ruta
                mejoro = True
        if mejor_ruta is None:
            # la salida no es alcanzable desde aqui, no tiene sentido seguir
            return None
        sin_mejora = 0 if mejoro else sin_mejora + 1
        if sin_mejora >= sin_mejora_max:
            break

        evaluados.sort(key=lambda x: x[0], reverse=True)
        nueva = [list(x[1]) for x in evaluados[:2]]  # elitismo
        while len(nueva) < poblacion_tam:
            p1, p2 = _torneo(evaluados, rng), _torneo(evaluados, rng)
            corte = rng.randrange(1, longitud)
            hijo = p1[:corte] + p2[corte:]
            hijo = [rng.random() if rng.random() < mutacion else g for g in hijo]
            nueva.append(hijo)
        poblacion = nueva

    return mejor_ruta
