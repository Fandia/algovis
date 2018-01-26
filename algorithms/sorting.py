# -*- coding: UTF-8 -*-
import random
import threading
import time
import copy
import math
import json
from abc import ABCMeta, abstractmethod

from algorithms.algo import AlgoWidget
from PyQt5 import QtCore, QtGui, QtWidgets

#    CONSTANTS
SORT_WIN_WIDTH = 800
SORT_WIN_HEIGHT = 800

PAUSE_TIME = 500

MIN_RAND = 1
MAX_RAND = 20
ELEMENTS_COUNT = 20
MIN_ELEMENTS_COUNT = 2
MAX_ELEMENTS_COUNT = 50
MIN_RAND_RANGE = -50
MAX_RAND_RANGE = 50

ELEMENT_COLOR = (0, 128, 255)
SELECT_COLOR = (255, 190, 0)

BUBBLE_SORT_STRING = "Сортировка пузырьком"
QUICK_SORT_STRING = "Быстрая сортировка"
ELEMENTS_COUNT_STRING = "Количество элементов"
MIN_RAND_RANGE_STRING = "Минимум"
MAX_RAND_RANGE_STRING = "Максимум"
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

class SortWidget(AlgoWidget):
    def __init__(self, min_rand, max_rand, elements_count, parent=None):
        super().__init__(parent)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.play_layout = QtWidgets.QHBoxLayout()
        self.descr_layout = QtWidgets.QHBoxLayout()
        self.sort_graphic_scene = QtWidgets.QGraphicsScene()
        self.sort_graphic_view = QtWidgets.QGraphicsView(self.sort_graphic_scene)
        #   Play buttons
        self.play_button = QtWidgets.QPushButton("Play - Pause", self)
        self.play_button.clicked.connect(self.change_play_states_wait_event)
        self.next_button = QtWidgets.QPushButton("Next", self)
        self.next_button.clicked.connect(self.next_state)
        self.prev_button = QtWidgets.QPushButton("Previous", self)
        self.prev_button.clicked.connect(self.prev_state)
        self.play_layout.addWidget(self.prev_button)
        self.play_layout.addWidget(self.play_button)
        self.play_layout.addWidget(self.next_button)
        #   States slider
        self.states_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.states_slider.valueChanged.connect(self.slider_changed)
        self.states_slider.sliderPressed.connect(self.slider_pressed)
        self.states_slider.sliderReleased.connect(self.slider_released)

        self.sort_list = []
        self.states_list = []
        self.current_state = 0
        self.max_state = 0
        self.play_states_event = threading.Event()
        self.play_states_event.clear()
        self.current_change_state_timer = 0

        self.max_value = max_rand
        self.values_range = max(abs(max_rand - min_rand), abs(max_rand), abs(min_rand))
        self.select_color = SELECT_COLOR
        self.standard_color = ELEMENT_COLOR

        for i in range(elements_count):
            element = SortElement(random.randint(min_rand, max_rand))
            element.setBrush(QtGui.QColor(*self.standard_color))
            self.sort_list.append(element)
            self.sort_graphic_scene.addItem(self.sort_list[-1])

        if(min_rand >= 0 and max_rand >= 0):
            self.ground_level = self.sort_graphic_view.height()
        elif(min_rand < 0 and max_rand > 0):
            self.ground_level = (1 - abs(min_rand) / self.values_range) * self.sort_graphic_view.height()
        else:
            self.ground_level = 0

        self.set_states()
        self.states_slider.setMaximum(self.max_state)
        self.states_slider.setMinimum(0)

        self.main_layout.addWidget(self.sort_graphic_view)
        self.main_layout.addWidget(self.states_slider)
        self.main_layout.addLayout(self.play_layout)
        self.main_layout.addLayout(self.descr_layout)
        self.setLayout(self.main_layout)
        self.paintEvent = self.update_diagramm
        self.resize(SORT_WIN_WIDTH, SORT_WIN_HEIGHT)

    def set_description(self, descr_str, alg_str):
        descr_label = QtWidgets.QLabel(descr_str)
        alg_label = QtWidgets.QLabel(alg_str)
        self.descr_layout.addWidget(descr_label)
        self.descr_layout.addWidget(alg_label)

    def update_diagramm(self, event):
        width = math.floor(self.sort_graphic_view.width() / len(self.sort_list))
        for i, element in enumerate(self.sort_list, 0):
            height = math.floor(abs(element.value) / self.values_range * self.sort_graphic_view.height())
            if(element.value > 0):
                y = self.ground_level - height
            else:
                y = self.ground_level
            element.setRect(i * width, math.floor(y), width, height)
        new_rect = self.sort_graphic_scene.itemsBoundingRect()
        border = 0.1 * min(new_rect.width(), new_rect.height())
        new_rect.setRect(new_rect.x() - border, new_rect.y() - border,
            new_rect.width() + border * 2, new_rect.height() + border * 2)
        self.sort_graphic_scene.setSceneRect(new_rect)
        self.sort_graphic_view.fitInView(new_rect)

    def set_states(self):
        pass

    def set_by_states(self):
        for i, state_element in enumerate(self.states_list[self.current_state], 0):
            self.sort_list[i].value = state_element["value"]
            self.sort_list[i].setBrush(QtGui.QColor(*state_element["color"]))
        self.update_diagramm(None)

    def timerEvent(self, event=None):
        self.set_by_states()
        if (self.current_state == self.max_state):
            #self.current_state = 0
            self.play_states_event.clear()
            self.killTimer(self.current_change_state_timer)
        else:
            self.current_state += 1
        self.states_slider.setValue(self.current_state)

    def change_play_states_wait_event(self):
        if (self.play_states_event.isSet()):
            self.play_states_event.clear()
            self.killTimer(self.current_change_state_timer)
        else:
            self.play_states_event.set()
            self.current_change_state_timer = self.startTimer(PAUSE_TIME)

    def slider_pressed(self):
        if (self.play_states_event.isSet()):
            self.killTimer(self.current_change_state_timer)
        self.current_state = self.states_slider.value()
        self.set_by_states()

    def slider_released(self):
        self.current_state = self.states_slider.value()
        self.set_by_states()
        if(self.play_states_event.isSet()):
            self.current_change_state_timer = self.startTimer(PAUSE_TIME)

    def slider_changed(self):
        self.current_state = self.states_slider.value()
        self.set_by_states()

    def next_state(self):
        if (self.current_state != self.max_state):
            self.current_state += 1
        self.states_slider.setValue(self.current_state)
        self.set_by_states()

    def prev_state(self):
        if (self.current_state != 0):
            self.current_state -= 1
        self.states_slider.setValue(self.current_state)
        self.set_by_states()


