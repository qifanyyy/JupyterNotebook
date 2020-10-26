# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        MainWindow.resize(484, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.filepicker_lbl = QtGui.QLabel(self.centralwidget)
        self.filepicker_lbl.setGeometry(QtCore.QRect(20, 20, 56, 13))
        self.filepicker_lbl.setObjectName(_fromUtf8("filepicker_lbl"))
        self.filepicker_textEdit = QtGui.QTextEdit(self.centralwidget)
        self.filepicker_textEdit.setGeometry(QtCore.QRect(80, 10, 321, 31))
        self.filepicker_textEdit.setObjectName(_fromUtf8("filepicker_textEdit"))
        self.report_lbl = QtGui.QLabel(self.centralwidget)
        self.report_lbl.setGeometry(QtCore.QRect(20, 70, 56, 13))
        self.report_lbl.setObjectName(_fromUtf8("report_lbl"))
        self.report_textEdit = QtGui.QPlainTextEdit(self.centralwidget)
        self.report_textEdit.setGeometry(QtCore.QRect(20, 90, 381, 121))
        self.report_textEdit.setReadOnly(True)
        self.report_textEdit.setObjectName(_fromUtf8("report_textEdit"))
        self.result_lbl = QtGui.QLabel(self.centralwidget)
        self.result_lbl.setGeometry(QtCore.QRect(20, 230, 56, 13))
        self.result_lbl.setObjectName(_fromUtf8("result_lbl"))
        self.result_textEdit = QtGui.QPlainTextEdit(self.centralwidget)
        self.result_textEdit.setGeometry(QtCore.QRect(20, 260, 381, 171))
        self.result_textEdit.setReadOnly(True)
        self.result_textEdit.setObjectName(_fromUtf8("result_TextEdit_2"))
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 450, 381, 16))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.stop_pushButton = QtGui.QPushButton(self.centralwidget)
        self.stop_pushButton.setGeometry(QtCore.QRect(20, 500, 191, 32))
        self.stop_pushButton.setObjectName(_fromUtf8("stop_pushButton"))
        self.start_pushButton = QtGui.QPushButton(self.centralwidget)
        self.start_pushButton.setGeometry(QtCore.QRect(250, 500, 161, 32))
        self.start_pushButton.setObjectName(_fromUtf8("start_pushButton"))
        self.select_pushButton = QtGui.QPushButton(self.centralwidget)
        self.select_pushButton.setGeometry(QtCore.QRect(300, 40, 110, 32))
        self.select_pushButton.setObjectName(_fromUtf8("select_pushButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 484, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.filepicker_lbl.setText(_translate("MainWindow", "URL Files", None))
        self.report_lbl.setText(_translate("MainWindow", "Report", None))
        self.result_lbl.setText(_translate("MainWindow", "Result", None))
        self.stop_pushButton.setText(_translate("MainWindow", "Stop", None))
        self.start_pushButton.setText(_translate("MainWindow", "Start", None))
        self.select_pushButton.setText(_translate("MainWindow", "Select", None))

