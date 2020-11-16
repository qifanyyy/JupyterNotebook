# coding=utf-8
import sys

import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import generator
from algorithms.dinica import Dinica
from algorithms.pushFlow import PushFlow
from graph import Graph
from ui import design
from ui.graphViz import GraphViz
from utils import clear_log, get_matrix_stats, parse_gen_args


class ExampleApp(QtWidgets.QDialog, design.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.HANDLER_DICT = {"Алгоритм Диница": self.handler_dinica,
                             "Проталкивание предпотока": self.handler_push_flow,
                             "Создать новый граф": self.handler_generate_next,
                             "Отобразить всё": self.handler_draw_graph,
                             "Отобразить только путь": self.handler_draw_onlyway_graph,
                             "Провести эксперимент": self.handler_experiment}
        self.flow_algorithm = None
        self.graph = None
        self.matrix = []

        grid = QGridLayout()
        self.setLayout(grid)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.gridLayout.addWidget(self.canvas, 0, 1, 9, 9)
        print(self.listWidget.selectedItems())
        self.executeBtn.clicked.connect(self.handler_execute_from_listbox)
        self.listWidget.itemDoubleClicked.connect(self.handler_double_clicked_list)

    def handler_draw_graph(self):
        self.__draw(self.flow_algorithm.getGraph())

    def handler_draw_onlyway_graph(self):
        self.__draw(self.flow_algorithm.getGraph(), True)

    def handler_generate_next(self):
        self.matrix = self.get_matrix()
        stat = get_matrix_stats(self.matrix)
        self.label_vertexes.setText('Кол-во вершин: ' + str(stat['v']))
        self.label_edges.setText('Кол-во ребер: ' + str(stat['e']))
        self.set_status('создан новый граф')

    def handler_experiment(self):
        count = int(self.editExperimentCount.text())

        params = self.__get_gen_atributes()
        params = parse_gen_args(params.split())
        gen = generator.GraphGenerator(params)

        ans_dinica = 0
        ans_preflow = 0

        for idx in range(count):
            M = next(gen)
            s, t = 0, len(M) - 1

            graph = Graph.initGraphFromMatrix(M)
            preflow_algorithm = PushFlow(graph, len(M), s, t)

            graph = Graph.initGraphFromMatrix(M)
            dinica_algorithm = Dinica(graph, len(M), s, t)

            assert dinica_algorithm.getMaxFlow() == preflow_algorithm.getMaxFlow()
            ans_dinica += dinica_algorithm.time
            ans_preflow += preflow_algorithm.time
        self.set_status(
            '{} тестов (Средний результат), Диница: {}, проталкивание предпотока: {}'.format(count, ans_dinica / count,
                                                                                             ans_preflow / count))

    def handler_execute_from_listbox(self):
        commands = []
        for item in self.listWidget.selectedItems():
            commands.append(item.text())
        for command in commands:
            self.HANDLER_DICT[command]()

    def handler_double_clicked_list(self, item):
        self.HANDLER_DICT[item.text()]()

    def __get_gen_atributes(self):
        try:
            params = self.lineEdit.text()
        except:
            params = []
        return params

    def get_matrix(self):
        params = self.__get_gen_atributes()
        params = parse_gen_args(params.split())
        M = generator.GraphGenerator(params)
        M = next(M)
        return M

    def handler_push_flow(self):
        M = self.matrix
        self.graph = Graph.initGraphFromMatrix(M)
        s, t = 0, len(M) - 1
        self.flow_algorithm = PushFlow(self.graph, len(M), s, t)
        self.label_time.setText("Время: {:.6f} sec".format(self.flow_algorithm.time))
        self.label_flow.setText("Максимальный поток: {}".format(self.flow_algorithm.getMaxFlow()))
        self.set_status('выполнен алгоритм проталкивания предпотока')

    def handler_dinica(self):
        M = self.matrix
        self.graph = Graph.initGraphFromMatrix(M)
        s, t = 0, len(M) - 1
        self.flow_algorithm = Dinica(self.graph, len(M), s, t)
        self.label_time.setText("Время: {:.6f} sec".format(self.flow_algorithm.time))
        self.label_flow.setText("Максимальный поток: {}".format(self.flow_algorithm.getMaxFlow()))
        self.set_status('выполнен алгоритм Диница')

    def set_status(self, text):
        self.label_status.setText('Последнее действие: {}'.format(text))

    def __draw(self, G, only_way=False):
        self.figure.clf()
        gv = GraphViz(G, only_way)
        plt.axis('off')
        gv.draw()
        self.canvas.draw_idle()


def run():
    clear_log()
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    run()
