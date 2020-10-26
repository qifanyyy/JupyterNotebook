#
#  generate_graphs.py
#  P2
#
#  Created by Filipe Araujo on 5/1/10.
#  Copyright (c) 2010 Universidade de Coimbra. All rights reserved.
#
import random
import sys

def generate_ring(nodes):
	print nodes   #nodes
	print nodes   #edges
	for i in xrange(nodes):
		if i != nodes - 1:
			print i, i + 1
		if i == 0:
			print i, nodes - 1
	
					
def generate_crown(halfnodes):
	print 2 * halfnodes
	print halfnodes * (halfnodes - 1)
	for i in xrange(halfnodes):
		a = 2 * i
		for j in xrange(halfnodes):
			b = 2 * j + 1
			if (i != j):
				print a, b
				
				
# Para grafos muito grandes tem de ser melhorado.
# O problema e que nao sabemos de antemao quantas 
# arestas vamos ter.
# O grafo pode sair desconexo
def generate_random_graph(nodes, p):
	list_edges = []
	for i in xrange(nodes):
		for j in range(i + 1, nodes, 1):
			rand_nbr = random.random()
			if rand_nbr < p:
				list_edges.append(str(i) + " " + str(j))
	print nodes
	print len(list_edges)
	for s in list_edges:
		print s
			

# m - x
# n - y
# p - z
def generate_grid(m, n, p):
	print n * m * p
	edges = p * ((m - 1) * n + (n - 1) * m) + (p - 1) * m * n
	print edges
	num = 0
	for z in range(0, p, 1):
		for y in range(0, n, 1):
			for x in range(0, m, 1):
				id = z * (m * n) + y * m + x
				if x < m - 1:
					print id, id + 1
					num += 1
				if y < n - 1:
					print id, id + m
					num += 1
				if z < p - 1:
					print id, id + (m * n)
					num += 1
	if num != edges:
		sys.stderr.write("A culpa deste erro e do professor...")
		


def little_test():
	generate_ring(40)
	print
	generate_crown(3)
	print
	generate_random_graph(10, 0.3)
	print
	generate_cube(30, 40, 20)


def input_errado():
	sys.stderr.write("Parametros errados. Formato correto:\n")
	sys.stderr.write("generate_graphs.py ring <tamanho>\n")
	sys.stderr.write("generate_graphs.py crown <meiotamanho>\n")
	sys.stderr.write("generate_graphs.py random <tamanho> <probabilidade>\n")
	sys.stderr.write("generate_graphs.py grid <tamanho-x> <tamanho-y> <tamanho-z>\n")
	sys.exit(1)

if len(sys.argv) < 2:
	input_errado()

graph = sys.argv[1]

if graph == "ring":
	if len(sys.argv) != 3:
		input_errado()
	tamanho = int(sys.argv[2])
	generate_ring(tamanho)
elif graph == "crown":	
	if len(sys.argv) != 3:
		input_errado()
	meiotamanho = int(sys.argv[2])
	generate_crown(meiotamanho)
elif graph == "random":	
	if len(sys.argv) != 4:
		input_errado()
	tamanho = int(sys.argv[2])
	probabilidade = float(sys.argv[3])
	generate_random_graph(tamanho, probabilidade)
elif graph == "grid":
	if len(sys.argv) != 5:
		input_errado()
	tamanhox = int(sys.argv[2])
	tamanhoy = int(sys.argv[3])
	tamanhoz = int(sys.argv[4])
	generate_grid(tamanhox, tamanhoy, tamanhoz)
else:
	input_errado()
	