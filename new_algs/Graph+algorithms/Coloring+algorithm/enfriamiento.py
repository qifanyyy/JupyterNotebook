import numpy as np
import time


def main(matrix, max_time, alpha=0.99, min_temp=0.001, optimo=0):
    '''
    Algoritmo de enfriamiento simulado para el problema del coloreado de mapas.

    matrix: matriz NxN simetrica con 1 en la diagonal principal que representa el grafo.
    max_time: maximo tiempo que el algoritmo ha de estar corriendo. 
    alpha: valor por el que se multiplica el alpha cada iteración.
    min_temp: valor mínimo para la temperatura antes de que el algoritmo pare.
    optimo: para benchmarks. si True, para el algoritmo una vez alcanzado el optimo.
    '''

    N = matrix.shape[0]
    best_sol = generate_solution(matrix)
    n_colores = len(set(best_sol)) - 1
    print('Colores usados por población generada: {}'.format(n_colores + 1))

    t2 = 0
    tiempos = []
    generar = True
    t1 = time.time()

    while t2 < max_time:
        
        if generar:
            sol = init_sol(N, n_colores)

        new_sol, new_fit, opt = enfriamiento(matrix, sol, min_temp, alpha)
        t2 = time.time() - t1 

        if opt: # Se ha alcanzado solucion para n_colores
            best_sol = new_sol
            n_colores = len(set(best_sol))
            print('Mejora. Colores usados: {} // Tiempo (s): {}'.format(n_colores, t2))
            tiempos.append((n_colores, t2))
            if n_colores == optimo:
                print('Óptimo alcanzado')
                break
            else:
                n_colores -= 1
                generar = True
        else:
            sol = new_sol
            generar = False

    return(best_sol, tiempos)

def init_sol(N, n_col):
    
    sol = list(np.random.randint(1, high=n_col + 1, size=N))
    return(sol)

def generate_solution(matrix):
    '''Inicializa una solución válida. matrix ha de ser np.array'''
    N = matrix.shape[0]

    # Miro que nodos tienen el máximo grado.
    # Almaceno sus índices en max_nodes
    vector_degrees = np.array([sum(row) for row in matrix])
    max_degrees = int(max(vector_degrees))
    max_nodes = [vector_degrees.argmax()]

    # Nodos con el número máximo de vecino
    if max_nodes[-1] + 1 != N:
        while vector_degrees[max_nodes[-1] + 1:].max() == max_degrees:
            max_nodes.append(
                vector_degrees[max_nodes[-1] + 1:].argmax() + max_nodes[-1] + 1)
            if max_nodes[-1] + 1 == N:
                break

    first_node = np.random.choice(max_nodes)
    colors_fn = list(range(1, max_degrees + 1))
    solution = list(np.zeros(N))

    # Coloreamos el nodo elegido y sus vecinos
    for i, nb in enumerate(matrix[first_node]):
        if nb == 1:
            solution[i] = np.random.choice(colors_fn)
            colors_fn.remove(solution[i])

    # Coloreamos los demás nodos
    for node, col_node in enumerate(solution):
        if col_node == 0:
            colors = list(range(1, max_degrees + 1))

            for k, nb in enumerate(matrix[node]):
                if nb == 1 and solution[k] != 0:
                    if solution[k] in colors:
                        colors.remove(solution[k])

            solution[node] = np.random.choice(colors)

    return(solution)


def fitness(matrix, solution):
    fit = 0
    for i in range(matrix.shape[0]):
        for j in range(i + 1, matrix.shape[1]):
            if matrix[i, j] == 1:
                if solution[i] == solution[j]:
                    fit += 1
    return(fit)


def enfriamiento(matrix, solution, min_temp, alpha):
    best_sol = solution
    best_fit = fitness(matrix, solution)
    fit = best_fit
    num_nodos = len(solution)
    temp = 1
    while temp > min_temp:

        colores = list(set(solution))
        new_solution = solution.copy()

        # Vecino
        nodo_cambio = np.random.choice(num_nodos)
        colores.remove(solution[nodo_cambio])
        color_cambio = np.random.choice(colores)
        new_solution[nodo_cambio] = color_cambio
        new_fit = fitness(matrix, new_solution)

        if new_fit == 0: # Return ya que hemos encontrado solución para n_colores
            return(new_solution, new_fit, True)
        else:
            if new_fit < fit: # Si la solución es mejor
                solution = new_solution
                fit = new_fit
                if new_fit < best_fit:
                    best_sol = solution
                    best_fit = fit
            else:
                if np.random.random() <= np.math.exp((fit - new_fit) / temp):
                    solution = new_solution
                    fit = new_fit

        temp *= alpha

    return(best_sol, best_fit, False)