# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created: Fri Jul 22 19:36:46 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1280, 718)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 10, 1231, 691))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.btnGetSongs = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnGetSongs.setObjectName(_fromUtf8("btnGetSongs"))
        self.verticalLayout_2.addWidget(self.btnGetSongs)
        self.btnGetArtists = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnGetArtists.setObjectName(_fromUtf8("btnGetArtists"))
        self.verticalLayout_2.addWidget(self.btnGetArtists)
        self.btnGetAlbums = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnGetAlbums.setObjectName(_fromUtf8("btnGetAlbums"))
        self.verticalLayout_2.addWidget(self.btnGetAlbums)
        self.btnFindDups = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnFindDups.setObjectName(_fromUtf8("btnFindDups"))
        self.verticalLayout_2.addWidget(self.btnFindDups)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 2, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.btnNumSongs = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnNumSongs.setObjectName(_fromUtf8("btnNumSongs"))
        self.verticalLayout.addWidget(self.btnNumSongs)
        self.btnTopA = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnTopA.setObjectName(_fromUtf8("btnTopA"))
        self.verticalLayout.addWidget(self.btnTopA)
        self.btnSingles = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnSingles.setObjectName(_fromUtf8("btnSingles"))
        self.verticalLayout.addWidget(self.btnSingles)
        self.btnCreateSS = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnCreateSS.setObjectName(_fromUtf8("btnCreateSS"))
        self.verticalLayout.addWidget(self.btnCreateSS)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.btnPrint = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.horizontalLayout_3.addWidget(self.btnPrint)
        self.btnLen = QtGui.QPushButton(self.gridLayoutWidget)
        self.btnLen.setObjectName(_fromUtf8("btnLen"))
        self.horizontalLayout_3.addWidget(self.btnLen)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.listWidget = QtGui.QListWidget(self.gridLayoutWidget)
        self.listWidget.setEnabled(True)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout_3.addWidget(self.listWidget)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnGetSongs.setText(_translate("MainWindow", "Get Songs", None))
        self.btnGetArtists.setText(_translate("MainWindow", "Get Artists", None))
        self.btnGetAlbums.setText(_translate("MainWindow", "Get Albums", None))
        self.btnFindDups.setText(_translate("MainWindow", "Find Duplicate Songs", None))
        self.btnNumSongs.setText(_translate("MainWindow", "Number of Songs", None))
        self.btnTopA.setText(_translate("MainWindow", "Top Artists", None))
        self.btnSingles.setText(_translate("MainWindow", "Singles", None))
        self.btnCreateSS.setText(_translate("MainWindow", "Create Spreadsheets", None))
        self.btnPrint.setText(_translate("MainWindow", "Print Playlist", None))
        self.btnLen.setText(_translate("MainWindow", "Length", None))

