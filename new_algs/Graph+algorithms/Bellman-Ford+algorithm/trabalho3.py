#!/usr/bin/python

# DANIEL GOBBI BERGHOLZ 16/0004551
# TRABALHO 3 FUNDAMENTOS DE REDES 1

# o codigo a seguir foi feito sob o efeito de muita pressao e cafeina
# nao recomendo mexer em nada, so deus sabe como isso tudo aqui funciona

from igraph import *
import os, re

# variavel global para ir armazenando decisoes do usuario 
n = 0

# variaveis globais do grafo
g = Graph() 
vertices = []
arestas = []
pesos = []

'''
g.add_vertices(4)
g.add_edges([(0,1), (1,2), (0,2), (2,3)])
g.vs["name"] = ["v0", "v1", "v2", "v3"]
g.es["weight"] = [1,2,3,4]

# plotar grafo
g.vs["label"] = g.vs["name"]
g.es["label"] = g.es["weight"]

layout = g.layout("kk")

print (g)
plot(g, layout = layout)
'''

# ----------------------------------------------------------------------MENU-----------------------------------------------
def menu(primeira_vez=True):
    global n  
    if (primeira_vez == True):
        os.system('clear')
        print ('Seja bem vindo ao meu programa que simula grafos\n')
    print ('\nA SEGUIR OS ALGORITMOS DISPONIVEIS:\n')
    print ('1) Dijkstra\n2) Bellman-Ford\n3) RPF\n4) Spanning Tree\n5) SAIR')
    n = input('Por favor, selecione um algoritmo que vc gostaria de executar:\n')
    while (n < 1 or n > 5):
        n = input('Escolha um numero valido (entre 1 e 5):\n')

def ler_dot():
    lista = []
    vertices_aux = []
    n_vertices = 0
    global vertices 
    global arestas
    global pesos
    global g
    g = Graph()
    vertices = []
    arestas = []
    pesos = []

    # abrir arquivo do usuario e ler cada linha 
    x = raw_input('Por favor digite o nome do arquivo: (eh preciso ter .dot no final e o PATH adequado)\n')
    file = open(x, 'r')
    linhas = file.readlines()
    pattern = '\w+\.*\w*'

    # lista = variavel que guarda par de vertices que possuem aresta
    # comeca a ler da linha 1 ao inves da 0, pois a linha zero contem o nome do grafo
    for i in range(1, len(linhas)): 
        lista.append(re.findall(pattern, linhas[i]))

    # apos o regex, temos de deletar o 'label' e salvar o peso da aresta
    for i in range(len(lista)):
        if (len(lista[i]) == 4):
            lista[i].remove('label')
            pesos.append(float(lista[i][2]))
            del lista[i][2]

    # lista = lista de listas. vertices = lista
    for sublista in lista:
        for item in sublista:
            vertices.append(item)

    # caso haja qualquer item vazio, eliminar da lista
    # repetir isso ate que nao haja mais item nenhum vazio
    while True:
        try:
            vertices.remove('')
        except ValueError:
            break 

    # agora iremos adicionar as arestas no grafo
    tupla = ()
    for i in range(0, len(vertices), 2):
        tupla = (vertices[i], vertices[i+1])
        arestas.append(tupla)

    # loop para eliminar duplicatas na lista "vertices"
    for i in vertices:
        if i not in vertices_aux:
            vertices_aux.append(i)
    vertices = vertices_aux

    # finalmente, vertices se tornou uma lista "limpa"
    n_vertices = len(vertices)
    g.add_vertices(n_vertices)
    g.vs["name"] = vertices
    g.add_edges(arestas)
    g.es["weight"] = pesos
    file.close()

