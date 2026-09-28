import random
from agente import Agente
from mapa import buscar_elemento, buscar_agentes, buscar_fuegos


def crear_escenario(mapa, semilla=None, variacion_agentes=True, variacion_fuego=True):
    rng = random.Random(semilla)
    salida = buscar_elemento(mapa, 'S')
    posiciones = buscar_agentes(mapa)
    fuegos = buscar_fuegos(mapa)

    # Variación estocástica leve: cada P puede desplazarse a una celda libre vecina.
    if variacion_agentes:
        nuevas = []
        ocupadas = set()
        for p in posiciones:
            candidatos = [p]
            f, c = p
            for q in [(f-1,c),(f+1,c),(f,c-1),(f,c+1)]:
                if 0 <= q[0] < len(mapa) and 0 <= q[1] < len(mapa[0]) and mapa[q[0]][q[1]] != '#' and q != salida:
                    candidatos.append(q)
            rng.shuffle(candidatos)
            elegido = next((q for q in candidatos if q not in ocupadas and q not in fuegos), p)
            nuevas.append(elegido)
            ocupadas.add(elegido)
        posiciones = nuevas

    if variacion_fuego and fuegos:
        # Activa un subconjunto no vacío de los focos marcados F.
        lista = list(fuegos)
        rng.shuffle(lista)
        cantidad = rng.randint(1, len(lista))
        fuegos = set(lista[:cantidad])

    agentes = [Agente(p, i) for i, p in enumerate(posiciones)]
    return agentes, salida, fuegos
