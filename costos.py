CAPACIDAD_MAXIMA = 4
ALPHA_CONGESTION = 1.0


def costo_congestion(ocupacion_resultante):
    if ocupacion_resultante <= 1:
        return 1.0
    return 1.0 + ALPHA_CONGESTION * ((ocupacion_resultante - 1) ** 2)