def criar_grafo():
    print  ('Agora iremos criar seu grafo de testes\n')
    y = raw_input('Voce gostaria de carregar um grafo a partir de um arquivo .DOT? (s/n)\n')
    if (y == 's'):
        ler_dot()
    else:
        global g
        g = Graph()
        vertices = []
        arestas = []
        while True:
            try:
                x = input('Quantos vertices tem seu grafo?\n')
            except SyntaxError:
                print ('Voce somente apertou ENTER. Por favor, digite um numero valido\n')
                continue
            break
        g.add_vertices(x)
        lista = [] # lista auxiliar
        for i in range(g.vcount()):
            lista.append("v" + str(i))
        g.vs["name"] = lista
        lista = []
        print ('Agora iremos construir as arestas deste grafo\nPara parar de criar arestas basta nao digitar valor e apertar enter\n')
        while True: 
            try:
                y, z = input('Escreva um vertice de origem e um de destino (dois valores separados por virgula)\n')
            except SyntaxError:
                y = z = None
            if ((y != None) and (z != None)):
                if((y > (g.vcount() - 1)) or ((z > (g.vcount() - 1)))):
                    print ('Voce digitou um numero invalido de vertice. Seu grafo tem ' + str(g.vcount()) + ' vertices.\n')
                else:
                    g.add_edges([(y, z)])
                    w = input('Qual o peso desta aresta?\n')
                    lista.append(w)
            else:
                g.es["weight"] = lista
                break
    g.vs["label"] = g.vs["name"]
    g.es["label"] = g.es["weight"]
    layout = g.layout("kk")
    print ('Grafo criado com sucesso!')
    plot(g, layout=layout)


# ------------------------------------------------------------FUNCOES-DOS-ALGORITMOS-----------------------------------------------

# caso o professor queira checar o recultado do algoritmo alguma outra hora, eh possivel salvar os resultados gerados 
def salvar(grafo, nome_do_arquivo, layout_do_grafo, raiz = []):
    x = raw_input('O senhor gostaria de salvar o resultado que o programa acabou de mostrar? (s/n)\n')
    if x.lower() == 's':
        if not raiz:
            plot(grafo, nome_do_arquivo, layout = layout_do_grafo)
        else: 
            plot(grafo, nome_do_arquivo, layout = layout_do_grafo, root = raiz)

        print ('Arquivo salvo com sucesso!\nNome do arquivo: ' + nome_do_arquivo + '\n')


# descobrir os vizinhos de um vertice e salvar na variavel adjacentes
def vizinhos(arestas, vertice, primeira_vez = False):
    aux = []
    predecessor = {}
    adjacentes = {}
    for i in range(len(arestas)):
        for j in range(2):
            if(arestas[i][j] == vertice):
                if(j == 1):
                    predecessor[arestas[i][0]] = arestas[i]
                    aux.append(arestas[i])
                elif (j == 0):
                    aux.append(arestas[i])
                    predecessor[arestas[i][1]] = arestas[i]
    adjacentes[vertice] = aux
    if (primeira_vez == True):
        return predecessor, adjacentes
    if (primeira_vez == False):
        return adjacentes