class BubbleSort(SortWidget):
    def __init__(self, min_rand, max_rand, elements_count, parent=None):
        super().__init__(min_rand, max_rand, elements_count, parent)
        self.setWindowTitle(BUBBLE_SORT_STRING)
        self.set_description(BUBBLE_SORT_DESCR, BUBBLE_SORT_ALG)

    def set_states(self):
        self.states_list = [[{"value":e.value, "color":self.standard_color} for e in self.sort_list]]
        for j in range(1, len(self.sort_list)):
            for i in range(len(self.sort_list) - j):
                #   change color in selected elements
                #self.states_list.append(copy.deepcopy(self.states_list[-1]))
                self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                self.states_list[-1][i]["color"] = self.select_color
                self.states_list[-1][i+1]["color"] = self.select_color
                #   swap selected elements
                self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                if(self.states_list[-1][i]["value"] > self.states_list[-1][i+1]["value"]):
                    self.states_list[-1][i], self.states_list[-1][i+1] = \
                        self.states_list[-1][i+1], self.states_list[-1][i]
                #   replace color by default brush
                self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                self.states_list[-1][i]["color"] = self.standard_color
                self.states_list[-1][i+1]["color"] = self.standard_color
        self.max_state = len(self.states_list) - 1


class QuickSort(SortWidget):
    def __init__(self, min_rand, max_rand, elements_count, parent=None):
        super().__init__(min_rand, max_rand, elements_count, parent)
        self.setWindowTitle(QUICK_SORT_STRING)
        self.set_description(BUBBLE_SORT_DESCR, BUBBLE_SORT_ALG)
