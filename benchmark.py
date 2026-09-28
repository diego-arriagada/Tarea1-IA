import argparse
import csv
import os
import statistics
from mapa import cargar_mapa
from escenario import crear_escenario
from simulacion import Simulacion

ALGORITMOS = ['bfs', 'ucs', 'greedy', 'astar', 'genetico']
MAPAS = ['mapa1_cuello.txt', 'mapa2_laberinto.txt', 'mapa3_abierto.txt']


def ejecutar_benchmark(iteraciones=80, carpeta_mapas='mapas', salida_csv='resultados/benchmark.csv'):
    os.makedirs(os.path.dirname(salida_csv) or '.', exist_ok=True)
    filas = []
    for nombre_mapa in MAPAS:
        mapa = cargar_mapa(os.path.join(carpeta_mapas, nombre_mapa))
        for algoritmo in ALGORITMOS:
            for i in range(iteraciones):
                # misma semilla para todos los algoritmos, asi comparan sobre el mismo escenario
                semilla = 100000 * MAPAS.index(nombre_mapa) + i
                agentes, salida, fuego = crear_escenario(mapa, semilla)
                sim = Simulacion(mapa, agentes, salida, algoritmo, fuego, semilla=semilla)
                r = sim.ejecutar()
                r.update({'mapa': nombre_mapa, 'iteracion': i, 'semilla': semilla})
                filas.append(r)
                print(nombre_mapa, algoritmo, i + 1, '/', iteraciones, 'superv=', round(r['tasa_supervivencia'], 3), 'despeje=', r['turnos_despeje'])

    campos = ['mapa','algoritmo','iteracion','semilla','turnos','turnos_despeje','total_agentes','sobrevivientes','bajas','tasa_supervivencia','costo_total','replanificaciones','limite_turnos']
    with open(salida_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader(); w.writerows(filas)

    resumen_csv = os.path.splitext(salida_csv)[0] + '_resumen.csv'
    resumen = []
    for mapa in MAPAS:
        for alg in ALGORITMOS:
            xs = [r for r in filas if r['mapa'] == mapa and r['algoritmo'] == alg]
            # las corridas sin sobrevivientes no tienen tiempo de despeje
            turnos = [r['turnos_despeje'] for r in xs if r['turnos_despeje'] is not None]
            supervivencias = [r['tasa_supervivencia'] for r in xs]
            resumen.append({
                'mapa': mapa, 'algoritmo': alg,
                'tasa_supervivencia_media': statistics.mean(supervivencias),
                'tasa_supervivencia_desv_est': statistics.stdev(supervivencias) if len(xs) > 1 else 0.0,
                'corridas_sin_sobrevivientes': len(xs) - len(turnos),
                'turnos_media': statistics.mean(turnos) if turnos else None,
                'turnos_desv_est': statistics.stdev(turnos) if len(turnos) > 1 else 0.0,
                'turnos_min': min(turnos) if turnos else None,
                'turnos_max': max(turnos) if turnos else None,
            })
    with open(resumen_csv, 'w', newline='', encoding='utf-8') as f:
        campos2 = list(resumen[0].keys())
        w = csv.DictWriter(f, fieldnames=campos2); w.writeheader(); w.writerows(resumen)
    return salida_csv, resumen_csv


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--iteraciones', type=int, default=80)
    p.add_argument('--mapas', default='mapas')
    p.add_argument('--salida', default='resultados/benchmark.csv')
    a = p.parse_args()
    ejecutar_benchmark(a.iteraciones, a.mapas, a.salida)
