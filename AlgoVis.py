import sys

from algorithms import sorting, graphs

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

#    CONSTANTS
MAIN_WIN_WIDTH = 800    #    Main window width
MAIN_WIN_HEIGHT = 640    #    Main window height

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #self.resize(MAIN_WIN_WIDTH, MAIN_WIN_HEIGHT)
        self.setWindowTitle(self.tr("Algovis - algorithms visualization"))
        main_layout = QtWidgets.QHBoxLayout(self)
        #   Initialization main_layout
        #   Sorting
        sort_group = QtWidgets.QGroupBox(self.tr("Sorting"), self)
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
        sort_params_layout.addRow(self.tr("Minimum"), self.min_rand_sbox)
        sort_params_layout.addRow(self.tr("Maximum"), self.max_rand_sbox)
        sort_params_layout.addRow(self.tr("Elements count"), self.elements_count_sbox)

        self.bubble_sort_btn = QtWidgets.QPushButton(self.tr("Bubble sort"), self)
        self.bubble_sort_btn.clicked.connect(self.bubble_sort_clicked)
        self.quick_sort_btn = QtWidgets.QPushButton(self.tr("Quick sort"), self)
        self.quick_sort_btn.clicked.connect(self.quick_sort_clicked)
        sort_group_layout.addWidget(self.bubble_sort_btn)
        sort_group_layout.addWidget(self.quick_sort_btn)
        sort_group_layout.addLayout(sort_params_layout)
        sort_group.setLayout(sort_group_layout)
        #   Graph
        graph_group = QtWidgets.QGroupBox(self.tr("Graphs"), self)
        graph_group_layout = QtWidgets.QVBoxLayout()
        self.bfs_btn = QtWidgets.QPushButton(self.tr("Breadth-first search"), self)
        self.bfs_btn.clicked.connect(self.bfs_clicked)
        self.dfs_btn = QtWidgets.QPushButton(self.tr("Depth-first search"), self)
        self.dfs_btn.clicked.connect(self.dfs_clicked)
        graph_params_layout = QtWidgets.QFormLayout()
        self.width_sbox = QtWidgets.QSpinBox(self)
        self.width_sbox.setRange(graphs.MIN_MATRIX_WIDTH, graphs.MAX_MATRIX_WIDTH)
        self.width_sbox.setValue(graphs.MATRIX_WIDTH)
        self.height_sbox = QtWidgets.QSpinBox(self)
        self.height_sbox.setRange(graphs.MIN_MATRIX_HEIGHT, graphs.MAX_MATRIX_HEIGHT)
        self.height_sbox.setValue(graphs.MATRIX_HEIGHT)
        self.nodes_count = QtWidgets.QSpinBox(self)
        self.nodes_count.setRange(graphs.MIN_NODES_COUNT, graphs.MAX_NODES_COUNT)
        self.nodes_count.setValue(graphs.NODES_COUNT)
        graph_params_layout.addRow(self.tr("Width"), self.width_sbox)
        graph_params_layout.addRow(self.tr("Height"), self.height_sbox)
        graph_params_layout.addRow(self.tr("Nodes count"), self.nodes_count)
        graph_group_layout.addWidget(self.bfs_btn)
        graph_group_layout.addWidget(self.dfs_btn)
        graph_group_layout.addLayout(graph_params_layout)
        graph_group.setLayout(graph_group_layout)

        main_layout.addWidget(sort_group)
        main_layout.addWidget(graph_group)

        self.setLayout(main_layout)
        self.setGeometry(QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight, 
            QtCore.Qt.AlignCenter, 
            self.size(), 
            QtWidgets.QApplication.desktop().availableGeometry()
            ))

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

    def bfs_clicked(self):
        self.bfs_widget = graphs.BFS(
            self.width_sbox.value(),
            self.height_sbox.value(),
            self.nodes_count.value(),
            self
            )
        self.bfs_widget.show()

    def dfs_clicked(self):
        self.dfs_widget = graphs.DFS(
            self.width_sbox.value(),
            self.height_sbox.value(),
            self.nodes_count.value(),
            self
            )
        self.dfs_widget.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.ico'))
    translator = QtCore.QTranslator()
    translator.load("algovis_ru")
    if not app.installTranslator(translator):
        print("Can not install translation!")
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
