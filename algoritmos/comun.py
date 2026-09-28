def reconstruir_ruta(padres, inicio, salida):
    if inicio == salida:
        return [inicio]
    if salida not in padres:
        return None
    ruta = [salida]
    actual = salida
    while actual != inicio:
        actual = padres[actual]
        ruta.append(actual)
    ruta.reverse()
    return ruta


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
