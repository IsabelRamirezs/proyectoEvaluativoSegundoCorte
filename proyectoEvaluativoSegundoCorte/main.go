package main

import (
	"fmt"
	"math"
)

// Estructura para pasar mensajes entre goroutines
type Tarea struct {
	nodoActual int
	visitados  map[int]bool
	resultado  chan int
}

func vecinoMasCercano(t Tarea, costos [][]int) {
	distanciaMinima := math.MaxInt64
	vecinoCercano := -1

	for nodo := range costos {
		if nodo != t.nodoActual && !t.visitados[nodo] {
			dist := costos[t.nodoActual][nodo]
			if dist < distanciaMinima {
				distanciaMinima = dist
				vecinoCercano = nodo
			}
		}
	}
	t.resultado <- vecinoCercano
}

func metodoDelCartero(nodos []string, costos [][]int) ([][2]int, int) {
	visitados := make(map[int]bool)
	visitados[0] = true
	nodoActual := 0
	ruta := [][2]int{}
	costoTotal := 0

	for len(visitados) < len(nodos) {
		// Canal para recibir el resultado del vecino más cercano
		resultado := make(chan int)
		// Crear una tarea y lanzarla como una goroutine
		t := Tarea{nodoActual, visitados, resultado}
		go vecinoMasCercano(t, costos)

		// Esperar el resultado del vecino más cercano
		vecino := <-resultado
		costo := costos[nodoActual][vecino]
		ruta = append(ruta, [2]int{nodoActual, vecino})
		visitados[vecino] = true
		nodoActual = vecino
		costoTotal += costo
	}

	// Agrega el último enlace para volver al punto de partida
	ruta = append(ruta, [2]int{nodoActual, 0})
	costoTotal += costos[nodoActual][0]

	return ruta, costoTotal
}

func main() {
	nodos := []string{"Pereira", "Armenia", "Medellín", "Cartago"}
	costos := [][]int{
		{0, 45, 60, 25},
		{45, 0, 90, 50},
		{60, 90, 0, 70},
		{25, 50, 70, 0},
	}

	rutaOptimizada, costoTotal := metodoDelCartero(nodos, costos)

	fmt.Println("Nodos:", nodos)
	fmt.Println("Matriz de costos:")
	for _, fila := range costos {
		fmt.Println(fila)
	}

	fmt.Println("\nRuta optimizada:")
	for _, enlace := range rutaOptimizada {
		punto1, punto2 := enlace[0], enlace[1]
		fmt.Printf("De %s a %s\n", nodos[punto1], nodos[punto2])
	}

	fmt.Println("Costo total:", costoTotal)
}
