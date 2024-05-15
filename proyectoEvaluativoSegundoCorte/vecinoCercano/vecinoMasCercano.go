package vecinoCercano

import "fmt"

func findNearestNeighbor(currentNode int, visited []int, costs [][]int) int {
    minDistance := int(^uint(0) >> 1) // max int value
    nearestNeighbor := -1

    for node := 0; node < len(costs); node++ {
        if node != currentNode && !contains(visited, node) {
            distance := costs[currentNode][node]
            if distance < minDistance {
                minDistance = distance
                nearestNeighbor = node
            }
        }
    }

    return nearestNeighbor
}

func contains(slice []int, val int) bool {
    for _, item := range slice {
        if item == val {
            return true
        }
    }
    return false
}

func travelingSalesman(nodes []string, costs [][]int) ([][2]int, int) {
    visited := []int{0} // Start at the first node
    currentNode := 0
    route := [][2]int{}
    totalCost := 0

    for len(visited) < len(nodes) {
        neighbor := findNearestNeighbor(currentNode, visited, costs)
        cost := costs[currentNode][neighbor]
        route = append(route, [2]int{currentNode, neighbor})
        visited = append(visited, neighbor)
        currentNode = neighbor
        totalCost += cost
    }

    // Add the last link to return to the starting point
    route = append(route, [2]int{visited[len(visited)-1], visited[0]})
    totalCost += costs[visited[len(visited)-1]][visited[0]]

    return route, totalCost
}

func main() {
    nodes := []string{"Pereira", "Armenia", "Medellín", "Cartago"}
    costs := [][]int{{0, 45, 60, 25},
                     {45, 0, 90, 50},
                     {60, 90, 0, 70},
                     {25, 50, 70, 0}}

    optimizedRoute, totalCost := travelingSalesman(nodes, costs)

    fmt.Println("Nodes:", nodes)
    fmt.Println("Cost matrix:")
    for _, row := range costs {
        fmt.Println(row)
    }

    fmt.Println("\nOptimized route:")
    for _, link := range optimizedRoute {
        point1, point2 := link[0], link[1]
        fmt.Printf("From %s to %s\n", nodes[point1], nodes[point2])
    }

    fmt.Printf("Total cost: %d\n", totalCost)
}