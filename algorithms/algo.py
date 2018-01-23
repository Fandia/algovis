from abc import ABCMeta, abstractmethod

from PyQt5 import QtCore, QtGui, QtWidgets


class AlgoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Window)
