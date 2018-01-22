import sys

from algorithms import sorting, graphs

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

#    CONSTANTS
MAIN_WIN_WIDTH = 800    #    Main window width
MAIN_WIN_HEIGHT = 640    #    Main window height
MAIN_WIN_TITLE = "AlgoVis - визуализация алгоритмов"    # Main window title
SORT_GROUP_TITLE = "Сортировка"
GRAPH_GROUP_TITLE = "Графы"


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.resize(MAIN_WIN_WIDTH, MAIN_WIN_HEIGHT)
        self.setWindowTitle(MAIN_WIN_TITLE)
        main_layout = QtWidgets.QHBoxLayout()

        #    initialization mainLayout
        sort_group_layout = QtWidgets.QVBoxLayout()
        graph_group_layout = QtWidgets.QVBoxLayout()

        bubble_sort_btn = sorting.BubbleSortBtn(self)
        quick_sort_btn = sorting.QuickSortBtn(self)
        dijkstra_btn = graphs.DijkstraBtn()

        sort_group_layout.addWidget(bubble_sort_btn)
        sort_group_layout.addWidget(quick_sort_btn)
        graph_group_layout.addWidget(dijkstra_btn)

        sort_group = QtWidgets.QGroupBox(SORT_GROUP_TITLE)
        sort_group.setLayout(sort_group_layout)
        graph_group = QtWidgets.QGroupBox(GRAPH_GROUP_TITLE)
        graph_group.setLayout(graph_group_layout)

        main_layout.addWidget(sort_group)
        main_layout.addWidget(graph_group)

        self.setLayout(main_layout)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
