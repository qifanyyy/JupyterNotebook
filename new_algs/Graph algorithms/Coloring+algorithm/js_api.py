import json
import logging
import ast

from PySide import QtCore, QtSvg, QtGui

import settings
from common.multigraph import MultiGraph
from four_color.ComplexEdgeColoring import EdgeColoring
from common.storage import SQLiteGraphStore
from four_color.InductionEngine import InductionEngine

logger = logging.getLogger(__name__)

class OJSAPI(QtCore.QObject):
    '''
        this class is the "oegarn" in the show.html
    '''
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.store = SQLiteGraphStore(settings.VIEW_THIS_DB)
        #self.store = SQLiteGraphStore(settings.DB_FILE)

    def attach(self, parent):
        self.setParent(parent)
        self.app = parent
        self.app.page.mainFrame().javaScriptWindowObjectCleared.connect(self.add_to_window)

    @QtCore.Slot()
    def add_to_window(self):
        # add OJSAPI to the GUI
        self.app.page.mainFrame().addToJavaScriptWindowObject('oegarn', self)

    @QtCore.Slot()
    def quit(self):
        #self.app.qt_gui.quit()
        #QtCore.QCoreApplication.instance().quit()
        pass

    update_graph_list = QtCore.Signal(str)  # Signal for update the graph list

    @QtCore.Slot()
    def list_graphs(self):
        graphs = self.store.list_graphs()
        self.update_graph_list.emit(json.dumps(graphs))

    @QtCore.Slot(str)
    def load_graph(self, id):
        graph = self.store.get_graph(id)
        self._graph = graph
        self._graph.g_id = id
        self._induction = InductionEngine(self._graph)
        self.update_current_graph.emit(self._graph.to_json())

    @QtCore.Slot(str, str)
    def create_graph(self, name, data):
        graph = MultiGraph.from_json(data)
        graph.name = name
        self.store.add_graph(graph)


    update_current_graph = QtCore.Signal(str) # Signal for update the current graph
    highlight = QtCore.Signal(str)

    @QtCore.Slot()
    def layout(self):
        self._induction.layout()
        #logger.info('layout engine !!!')
        self.update_current_graph.emit(self._graph.to_json())

    @QtCore.Slot()
    def random_color(self):
        self._graph.random_color()
        self.update_current_graph.emit(self._graph.to_json())


    @QtCore.Slot()
    def color(self):
        if not self._induction.edge_coloring():
            print "no success"
        self.update_current_graph.emit(self._graph.to_json())

    @QtCore.Slot()
    def edge_coloring_by_perfect_matching(self):
        self._induction.edge_coloring_by_perfect_matching()
        self.update_current_graph.emit(self._graph.to_json())

    @QtCore.Slot()
    def cut_edges(self):
        re = self._induction.cut_edges()
        print "cut edges:", re
        
    @QtCore.Slot()
    def perfect_matching(self):
        if self._induction.perfect_matching():
            print "yes"
        else:
            print "no"
        self.update_current_graph.emit(self._graph.to_json())

    @QtCore.Slot()
    def exhaustive_matching(self):
        self._induction.try_to_find()
        

    @QtCore.Slot()
    def find_pentagon(self):
        data = self._induction.highlight_pentagon()
        self.highlight.emit(json.dumps(data))
    
    @QtCore.Slot()
    def highlight_blocking(self):
        data = self._induction.highlight_two_locking_cycles()
        self.highlight.emit(json.dumps(data))

    @QtCore.Slot()
    def highlight_ac_exclusive_chain(self):
        data = self._induction.highlight_ac_exclusive_chain()
        self.highlight.emit(json.dumps(data))

    @QtCore.Slot()
    def highlight_bc_exclusive_chain(self):
        data = self._induction.highlight_bc_exclusive_chain()
        self.highlight.emit(json.dumps(data))


    @QtCore.Slot()
    def highlight_ab_cycles(self):
        data = self._induction.highlight_ab_cycles()
        self.highlight.emit(json.dumps(data))

    @QtCore.Slot()
    def highlight_ac_cycles(self):
        data = self._induction.highlight_ac_cycles()
        self.highlight.emit(json.dumps(data))

    @QtCore.Slot()
    def highlight_bc_cycles(self):
        data = self._induction.highlight_bc_cycles()
        self.highlight.emit(json.dumps(data))

    @QtCore.Slot()
    def highlight_petersen_subdivision(self):
        data = self._induction.find_petersen_subdivision()
        if data != False:
            self.highlight.emit(json.dumps(data))

    @QtCore.Slot()
    def invert_highlighted(self):
        data = self._induction.invert_highlighted()
        if data['edges'] == [] and data['vertices'] == []:
            return
        self.update_current_graph.emit(self._graph.to_json())
        self.highlight.emit(json.dumps(data))
        

    @QtCore.Slot()
    def move_left(self):
        self._induction.move_left()
        self.update_current_graph.emit(self._graph.to_json())

    @QtCore.Slot()
    def move_right(self):
        self._induction.move_right()
        self.update_current_graph.emit(self._graph.to_json())

    @QtCore.Slot()
    def count_resolve(self):
        self._induction.count_resolve_with_even_ab()
        

    @QtCore.Slot()
    def check_resolvable(self):
        if self._induction.check_resolvable():
            print "yes"
        else:
            print "no"


    @QtCore.Slot()
    def smooth(self):
        self._induction.smooth()
        self.update_current_graph.emit(self._graph.to_json())
        
    @QtCore.Slot(str)
    def remove_one_edge(self, info):
        data = ast.literal_eval(info)
        if type(data) != tuple and len(data) != 2:
            print "error input"
            return
        a, b = data
        edge = self._induction.graph.get_edge_by_endpoints(a, b)
        if edge is None:
            print "not such edge"
            return
        self._induction.remove_specified_edge(edge)
        self.update_current_graph.emit(self._graph.to_json())

    @QtCore.Slot()
    def delete_even_ab_cycles(self):
        self._induction.delete_even_ab_cycles()
        self.update_current_graph.emit(self._graph.to_json())


    @QtCore.Slot()
    def put_back(self):
        self._induction.putback_the_last_deleted_edge(True)
        print "put back edge"
        self.update_current_graph.emit(self._graph.to_json())

    @QtCore.Slot()
    def clear_colors(self):
        self._induction.clear_colors()
        self.update_current_graph.emit(self._graph.to_json())

    
    @QtCore.Slot()
    def bicycle_format(self):
        self._induction.bicycle_layout()
        self.update_current_graph.emit(self._graph.to_json())

    @QtCore.Slot(str)
    def save(self, string):
        if hasattr(self._graph, 'g_id'):
            graph = MultiGraph.from_json(string)
            graph.name = self._graph.name
            self.store.save_graph(self._graph.g_id, graph)

    @QtCore.Slot(str)
    def print_svg(self, svg_source):
        #logger.info(svg_source)
        svg_renderer = QtSvg.QSvgRenderer()
        svg_renderer.load(QtCore.QByteArray(svg_source))
        logger.info('svg renderer')
        printer = QtGui.QPrinter()
        printer.setPageMargins(50, 250, 50, 250, QtGui.QPrinter.DevicePixel)
        print_dialog = QtGui.QPrintDialog(printer, self.app.view)
        print_dialog.setOption(QtGui.QAbstractPrintDialog.PrintToFile, True)
        print_dialog.setOption(QtGui.QAbstractPrintDialog.PrintPageRange, True)
        if print_dialog.exec_() == QtGui.QDialog.Accepted:
            painter = QtGui.QPainter()
            painter.begin(printer)
            svg_renderer.render(painter)
            painter.end()
