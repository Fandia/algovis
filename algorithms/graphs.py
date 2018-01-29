from algorithms.algo import AlgoWidget
from PyQt5 import QtCore, QtGui, QtWidgets

#	CONSTANTS


class GraphWidget(AlgoWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class BFS(GraphWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Breadth-first search"))
