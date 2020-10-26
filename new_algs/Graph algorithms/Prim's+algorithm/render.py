from typing import Dict, Optional, Tuple
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation, PillowWriter

from .type_constants import Edges, Number, T
from .graph import Graph


class GraphConverter:

    def graph_to_nx_graph(self, g: Graph) -> nx.Graph:
        edges_flat = [(*edge, w) for edge, w in g.edges()]
        g_nx = nx.Graph()
        g_nx.add_weighted_edges_from(edges_flat)
        return g_nx

    def weighted_edges(self, g: Graph) -> Dict[Tuple[T, T], Number]:
        d = {edge: w for edge, w in g.edges()}
        return d


class GraphRenderer:
    NODE_COLOR = 'g'
    G_EDGE_COLOR = 'g'
    G_EDGE_LABEL_COLOR = 'g'
    MST_EDGE_COLOR = 'r'
    MST_EDGE_LABEL_COLOR = 'r'
    EDGE_WIDTH = 2.0
    FRAME_INTERVAL = 1000
    GIF_FPS = 1
    WINDOWS_TITLE = 'MstFind'

    def __init__(self, figsize=None):
        self._converter = GraphConverter()
        self._fig, self._ax = plt.subplots(figsize=figsize)
        self._fig.canvas.set_window_title(GraphRenderer.WINDOWS_TITLE)
    
    def render_mst(self, g: Graph, mst: Graph, animated: bool = False, trace: Optional[Edges] = None, gifpath=None):
        if animated:
            if trace is None:
                raise ValueError('argument trace must contain sequence of edges')
            self._render_mst_complex(g, trace, gifpath)
        else:
            self._render_mst_simple(g, mst)

    def _render_mst_simple(self, g: Graph, mst: Graph):
        g_nx = self._converter.graph_to_nx_graph(g)
        mst_nx = self._converter.graph_to_nx_graph(mst)

        g_weighthed_edges = self._converter.weighted_edges(g)
        mst_weighted_edges = self._converter.weighted_edges(mst)

        pos = nx.spring_layout(g_nx, k=0.4)

        nx.draw_networkx(g_nx, pos=pos, with_labels=True, node_color=self.NODE_COLOR)
        
        nx.draw_networkx_edges(g_nx, pos, edge_color=self.G_EDGE_COLOR, width=self.EDGE_WIDTH, 
                               arrows=False, ax=self._ax)
        nx.draw_networkx_edge_labels(g_nx, pos, edge_labels=g_weighthed_edges, 
                                     font_color=self.G_EDGE_LABEL_COLOR, ax=self._ax)
    
        nx.draw_networkx_edges(mst_nx, pos, edge_color=self.MST_EDGE_COLOR, width=self.EDGE_WIDTH, 
                               arrows=False, ax=self._ax)
        nx.draw_networkx_edge_labels(mst_nx, pos, edge_labels=mst_weighted_edges, 
                                     font_color=self.MST_EDGE_LABEL_COLOR, ax=self._ax)
        plt.axis('off')
        plt.show()
    
    def _render_mst_complex(self, g: Graph, trace: Edges, gifpath=None):
        g_nx = self._converter.graph_to_nx_graph(g)
        g_weighthed_edges = self._converter.weighted_edges(g)
        
        pos = nx.spring_layout(g_nx, k=0.4)
        def _init():
            self._ax.set_title(f'initial graph')
            nx.draw_networkx(g_nx, pos=pos, with_labels=True, 
                             node_color=GraphRenderer.NODE_COLOR)
        
            nx.draw_networkx_edges(g_nx, pos, edge_color=GraphRenderer.G_EDGE_COLOR, 
                                   width=GraphRenderer.EDGE_WIDTH, arrows=False, 
                                   ax=self._ax)
            nx.draw_networkx_edge_labels(g_nx, pos, edge_labels=g_weighthed_edges, 
                                         font_color=GraphRenderer.G_EDGE_LABEL_COLOR, ax=self._ax)
    
        def _update(frame):
            self._ax.set_title(f'step {frame + 1}. - edge {trace[frame]} added to the tree')

            edgelist = [edge for edge, _ in trace[:frame+1]]
            edge_labels = {edge: w for edge, w in trace[:frame+1]}
            
            nx.draw_networkx_edges(g_nx, pos, edgelist=edgelist, 
                                   edge_color=GraphRenderer.MST_EDGE_COLOR, 
                                   width=GraphRenderer.EDGE_WIDTH, 
                                   arrows=False, ax=self._ax)
            nx.draw_networkx_edge_labels(g_nx, pos, edge_labels=edge_labels, 
                                         font_color=GraphRenderer.MST_EDGE_LABEL_COLOR, 
                                         ax=self._ax)

        self.ani = FuncAnimation(self._fig, _update, frames=len(trace), init_func=_init, 
                                 interval=GraphRenderer.FRAME_INTERVAL, repeat=False)
        
        if gifpath:
            writer = PillowWriter(fps=GraphRenderer.GIF_FPS)
            self.ani.save(gifpath, writer=writer)

        plt.axis('off')
        plt.show()