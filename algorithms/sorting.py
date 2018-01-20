

from PyQt5 import QtCore, QtGui, QtWidgets

#    CONSTANTS
BUBBLE_SORT_STRING = "Сортировка пузырьком"
QUICK_SORT_STRING = "Быстрая сортировка"


class SortWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class BubbleSort(SortWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(BUBBLE_SORT_STRING)


class QuickSort(SortWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(QUICK_SORT_STRING)


class BubbleSortBtn(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bubble_sort_widget = BubbleSort()
        self.clicked.connect(self.clickedMethod)
        self.setText(BUBBLE_SORT_STRING)

    def clickedMethod(self):
        self.bubble_sort_widget.show()


class QuickSortBtn(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.quick_sort_widget = QuickSort()
        self.clicked.connect(self.clickedMethod)
        self.setText(QUICK_SORT_STRING)

    def clickedMethod(self):
        self.quick_sort_widget.show()
