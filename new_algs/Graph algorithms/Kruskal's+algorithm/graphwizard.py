# Matthew Smith-Kennedy

import re
import edge
import Kruskal
import Prim
import matplotlib.pyplot as plt
import networkx as nx
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog


class Ui_MainWindow(object):

    def opengraphWindow(self):
        MainWindow.hide()
        GraphWindow.show()

    def exit(self):
        sys.exit(app.exec_())

    def setupUi(self):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        MainWindow.setWindowTitle("GraphWizard 1.0")
        MainWindow.setAutoFillBackground(False)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")


        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        path = "maintitleimage.png"
        titleimage = QtGui.QImage(path)

        titleimagepix= QtGui.QPixmap.fromImage(titleimage)
        self.label.setPixmap(titleimagepix)
        self.label.resize(titleimage.width(),titleimage.height())


        self.maininstructions = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.maininstructions.setFont(font)
        self.maininstructions.setObjectName("maininstructions")
        self.verticalLayout.addWidget(self.maininstructions)
        self.maininstructions.setReadOnly(True)
        welcome = "Welcome to GraphWizard!\n"
        a = "Instructions:  To use graphing functions go to drop-down menu in upper left corner and go to graphing page.\n"
        b = "In graphing page, select graph type or algorithm from Graph Type menu.\n"
        c = "Choose data selection either from file or from textbox provided by selecting a button.\n"
        d = "Enter data as a series of edges like: source[if Longest Path] dest[if Longest Path] vertex1 vertex2 weight , vertex1 vertex2 weight, ...\n"
        e= "Click Get Results button.  Results will display as a graph window and in the program window.\n"
        f = "The submitted data will be checked formatting and duplicate edges will be removed.\n"
        g = "Data limitations:  Maximum number of edges = 100.  Maximum number of nodes = 100.  Vertices should be in range [0,999]"

        self.maininstructions.setText(welcome + a +b + c + d +e +f+ g)
        MainWindow.setCentralWidget(self.centralwidget)
        self.mainmenu = QtWidgets.QMenuBar(MainWindow)
        self.mainmenu.setGeometry(QtCore.QRect(0, 0, 1000, 18))
        self.mainmenu.setObjectName("mainmenu")
        self.menuOptions = QtWidgets.QMenu(self.mainmenu)
        self.menuOptions.setObjectName("menuOptions")
        self.menuExit = QtWidgets.QMenu(self.mainmenu)
        self.menuExit.setObjectName("menuExit")
        MainWindow.setMenuBar(self.mainmenu)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionClick_to_Confirm_Exit = QtWidgets.QAction(MainWindow)
        self.actionClick_to_Confirm_Exit.setObjectName("actionClick_to_Confirm_Exit")
        self.actionClick_to_Go_to_Graphing_Page = QtWidgets.QAction(MainWindow)
        self.actionClick_to_Go_to_Graphing_Page.triggered.connect(self.opengraphWindow)
        self.menuOptions.addAction(self.actionClick_to_Go_to_Graphing_Page)
        self.actionClick_to_Confirm_Exit.triggered.connect(self.exit)
        self.menuExit.addAction(self.actionClick_to_Confirm_Exit)
        self.mainmenu.addAction(self.menuOptions.menuAction())
        self.mainmenu.addAction(self.menuExit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.menuOptions.setTitle(_translate("MainWindow", "Graph Types"))
        self.menuExit.setTitle(_translate("MainWindow", "Exit"))
        self.actionClick_to_Confirm_Exit.setText(_translate("MainWindow", "Click to Confirm Exit"))
        self.actionClick_to_Go_to_Graphing_Page.setText(_translate("MainWindow", "Click to Go to Graphing Page"))


#class for calling graphing functions window
class Ui_GraphWindow(object):

    graphtype = 0  # 0 not selected, 1 prim, 2 kruskal, 3 dijkstra, 4 longest path problem
    edgelist = []
    nodecount = int
    datafilename = ""
    v = "Choose data selection either from file or from textbox provided by selecting a button.\n"
    w =  "Enter data as a series of edges like: vertex1 vertex2 weight , vertex1 vertex2 weight, ....\n"
    x = "Click Get Results button.  Results will display as a graph window and in the program window.\n"
    y = "The submitted data will be checked formatting and duplicate edges will be removed.\n"
    z = "Data limitations:  Maximum number of edges = 100.  Maximum number of nodes = 100.  Vertices should be in range [0,999].\n"
    u =  "Enter data as a series of edges like: source dest, vertex1 vertex2 weight , vertex1 vertex2 weight, ....  \n"

    def exit(self):
        app = QtWidgets.QApplication(sys.argv)
        sys.exit(app.exec_())

    def openmainWindow(self):
        MainWindow.show()
        GraphWindow.hide()

    def setupUi(self):
        self.errordialog = QtWidgets.QErrorMessage()
        GraphWindow.setObjectName("GraphWindow")
        GraphWindow.resize(1200, 1000)
        self.centralwidget = QtWidgets.QWidget(GraphWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout.addLayout(self.gridLayout_2, 10, 1, 3, 1)
        self.graphinstructions = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.graphinstructions.setObjectName("graphinstructions")
        self.gridLayout.addWidget(self.graphinstructions, 15, 1, 2, 3)
        self.graphinstructions.setReadOnly(True)
        self.cleardatabutton = QtWidgets.QPushButton(self.centralwidget)
        self.cleardatabutton.setObjectName("cleardatabutton")
        self.gridLayout.addWidget(self.cleardatabutton, 7, 2, 1, 1)
        self.cleardatabutton.clicked.connect(self.cleardata)
        self.selectfilebutton = QtWidgets.QRadioButton(self.centralwidget)
        self.selectfilebutton.setObjectName("radioButton")
        self.selectfilebutton.clicked.connect(self.getfilename)
        self.buttonGroup = QtWidgets.QButtonGroup(GraphWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.selectfilebutton)
        self.gridLayout.addWidget(self.selectfilebutton, 0, 2, 1, 1)
        self.submitdata = QtWidgets.QPushButton(self.centralwidget)
        self.submitdata.setObjectName("submitdata")
        self.gridLayout.addWidget(self.submitdata, 7, 1, 1, 1)
        self.submitdata.clicked.connect(self.rundata)
        self.manualentrybutton = QtWidgets.QRadioButton(self.centralwidget)
        self.manualentrybutton.setObjectName("manualentrybutton")
        self.buttonGroup.addButton(self.manualentrybutton)
        self.gridLayout.addWidget(self.manualentrybutton, 0, 1, 1, 1)

        self.rawresultstext = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.rawresultstext.setPlainText("Text Results Appear Here")
        self.rawresultstext.setObjectName("rawresultstext")
        self.gridLayout.addWidget(self.rawresultstext, 16, 0, 1, 1)
        self.rawresultstext.setReadOnly(True)

        self.manualdataentry = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.manualdataentry.setPlainText("Select Manual Data Entry or File Name Button. Press Clear Data box if using manual entry.")
        self.manualdataentry.setObjectName("manualdataentry")
        self.gridLayout.addWidget(self.manualdataentry, 5, 1, 1, 3)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setMaximumSize(QtCore.QSize(700, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)



        GraphWindow.setCentralWidget(self.centralwidget)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setObjectName("label")   #for main graph image area
        self.gridLayout.addWidget(self.label, 3, 0, 7, 1)

        self.graphoptions2 = QtWidgets.QMenuBar(GraphWindow)
        self.graphoptions2.setGeometry(QtCore.QRect(0, 0, 1000, 18))
        self.graphoptions2.setObjectName("graphoptions2")
        self.menuPrim = QtWidgets.QMenu(self.graphoptions2)
        self.menuPrim.setObjectName("menuPrim")
        self.menuExit = QtWidgets.QMenu(self.graphoptions2)
        self.menuExit.setObjectName("menuExit")
        self.menuExit_2 = QtWidgets.QMenu(self.graphoptions2)
        self.menuExit_2.setObjectName("menuExit_2")
        GraphWindow.setMenuBar(self.graphoptions2)
        self.statusbar = QtWidgets.QStatusBar(GraphWindow)
        self.statusbar.setObjectName("statusbar")
        GraphWindow.setStatusBar(self.statusbar)
        self.actionKruskal = QtWidgets.QAction(GraphWindow)
        self.actionKruskal.setObjectName("actionKruskal")
        self.actionDijkstra = QtWidgets.QAction(GraphWindow)
        self.actionDijkstra.setObjectName("actionDijkstra")
        ##self.actionLongest_Path_Problem = QtWidgets.QAction(GraphWindow)
        ##self.actionLongest_Path_Problem.setObjectName("actionLongest_Path_Problem")
        self.actionPrim = QtWidgets.QAction(GraphWindow)
        self.actionPrim.setObjectName("Prim")
        ##self.actionLongest_Path_Problem = QtWidgets.QAction(GraphWindow)
        ##self.actionLongest_Path_Problem.setObjectName("actionLongest_Path_Problem_2")
        self.actionReturnMain = QtWidgets.QAction(GraphWindow)
        self.actionReturnMain.setObjectName("Return to Main Window")
        self.actionReturnMain.triggered.connect(self.openmainWindow)
        self.actionExit = QtWidgets.QAction(GraphWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionConfirm_Exit = QtWidgets.QAction(GraphWindow)
        self.actionConfirm_Exit.setObjectName("actionConfirm_Exit")
        self.actionConfirm_Exit.triggered.connect(self.exit)
        self.menuPrim.addAction(self.actionPrim)
        self.actionPrim.triggered.connect(self.selectedPrim)
        self.menuPrim.addAction(self.actionKruskal)
        self.actionKruskal.triggered.connect(self.selectedKruskal)
        self.menuPrim.addAction(self.actionDijkstra)
        self.actionDijkstra.triggered.connect(self.selectedDijkstra)
        ##self.menuPrim.addAction(self.actionLongest_Path_Problem)
        ##self.actionLongest_Path_Problem.triggered.connect(self.selectedLongestPath)
        self.menuExit.addAction(self.actionReturnMain)

        self.menuExit_2.addAction(self.actionConfirm_Exit)
        self.graphoptions2.addAction(self.menuPrim.menuAction())
        self.graphoptions2.addAction(self.menuExit.menuAction())
        self.graphoptions2.addAction(self.menuExit_2.menuAction())
        self.retranslateUi(GraphWindow)
        QtCore.QMetaObject.connectSlotsByName(GraphWindow)

    def retranslateUi(self, GraphWindow):
        _translate = QtCore.QCoreApplication.translate
        GraphWindow.setWindowTitle(_translate("GraphWindow", "Graph Page"))
        self.cleardatabutton.setText(_translate("GraphWindow", "Clear Manual Entry Data Box"))
        self.selectfilebutton.setText(_translate("GraphWindow", "Select File Input (provide filename/path)"))
        self.submitdata.setText(_translate("GraphWindow", "Get Results/Graph"))
        self.manualentrybutton.setText(_translate("GraphWindow", "Select Manul Data Entry (to left)"))
        self.textEdit.setText(_translate("GraphWindow", "Graph Type"))
        self.menuPrim.setTitle(_translate("GraphWindow", "Graph Options"))
        self.menuExit.setTitle(_translate("GraphWindow", "Other Options"))
        self.menuExit_2.setTitle(_translate("GraphWindow", "Exit"))
        self.actionKruskal.setText(_translate("GraphWindow", "Kruskal"))
        self.actionDijkstra.setText(_translate("GraphWindow", "Dijkstra"))
        ##self.actionLongest_Path_Problem.setText(_translate("GraphWindow", "Longest Path Problem"))
        self.actionPrim.setText(_translate("GraphWindow", "Prim"))
        ##self.actionLongest_Path_Problem.setText(_translate("GraphWindow", "Longest Path Problem"))
        self.actionReturnMain.setText(_translate("GraphWindow", "Return to Main Window"))
        self.actionExit.setText(_translate("GraphWindow", "Exit"))
        self.actionConfirm_Exit.setText(_translate("GraphWindow", "Click to Confirm Exit"))

#functions for if graph type selected below
    def selectedKruskal(self):
        self.textEdit.setText("Graph Type: Kruskal Selected")
        self.graphtype = 2
        instructions = self.v + self.w + self.x + self.y + self.z
        self.graphinstructions.setPlainText(instructions)

    def selectedPrim(self):
        self.textEdit.setText("Graph Type: Prim Selected")
        self.graphtype = 1
        instructions = self.v + self.w + self.x + self.y + self.z
        self.graphinstructions.setPlainText(instructions)

    def selectedDijkstra(self):
        self.textEdit.setText("Graph Type: Dijkstra Selected")
        self.graphtype = 3
        instructions = self.v + self.u + self.x + self.y + self.z
        self.graphinstructions.setPlainText(instructions)

    def selectedLongestPath(self):
        self.textEdit.setText("Graph Type: Longest Path Selected")
        self.graphtype = 4
        instructions = self.v + self.u + self.x + self.y + self.z
        self.graphinstructions.setPlainText(instructions)

#this function controls input checking, algorithm calling, graph building, and and graphing
    def getInput(self):
        counterrorflag = False
        source = int(0)
        dest = int(0)
        pathlength = int
        self.edgelist.clear()
        if self.selectfilebutton.isChecked() or self.manualentrybutton.isChecked():
            inputstring = self.manualdataentry.toPlainText()
            print(inputstring)
            #if statements below checks for proper input format
            if self.graphtype == 4 or self.graphtype == 3:
                datalist = [int(inputstring) for inputstring in re.findall(r'\d+',inputstring)]
                if (inputstring==""):
                    counterrorflag = True
                    self.rawresultstext.setPlainText("Error:  Input Not Given")
                    self.errordialog.showMessage("Error:  Input Not Given")
                elif (len(datalist)%3 != 2):
                    counterrorflag = True
                    self.rawresultstext.setPlainText("Error: Incorrect Data Input: Enter as 0 [source] 4 [destination] ,0 1 2, 1 2 3 , 2 3 4  ... etc...")
                    self.errordialog.showMessage("Error: Incorrect Data Input: Enter as 0 [source] 4 [destination] ,0 1 2, 1 2 3 , 2 3 4  ... etc...")
                else:
                    source = datalist[0]
                    dest = datalist[1]
                    datalist = datalist[2 :]
            else:
                datalist = [int(inputstring) for inputstring in re.findall(r'\d+',inputstring)]
                if (inputstring==""):
                    counterrorflag = True
                    self.rawresultstext.setPlainText("Error:  Input Not Given")
                    self.errordialog.showMessage("Error:  Input Not Given")
                elif (len(datalist)%3 != 0):
                    counterrorflag = True
                    self.rawresultstext.setPlainText("Error: Incorrect Data Input: Enter as 0 1 2, 1 2 3 , 2 3 4  ... etc...")
                    self.errordialog.showMessage("Error: Incorrect Data Input: Enter as 0 1 2, 1 2 3 , 2 3 4  ... etc...")


            if counterrorflag is False:
                count = len(datalist)
                self.edgelist.clear()
                i = 0

                ## if no counterror then proceed with building edgelist, which is passed to other classes
                while i < count:

                    newedge = edge.Edge()
                    newedge.Vertex1 = datalist[i]
                    i+=1
                    newedge.Vertex2 = datalist[i]
                    i+=1
                    newedge.weight = datalist[i]
                    newedge.extra = 1
                    self.edgelist.append(newedge)
                    i+=1
                self.nodecount = self.countNodes()

                #if statements below run algorithms as needed depending on type
                if self.graphtype == 1:
                    Prim.runPrim(self, self.edgelist, self.nodecount)
                if self.graphtype == 2:
                    Kruskal.runKruskal(self, self.edgelist, self.nodecount)
                if self.graphtype == 3:
                    pass   #this algorithm is handled later in this class

                ##longest path is disabled (will be implemented by me)
                ##if self.graphtype == 4:

                ##    LongestPath.runLongestPath(self, source, dest, self.edgelist, self.nodecount)

                if self.edgelist[0] == 99999:  # check for no path error value
                    self.rawresultstext.setPlainText("No path can be found from Source " + str(source) + " to Destination "  + str(dest))
                    self.errordialog.showMessage("No path can be found from Source " + str(source) + " to Destination "  + str(dest))
                else:

                    graph = nx.Graph()

                    #for loop below adds edges to graph.
                    for e in self.edgelist:
                        if self.graphtype == 4:
                            if e.extra == 1:
                                graph.add_edge(e.Vertex1,e.Vertex2, weight = e.weight)

                        else:
                            graph.add_edge(e.Vertex1,e.Vertex2, weight = e.weight)

                    #this if statement processes graph through nx.dijkstra
                    if self.graphtype == 3:
                        pathlist = nx.dijkstra_path(graph, source, dest)
                        pathlength = nx.dijkstra_path_length(graph, source, dest)  # for later display
                        for x in range(0,len(pathlist)-1):
                            for y in self.edgelist:
                                if y.Vertex1 == pathlist[x] and y.Vertex2 == pathlist[x+1] or y.Vertex2 == pathlist[x] and y.Vertex1 == pathlist[x+1]:
                                    y.selected = True
                                    break

                    selected = []
                    unselected = []
                    labels = dict([((u,v,),w['weight']) for u,v,w in graph.edges(data=True)])

                    if self.graphtype == 4:
                        for x in self.edgelist:
                            if x.selected:
                                selected.append((x.Vertex1, x.Vertex2))
                            else:
                                unselected.append((x.Vertex1, x.Vertex2))
                    else:
                        for x in self.edgelist:
                            if x.selected:
                                selected.append((x.Vertex1, x.Vertex2))
                            else:
                                unselected.append((x.Vertex1, x.Vertex2))


                    #begin drawing graph
                    pos = nx.planar_layout(graph)
                    if nx.is_connected(graph):
                        pos = nx.spring_layout(graph)

                    nx.draw_networkx_nodes(graph, pos, node_size = 200)
                    nx.draw_networkx_edges(graph, pos, edgelist=selected, width=5)
                    nx.draw_networkx_edges(graph, pos, edgelist=unselected, width=5, alpha=0.5, edge_color='b', style='dashed')
                    nx.draw_networkx_labels(graph, pos, font_size=14, font_family='sans-serif')
                    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_size=10, font_family='sans-serif')
                    plt.axis('off')

                    #setting titles for graph depending on type
                    if self.graphtype == 1 or self.graphtype == 2:
                        plt.title("Minimum Spanning Tree/Forest")
                    if self.graphtype == 3:
                        plt.title("Shortest path length from node " +str(source) + " to " + str(dest) + " is:  " +str(pathlength))
                    if self.graphtype == 4:
                        plt.title("Longest path length from node " +str(source) + " to " + str(dest) + " shown below")
                    figure = plt.savefig('figure.png', bbox_inches = 'tight', dpi= 150)
                    path = "figure.png"   #used to store graph image
                    graphimage = QtGui.QImage(path)
                    graphimagepix= QtGui.QPixmap.fromImage(graphimage)
                    self.label.setPixmap(graphimagepix)
                    self.label.resize(graphimage.width(),graphimage.height())
                    plt.close(figure)
                    message = []
                    for m in self.edgelist:
                        message.append(str(m.Vertex1) + " " +str(m.Vertex2)+ " "+ str(m.weight)+ " Sel: "+ str(m.selected) + "   ")
                    message2 = " ".join(message)
                    self.rawresultstext.setPlainText(message2)

    def countNodes(self):
        temp = []
        for var in self.edgelist:
            temp.append(var.Vertex1)
            temp.append(var.Vertex2)
        tempset = set(temp)
        temp = list(tempset)
        return int(len(temp))

    #this function is called upon submit data button.  checks for data entry and graph type selection and calls input()
    def rundata(self):
        errorflag = True
        if (self.selectfilebutton.isChecked() or self.manualentrybutton.isChecked()):
            errorflag = False
        if self.graphtype==0:
            errorflag = True
        if errorflag:
            self.rawresultstext.setPlainText("Error:  Select File or Manual Entry and make sure graph type is selected")
            self.errordialog.showMessage("Error:  Select File or Manual Entry and make sure graph type is selected")
        else:
            self.getInput()

    #clears manual data entry box
    def cleardata(self):
        self.rawresultstext.setPlainText("")
        self.manualdataentry.setPlainText("")


    #gets file name through dialog
    def getfilename(self):
        hold = QFileDialog.getOpenFileName()
        self.datafilename = hold [0]
        if hold[0] == "":
            return
        else:
            fp = open(self.datafilename, "r")
            data = fp.read()
            self.manualdataentry.setPlainText(data)
            fp.close()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui_Main = Ui_MainWindow()
    ui_Main.setupUi()
    MainWindow.show()
    GraphWindow = QtWidgets.QMainWindow()
    ui_graph = Ui_GraphWindow()
    ui_graph.setupUi()
    GraphWindow.hide()
    sys.exit(app.exec_())
