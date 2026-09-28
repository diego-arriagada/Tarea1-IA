import random
from costos import CAPACIDAD_MAXIMA, costo_congestion
from mapa import obtener_vecinos
from algoritmos import ALGORITMOS


class Simulacion:
    def __init__(self, mapa, agentes, salida, algoritmo='bfs', fuego_inicial=None,
                 intervalo_fuego=3, probabilidad_fuego=0.65, semilla=None,
                 max_turnos=300):
        self.mapa = mapa
        self.agentes = agentes
        self.salida = salida
        self.algoritmo = algoritmo.lower()
        self.fuego = set(fuego_inicial or set())
        self.intervalo_fuego = intervalo_fuego
        self.probabilidad_fuego = probabilidad_fuego
        # rng separados para que el genetico no cambie el fuego respecto a los otros algoritmos
        self.rng = random.Random(semilla)
        self.rng_algoritmo = random.Random(None if semilla is None else semilla + 7)
        self.semilla = semilla
        self.casillas_adelante = 3
        self.turno = 0
        self.max_turnos = max_turnos
        self.capacidad_maxima = CAPACIDAD_MAXIMA
        self.finalizada_por_limite = False

    def obtener_ocupacion(self):
        ocupacion = {}
        for a in self.agentes:
            if a.vivo and not a.evacuado:
                p = tuple(a.posicion)
                ocupacion[p] = ocupacion.get(p, 0) + 1
        return ocupacion

    def planificar(self, agente):
        if not agente.vivo or agente.evacuado:
            return False
        fn = ALGORITMOS[self.algoritmo]
        kwargs = dict(fuego=self.fuego, ocupacion=self.obtener_ocupacion())
        if self.algoritmo == 'genetico':
            kwargs['semilla'] = self.rng_algoritmo.randrange(2**31)
        ruta = fn(self.mapa, tuple(agente.posicion), self.salida, **kwargs)
        agente.ruta_planificada = ruta[1:] if ruta else []
        agente.replanificaciones += 1
        return ruta is not None

    def planificar_todos(self):
        for a in self.agentes:
            self.planificar(a)

    def propagar_fuego(self):
        nuevos = set()
        for celda in self.fuego:
            for vecino in obtener_vecinos(self.mapa, celda, fuego=None):
                if vecino == self.salida or vecino in self.fuego:
                    continue
                if self.rng.random() <= self.probabilidad_fuego:
                    nuevos.add(vecino)
        self.fuego.update(nuevos)
        return nuevos

    def aplicar_bajas_por_fuego(self):
        for a in self.agentes:
            if a.vivo and not a.evacuado and tuple(a.posicion) in self.fuego:
                a.vivo = False
                a.ruta_planificada = []

    def replanificar_si_necesario(self):
        ocupacion = self.obtener_ocupacion()
        for a in self.agentes:
            if not a.vivo or a.evacuado:
                continue
            invalida = any(p in self.fuego for p in a.ruta_planificada)
            sin_ruta = not a.ruta_planificada
            # si las proximas casillas de la ruta estan llenas se busca otra ruta,
            # si no la congestion solo se consideraba al inicio
            adelante = a.ruta_planificada[:self.casillas_adelante]
            congestionada = any(ocupacion.get(p, 0) >= 2 for p in adelante if p != self.salida)
            if invalida or sin_ruta or a.bloqueado >= 2 or congestionada:
                self.planificar(a)
                a.bloqueado = 0

    def _resolver_movimientos(self, propuestas, ocupacion_inicial):
        aceptados = [(a, d) for d, agentes in propuestas.items() for a in agentes]
        while True:
            salidas, entradas = {}, {}
            for a, d in aceptados:
                o = tuple(a.posicion)
                salidas[o] = salidas.get(o, 0) + 1
                entradas[d] = entradas.get(d, 0) + 1
            rechazar = set()
            for destino, n_entra in entradas.items():
                if destino == self.salida:
                    continue
                final = ocupacion_inicial.get(destino, 0) - salidas.get(destino, 0) + n_entra
                exceso = max(0, final - self.capacidad_maxima)
                if exceso:
                    candidatos = [(a, d) for a, d in aceptados if d == destino]
                    for mov in candidatos[-exceso:]:
                        rechazar.add(mov)
            if not rechazar:
                return aceptados
            nuevos = [m for m in aceptados if m not in rechazar]
            if len(nuevos) == len(aceptados):
                return aceptados
            aceptados = nuevos

    def ejecutar_turno(self):
        if self.termino():
            return
        if self.turno >= self.max_turnos:
            self.finalizada_por_limite = True
            return

        if self.turno > 0 and self.intervalo_fuego > 0 and self.turno % self.intervalo_fuego == 0:
            self.propagar_fuego()
            self.aplicar_bajas_por_fuego()

        self.replanificar_si_necesario()
        ocupacion_inicial = self.obtener_ocupacion()
        propuestas = {}
        for a in self.agentes:
            if not a.vivo or a.evacuado or not a.ruta_planificada:
                continue
            destino = a.ruta_planificada[0]
            if destino in self.fuego:
                continue
            propuestas.setdefault(destino, []).append(a)

        aceptados = self._resolver_movimientos(propuestas, ocupacion_inicial)
        salidas, entradas = {}, {}
        for a, d in aceptados:
            o = tuple(a.posicion)
            salidas[o] = salidas.get(o, 0) + 1
            entradas[d] = entradas.get(d, 0) + 1

        ocup_final = dict(ocupacion_inicial)
        for p, n in salidas.items():
            ocup_final[p] = ocup_final.get(p, 0) - n
        for p, n in entradas.items():
            ocup_final[p] = ocup_final.get(p, 0) + n

        movieron = set()
        for a, destino in aceptados:
            movieron.add(a)
            # La salida representa abandonar el edificio: no penaliza por acumulación externa.
            costo = 1.0 if destino == self.salida else costo_congestion(ocup_final.get(destino, 1))
            a.costo_total += costo
            a.mover_a(destino)
            a.ruta_planificada.pop(0)
            if destino == self.salida:
                a.evacuado = True
                a.turno_evacuacion = self.turno + 1

        for a in self.agentes:
            if a.vivo and not a.evacuado and a not in movieron:
                if a.ruta_planificada:
                    a.bloqueado += 1
                a.esperar()
                a.costo_total += 1.0

        self.turno += 1
        self.aplicar_bajas_por_fuego()

    def termino(self):
        if self.finalizada_por_limite:
            return True
        return all((not a.vivo) or a.evacuado for a in self.agentes)

    def ejecutar(self):
        self.planificar_todos()
        while not self.termino():
            self.ejecutar_turno()
        return self.resumen()

    def resumen(self):
        total = len(self.agentes)
        sobrevivientes = sum(a.evacuado for a in self.agentes)
        bajas = sum(not a.vivo for a in self.agentes)
        # tiempo de despeje = turno en que salio el ultimo sobreviviente
        tiempos = [a.turno_evacuacion for a in self.agentes if a.evacuado]
        return {
            'algoritmo': self.algoritmo,
            'turnos': self.turno,
            'turnos_despeje': max(tiempos) if tiempos else None,
            'total_agentes': total,
            'sobrevivientes': sobrevivientes,
            'bajas': bajas,
            'tasa_supervivencia': sobrevivientes / total if total else 0.0,
            'costo_total': sum(a.costo_total for a in self.agentes),
            'replanificaciones': sum(a.replanificaciones for a in self.agentes),
            'limite_turnos': self.finalizada_por_limite,
        }
