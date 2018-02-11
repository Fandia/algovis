# -*- coding: UTF-8 -*-
import random
import time
import math
import json

from algorithms.algo import *
from PyQt5 import QtCore, QtGui, QtWidgets

#    CONSTANTS
MIN_RAND = 1
MAX_RAND = 20
ELEMENTS_COUNT = 20
MIN_ELEMENTS_COUNT = 2
MAX_ELEMENTS_COUNT = 50
MIN_RAND_RANGE = -50
MAX_RAND_RANGE = 50

ELEMENT_COLOR = (0, 128, 255)
SELECT_COLOR = (255, 190, 0)
PIVOT_COLOR = (240, 0, 20)

BUBBLE_SORT_ALG = r"""
FOR J=1 TO N-1 STEP 1
    F=0
    FOR I=1 TO N-J STEP 1
        IF A[I]>A[I+1] THEN SWAP A[I],A[I+1]:F=1
    NEXT I
    IF F=0 THEN EXIT FOR
NEXT J
"""
QUICK_SORT_ALG = r"""
algorithm quicksort(A, lo, hi) is
    if lo < hi then
        p := partition(A, lo, hi)
        quicksort(A, lo, p – 1)
        quicksort(A, p, hi)

algorithm partition(A, lo, hi) is
    pivot := get_pivot(A, lo, hi)
    i := lo
    j := hi    
    while i <= j do
        while A[i] < pivot do
          i := i + 1 
        while A[j] > pivot do
          j := j - 1 
        if i <= j then
            swap A[i] with A[j]
            i := i + 1
            j := j - 1
    return i
"""

class SortElement(QtWidgets.QGraphicsRectItem):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.value = value

class SortWidget(AlgoWidget):
    def __init__(self, min_rand, max_rand, elements_count, parent=None):
        super().__init__(parent)
        self.sort_list = []

        self.max_value = max_rand
        self.values_range = max(abs(max_rand - min_rand), abs(max_rand), abs(min_rand))

        element_pen = QtGui.QPen()
        element_pen.setWidth(2)
        for i in range(elements_count):
            element = SortElement(random.randint(min_rand, max_rand))
            element.setBrush(QtGui.QColor(*ELEMENT_COLOR))
            element.setPen(element_pen)
            text = QtWidgets.QGraphicsTextItem(str(element.value), element)
            self.sort_list.append(element)
            self.graphic_scene.addItem(self.sort_list[-1])

        if(min_rand >= 0 and max_rand >= 0):
            self.ground_level = self.graphic_view.height()
        elif(min_rand < 0 and max_rand > 0):
            self.ground_level = math.floor((1 - abs(min_rand) / self.values_range) * self.graphic_view.height())
        else:
            self.ground_level = 0

        self.states_list = []
        self.set_states()
        self.states_slider.setMaximum(self.max_state)
        self.states_slider.setMinimum(0)

        self.paintEvent = self.update_diagramm
        self.resizeEvent = self.update_diagramm

    def update_diagramm(self, event):
        width = self.graphic_view.width() / len(self.sort_list)
        for i, element in enumerate(self.sort_list, 0):
            height = math.floor(abs(element.value) / self.values_range * self.graphic_view.height())
            if(element.value > 0):
                y = self.ground_level - height
            else:
                y = self.ground_level
            element.setRect(i * width, math.floor(y), width, height)
            element.childItems()[0].setPlainText(str(element.value))
            current_font = element.childItems()[0].font()
            current_font.setPixelSize(width / 2.5)
            text_width = element.childItems()[0].boundingRect().width()
            text_height = element.childItems()[0].boundingRect().height()
            element.childItems()[0].setFont(current_font)
            element.childItems()[0].setPos(i * width + (width - text_width) / 2, math.floor(y) - text_height)
        new_rect = self.graphic_scene.itemsBoundingRect()
        border = 0.1 * min(new_rect.width(), new_rect.height())
        new_rect.setRect(new_rect.x() - border, new_rect.y() - border,
            new_rect.width() + border * 2, new_rect.height() + border * 2)
        self.graphic_scene.setSceneRect(new_rect)
        self.graphic_view.fitInView(new_rect)

    def set_by_states(self):
        for i, state_element in enumerate(self.states_list[self.current_state], 0):
            self.sort_list[i].value = state_element["value"]
            self.sort_list[i].setBrush(QtGui.QColor(*state_element["color"]))
        self.update_diagramm(None)


