package main

import (
	"bufio"
	"fmt"
	"image/color"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"

	"gonum.org/v1/gonum/graph"
	"gonum.org/v1/gonum/graph/simple"
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/vg"
)

// Cliente representa un cliente con coordenadas.
type Cliente struct {
	id int
	x  float64
	y  float64
}

// Crear grafo desde matriz de adyacencia
func crearGrafo(matrizAdyacencia [][]int) *simple.WeightedGraph {
	gr := simple.NewWeightedGraph()
	for i := range matrizAdyacencia {
		for j := range matrizAdyacencia[i] {
			if matrizAdyacencia[i][j] > 0 {
				gr.SetWeightedEdge(gr.NewWeightedEdge(simple.Node(i), simple.Node(j), float64(matrizAdyacencia[i][j])))
			}
		}
	}
	return gr
}

// Visualizar grafo
func mostrarGrafo(matrizAdyacencia [][]int, etiquetas map[int]string) {
	gr := crearGrafo(matrizAdyacencia)
	p := plot.New()
	p.Title.Text = "Grafo"
	nodes := make(plotter.XYs, gr.Nodes().Len())
	for i := range nodes {
		nodes[i].X = float64(i)
		nodes[i].Y = float64(i)
	}
	scatter, _ := plotter.NewScatter(nodes)
	scatter.GlyphStyle.Radius = vg.Points(3)
	scatter.GlyphStyle.Color = color.RGBA{R: 255, G: 0, B: 0, A: 255}
	p.Add(scatter)
	for _, n := range gr.Nodes() {
		label := etiquetas[int(n.ID())]
		p.X.Label.Text = label
		p.Y.Label.Text = label
	}
	if err := p.Save(4*vg.Inch, 4*vg.Inch, "grafo.png"); err != nil {
		log.Fatalf("could not save plot: %v", err)
	}
}

// Generar coordenadas del tour
func generarCoordenadasSolucion(coordenadasClientes []Cliente, tour []int) ([]float64, []float64) {
	var tourX, tourY []float64
	for i := 0; i < len(tour)-1; i++ {
		tourX = append(tourX, coordenadasClientes[tour[i]].x, coordenadasClientes[tour[i+1]].x)
		tourY = append(tourY, coordenadasClientes[tour[i]].y, coordenadasClientes[tour[i+1]].y)
	}
	tourX = append(tourX, coordenadasClientes[tour[len(tour)-1]].x, coordenadasClientes[tour[0]].x)
	tourY = append(tourY, coordenadasClientes[tour[len(tour)-1]].y, coordenadasClientes[tour[0]].y)
	return tourX, tourY
}

// Dibujar solución
func dibujarSolucion(coordenadasClientes []Cliente, tour []int, optimo ...float64) {
	p := plot.New()
	p.Title.Text = "Solución TSP"
	p.X.Label.Text = "Eje X"
	p.Y.Label.Text = "Eje Y"

	points := make(plotter.XYs, len(coordenadasClientes))
	for i, cliente := range coordenadasClientes {
		points[i].X = cliente.x
		points[i].Y = cliente.y
	}

	scatter, err := plotter.NewScatter(points)
	if err != nil {
		log.Fatalf("could not create scatter: %v", err)
	}
	scatter.GlyphStyle.Radius = vg.Points(3)
	scatter.GlyphStyle.Color = color.RGBA{B: 255, A: 255}

	p.Add(scatter)

	coordenadasSolucionX, coordenadasSolucionY := generarCoordenadasSolucion(coordenadasClientes, tour)
	tourPoints := make(plotter.XYs, len(coordenadasSolucionX))
	for i := range tourPoints {
		tourPoints[i].X = coordenadasSolucionX[i]
		tourPoints[i].Y = coordenadasSolucionY[i]
	}

	line, err := plotter.NewLine(tourPoints)
	if err != nil {
		log.Fatalf("could not create line: %v", err)
	}
	line.LineStyle.Width = vg.Points(1)
	line.LineStyle.Color = color.RGBA{R: 255, A: 255}

	p.Add(line)

	if err := p.Save(6*vg.Inch, 6*vg.Inch, "solucion.png"); err != nil {
		log.Fatalf("could not save plot: %v", err)
	}
}

func leerArchivo(nombreArchivo string) ([]Cliente, int) {
	file, err := os.Open(nombreArchivo)
	if err != nil {
		log.Fatalf("no se pudo abrir el archivo: %v", err)
	}
	defer file.Close()

	var coordenadasClientes []Cliente
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		linea := scanner.Text()
		partes := strings.Fields(linea)
		if len(partes) == 3 {
			id, _ := strconv.Atoi(partes[0])
			x, _ := strconv.ParseFloat(partes[1], 64)
			y, _ := strconv.ParseFloat(partes[2], 64)
			coordenadasClientes = append(coordenadasClientes, Cliente{id: id, x: x, y: y})
		}
	}
	return coordenadasClientes, len(coordenadasClientes)
}

func construirMatrizAdyacencia(coordenadasClientes []Cliente) [][]int {
	numeroNodos := len(coordenadasClientes)
	matrizAdyacencia := make([][]int, numeroNodos)
	for i := range matrizAdyacencia {
		matrizAdyacencia[i] = make([]int, numeroNodos)
		for j := range matrizAdyacencia[i] {
			if i != j {
				distanciaEuclidiana := int(math.Hypot(coordenadasClientes[i].x-coordenadasClientes[j].x, coordenadasClientes[i].y-coordenadasClientes[j].y))
				matrizAdyacencia[i][j] = distanciaEuclidiana
			}
		}
	}
	return matrizAdyacencia
}

func vecinoMasCercano(matrizAdyacencia [][]int, numeroNodos int) []int {
	tour := []int{0}
	nodosSinCubrir := make(map[int]struct{})
	for i := 1; i < numeroNodos; i++ {
		nodosSinCubrir[i] = struct{}{}
	}
	for len(nodosSinCubrir) > 0 {
		nodoActual := tour[len(tour)-1]
		masCercano := -1
		distanciaMinima := math.MaxInt64
		for nodo := range nodosSinCubrir {
			if matrizAdyacencia[nodoActual][nodo] < distanciaMinima {
				distanciaMinima = matrizAdyacencia[nodoActual][nodo]
				masCercano = nodo
			}
		}
		delete(nodosSinCubrir, masCercano)
		tour = append(tour, masCercano)
	}
	return tour
}

func main() {
	// Leer archivo y obtener coordenadas
	nombreArchivo := "st70.tsp"
	coordenadasClientes, numeroNodos := leerArchivo(nombreArchivo)

	// Construir matriz de adyacencia
	matrizAdyacencia := construirMatrizAdyacencia(coordenadasClientes)

	// Mostrar grafo
	etiquetas := make(map[int]string)
	for _, cliente := range coordenadasClientes {
		etiquetas[cliente.id-1] = fmt.Sprintf("%d", cliente.id)
	}
	mostrarGrafo(matrizAdyacencia, etiquetas)

	// Aplicar algoritmo del vecino más cercano
	tour := vecinoMasCercano(matrizAdyacencia, numeroNodos)

	// Mostrar tour resultante
	fmt.Println("Tour encontrado:", tour)

	// Dibujar solución
	dibujarSolucion(coordenadasClientes, tour)
}
