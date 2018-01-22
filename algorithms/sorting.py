# -*- coding: UTF-8 -*-
import random
import threading
import time
import copy
from abc import ABCMeta, abstractmethod

from algorithms.algo import AlgoWidget
from PyQt5 import QtCore, QtGui, QtWidgets

#    CONSTANTS
SORT_WIN_WIDTH = 800
SORT_WIN_HEIGHT = 800

PAUSE_TIME = 500

MIN_RAND = 1
MAX_RAND = 10
ELEMENTS_COUNT = 20

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

class StateElement():
    def __init__(self, value, color):
        self.value = value
        self.color = color


class SortWidget(AlgoWidget):
    __metaclass__ = ABCMeta
    @abstractmethod
    def __init__(self, min_rand, max_rand, elements_count, parent=None):
        super().__init__(parent)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.descr_layout = QtWidgets.QHBoxLayout()
        self.sort_graphic_scene = QtWidgets.QGraphicsScene()
        self.sort_graphic_view = QtWidgets.QGraphicsView(self.sort_graphic_scene)
        self.control_button = QtWidgets.QPushButton("Play - Pause", self)
        self.control_button.clicked.connect(self.change_play_states_wait_event)
        self.sort_list = []

        self.states_list = []
        self.current_state = 0
        self.max_state = 0
        self.play_states_event = threading.Event()
        self.play_states_event.clear()
        self.current_change_state_timer = 0

        self.max_value = max_rand
        self.values_range = max(abs(max_rand - min_rand), abs(max_rand), abs(min_rand))
        self.select_color = QtGui.QColor(150,250,0)
        self.standard_color = QtGui.QColor(200,200,0)

        if(min_rand >= 0 and max_rand >= 0):
            self.ground_level = self.sort_graphic_view.height()
        elif(min_rand < 0 and max_rand > 0):
            self.ground_level = (1 - abs(min_rand) / self.values_range) * self.sort_graphic_view.height()
        else:
            self.ground_level = 0

        for i in range(elements_count):
            element = SortElement(random.randint(min_rand, max_rand))
            element.setBrush(self.standard_color)
            self.sort_list.append(element)
            self.sort_graphic_scene.addItem(self.sort_list[-1])
        #self.sort_list.sort()
        #self.update_elements(None)

        self.main_layout.addWidget(self.sort_graphic_view)
        self.main_layout.addWidget(self.control_button)
        self.main_layout.addLayout(self.descr_layout)
        self.resizeEvent = self.update_elements
        self.setLayout(self.main_layout)
        self.resize(SORT_WIN_WIDTH, SORT_WIN_HEIGHT)

    def set_description(self, descr_str, alg_str):
        descr_label = QtWidgets.QLabel(descr_str)
        alg_label = QtWidgets.QLabel(alg_str)
        self.descr_layout.addWidget(descr_label)
        self.descr_layout.addWidget(alg_label)

    def update_elements(self, event):
        width = self.sort_graphic_view.width() * 0.04
        for i, element in enumerate(self.sort_list, 0):
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

    def swap_elements(self, first, second):
        self.sort_list[first], self.sort_list[second] = self.sort_list[second], self.sort_list[first]

    @abstractmethod
    def set_states(self):
        pass

    def timerEvent(self, event=None):
        for i, state_element in enumerate(self.states_list[self.current_state], 0):
            self.sort_list[i].value = state_element.value
            self.sort_list[i].setBrush(state_element.color)

        if (self.current_state == self.max_state):
            self.current_state = 0
        else:
            self.current_state += 1

        self.update_elements(None)

    def change_play_states_wait_event(self):
        if (self.play_states_event.isSet()):
            self.play_states_event.clear()
            self.killTimer(self.current_change_state_timer)
        else:
            self.play_states_event.set()
            self.current_change_state_timer = self.startTimer(PAUSE_TIME)      

    def play_states(self):
        while(True):
            self.play_states_event.wait()
            self.change_state_timer.start(PAUSE_TIME)


class BubbleSort(SortWidget):
    def __init__(self, min_rand, max_rand, elements_count, parent=None):
        super().__init__(min_rand, max_rand, elements_count, parent)
        self.setWindowTitle(BUBBLE_SORT_STRING)
        self.set_description(BUBBLE_SORT_DESCR, BUBBLE_SORT_ALG)
        self.set_states()
        #self.sort_thread = threading.Thread(target=BubbleSort.bubble_sort, args=(self,))
        #self.sort_thread.setDaemon(True)

    def set_states(self):
        self.states_list = [[StateElement(e.value, self.standard_color) for e in self.sort_list]]
        for j in range(1, len(self.sort_list)):
            for i in range(len(self.sort_list) - j):
                #   change color in selected elements
                self.states_list.append(copy.deepcopy(self.states_list[-1]))
                self.states_list[-1][i].color = self.select_color
                self.states_list[-1][i+1].color = self.select_color
                #   swap selected elements
                self.states_list.append(copy.deepcopy(self.states_list[-1]))
                if(self.states_list[-1][i].value > self.states_list[-1][i+1].value):
                    self.states_list[-1][i], self.states_list[-1][i+1] = \
                        self.states_list[-1][i+1], self.states_list[-1][i]
                    #self.swap_elements(i, i + 1)
                #   replace color by default brush
                self.states_list.append(copy.deepcopy(self.states_list[-1]))
                self.states_list[-1][i].color = self.standard_color
                self.states_list[-1][i+1].color = self.standard_color
        self.max_state = len(self.states_list) - 1


class QuickSort(SortWidget):
    def __init__(self, min_rand, max_rand, elements_count, parent=None):
        super().__init__(min_rand, max_rand, elements_count, parent)
        self.setWindowTitle(QUICK_SORT_STRING)
        self.set_description(BUBBLE_SORT_DESCR, BUBBLE_SORT_ALG)

class SortButton(QtWidgets.QPushButton):
    __metaclass__ = ABCMeta
    @abstractmethod
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicked.connect(self.clicked_method)
        self.min_rand = MIN_RAND
        self.max_rand = MAX_RAND
        self.elements_count = ELEMENTS_COUNT

    @abstractmethod
    def clicked_method(self):
        pass

    def set_widget_params(self, min_rand, max_rand, elements_count):
        self.min_rand = min_rand
        self.max_rand = max_rand
        self.elements_count = elements_count


class BubbleSortBtn(SortButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText(BUBBLE_SORT_STRING)

    def clicked_method(self):
        self.bubble_sort_widget = BubbleSort(
            self.min_rand,
            self.max_rand,
            self.elements_count,
            self
            )
        self.bubble_sort_widget.show()


class QuickSortBtn(SortButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText(QUICK_SORT_STRING)

    def clicked_method(self):
        self.quick_sort_widget = QuickSort(
            self.min_rand,
            self.max_rand,
            self.elements_count,
            self
            )
        self.quick_sort_widget.show()
