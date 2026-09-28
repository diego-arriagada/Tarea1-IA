class Agente:
    def __init__(self, posicion, identificador=None):
        self.id = identificador
        self.posicion = list(posicion)
        self.vivo = True
        self.evacuado = False
        self.ruta = [tuple(posicion)]
        self.ruta_planificada = []
        self.costo_total = 0.0
        self.turno_evacuacion = None
        self.replanificaciones = 0
        self.bloqueado = 0

    def mover_a(self, destino):
        self.posicion = list(destino)
        self.ruta.append(tuple(destino))

    def esperar(self):
        self.ruta.append(tuple(self.posicion))