# ----------------------------------------------------------------------ALGORITMOS-----------------------------------------------
# caso queira, pode retornar a arvore gerada pelo dijkstra
def dijkstra(no_inicial = '', no_final = '', quer_somente_o_resultado = False, so_mensagem = False): # DIJKSTRA -----------------
    global g
    global vertices
    global arestas
    global pesos
    v_visitados = []
    predecessor = {}
    custo = {}
    menor_custo = {}
    adjacentes = {}

    # mensagem de boas vindas / relembrar quais vertices existem no grafo
    if quer_somente_o_resultado == False:
        no_inicial = ''
        no_final = ''
        print ('\nVoce selecionou o algoritmo de DIJKSTRA\nA seguir o nome dos vertices do seu grafo:\nV = {',)
        for i in range(len(vertices)):
            if (i < len(vertices)-1):
                print (vertices[i] + ', ',)
            else:
                print (vertices[i] + ' }')

    # loop para selecionar vertice raiz e destino
        while True:
            no_inicial = raw_input('Qual sera o seu no inicial(Raiz)?\n')
            no_final = raw_input('E o seu no final?\n')
            if ((no_inicial not in vertices) or (no_final not in vertices)):
                print ('Por favor, digite um vertice que realmente exista no grafo\nA seguir os vertices do seu grafo:\nV = {',)
                for i in range(len(vertices)):
                    if (i < len(vertices)-1):
                        print (vertices[i] + ', ',)
                    else:
                        print (vertices[i] + ' }')
            else:
                break

    # inicializando o dijkstra
    v_visitados.append(no_inicial)
    menor_custo[no_inicial] = 0
    for i in range(len(arestas)):
        custo[arestas[i]] = pesos[i]
    predecessor, adjacentes =  vizinhos(arestas, no_inicial, True)
    dict = {}
    for v in vertices:
        if (v not in predecessor) and (v != no_inicial):
            menor_custo[v] = 999
        if v in predecessor:
            menor_custo[v] = custo[predecessor[v]]

    # salva em adjacentes todas as arestas que sao adjacentes em cada vertice
    for v in vertices:
        dict = vizinhos(arestas, v)
        adjacentes.update(dict)
   
    # agora comecando de verdade o algoritmo
    predecessor_aux = {}
    falta_vertice = True
    while True:
        for p in predecessor:
            for a in adjacentes[p]:
                if (a != predecessor[p]):
                    for tupla in a:
                        if (tupla != p):
                            if ((menor_custo[p] + custo[a]) < menor_custo[tupla]):
                                aux =  menor_custo[p] + custo[a]
                                aux2 = aux%(int(aux))
                                if ((aux2 > 0.09) and (aux2 < 0.1)):
                                    aux = int(aux) + 0.1
                                elif (aux2 < 0.009): 
                                    aux = int(aux)
                                menor_custo[tupla] = aux
                                predecessor_aux[tupla] = a
        predecessor.update(predecessor_aux)
        falta_vertice = False
        for v in vertices:
            if v not in predecessor:
                if(v != no_inicial):
                    falta_vertice = True
        if falta_vertice == False:
            break

    # printar na tela o menor caminho e o menor custo
    aux = []
    cont = 0
    cabou = False
    if so_mensagem == True or (quer_somente_o_resultado == False and so_mensagem == False):
        print ('O menor caminho entre ' + no_inicial + ' e ' + no_final + ' eh: ',)
    aux.append(no_final)
    while cabou == False:
        for tupla in predecessor[aux[cont]]:
            if (tupla == no_inicial):
                cabou = True
            if (tupla != aux[cont]):
                aux.append(tupla)
                a = cont + 1
        cont = a
    aux = aux[::-1]

    if so_mensagem == True or (quer_somente_o_resultado == False and so_mensagem == False):
        for i in range(len(aux)):
            if (i == (len(aux)-1)):
                print (aux[i])
            else:
                print (aux[i] + ' -> ',)
        print ('Com o custo total de: ' + str(menor_custo[no_final]))
        if (quer_somente_o_resultado == False and so_mensagem == False):
            print ('A seguir a arvore de caminho minimo criada pelo DIJKSTRA:')

    # printar arvore criada para o dijkstra
    t = Graph()
    t.add_vertices(len(vertices))
    arestas_final = []
    lista = []
    for p in predecessor:
        if quer_somente_o_resultado == False:
            arestas_final.append(predecessor[p])
            lista.append(custo[predecessor[p]])
        elif quer_somente_o_resultado == True:
            if p in aux:
                arestas_final.append(predecessor[p])
                lista.append(custo[predecessor[p]])
    t.vs["name"] = vertices
    t.add_edges(arestas_final)
    t.es["weight"] = lista
    t.vs["label"] = t.vs["name"]
    t.es["label"] = t.es["weight"]
    cont = 0
    for v in vertices:
        if(v == no_inicial):
            break
        cont = cont + 1
    lista = []
    lista.append(cont)
    layout = t.layout("tree", root = lista)
    if quer_somente_o_resultado == False:
        plot(t, layout=layout)
        salvar(t, 'dijkstra.png', 'tree', lista)
    elif quer_somente_o_resultado == True and so_mensagem == False:
        return t

