from algorithms.algo import AlgoWidget
from PyQt5 import QtCore, QtGui, QtWidgets

#	CONSTANTS
DIJKSTRA_STRING = "Алгоритм Дейкстры"


class GraphWidget(AlgoWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class Dijkstra(GraphWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(DIJKSTRA_STRING)


class DijkstraBtn(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicked.connect(self.clicked_method)
        self.setText(DIJKSTRA_STRING)

    def clicked_method(self):
        self.dijkstraWidget = Dijkstra()
        self.dijkstraWidget.show()
