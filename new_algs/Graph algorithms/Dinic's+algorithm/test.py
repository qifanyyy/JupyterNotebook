
import sys

from PyQt5.QtWidgets import QListWidget, QMessageBox, QApplication


class myListWidget(QListWidget):

    def Clicked(self, item):
        QMessageBox.information(self, "ListWidget", "You clicked: " + item.text())


def main():
    app = QApplication(sys.argv)
    listWidget = myListWidget()

    # Resize width and height
    listWidget.resize(300, 120)

    listWidget.addItem("Item 1")
    listWidget.addItem("Item 2")
    listWidget.addItem("Item 3")
    listWidget.addItem("Item 4")

    listWidget.setWindowTitle('PyQT QListwidget Demo')
    #listWidget.itemClicked.connect(listWidget.Clicked)
    listWidget.itemDoubleClicked.connect(listWidget.Clicked)

    listWidget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
