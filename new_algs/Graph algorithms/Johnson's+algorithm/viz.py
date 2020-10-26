import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
from matplotlib.widgets import Button
from algorithm import reweight,Dijkstras
import numpy as np

#run the algowrihm in advancee
# G1 = {
#     0:{1:-2},
#     1:{2:-1},
#     2:{0:4,3:2,4:-3},
#     3:{},
#     4:{},
#     5:{3:1,4:-4}
# }
# V1=[0,1,2,3,4,5]


G1={
    0:{1:4,2:3,3:3},
    1:{2:-2},
    2:{3:1},
    3:{}
}
V1=[0,1,2,3]



Gw=reweight(G1,V1)
print(Gw)
Paths = []
Records=[]
for v in V1:
    out = Dijkstras(Gw,V1,v)
    Paths.append(out[2])
    Records.append(out[3])

#print(Paths[0])
print(len(Records))
for r in Records:
    print(r)

class GraphVisualize:
    def __init__(self):
        self.G = nx.DiGraph(directed=True)
        # self.G.add_nodes_from([(0, {'name': 0}),
        #                   (1, {'name': 1}),
        #                   (2, {'name': 2}),
        #                   (3, {'name': 3}),
        #                   (4, {'name': 4}),
        #                   (5, {'name': 5})])
        #

        # self.G.add_edges_from([(0, 1, {'weight': -2}),
        #                   (1, 2, {'weight': -1}),
        #                   (2, 0, {'weight': 4}),
        #                   (2, 3, {'weight': 2}),
        #                   (2, 4, {'weight': -3}),
        #                   (5, 3, {'weight': 1}),
        #                   (5, 4, {'weight': -4})])

        self.G.add_edges_from([(0, 1, {'weight': 4}),
                               (0, 2, {'weight': 3}),
                               (0, 3, {'weight': 3}),
                               (1, 2, {'weight': -2}),
                               (2, 3, {'weight': 1})])
        self.G.add_nodes_from([(0, {'name': 0}),
                               (1, {'name': 1}),
                               (2, {'name': 2}),
                               (3, {'name': 3})])
        self.pos = nx.spring_layout(self.G)
        self.source_node=0
        self.step=0

        self.pause=False
        self.if_reweighted=False
        self.fig, self.ax=plt.subplots(figsize=(10,10))
        self.anim = matplotlib.animation.FuncAnimation(self.fig, self.update, interval=1000, repeat=True)

    def updateGraphWeights(self,graph,weights):
        for key in weights:
            adj = weights[key]
            if adj == {}:
                continue
            for k in adj:
                start=int(key)
                end=int(k)
                dis=adj[k]
                self.G[start][end]['weight'] = dis


    def update(self,num):
        self.ax.clear()
        self.node_labels = nx.get_node_attributes(self.G, 'name')
        self.edge_labels = nx.get_edge_attributes(self.G, 'weight')
        #print(self.edge_labels)
        color_map=[] # for the nodes
        color_list=[] # for the edges
        for edge in self.edge_labels:
            color_list.append('black')
        for node in self.node_labels:
            color_map.append('green')
        # set the map for drawing
        if self.if_reweighted == True:
            for node in self.node_labels:
                if node == self.source_node:
                    color_map[node]='red'
            rec = Records[self.source_node]  # the record of steps starting at source
            #print(rec)
            if len(rec)==0:
                self.step = 0
                self.source_node += 1
            else:
                rec_of_this_step = rec[self.step]

                for node in rec_of_this_step:
                    nodename = node[0]
                    dis = node[1]
                    prev = node[2]
                    self.node_labels[nodename] = str(nodename)+'/'+str(dis)
                    if prev != None:
                        e = (prev, nodename)
                        i = 0
                        for key in self.edge_labels.keys():
                            if key == e:
                                color_list[i] = 'red'
                            i += 1


                if self.step == len(rec)-1:
                    self.step = 0
                    self.source_node += 1
                else:
                    self.step += 1







        #print(type(self.node_labels[0]))
        # print(edge_labels)
        #if self.if_reweighted == True:

        nx.draw_networkx_edges(self.G,pos=self.pos,ax=self.ax,arrowsize=20, edge_color=color_list)
        nx.draw_networkx_edge_labels(self.G,self.pos,ax=self.ax,edge_labels=self.edge_labels)
        nx.draw_networkx_nodes(self.G,self.pos,node_color=color_map,ax=self.ax,node_size=1000, alpha=0.9)
        nx.draw_networkx_labels(self.G,self.pos,self.node_labels,16,ax=self.ax)
        if self.if_reweighted == False:
            self.updateGraphWeights(self.G,Gw)
            self.if_reweighted = True

    def _pause(self, event):
        if self.pause == False:
            self.pause = True
            self.anim.event_source.stop()
            self.pause_button.label.set_text('resume')
        else:
            self.pause = False
            self.anim.event_source.start()
            self.pause_button.label.set_text('pause')


    def animate(self):
        pause_ax = self.fig.add_axes([0.75, 0.025, 0.1, 0.04])
        self.pause_button = Button(pause_ax,'pause')
        self.pause_button.on_clicked(self._pause)
        plt.show()



#nx.draw_networkx_edges(G,pos=pos,ax=ax,arrowsize=12)
#nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
#nx.draw_networkx_nodes(G,pos,node_color='g',ax=ax,nodesize=500,alpha=0.9)
#nx.draw_networkx_labels(G,pos,node_labels,16)

vis = GraphVisualize()
vis.animate()