class BubbleSort(SortWidget):
    def __init__(self, min_rand, max_rand, elements_count, parent=None):
        super().__init__(min_rand, max_rand, elements_count, parent)
        self.setWindowTitle(self.tr("Bubble sort"))
        self.set_description(self.tr(
        """
        <b>Bubble sort</b>, sometimes referred to as <b>sinking sort</b>, is a simple sorting algorithm that repeatedly \
        steps through the list to be sorted, compares each pair of adjacent items and swaps them if they are \
        in the wrong order. The pass through the list is repeated until no swaps are needed, which indicates \
        that the list is sorted. The algorithm, which is a comparison sort, is named for the way smaller or \
        larger elements "bubble" to the top of the list. Although the algorithm is simple, it is too slow and \
        impractical for most problems even when compared to insertion sort. It can be practical if the input \
        is usually in sorted order but may occasionally have some out-of-order elements nearly in position.\
        """), BUBBLE_SORT_ALG)

    def set_states(self):
        self.states_list = [[{"value":e.value, "color":ELEMENT_COLOR} for e in self.sort_list]]
        for j in range(1, len(self.sort_list)):
            done = True
            for i in range(len(self.sort_list) - j):
                #   change color in selected elements
                self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                self.states_list[-1][i]["color"] = SELECT_COLOR
                self.states_list[-1][i+1]["color"] = SELECT_COLOR
                #   swap selected elements
                self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                if(self.states_list[-1][i]["value"] > self.states_list[-1][i+1]["value"]):
                    self.states_list[-1][i], self.states_list[-1][i+1] = \
                        self.states_list[-1][i+1], self.states_list[-1][i]
                    done = False
                #   replace color by default brush
                self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                self.states_list[-1][i]["color"] = ELEMENT_COLOR
                self.states_list[-1][i+1]["color"] = ELEMENT_COLOR
            if (done):
                break
        self.max_state = len(self.states_list) - 1


class QuickSort(SortWidget):
    def __init__(self, min_rand, max_rand, elements_count, parent=None):
        super().__init__(min_rand, max_rand, elements_count, parent)
        self.setWindowTitle(self.tr("Quick sort"))
        self.set_description(self.tr(
        """
        <b>Quicksort</b> (sometimes called <b>partition-exchange sort</b>) is an efficient sorting algorithm, \
        serving as a systematic method for placing the elements of an array in order. \
        Developed by <a href="https://en.wikipedia.org/wiki/Tony_Hoare">Tony Hoare</a> in 1959 and published in 1961, \
        it is still a commonly used algorithm for sorting. When implemented well, it can be about two or three \
        times faster than its main competitors, merge sort and heapsort.
        Quicksort is a comparison sort, meaning that it can sort items of any type for which a "less-than" relation \
        (formally, a total order) is defined. In efficient implementations it is not a stable sort, meaning that the \
        relative order of equal sort items is not preserved. Quicksort can operate in-place on an array, requiring \
        small additional amounts of memory to perform the sorting. It is very similar to selection sort, except that \
        it does not always choose worst-case partition.
        """), QUICK_SORT_ALG)

    def set_states(self):
        self.states_list = [[{"value":e.value, "color":ELEMENT_COLOR} for e in self.sort_list]]
        def get_pivot(lo, hi):
            # for element in self.states_list[-1]:
            #     if element["color"] == PIVOT_COLOR:
            #         element["color"] = ELEMENT_COLOR
            # self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
            # self.states_list[-1][hi]["color"] = PIVOT_COLOR
            return self.states_list[-1][hi]["value"]

        def partition(lo, hi):
            pivot = get_pivot(lo, hi)
            i = lo
            j = hi
            self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
            self.states_list[-1][i]["color"] = SELECT_COLOR
            self.states_list[-1][j]["color"] = SELECT_COLOR
            while i <= j:
                while self.states_list[-1][i]["value"] < pivot:
                    self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                    self.states_list[-1][i]["color"] = ELEMENT_COLOR
                    i += 1
                    self.states_list[-1][i]["color"] = SELECT_COLOR
                while self.states_list[-1][j]["value"] > pivot:
                    self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                    self.states_list[-1][j]["color"] = ELEMENT_COLOR
                    j -= 1
                    self.states_list[-1][j]["color"] = SELECT_COLOR
                if i < j:
                    self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                    self.states_list[-1][i], self.states_list[-1][j] = \
                    self.states_list[-1][j], self.states_list[-1][i]
                    self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                    self.states_list[-1][i]["color"] = ELEMENT_COLOR
                    self.states_list[-1][j]["color"] = ELEMENT_COLOR
                    i += 1
                    j -= 1
                    self.states_list[-1][i]["color"] = SELECT_COLOR
                    self.states_list[-1][j]["color"] = SELECT_COLOR
                else:
                    break
            self.states_list[-1][i]["color"] = ELEMENT_COLOR
            self.states_list[-1][j]["color"] = ELEMENT_COLOR
            return i

        def quicksort(lo, hi):
            if lo < hi:
                p = partition(lo, hi)
                quicksort(lo, p - 1)
                quicksort(p, hi)
        quicksort(0, len(self.states_list[-1]) - 1)

        for j in range(1, len(self.sort_list)):
            done = True
            for i in range(len(self.sort_list) - j):
                #   change color in selected elements
                self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                self.states_list[-1][i]["color"] = SELECT_COLOR
                self.states_list[-1][i+1]["color"] = SELECT_COLOR
                #   swap selected elements
                self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                if(self.states_list[-1][i]["value"] > self.states_list[-1][i+1]["value"]):
                    self.states_list[-1][i], self.states_list[-1][i+1] = \
                        self.states_list[-1][i+1], self.states_list[-1][i]
                    done = False
                #   replace color by default brush
                self.states_list.append(json.loads(json.dumps(self.states_list[-1])))
                self.states_list[-1][i]["color"] = ELEMENT_COLOR
                self.states_list[-1][i+1]["color"] = ELEMENT_COLOR
            if (done):
                break
        self.max_state = len(self.states_list) - 1
