#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 17:14:59 2020

@author: luismiguelescobarfalcon
"""

#Importar librerías
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

#Definición de funciones

#Visualizar grafo
def mostrarGrafo(npMatrizAdyacencia,diccionarioEtiquetas):
    #Construir nuestro grafo en networkx
    rows, cols = np.where(npMatrizAdyacencia > 0)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    nx.draw(gr, labels=diccionarioEtiquetas, with_labels=True, arrowsize=30) 
    plt.show() 
    
#Visualizar grafo
def mostrarDiGrafo(npMatrizAdyacencia,diccionarioEtiquetas):
    #Construir nuestro grafo en networkx
    rows, cols = np.where(npMatrizAdyacencia > 0)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.DiGraph()
    gr.add_edges_from(edges)
    nx.draw(gr, labels=diccionarioEtiquetas, with_labels=True, arrowsize=30) 
    plt.show() 

#Generar coordenadas graficables del camino (arcos solución)
def generarCoordenadasSolucion(coordenadasClientes,tour):
    tourX = []
    tourY = []
    for i in range(0,len(tour)-1):
        tourX.append(coordenadasClientes[ tour[i] ][1])
        tourX.append(coordenadasClientes[ tour[i+1] ][1])
        tourY.append(coordenadasClientes[  tour[i] ][2])
        tourY.append(coordenadasClientes[ tour[i+1] ][2])
        #i = i + 1
    #Agregar el retorno
    tourX.append(coordenadasClientes[ tour[-1] ][1])
    tourX.append(coordenadasClientes[ tour[0] ][1])
    tourY.append(coordenadasClientes[ tour[-1] ][2])
    tourY.append(coordenadasClientes[ tour[0] ][2])    
    return tourX,tourY

# Función para graficar solución
def dibujarSolucion(coordenadasClientes,tour,optimo=None):

    #Componente x de las coordenadas de los clientes
    componentesX = [i[1] for i in coordenadasClientes]

    #Componente y de las coordenadas de los clientes
    componentesY = [i[2] for i in coordenadasClientes]

    #Draw point based on above x, y axis values    
    plt.scatter(componentesX, componentesY, s=10)    
    
    
    #Generar coordenadas solucion
    coordenadasSolucionX,coordenadasSolucionY = generarCoordenadasSolucion(coordenadasClientes,tour)
    
    #Colocar etiquetas
    etiquetas = range(len(coordenadasClientes))
    #plt.text(componentesX, componentesX, etiquetas, fontsize=9)
    for et in etiquetas:
        plt.annotate(et, (coordenadasClientes[et][1] + 0.05, coordenadasClientes[et][2]))  # add labels            
        
    """plt.annotate(
        label,
        xy=(x, y), xytext=(-20, 20),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))"""
    
    #Salida de diagnóstico
    print("Coordenadas solución")
    print(coordenadasSolucionX,coordenadasSolucionY)    
    print(list(zip(coordenadasSolucionX,coordenadasSolucionY)))
    print("Coordenadas problema")
    print(coordenadasClientes)        
    
    #Dibujar camino si llega como parámetro
    if len(tour)>0 and optimo==None:
        plt.plot(coordenadasSolucionX,coordenadasSolucionY,linewidth=0.5)
    

    # Set chart title.
    plt.title("Caso TSP " + str(len(coordenadasClientes)) + " Clientes (Nodos)")    

    # Set x, y label text.
    plt.xlabel("Eje X")
    plt.ylabel("Eje Y")
    plt.show()


#Sección Principal
#-----------------


#Obtener información de archivo
#nombreArchivo = './eil51.tsp'
nombreArchivo = 'st70.tsp'


#Abrir el archivo
with open(nombreArchivo) as manejadorArchivo:
    coordenadasPuntos = []
    for linea_n in manejadorArchivo:    
        linea_n = linea_n.strip()
        linea_n = linea_n.split(' ')     
        if len(linea_n) == 3:           
                
            coordenadasPuntos.append( [ int(linea_n[0]), int(linea_n[1]), int(linea_n[2]) ] )  

numeroNodos = len(coordenadasPuntos)

#Construir matriz de adyacencia
matrizAdyacencia = []
for i in range(numeroNodos):
    matrizAdyacencia.append( [0] *  numeroNodos)

for i in range(numeroNodos):
    for j in range(numeroNodos):
        if i!=j:
            p_1 = [coordenadasPuntos[i][1], coordenadasPuntos[i][1]]
            p_2 = [coordenadasPuntos[j][1], coordenadasPuntos[j][1]]
            distanciaEuclidiana_p1_p2 = int(((p_1[0] - p_2[0])**2 + (p_1[1] - p_2[1])**2)**(1/2))
            matrizAdyacencia[i][j] = distanciaEuclidiana_p1_p2

#print(matrizAdyacencia) 

#Distancia euclidiana (consultar)
#p_1 = [34,56]
#p_2 = [33,88]
#distanciaEuclidiana_p1_p2 = int(((p_1[0] - p_2[0])**2 + (p_1[1] - p_2[1])**2)**(1/2))

#Parámetros de entrada (representación del problema)
'''matrizAdyacencia = [
                    [0,12,10,0,0,0,12],
                    [12,0,8,12,0,0,0],
                    [10,8,0,11,3,0,9],
                    [0,12,11,0,11,10,0],
                    [0,0,3,11,0,6,7],
                    [0,0,0,10,6,0,9],
                    [12,0,0,0,7,9,0]
                    
                    ]'''


#Distancia más corta entre nodos
#Distancia más larga
#Grado más alto entrelos nodos
#Nodo con el grado más alto

#Codificación de la solución
#[3,4,7,1,2,6,5] -> posible tour 
tour = []

#Constructivo del vecino más cercano TSP
#Nearest Neighbor

#Estructuras de control
nodosCubiertos = set()
nodosSinCubrir = set()
for i in range(numeroNodos):
    nodosSinCubrir.add(i)
    
#Inicializar en el primer nodo
nodoInicial = 0
nodosCubiertos.add(nodoInicial)
nodosSinCubrir.remove(nodoInicial)
tour.append(nodoInicial)

#Envolvente convexa más sencilla (triángulo)

#Desde el último elemento adicionado, revisar posibles saltos      
posiblesVerticesEnvolvente=[]
for i in range(numeroNodos):
    if matrizAdyacencia[ nodoInicial ][i] != 0 and i != nodoInicial:        
        posiblesVerticesEnvolvente.append( [ matrizAdyacencia[ nodoInicial ][i] , i ] )

#Ordenar por el criterio (más cercano o menor)
posiblesVerticesEnvolvente = sorted(posiblesVerticesEnvolvente, key=lambda x:x[0],reverse=True)

#Añadir a la solución
tour.append(posiblesVerticesEnvolvente[0][1])#Primera esquina más lejana de la envolvente
nodosCubiertos.add(posiblesVerticesEnvolvente[0][1])
nodosSinCubrir.remove(posiblesVerticesEnvolvente[0][1]) 
tour.append(posiblesVerticesEnvolvente[1][1])#Segunda esquina más lejana de la envolvente
nodosCubiertos.add(posiblesVerticesEnvolvente[1][1])
nodosSinCubrir.remove(posiblesVerticesEnvolvente[1][1])

#Mostrar tour por consola:
print('Estado envolvente:')
#print(tour)
print(list(map(lambda x:x+1,tour)))

#Mostrar envolvente convexa inicial
dibujarSolucion(coordenadasPuntos,tour)

#Criterio del constructivo
while(not(nodosSinCubrir == set())):

    #Una iteración de inserción
    listadoInserciones = []
    for i in range(len(tour)-1):
        
        #tour[i], tour[i+1]
        costoOriginalArista = matrizAdyacencia[ tour[i] ][ tour[i+1] ]   
        
        for k in nodosSinCubrir:
            costoInsercionK = 0
            costoInsercionK += matrizAdyacencia[ tour[i] ][ k ] 
            costoInsercionK += matrizAdyacencia[ k ][ tour[i+1] ]        
            diferenciaInsercion = costoInsercionK - costoOriginalArista
            
            #0 - A quién vamos a insertar
            #1 - Dónde lo vamos a insertar (posición)
            #2 - Calidad de la inserción (diferencia)
            listadoInserciones.append( [k, i+1, diferenciaInsercion] )
            
    #Inserciones en la arista de retorno (cierre del ciclo)
    costoOriginalArista = matrizAdyacencia[ tour[-1] ][ tour[0] ]   
    
    for k in nodosSinCubrir:
        costoInsercionK = 0
        costoInsercionK += matrizAdyacencia[ tour[-1] ][ k ] 
        costoInsercionK += matrizAdyacencia[ k ][ tour[0] ]        
        diferenciaInsercion = costoInsercionK - costoOriginalArista
        
        #0 - A quién vamos a insertar
        #1 - Dónde lo vamos a insertar (posición)
        #2 - Calidad de la inserción (diferencia)
        listadoInserciones.append( [k, 0, diferenciaInsercion] )
        
    #Ordenar todas las posibles inserciones
    listadoInserciones = sorted(listadoInserciones, key=lambda x:x[2])
    
    #Añadir a la solución
    tour.insert(listadoInserciones[0][1],listadoInserciones[0][0])#Primera esquina más lejana de la envolvente
    nodosCubiertos.add(listadoInserciones[0][0])
    nodosSinCubrir.remove(listadoInserciones[0][0]) 
    
    #Mostrar envolvente convexa inicial
    dibujarSolucion(coordenadasPuntos,tour)
    

#Función objetivo
fo = 0
for i in range(len(tour)-1):
    fo+= matrizAdyacencia[ tour[i] ][ tour[i+1] ]
fo+= matrizAdyacencia[ tour[-1] ][ tour[0] ]    
print()
print('Función Objetivo->',fo)
print(tour)

#Inserción más cercana 228
#Inserción más lejana 228



        

    
    
    














"""    
#Proceso de construcción
while(not(nodosSinCubrir == set())):
    
    #Desde el último elemento adicionado, revisar posibles saltos      
    posiblesSaltos=[]
    for i in range(numeroNodos):
        if matrizAdyacencia[ tour[-1] ][i] != 0 and not( i in nodosCubiertos ):
            posiblesSaltos.append( [ matrizAdyacencia[ tour[-1] ][i] , i ] )
    
    #Agregarle salida por el otro extremo
    if len(posiblesSaltos)==0:
        tour.reverse()
        continue
    
    #Ordenar por el criterio (más cercano o menor)
    posiblesSaltos = sorted(posiblesSaltos, key=lambda x:x[0],reverse=True)
    
    #Añadir a la solución
    tour.append(posiblesSaltos[-1][1])
    
    #Actualizar contenedores de control
    nodosCubiertos.add(posiblesSaltos[-1][1])
    nodosSinCubrir.remove(posiblesSaltos[-1][1])    

