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
        main_layout = QtWidgets.QHBoxLayout(self)

        #   Initialization main_layout
        #   Sorting
        sort_group = QtWidgets.QGroupBox(SORT_GROUP_TITLE, self)
        sort_group_layout = QtWidgets.QVBoxLayout()
        sort_params_layout = QtWidgets.QFormLayout()
        self.min_rand_sbox = QtWidgets.QSpinBox(self)
        self.min_rand_sbox.setRange(sorting.MIN_RAND_RANGE, sorting.MAX_RAND_RANGE)
        self.min_rand_sbox.setValue(sorting.MIN_RAND)
        self.max_rand_sbox = QtWidgets.QSpinBox(self)
        self.max_rand_sbox.setRange(sorting.MIN_RAND_RANGE, sorting.MAX_RAND_RANGE)
        self.max_rand_sbox.setValue(sorting.MAX_RAND)
        self.elements_count_sbox = QtWidgets.QSpinBox(self)
        self.elements_count_sbox.setRange(sorting.MIN_ELEMENTS_COUNT, sorting.MAX_ELEMENTS_COUNT)
        self.elements_count_sbox.setValue(sorting.ELEMENTS_COUNT)
        sort_params_layout.addRow(sorting.MIN_RAND_RANGE_STRING, self.min_rand_sbox)
        sort_params_layout.addRow(sorting.MAX_RAND_RANGE_STRING, self.max_rand_sbox)
        sort_params_layout.addRow(sorting.ELEMENTS_COUNT_STRING, self.elements_count_sbox)

        self.bubble_sort_btn = QtWidgets.QPushButton(sorting.BUBBLE_SORT_STRING, self)
        self.bubble_sort_btn.clicked.connect(self.bubble_sort_clicked)
        self.quick_sort_btn = QtWidgets.QPushButton(sorting.QUICK_SORT_STRING, self)
        self.quick_sort_btn.clicked.connect(self.quick_sort_clicked)
        sort_group_layout.addWidget(self.bubble_sort_btn)
        sort_group_layout.addWidget(self.quick_sort_btn)
        sort_group_layout.addLayout(sort_params_layout)
        sort_group.setLayout(sort_group_layout)
        #   Graph
        graph_group = QtWidgets.QGroupBox(GRAPH_GROUP_TITLE, self)
        graph_group_layout = QtWidgets.QVBoxLayout()
        self.dijkstra_btn = QtWidgets.QPushButton(graphs.DIJKSTRA_STRING, self)
        graph_group_layout.addWidget(self.dijkstra_btn)
        graph_group.setLayout(graph_group_layout)

        main_layout.addWidget(sort_group)
        main_layout.addWidget(graph_group)

        self.setLayout(main_layout)

    def bubble_sort_clicked(self):
        self.bubble_sort_widget = sorting.BubbleSort(
            self.min_rand_sbox.value(),
            self.max_rand_sbox.value(),
            self.elements_count_sbox.value(),
            self
            )
        self.bubble_sort_widget.show()

    def quick_sort_clicked(self):
        self.quick_sort_widget = sorting.QuickSort(
            self.min_rand_sbox.value(),
            self.max_rand_sbox.value(),
            self.elements_count_sbox.value(),
            self
            )
        self.quick_sort_widget.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