# o algoritmo usado na spanning tree foi o de Kruskal
def spanning_tree(): # SPANNING TREE --------------------------------------------------------------------------------------------
    global vertices
    global arestas
    global pesos
    antes = {} # aresta: peso
    
    print ('\nBem vindo ao algoritmo do SPANNING TREE\nIremos gerar uma arvore de custo minimo a partir do grafo que voce escolheu')
    v_raiz = ['kk eae men']
    while v_raiz not in vertices:
        if v_raiz != ['kk eae men']:
            print ('Por favor, digite um vertice valido\nA seguir os vertices do seu grafo:\nV = { ',)
            for v in vertices:
                if v != vertices[-1]:
                    print (v + ', ',)
                else:
                    print (v + ' }')
        v_raiz = raw_input('Qual sera o seu vertice raiz?\n')

    # ordenar os pesos em ordem crescente  
    for i in range(len(arestas)):
        antes[arestas[i]] = pesos[i]
    menor_pesos = pesos
    menor_pesos.sort()
    menor_arestas = []
    for p in menor_pesos:
        for a in arestas:
            if(antes[a] == p):
                menor_arestas.append(a)

    # inicializando o grafo DE TESTES
    t = Graph()
    t.add_vertices(len(vertices))
    t.vs["name"] = vertices
    
    # ja adicionar as arestas do vertice raiz no grafo
    aux3 = []
    aux4 = []
    aux = t.neighbors(v_raiz)
    for i in range(len(menor_arestas)):
        for a in menor_arestas[i]:
            if a in aux:
                aux3.append(menor_arestas[i])
                aux4.append(menor_pesos[i])
                del menor_arestas[i]
                del menor_pesos[i]
    for i in range(len(aux3)):
        menor_arestas.insert(0, aux3[i])
        menor_pesos.insert(0, aux4[i])

    # comecar o algoritmo de kruskal
    aux = menor_arestas
    aux2 = menor_pesos
    cont = 0
    n_arestas = 0
    while (n_arestas < (len(vertices)-1)):
        lista = []
        lista.append(aux[cont])
        t.add_edges(lista)
        if (t.cohesion() > 1):
            t.delete_edges(lista)
            del aux[cont]
            del aux2[cont]
        else:
            cont = cont + 1
            n_arestas = n_arestas + 1

    # inicializando o grafo FINAL e salvando arquivo
    t.es["weight"] = aux2
    t.vs["label"] = t.vs["name"]
    t.es["label"] = t.es["weight"]

    # calculando o custo total da arvore gerada
    custo_total = 0
    for tzin in t.es["weight"]:
        custo_total = custo_total + tzin
    
    print ('A seguir a sua arvore gerada a partir do Spanning Tree algorithm!')
    print ('Que tem custo total = ' + str(custo_total))
    plot(t, layout = "kk")
    salvar(t, "spanning_tree.png", "kk")

# algoritmo que constroi arvore a partir dos menores caminhos entre os vertices
def rpf(): # RPF ----------------------------------------------------------------------------------------------------------------
    global g
    global vertices
    global arestas
    global pesos
    custo = {} # aresta: peso
    arestas2 = []

    # criar o dicionario do custo
    for i in range(len(arestas)):
        custo[arestas[i]] = pesos[i]
        custo[arestas[i][::-1]] = pesos[i]

    # loop para selecionar vertice raiz e destino
    print ('\nBem vindo ao algoritmo RPF')
    while True:
        print ('A seguir os vertices do seu grafo:\nV = {',)
        for i in range(len(vertices)):
            if (i < len(vertices)-1):
                print (vertices[i] + ', ',)
            else:
                print (vertices[i] + ' }')
        no_inicial = raw_input('Qual sera o seu no inicial(Raiz)?\n')
        if no_inicial not in vertices:
            print ('Por favor, digite um vertice que realmente exista no grafo\n')
        else:
            break
    grafos = []
    for v in vertices:
        if v != no_inicial:
            grafos.append(dijkstra(no_inicial, v, True))

    aux = Graph()
    for graf in grafos:
        aux = aux + graf
    print ('A seguir a sua arvore gerada a partir do Reverse Path Fowarding!')
    aux.vs["name"] = vertices
    aux.vs["label"] = aux.vs["name"]

    # deletar todos os vertices que vieram sem aresta: degree = 0
    cont = []
    for i in range(len(aux.vs)):
        if aux.degree(aux.vs[i]) == 0:
            cont.append(i)
    i = len(cont) - 1
    while i >= 0:
        aux.delete_vertices(cont[i])
        i = i -1


    # deletar todos os vertices que sao o no_inicial
    a = []
    cont = []
    for i in range(len(aux.vs)):
        if aux.vs[i]["name"] == no_inicial:
            cont.append(i)
    i = len(cont) - 1
    while i >= 0:
        a.append(aux.incident(cont[i])[0])
        aux.delete_vertices(cont[i])
        i = i -1

    # criar a arvore final a partir de tudo isso
    g = Graph()
    g = g or aux
    g.add_vertices(no_inicial)
    g.vs[g.vcount()-1]["label"]=g.vs[g.vcount()-1]["name"]
    for azin in a:
        g.add_edges([(azin, no_inicial)])    
    for e in g.es:
        arestas2.append((g.vs[e.source]["name"], g.vs[e.target]["name"]))
    pesos2 = []
    for a in arestas2:
        pesos2.append(custo[a])
    g.es["weight"] = pesos2
    g.es["label"] = g.es["weight"]
    raiz = []
    raiz.append(no_inicial)
    print ('A arvore a seguir mostra o menor caminho entre ' + no_inicial + ' e todos os outros vertices do grafo')

    # printar na tela o menor caminho entre todos os vertices
    for v in vertices:
        if v != no_inicial:
            dijkstra(no_inicial, v, True, True)

    plot(g, layout = "tree", root = raiz)
    salvar(g, "rpf.png", "tree", raiz)