#Mostrar tour por consola:
print('Solución:')
print(tour)
print(list(map(lambda x:x+1,tour)))

dibujarSolucion(coordenadasPuntos,tour)

#Mostrar grafo o red original por plot
#Matriz de adyacencia numérica
npMatrizAdyacencia = np.asarray(matrizAdyacencia)
#Diccionario de etiquetas
diccionarioEtiquetas = {}
for i in range(numeroNodos):
    diccionarioEtiquetas.update( { i:i+1 } )    
mostrarGrafo(npMatrizAdyacencia, diccionarioEtiquetas)

#Mostrar solución o ciclo hamiltoniano
#Matriz de adyacencia únicamente de la solución
npMatrizAdyacenciaSolucion = np.zeros((numeroNodos,numeroNodos))
for i in range(0,len(tour)-1):
    npMatrizAdyacenciaSolucion[tour[i],tour[i+1]] = matrizAdyacencia[tour[i]][tour[i+1]]    
#npMatrizAdyacenciaSolucion[tour[-1],tour[0]] = matrizAdyacencia[tour[-1]][tour[0]]
npMatrizAdyacenciaSolucion[tour[-1],tour[0]] = 1
mostrarDiGrafo(npMatrizAdyacenciaSolucion, diccionarioEtiquetas)

"""
