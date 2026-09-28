def cargar_mapa(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        mapa = [list(linea.rstrip('\n')) for linea in archivo if linea.strip('\n')]
    if not mapa:
        raise ValueError('El mapa está vacío.')
    ancho = len(mapa[0])
    if any(len(fila) != ancho for fila in mapa):
        raise ValueError('Todas las filas del mapa deben tener el mismo ancho.')
    return mapa


def buscar_elemento(mapa, elemento):
    for f, fila in enumerate(mapa):
        for c, valor in enumerate(fila):
            if valor == elemento:
                return (f, c)
    return None


def buscar_agentes(mapa):
    return [(f, c) for f, fila in enumerate(mapa) for c, valor in enumerate(fila) if valor == 'P']


def buscar_fuegos(mapa):
    return {(f, c) for f, fila in enumerate(mapa) for c, valor in enumerate(fila) if valor == 'F'}


def dentro(mapa, posicion):
    f, c = posicion
    return 0 <= f < len(mapa) and 0 <= c < len(mapa[f])


def es_transitable(mapa, posicion, fuego=None):
    if not dentro(mapa, posicion):
        return False
    if mapa[posicion[0]][posicion[1]] == '#':
        return False
    return fuego is None or posicion not in fuego


def obtener_vecinos(mapa, posicion, fuego=None):
    f, c = posicion
    posibles = [(f - 1, c), (f + 1, c), (f, c - 1), (f, c + 1)]
    return [p for p in posibles if es_transitable(mapa, p, fuego)]
