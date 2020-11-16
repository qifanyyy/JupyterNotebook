import numpy as np
import time

def main(matrix, max_time, max_iter=10000, max_pob=50, prob_mut=0.7, optimo=0):
    '''
    Algoritmo genético para el problema del coloreado de mapas.

    matrix: matriz NxN simetrica con 1 en la diagonal principal que representa el grafo.
    max_time: maximo tiempo que el algoritmo ha de estar corriendo. 
    max_iter: maximo de iteraciones antes de generar otra población.
    min_pob: tamaño de la población.
    optimo: para benchmarks. si True, para el algoritmo una vez alcanzado el optimo.
    '''
    
    N = matrix.shape[0]
    best_sol = generate_solution(matrix)
    n_colores = len(set(best_sol)) - 1
    print('Colores usados por población generada: {}'.format(n_colores + 1))
    max_iter_temp = max_iter
    tiempos = []
    t2 = 0
    t1 = time.time()

    while t2 < max_time:
        
        poblacion = init_pob(N, max_pob, n_colores)
        fit_poblacion = [fitness(matrix, p) for p in poblacion]
        mejora = False

        for i in range(max_iter_temp):

            best_fit = min(fit_poblacion)
            if best_fit > 4:
                p1, p2 = selection1(poblacion, fit_poblacion)
                hijo = cruce(p1, p2)
                hijo = mutacion1(hijo, matrix, prob_mut)
            else:
                p1, p2 = selection2(poblacion, fit_poblacion)
                hijo = cruce(p1, p2)
                hijo = mutacion2(hijo, matrix, prob_mut)

            fit_hijo = fitness(matrix, hijo)
            ncol_hijo = len(set(hijo))
            if fit_hijo == 0:
                mejora = True
                best_sol = hijo
                break
            else:
                poblacion.append(hijo)
                fit_poblacion.append(fit_hijo)
                        
            peor = np.argmax(fit_poblacion)
            poblacion.pop(peor)
            fit_poblacion.pop(peor)


        t2 = time.time() - t1
          
        if mejora:
            n_colores = len(set(best_sol))
            print('Mejora. Colores usados: {} // Tiempo (s): {}'.format(n_colores, t2))
            tiempos.append((n_colores, t2))
            max_iter_temp = max_iter
            if n_colores == optimo:
                print('Optimo alcanzado!')
                break
            else:
                n_colores -= 1
        else:
            max_iter_temp = max_iter*2

    return(best_sol, tiempos)


def init_pob(N, maxfs, n_col):
    '''Inicializa las primeras soluciones. matrix ha de ser np.array'''
    pob = []

    for i in range(maxfs):
        pob.append(list(np.random.randint(1, high=n_col + 1, size=N)))

    return(pob)


def fitness(matrix, solution):
    fit = 0
    for i in range(matrix.shape[0]):
        for j in range(i + 1, matrix.shape[1]):
            if matrix[i, j] == 1:
                if solution[i] == solution[j]:
                    fit += 1
    return(fit)


def selection1(m_sol, m_fit):
    tor = np.random.choice(len(m_sol), size=4, replace=False)
    
    # Padre 1
    if m_fit[tor[0]] < m_fit[tor[1]]:
        pad1 = m_sol[tor[0]]
    else:
        pad1 = m_sol[tor[1]] 

    # Padre 2
    if m_fit[tor[2]] < m_fit[tor[3]]:
        pad2 = m_sol[tor[2]]
    else:
        pad2 = m_sol[tor[3]]

    return(pad1, pad2)

def selection2(m_sol, m_fit):
    m2_fit = m_fit.copy()
    m2_sol = m_sol.copy()

    p1 = np.argmin(m2_fit)
    pad1 = m2_sol.pop(p1)
    m2_fit.pop(p1)
    p2 = np.argmin(m2_fit)
    pad2 = m2_sol.pop(p2)

    return(pad1, pad2)


def cruce(pad1,pad2):
    N = len(pad1)
    corte = np.random.randint(1, high=N+1)
    hijo = pad1[:corte] + pad2[corte:]    
    return(hijo)


def mutacion1(hijo, matrix, prob_mut):
    if np.random.random() <= prob_mut:
        for i in range(len(hijo)):
            adj_colors = []
            for j, other_node in enumerate(matrix[i,:]):
                if j != i and other_node == 1:
                    if hijo[j] not in adj_colors:
                        adj_colors.append(hijo[j])

            if hijo[i] in adj_colors:
                valid_colors = list(set(hijo))            
                for adj_c in adj_colors:
                    if adj_c in valid_colors:
                        valid_colors.remove(adj_c)
                
                if valid_colors:
                    hijo[i] = np.random.choice(valid_colors)

    return(hijo)

def mutacion2(hijo, matrix, prob_mut):
    all_colors = list(set(hijo))    
    if np.random.random() <= prob_mut:
        for i in range(len(hijo)):
            for j, other_node in enumerate(matrix[i,:]):
                if i != j and other_node == 1:
                    if hijo[i] == hijo[j]:
                        hijo[i] = np.random.choice(all_colors)
                        break
                        
    return(hijo)

def generate_solution(matrix):
    N = matrix.shape[0]

    # Miro que nodos tienen el máximo grado.
    # Almaceno sus índices en max_nodes
    vector_degrees = np.array([sum(row) for row in matrix])
    max_degrees = int(vector_degrees.max())
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
