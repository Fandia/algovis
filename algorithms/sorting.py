import random
import math

from algorithms.algo import AlgoWidget
from PyQt5 import QtCore, QtGui, QtWidgets

#    CONSTANTS
BUBBLE_SORT_STRING = "Сортировка пузырьком"
QUICK_SORT_STRING = "Быстрая сортировка"
BUBBLE_SORT_DESCR = r"""
Алгоритм состоит из повторяющихся проходов по сортируемому массиву. 
За каждый проход элементы последовательно сравниваются попарно и, если порядок в паре неверный, выполняется обмен элементов. 
Проходы по массиву повторяются N-1 раз или до тех пор, пока на очередном проходе не окажется, 
что обмены больше не нужны, что означает — массив отсортирован. При каждом проходе алгоритма по внутреннему циклу, 
очередной наибольший элемент массива ставится на своё место в конце массива рядом с предыдущим «наибольшим элементом», 
а наименьший элемент перемещается на одну позицию к началу массива («всплывает» до нужной позиции, как пузырёк в воде. 
Отсюда и название алгоритма).
"""
BUBBLE_SORT_ALG = r"""
FOR J=1 TO N-1 STEP 1
    F=0
    FOR I=1 TO N-J STEP 1
        IF A[I]>A[I+1] THEN SWAP A[I],A[I+1]:F=1
    NEXT I
    IF F=0 THEN EXIT FOR
NEXT J
"""

class SortElement(QtWidgets.QGraphicsRectItem):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.value = value

    def set_value(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value
    
    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __hash__(self):
        rect = self.rect()
        return self.rect.x()


class SortWidget(AlgoWidget):
    def __init__(self, parent=None, min_rand=0, max_rand=10, elements_count=10):
        super().__init__(parent)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.sort_layout = QtWidgets.QHBoxLayout()
        self.descr_layout = QtWidgets.QHBoxLayout()

        self.sort_graphic_scene = QtWidgets.QGraphicsScene()
        self.sort_graphic_view = QtWidgets.QGraphicsView(self.sort_graphic_scene)

        self.sort_list = []
        e_brush = QtGui.QBrush(QtGui.QColor(200,200,0))

        self.max_value = max_rand
        self.values_range = max(abs(max_rand - min_rand), abs(max_rand), abs(min_rand))

        if(min_rand >= 0 and max_rand >= 0):
            self.ground_level = self.sort_graphic_view.height()
        elif(min_rand < 0 and max_rand > 0):
            self.ground_level = (1 - abs(min_rand) / self.values_range) * self.sort_graphic_view.height()
        else:
            self.ground_level = 0

        for i in range(elements_count):
            element = SortElement(value=random.randint(min_rand, max_rand))
            #element.setRect(i * 50, 0, 50, element.value * 10)
            element.setBrush(e_brush)
            self.sort_list.append(element)
            self.sort_graphic_scene.addItem(self.sort_list[-1])

        self.main_layout.addWidget(self.sort_graphic_view)
        self.main_layout.addLayout(self.descr_layout)
        self.resizeEvent = self.update_elements
        self.setLayout(self.main_layout)

    def set_description(self, descr_str, alg_str):
        descr_label = QtWidgets.QLabel(descr_str)
        alg_label = QtWidgets.QLabel(alg_str)
        self.descr_layout.addWidget(descr_label)
        self.descr_layout.addWidget(alg_label)

    def update_elements(self, event):
        for i, element in enumerate(self.sort_graphic_scene.items()):
            width = self.sort_graphic_view.width() * 0.04
            height = abs(element.value) / self.values_range * self.sort_graphic_view.height()
            if(element.value > 0):
                y = self.ground_level - height
            else:
                y = self.ground_level
            element.setRect(i * width, y, width, height)
        new_rect = self.sort_graphic_scene.itemsBoundingRect()
        border = 0.1 * min(new_rect.width(), new_rect.height())
        new_rect.setRect(new_rect.x() - border, new_rect.y() - border, 
            new_rect.width() + border * 2, new_rect.height() + border * 2)
        self.sort_graphic_scene.setSceneRect(new_rect)
        self.sort_graphic_view.fitInView(new_rect)


class BubbleSort(SortWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(BUBBLE_SORT_STRING)
        self.set_description(BUBBLE_SORT_DESCR, BUBBLE_SORT_ALG)


class QuickSort(SortWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(QUICK_SORT_STRING)
        self.set_description(BUBBLE_SORT_DESCR, BUBBLE_SORT_ALG)


class BubbleSortBtn(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bubble_sort_widget = BubbleSort()
        self.clicked.connect(self.clicked_method)
        self.setText(BUBBLE_SORT_STRING)

    def clicked_method(self):
        self.bubble_sort_widget.show()


class QuickSortBtn(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.quick_sort_widget = QuickSort()
        self.clicked.connect(self.clicked_method)
        self.setText(QUICK_SORT_STRING)

    def clicked_method(self):
        self.quick_sort_widget.show()
