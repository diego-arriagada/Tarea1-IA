import argparse
from mapa import cargar_mapa
from escenario import crear_escenario
from simulacion import Simulacion


def main():
    p = argparse.ArgumentParser(description='Tarea 1 IA - Escape de la Torre')
    p.add_argument('--mapa', default='mapas/mapa1_cuello.txt')
    p.add_argument('--algoritmo', choices=['bfs','ucs','greedy','astar','genetico'], default='astar')
    p.add_argument('--semilla', type=int, default=42)
    p.add_argument('--sin-variacion', action='store_true')
    p.add_argument('--verbose', action='store_true')
    args = p.parse_args()

    mapa = cargar_mapa(args.mapa)
    agentes, salida, fuego = crear_escenario(mapa, args.semilla, not args.sin_variacion, not args.sin_variacion)
    sim = Simulacion(mapa, agentes, salida, args.algoritmo, fuego, semilla=args.semilla)
    sim.planificar_todos()
    while not sim.termino():
        if args.verbose:
            print(f'Turno {sim.turno} | fuego={len(sim.fuego)} | vivos={sum(a.vivo and not a.evacuado for a in agentes)}')
        sim.ejecutar_turno()
    print(sim.resumen())
    if args.verbose:
        for a in agentes:
            print('Agente', a.id, 'vivo=', a.vivo, 'evacuado=', a.evacuado, 'costo=', a.costo_total, 'ruta=', a.ruta)


if __name__ == '__main__':
    main()
