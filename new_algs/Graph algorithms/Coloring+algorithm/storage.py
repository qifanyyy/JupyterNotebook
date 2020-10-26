import os
import sqlite3
import logging

from contextlib import closing
from common.multigraph import MultiGraph

logger = logging.getLogger(__name__)

CUR_BASE = os.path.abspath(os.path.dirname(__file__))
BASE = os.path.join(CUR_BASE, os.pardir)

DATA_DIR = os.path.join(BASE, 'data')
DB_FILE = os.path.join(DATA_DIR, 'graphs.db')
DB_FILE_FOR_FAILED_GRAPH = os.path.join(DATA_DIR,'failedGraphs.db')
#DB_FILE_FOR_FAILED_GRAPH = os.path.join(DATA_DIR,'allcubicGraphs.db')
SNARK_GRAPH = os.path.join(DATA_DIR,'snarkGraphs.db')
SNARK_GRAPH_2 = os.path.join(DATA_DIR,'snarkGraphs1.db')
VIEW_THIS_DB = DB_FILE_FOR_FAILED_GRAPH
#VIEW_THIS_DB = SNARK_GRAPH
#os.path.join(DATA_DIR,'snarkGraphs.db') 


class GraphStore(object):


    def list_graphs(self):
        pass

    def get_graph(self, g_id):
        pass

    def save_graph(self, g_id, graph):
        pass


class SQLiteGraphStore(GraphStore):

    def __init__(self, connect_str):
        self.db = sqlite3.connect(connect_str)
        try:
            self.initialize()
        except :
            pass

    def initialize(self):
        with closing(self.db.cursor()) as c:
            # Create table
            c.execute('''CREATE TABLE graphs (id integer primary key asc, name text, json text)''')
            self.db.commit()

    def add_graph(self, name,graph):
        with closing(self.db.cursor()) as c:
        #    c.execute('''INSERT INTO graphs (`name`, `json`) VALUES (?, ?)''', (graph.name, graph.to_json(), ))
            c.execute('''INSERT INTO graphs (`name`, `json`) VALUES (?, ?)''', (name, graph, ))
            self.db.commit()

    def get_graph(self, g_id):
        with closing(self.db.cursor()) as c:
            c.execute('''SELECT * FROM graphs WHERE `id`=?''', (g_id, ))
            row = c.fetchone()
            json_data = row[2]
            g = MultiGraph.from_json(json_data)
            g.name = row[1]
            return g


    def save_graph(self, g_id, graph):
        with closing(self.db.cursor()) as c:
            json_data = graph.to_json()
            c.execute('''INSERT OR REPLACE INTO graphs (`id`, `name`, `json`) VALUES (?, ?, ?)''', (g_id, graph.name, json_data))
            self.db.commit()

    def list_graphs(self):
        with closing(self.db.cursor()) as c:
            c.execute('''SELECT `id`, `name` FROM graphs;''')
            rows = c.fetchall()
            graphs = []
            for row in rows:
                graphs.append({
                    'id': row[0],
                    'name': row[1],
                })
            return graphs

    def __del__(self):
        self.db.close()

class Stat():
    def __init__(self):
        self.stats = dict()

    def count(self, x):
        if self.stats.has_key(x):
            self.stats[x] = self.stats[x] + 1
        else:
            self.stats[x] = 1

    def print_out(self):
        for x in self.stats:
            print x, ": ", self.stats[x]


count_utility = Stat()


failed_graph_DB = SQLiteGraphStore(DB_FILE_FOR_FAILED_GRAPH)
snark_graph_DB = SQLiteGraphStore(SNARK_GRAPH)
snark_graph_DB_2 = SQLiteGraphStore(SNARK_GRAPH_2)


