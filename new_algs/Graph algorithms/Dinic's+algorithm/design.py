# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\design.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(824, 585)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_left = QtWidgets.QFrame(Dialog)
        self.frame_left.setMinimumSize(QtCore.QSize(201, 0))
        self.frame_left.setMaximumSize(QtCore.QSize(201, 16777215))
        self.frame_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left.setObjectName("frame_left")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_left)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame_left)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(self.frame_left)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.verticalLayout.addWidget(self.listWidget)
        self.executeBtn = QtWidgets.QPushButton(self.frame_left)
        self.executeBtn.setObjectName("executeBtn")
        self.verticalLayout.addWidget(self.executeBtn)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.label_time = QtWidgets.QLabel(self.frame_left)
        self.label_time.setObjectName("label_time")
        self.verticalLayout_3.addWidget(self.label_time)
        self.label_edges = QtWidgets.QLabel(self.frame_left)
        self.label_edges.setObjectName("label_edges")
        self.verticalLayout_3.addWidget(self.label_edges)
        self.label_vertexes = QtWidgets.QLabel(self.frame_left)
        self.label_vertexes.setObjectName("label_vertexes")
        self.verticalLayout_3.addWidget(self.label_vertexes)
        self.label_flow = QtWidgets.QLabel(self.frame_left)
        self.label_flow.setObjectName("label_flow")
        self.verticalLayout_3.addWidget(self.label_flow)
        self.gridLayout_2.addWidget(self.frame_left, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)
        self.frame_bottom = QtWidgets.QFrame(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(11)
        sizePolicy.setHeightForWidth(self.frame_bottom.sizePolicy().hasHeightForWidth())
        self.frame_bottom.setSizePolicy(sizePolicy)
        self.frame_bottom.setMinimumSize(QtCore.QSize(691, 51))
        self.frame_bottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom.setObjectName("frame_bottom")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_bottom)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.line_2 = QtWidgets.QFrame(self.frame_bottom)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_6.addWidget(self.line_2, 0, 0, 1, 1)
        self.label_status = QtWidgets.QLabel(self.frame_bottom)
        self.label_status.setObjectName("label_status")
        self.gridLayout_6.addWidget(self.label_status, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_bottom, 2, 0, 1, 2)
        self.frame_top = QtWidgets.QFrame(Dialog)
        self.frame_top.setMinimumSize(QtCore.QSize(691, 61))
        self.frame_top.setStyleSheet("")
        self.frame_top.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top.setObjectName("frame_top")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_top)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.editExperimentCount = QtWidgets.QLineEdit(self.frame_top)
        self.editExperimentCount.setMaximumSize(QtCore.QSize(30, 16777215))
        self.editExperimentCount.setObjectName("editExperimentCount")
        self.verticalLayout_5.addWidget(self.editExperimentCount)
        self.gridLayout_4.addLayout(self.verticalLayout_5, 0, 3, 2, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_top)
        self.lineEdit.setMinimumSize(QtCore.QSize(250, 0))
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_4.addWidget(self.lineEdit, 0, 1, 2, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.frame_top)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6)
        self.gridLayout_4.addLayout(self.verticalLayout_4, 0, 2, 2, 1)
        self.label_load_from_file = QtWidgets.QLabel(self.frame_top)
        self.label_load_from_file.setObjectName("label_load_from_file")
        self.gridLayout_4.addWidget(self.label_load_from_file, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.frame_top)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_4.addWidget(self.line, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_top, 0, 0, 1, 2)
        self.frame_top.raise_()
        self.frame_bottom.raise_()
        self.frame_left.raise_()
        self.label_load_from_file.setBuddy(self.listWidget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEdit, self.listWidget)
        Dialog.setTabOrder(self.listWidget, self.executeBtn)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Нахождение максимального потока"))
        self.label.setText(_translate("Dialog", "Доступные действия"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Dialog", "Создать новый граф"))
        item = self.listWidget.item(1)
        item.setText(_translate("Dialog", "Проталкивание предпотока"))
        item = self.listWidget.item(2)
        item.setText(_translate("Dialog", "Алгоритм Диница"))
        item = self.listWidget.item(3)
        item.setText(_translate("Dialog", "Отобразить всё"))
        item = self.listWidget.item(4)
        item.setText(_translate("Dialog", "Отобразить только путь"))
        item = self.listWidget.item(5)
        item.setText(_translate("Dialog", "Провести эксперимент"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.executeBtn.setText(_translate("Dialog", "Выполнить"))
        self.label_time.setText(_translate("Dialog", "Время:"))
        self.label_edges.setText(_translate("Dialog", "Ребра:"))
        self.label_vertexes.setText(_translate("Dialog", "Вершины:"))
        self.label_flow.setText(_translate("Dialog", "Максимальны поток:"))
        self.label_status.setText(_translate("Dialog", "Статус:"))
        self.editExperimentCount.setText(_translate("Dialog", "10"))
        self.lineEdit.setText(_translate("Dialog", "-file input"))
        self.label_6.setText(_translate("Dialog", "Количество экспериментов:"))
        self.label_load_from_file.setText(_translate("Dialog", "Параметры: "))

