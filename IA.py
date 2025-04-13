import random
import time
import itertools
import math

# Generador de grafo completo aleatorio
def generar_grafo(N, distancia_max=100):
    grafo = [[0 if i == j else random.randint(1, distancia_max) for j in range(N)] for i in range(N)]
    return grafo

# BACKTRACKING
# Es un algoritmo exacto que intenta todas las posibles rutas que:Comienzan en la ciudad de origen (0),
# Visitan todas las demás ciudades una sola vez y regresan a la ciudad de origen.
# En cada paso
# A cada paso: Se elige una ciudad no visitada y se "visita". Se repite esto recursivamente.
# Si la ruta completa es válida, se calcula el costo total. Se compara con la mejor encontrada hasta ahora.
# Es como tratar todas las combinaciones posibles de caminos en una lista de entregas, y te quedaras con el que más cpnviene
# Es lento y no escalable pero óptimo 
def tsp_backtracking(grafo):
    N = len(grafo)
    mejor_costo = math.inf
    mejor_ruta = []
    estados_expandidos = 0

    def backtrack(ciudad_actual, visitadas, costo_actual, ruta_actual):
        nonlocal mejor_costo, mejor_ruta, estados_expandidos
        estados_expandidos += 1

        if len(visitadas) == N:
            costo_total = costo_actual + grafo[ciudad_actual][0]  # Regresa al inicio
            if costo_total < mejor_costo:
                mejor_costo = costo_total
                mejor_ruta = ruta_actual + [0]
            return

        for ciudad_siguiente in range(N):
            if ciudad_siguiente not in visitadas:
                backtrack(
                    ciudad_siguiente,
                    visitadas + [ciudad_siguiente],
                    costo_actual + grafo[ciudad_actual][ciudad_siguiente],
                    ruta_actual + [ciudad_siguiente]
                )

    inicio = time.time()
    backtrack(0, [0], 0, [0])
    fin = time.time()

    return mejor_ruta, mejor_costo, fin - inicio, estados_expandidos

# GREEDY: PRIMERO EL MEJOR AVARO
# Comienza en la ciudad 0. En cada paso, elige la ciudad más cercana que aún no haya visitado.
# Repite hasta que haya visitado todas las ciudades. Finalmente, regresa a la ciudad de origen.
# Es como que va siempre a la ciudad más cercana, sin pensar en el camino total.
# Es rápido, subóptimo pero escalable
def tsp_greedy(grafo):
    N = len(grafo)
    visitadas = [False] * N
    ruta = [0]
    visitadas[0] = True
    costo = 0
    estados_expandidos = 0

    ciudad_actual = 0
    for _ in range(N - 1):
        menor_costo = math.inf
        siguiente_ciudad = None
        for ciudad in range(N):
            if not visitadas[ciudad] and grafo[ciudad_actual][ciudad] < menor_costo:
                menor_costo = grafo[ciudad_actual][ciudad]
                siguiente_ciudad = ciudad
            estados_expandidos += 1
        ruta.append(siguiente_ciudad)
        visitadas[siguiente_ciudad] = True
        costo += menor_costo
        ciudad_actual = siguiente_ciudad

    costo += grafo[ciudad_actual][0]
    ruta.append(0)  # Vuelta al inicio

    return ruta, costo, estados_expandidos

# OPTIMIZACIÓN 2-OPT
# Toma una ruta existente (como la generada por Greedy). Parte de una solución ya armada y busca pequeñas modificaciones que la hagan mejor.
# Recorre todos los pares de aristas de la ruta.
# Intenta intercambiar el orden de dos tramos (hacer un "swap") y ver si el nuevo camino tiene menor costo.
# Si el nuevo camino es mejor, se acepta. Repite hasta que no se puedan hacer más mejoras.
# Es rápido, Mejora Heurística y escalable
def calcular_costo(grafo, ruta):
    return sum(grafo[ruta[i]][ruta[i+1]] for i in range(len(ruta) - 1))

def two_opt(grafo, ruta):
    N = len(ruta)
    mejor_ruta = ruta
    mejor_costo = calcular_costo(grafo, ruta)
    mejorado = True

    while mejorado:
        mejorado = False
        for i in range(1, N - 2):
            for j in range(i + 1, N - 1):
                nueva_ruta = mejor_ruta[:i] + mejor_ruta[i:j+1][::-1] + mejor_ruta[j+1:]
                nuevo_costo = calcular_costo(grafo, nueva_ruta)
                if nuevo_costo < mejor_costo:
                    mejor_ruta = nueva_ruta
                    mejor_costo = nuevo_costo
                    mejorado = True

    return mejor_ruta, mejor_costo

# COMPARACIÓN
def comparar_algoritmos(N):
    grafo = generar_grafo(N)
    print(f"\n--- Comparando para N = {N} ---")

    # Backtracking
    ruta_bt, costo_bt, tiempo_bt, estados_bt = tsp_backtracking(grafo)
    print(f"Backtracking:")
    print(f"  Ruta: {ruta_bt}")
    print(f"  Costo: {costo_bt}")
    print(f"  Tiempo: {tiempo_bt:.4f} s")
    print(f"  Estados expandidos: {estados_bt}")

    # Greedy
    inicio = time.time()
    ruta_greedy, costo_greedy, estados_greedy = tsp_greedy(grafo)
    tiempo_greedy = time.time() - inicio
    print(f"\nGreedy:")
    print(f"  Ruta: {ruta_greedy}")
    print(f"  Costo: {costo_greedy}")
    print(f"  Tiempo: {tiempo_greedy:.4f} s")
    print(f"  Estados expandidos: {estados_greedy}")

    # 2-opt
    inicio = time.time()
    ruta_opt, costo_opt = two_opt(grafo, ruta_greedy)
    tiempo_opt = time.time() - inicio
    print(f"\nGreedy + 2-opt:")
    print(f"  Ruta: {ruta_opt}")
    print(f"  Costo: {costo_opt}")
    print(f"  Tiempo: {tiempo_opt:.4f} s")

# PROBAR
if __name__ == "__main__":
    comparar_algoritmos(9)  # Se puede cambiarle al valor., pero atender con el backtracking
#Situación	                                             Mejor opción
#Quieres una solución perfecta y el problema es pequeño	 Backtracking
#Quieres una solución rápido, sin importar la calidad	 Greedy
#Quieres una buena solución, rápida y razonable	         Greedy + 2-opt