from algorithms.algo import AlgoWidget
from PyQt5 import QtCore, QtGui, QtWidgets

#	CONSTANTS

class GraphNode(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, i, j, id, parent=None):
        super().__init__(parent)
        self.index = (i, j)
        self.id = id
        self.enable = False

    def __str__(self):
        return str((self.index, self.id))


class GraphWidget(AlgoWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.graph_matrix = [[GraphNode(i, j, i * width + j) for j in range(width)] for i in range(height)]
                


class BFS(GraphWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(width, height, parent)
        self.setWindowTitle(self.tr("Breadth-first search"))
