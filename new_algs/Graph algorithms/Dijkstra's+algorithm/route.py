#!/usr/bin/env python
# coding: utf-8

# Autor:   Ricardo Galiardi
# 
# Base:    Uso do algorítmo de Dijkstra (teoria dos Grafos)
#          Foram usadas peças de vários modelos já existentes
#          para elaboração do código.
#          
# Versões: Python 3.7
# 
# Arquivo: Arquivo util com rotinas para definição das rotas
#
# Regras:
#       * Como executar a aplicação;
#         
#       * Estrutura dos arquivos/pacotes;
#         Uso da biblioteca Pandas e Flask
#         
#       * Explique as decisões de design adotadas para a solução;
#         Foram usadas rotinas básicas de python e flask para aplicação
#         desse exercício. 
#         Python: foi utilizado para criação do código e aplicação da 
#         teoria dos gráfos aplicada ao algorítmo de Dijkstra
#         Flask: foi utilizado para criação dos endpoints rest para iteração
#         do usuário via interface web.
#         
#       * Descreva sua APÌ Rest de forma simplificada;
#         Com base no Flask para Python, a api utiliza duas rotinas básicas
#         uma para consulta da melhor rota dada uma partida e um destino.
#         E a segunda para adicionar uma nova rota a lista de rotas já existentes
#         importadas no inicio do programa.
# 

# Definição e importação das bibliotecas
import sys
import os
import re 
import pandas as pd
import collections
from collections import deque, namedtuple


# Definição das variáveis
global flights
global edges
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')

# Função para limpeza da tela
def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para carregar as rotas importadas
def read_routes(file):
    rows = pd.read_csv(file, sep=",")
    rows.dropna(inplace = True)   
    rows.apply(lambda x: x.astype(str).str.upper())
    
    return [tuple(x) for x in rows.itertuples(index=False)]


# Função para mapear as rotas importadas na variável das arestas
def make_edge(start, end, cost=1):
    return Edge(start, end, cost)


# Classe principal - Criação e gestão dos Grafos
# Funções e propriedades de consumo para montagem e manutenção do Grafo (Nós e Arestas)
class Graph:

    def __init__(self, edges):
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]

        if wrong_edges:
            raise ValueError('Dados incorretos da rota: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]
    
    @property
    def vertices(self):
        
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def get_node_pairs(self, source, dest, both_ends=True):
        source = source.upper()
        dest = dest.upper()

        if both_ends:
            node_pairs = [[source, dest], [dest, source]]
        else:
            node_pairs = [[source, dest]]
            
        return node_pairs

    def remove_edge(self, source, dest, both_ends=True):
        source = source.upper()
        dest = dest.upper()

        node_pairs = self.get_node_pairs(source, dest, both_ends)
        edges = self.edges[:]
        
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)
                return ('Rota de {} até {} removida com sucesso!'.format(source, dest))

        return ('Rota de {} até {} não encontrada!'.format(source, dest))

    def add_edge(self, source, dest, cost=1, both_ends=True):
        source = source.upper()
        dest = dest.upper()

        node_pairs = self.get_node_pairs(source, dest, both_ends)

        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ('Rota de {} até {} já existente!'.format(source, dest))

        self.edges.append(Edge(start=source, end=dest, cost=cost))
        
        if both_ends:
            self.edges.append(Edge(start=dest, end=source, cost=cost))

        return ('Rota de {} até {} incluída com sucesso!'.format(source, dest))

    def dijkstra(self, source, dest):
        source = source.upper()
        dest = dest.upper()
        
        assert source in self.vertices, 'Essa origem não existe!'
        distances = {vertex: inf for vertex in self.vertices}
        
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            
            if distances[current_vertex] == inf:
                break
                
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        distance = 0
        path, current_vertex = deque(), dest
        
        try:        
            while previous_vertices[current_vertex] is not None:
                path.appendleft(current_vertex)
                current_vertex = previous_vertices[current_vertex]

            if path:
                path.appendleft(current_vertex)

            for index in range(1, len(path)):
                for thing in self.edges:
                    if thing.start == path[index - 1] and thing.end == path[index]:
                        distance += thing.cost
        
            return ("A melhor rota é " + (" - ".join(list(collections.deque(path)))) + (" > ${0}").format(distance) + "") 

        except:
            return ('O aeroporto não tem voos para  {!r}'.format(current_vertex))

# Função para validar a entrada de dados
def inputvalid(regex, text):
    choice = re.match(regex, input(text).upper())

    if choice:
        return choice.string
    else:
        return None

def fieldvalid(regex, text):
    choice = re.match(regex, str(text).upper())

    if choice:
        return choice.string
    else:
        return None