# ----------------------------------------------------------------------ALGORITMOS-----------------------------------------------
def bellman_ford(): # BELLMAN-FORD ----------------------------------------------------------------------------------------------
    global g # Graph
    global vertices # string 
    global arestas # (vertice1, vertice2)
    global pesos # int 
    custo = {} # aresta: peso
    vizinhos = {} # vertice: [aresta1, aresta2 ...]
    matriz = [] # matriz do algoritmo de bellman-ford 
    indent = {} # int : vertice / indentificador do vertice

    print ('\nBem vindo ao algoritmo Bellman-Ford!')
    print ('A seguir sera gerada uma tabela que contem o caminho minimo entre cada vertice')

    # criar o dicionario do custo
    for i in range(len(arestas)):
        custo[arestas[i]] = pesos[i]
        #custo[arestas[i][::-1]] = pesos[i]

    # adicionar os vizinhos de cada vertice na variavel "vizinhos"
    for v in vertices:
        lista = []
        for a in arestas:
            for i in range(2):
                if a[i] == v:
                    lista.append(a)
        vizinhos[v] = lista

    # achar o numero (indentificador) de cada vertice e salvar na variavel "indent"
    # na moral que esse pedaco de codigo nao serve pra absolutamente nada 
    cont = 0
    for gzin in g.vs["name"]:
        for v in vertices:
            if v == gzin:
                indent[cont] = v
        cont = cont + 1
    
    # preenchendo a matriz pela primeira vez / com os custos dos vizinhos somente
    for i in range(g.vcount()):
        linha = []
        for j in range(g.vcount()):
            if j in g.neighbors(i):
                for a in vizinhos[indent[i]]:
                    if g.vs["name"][j] in a:
                        linha.append(custo[a])
            elif j == i:
                linha.append(0) # o custo so eh zero quando o vertice for ele mesmo
            else:
                linha.append(999) # 999 = INFINITO
        matriz.append(linha)

    # o algoritmo propriamente dito
    cabou = False
    while cabou == False: 
        cabou = True
        for i in range(g.vcount()):
            for j in range(g.vcount()): # percorrer toda a matriz
                if matriz[i][j] != 0: # se != 0, significa que o elemento eh vizinho do vertice
                    D = []
                    D.append(matriz[i][j]) # adicionar custo deste vizinho
                    offset = 0
                    while offset < g.vcount():
                        if (matriz[offset][j] != 0 and matriz[offset][j] != 999):
                            if matriz[i][offset] != 0 and matriz[i][offset] != 999:
                                D.append(matriz[i][offset] + matriz[offset][j])
                        offset = offset +1
                    D_min = min(D)
                    if D_min < matriz[i][j]:
                        matriz[i][j] = D_min
                        cabou = False

    # printando em formato de tabela
    print ('\nTABELA DE CAMINHOS MINIMOS\n')
    print ('    | ',)
    for v in vertices:
        print (v + '  | ',)
    print ('')
    print ('-----------------------------------------------')
    cont = 0
    for M in matriz:
        print (vertices[cont] + '  | ',)
        for m in M:
            x = str(m)
            if len(x) == 2:
                print (x + '  | ',)
            elif len(x) == 3:
                print (x + ' | ',)
            elif len(x) == 1:
                print (x + '   | ',)
        print ('')
        cont = cont + 1

    '''
    # printar na tela o menor caminho entre todos os vertices
    for v1 in vertices:
        for v in vertices:
            if v != v1:
                dijkstra(v1, v, True, True)
    print 'A seguir a tabela final de caminhos minimos desta rede:\n'
    plot(g, layout = "tree", root = raiz)
    '''

# ----------------------------------------------------------------------MAIN-----------------------------------------------------
def main():
    menu()
    while (n != 5):
        criar_grafo()
        if (n == 1):
            dijkstra()
        elif n == 2:
            bellman_ford()
        elif n == 3:
            rpf()
        elif n == 4:
            spanning_tree()
        menu(False)

if __name__ == "__main__":
    main()








