import sys

def vecino_mas_cercano(nodo_actual, visitados, costos):
    # Encuentra el vecino más cercano no visitado al nodo actual
    distancia_minima = sys.maxsize
    vecino_cercano = None

    for nodo in range(len(costos)):
        if nodo != nodo_actual and nodo not in visitados:
            dist = costos[nodo_actual][nodo]
            if dist < distancia_minima:
                distancia_minima = dist
                vecino_cercano = nodo
    
    return vecino_cercano

def metodo_del_cartero(nodos, costos):
    visitados = [0]  # Inicia en el primer nodo
    nodo_actual = 0
    ruta = []
    costo_total = 0

    while len(visitados) < len(nodos):
        vecino = vecino_mas_cercano(nodo_actual, visitados, costos)
        costo = costos[nodo_actual][vecino]
        ruta.append((nodo_actual, vecino))
        visitados.append(vecino)
        nodo_actual = vecino
        costo_total += costo

    # Agrega el último enlace para volver al punto de partida
    ruta.append((visitados[-1], visitados[0]))
    costo_total += costos[visitados[-1]][visitados[0]]

    return ruta, costo_total

# Ejemplo 1
nodos = ['Pereira', 'Armenia', 'Medellín', 'Cartago']
costos = [[0, 45, 60, 25],
          [45, 0, 90, 50],
          [60, 90, 0, 70],
          [25, 50, 70, 0]]

ruta_optimizada, costo_total = metodo_del_cartero(nodos, costos)

print("Nodos:", nodos)
print("Matriz de costos:")
for fila in costos:
    print(fila)

print("\nRuta optimizada:")
for enlace in ruta_optimizada:
    punto1, punto2 = enlace
    print("De", nodos[punto1], "a", nodos[punto2])

print("Costo total:", costo_total)


""" # Ejemplo 2 de uso
nodos = ['Pereira', 'Armenia', 'Manizales', 'Ibague', 'Medellín', 'Bogota']
costos = [[0, 31.78, 52.3, 64.95, 158.63, 180.99],
          [31.78, 0, 105, 90.2, 267, 282],
          [52.3, 105, 0, 176, 202, 303],
          [64.95, 90.2, 176, 0, 345, 203],
          [158.63, 267, 202, 345, 0, 444],
          [180.99, 282, 303, 203, 444, 0]]

ruta_optimizada, costo_total = metodo_del_cartero(nodos, costos)

print("Nodos:", nodos)
print("Matriz de costos:")
for fila in costos:
    print(fila)

print("\nRuta optimizada:")
for enlace in ruta_optimizada:
    punto1, punto2 = enlace
    print("De", nodos[punto1], "a", nodos[punto2])

print("Costo total:", costo_total) """