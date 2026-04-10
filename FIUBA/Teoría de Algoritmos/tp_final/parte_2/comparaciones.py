import random
import time
from algo1_greedy import ratio_inversores
import numpy as np
from montecarlo import monte_carlo_inversores


def generar_instancia_aleatoria(n_inversores, densidad_conflictos, rango_dinero):
    inversores = [f"I{i}" for i in range(n_inversores)]
    dinero = [random.randint(rango_dinero[0], rango_dinero[1]) for _ in range(n_inversores)]

    conflictos = {}
    for inversor in inversores:
        conflictos[inversor] = {}
    for i in range(n_inversores):
        for j in range(n_inversores):
            if i != j:
                if random.random() < densidad_conflictos:
                    if inversores[j] not in conflictos[inversores[i]]:
                        aux = conflictos[inversores[i]]
                        aux[inversores[j]] = True
    return inversores, dinero, conflictos

def comparar_algoritmos(n_inversores_lista, densidades, num_repeticiones=10):
    resultados = {
        'ratio_mejor': 0,
        'aleatorio_mejor': 0,
        'empates': 0,
        'tiempo_ratio': [],
        'tiempo_aleatorio': [],
        'calidad_ratio': [],
        'calidad_aleatorio': [],
        'densidades': [],
        'n_inversores': []
    }

    for n in n_inversores_lista:
        for densidad in densidades:
            for _ in range(num_repeticiones):
                inversores, dinero, conflictos = generar_instancia_aleatoria(n, densidad, (100, 1000000))

                start = time.time()
                sol_ratio, ganancia_ratio = ratio_inversores(inversores, dinero, conflictos)
                tiempo_ratio = time.time() - start

                start = time.time()
                sol_aleatoria, ganancia_aleatoria = monte_carlo_inversores(inversores, dinero, conflictos)
                tiempo_aleatorio = time.time() - start

                if ganancia_ratio > ganancia_aleatoria:
                    resultados['ratio_mejor'] += 1
                elif ganancia_aleatoria > ganancia_ratio:
                    resultados['aleatorio_mejor'] += 1
                else:
                    resultados['empates'] += 1

                resultados['tiempo_ratio'].append(tiempo_ratio)
                resultados['tiempo_aleatorio'].append(tiempo_aleatorio)
                resultados['calidad_ratio'].append(ganancia_ratio)
                resultados['calidad_aleatorio'].append(ganancia_aleatoria)
                resultados['densidades'].append(densidad)
                resultados['n_inversores'].append(n)

    return resultados


def analizar_por_densidad(resultados):
    print("\n--- ANÁLISIS POR DENSIDAD DE CONFLICTOS ---")
    densidades_unicas = sorted(list(set(resultados['densidades'])))
    for densidad in densidades_unicas:
        indices = [i for i, d in enumerate(resultados['densidades']) if d == densidad]

        ratio_wins = sum(1 for i in indices if resultados['calidad_ratio'][i] > resultados['calidad_aleatorio'][i])
        aleatorio_wins = sum(1 for i in indices if resultados['calidad_aleatorio'][i] > resultados['calidad_ratio'][i])
        empates = len(indices) - ratio_wins - aleatorio_wins

        print(f"\nDensidad {densidad:.1f}:")
        print(f"  Ratio ganó: {ratio_wins}/{len(indices)} ({100 * ratio_wins / len(indices):.1f}%)")
        print(f"  Aleatorio ganó: {aleatorio_wins}/{len(indices)} ({100 * aleatorio_wins / len(indices):.1f}%)")
        print(f"  Empates: {empates}/{len(indices)} ({100 * empates / len(indices):.1f}%)")


def generar_reporte_estadistico(resultados):
    print("=" * 60)
    print("REPORTE ESTADÍSTICO")
    print("=" * 60)

    total_experimentos = len(resultados['calidad_ratio'])

    print(f"Total de experimentos: {total_experimentos}")
    print(f"Ratio ganó: {resultados['ratio_mejor']} ({100 * resultados['ratio_mejor'] / total_experimentos:.1f}%)")
    print(f"Aleatorio ganó: {resultados['aleatorio_mejor']} ({100 * resultados['aleatorio_mejor'] / total_experimentos:.1f}%)")
    print(f"Empates: {resultados['empates']} ({100 * resultados['empates'] / total_experimentos:.1f}%)")

    print("\n--- TIEMPOS DE EJECUCIÓN ---")
    print(f"Ratio - Promedio: {np.mean(resultados['tiempo_ratio']):.8f}s, Mediana: {np.median(resultados['tiempo_ratio']):.8f}s")
    print(f"Aleatorio - Promedio: {np.mean(resultados['tiempo_aleatorio']):.8f}s, Mediana: {np.median(resultados['tiempo_aleatorio']):.8f}s")

    print("\n--- CALIDAD DE SOLUCIONES ---")
    print(f"Ratio - Promedio: {np.mean(resultados['calidad_ratio']):.2f}, Std: {np.std(resultados['calidad_ratio']):.2f}")
    print(f"Aleatorio - Promedio: {np.mean(resultados['calidad_aleatorio']):.2f}, Std: {np.std(resultados['calidad_aleatorio']):.2f}")

    print("\nTiempos promedio por densidad:")
    densidades_unicas = sorted(list(set(resultados['densidades'])))

    for densidad in densidades_unicas:
        indices = [i for i, d in enumerate(resultados['densidades']) if d == densidad]

        tiempo_ratio_densidad = [resultados['tiempo_ratio'][i] for i in indices]
        tiempo_aleatorio_densidad = [resultados['tiempo_aleatorio'][i] for i in indices]

        print(f" \nDensidad {densidad:.1f}:")
        print(f"  Ratio - Promedio: {np.mean(tiempo_ratio_densidad):.8f}s, Std: {np.std(tiempo_ratio_densidad):.8f}s")
        print(f"  Aleatorio - Promedio: {np.mean(tiempo_aleatorio_densidad):.8f}s, Std: {np.std(tiempo_aleatorio_densidad):.8f}s")


if __name__ == "__main__":
    print("Ejecutando análisis empírico...")

    resultados = comparar_algoritmos(
        n_inversores_lista=[5], #Cambiar lista para modificar numero de inversores, se pueden poner varios valores en la lista para combinar los resultados.
        densidades=[0.1, 0.3, 0.5, 0.7, 0.9], #Probabilidades de que dos inversores sean rivales. Se hace la prueba con distintas probabilidades
        num_repeticiones=50
    )
    generar_reporte_estadistico(resultados)
    analizar_por_densidad(resultados)