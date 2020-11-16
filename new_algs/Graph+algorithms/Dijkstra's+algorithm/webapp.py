#!flask/bin/python
# coding: utf-8

# Autor:   Ricardo Galiardi
# 
# Base:    Uso do algorítmo de Dijkstra (teoria dos Grafos)
#          Foram usadas peças de vários modelos já existentes
#          para elaboração do código.
#          
# Versões: Python 3.7
#
# Arquivo: Arquivo principal para execução em shell - WebApi
#
# Execução:
#   Abrir o prompt shell e executar python app.py e seguir as instruções do menu.
#   Para testar a Api é necessário abrir um outro prompt shell e executar os comandos
#   abaixo para cada tipo de execução: Listar, Selecionar, Incluir, Alterar, Excluir
#
#   Para listar tudo
#       http://localhost:5000/api/route
#
#   Teste para consulta de rota
#       Usar a url no browser aberto (trocar os parâmetros dep e arr): 
#       http://127.0.0.1:5000/api/route/?dep=FRA&arr=MAD
#
#   Teste para inclusão
#       Usar um prompt do shel para execução do curl (linux)    
#       curl -i -H "Content-Type: application/json" -X POST -d '{"dep":"GRU", "arr": "AEP", "cost": 8}' http://localhost:5000/api/route

# Definição e importação das bibliotecas
import sys
import webbrowser
from flask import Flask, jsonify, abort, make_response, request
import route

# Função para criação do objeto do Flask
app = Flask(__name__)

# Função para página de abertura
@app.route('/')
def index():
    return make_response(jsonify({'Bem Vindo': 'Ao sistema de Rotas'}), 200)

# Função para página de abertura
@app.route('/api/route', methods=['GET'])
def get_tasks():
    return make_response(jsonify({'Bem Vindo': 'Ao sistema de Rotas'}), 200)

# Função para busca da melhor rota (Parâmetros: dep e arr)
@app.route('/api/route/', methods=['GET'])
def get_task():
    
    if len(request.args) != 2:
        return make_response(jsonify({'error': 'Rotas não identificadas'}), 404)

    source = route.fieldvalid("[a-zA-Z]{3,}", request.args.get('dep', ''))
    dest = route.fieldvalid("[a-zA-Z]{3,}", request.args.get('arr', ''))

    if source and dest:
        ret = route.flights.dijkstra(source, dest)
        return make_response(jsonify({'Resultado': ret}), 201)
    else:
        return make_response(jsonify({'Erro': 'Valores digitados não são válidos, tente novamente!'}), 404)

# Função para criação de uma nova rota
@app.route('/api/route', methods=['POST'])
def create_task():

    if len(request.json) != 3:
        return make_response(jsonify({'error': 'Rotas e valor não identificados'}), 404)

    source = route.fieldvalid("[a-zA-Z]{3,}", request.json['dep'])
    dest = route.fieldvalid("[a-zA-Z]{3,}", request.json['arr'])
    cost = route.fieldvalid("[\d]*$", request.json['cost'])

    if source and dest and cost:
        ret = route.flights.add_edge(source, dest, int(cost))
        return make_response(jsonify({'Resultado': ret}), 201)
    else:
        return make_response(jsonify({'Erro': 'Valores digitados não são válidos, tente novamente!'}), 404)

# Função para página não encontrada
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# Definição do arquivo de rotas
def loadfile():
    load = input("Carregue o arquivo de rotas: ")

    if not load:
        print("Arquivo de rotas não definido!")
        sys.exit

    route.clearscreen()
    routes = route.read_routes(load)

    route.flights = route.Graph(routes)
    route.edges = len(route.flights.edges)

    if route.edges == 0:
        print("O arquivo selecionado não possui rotas, \n Por favor, seleciona um arquivo válido.")
        loadfile()

# Função para execução da WebApi via chamada
def run():
    url = 'http://127.0.0.1:5000/api/route'
    webbrowser.open_new(url)
    app.run()

# Chamada principal
if __name__ == '__main__':
    route.clearscreen()
    loadfile()
    run()