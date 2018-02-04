import threading
import copy

from PyQt5 import QtCore, QtGui, QtWidgets

#   CONSTANTS
PAUSE_TIME = 500
WIN_DISPL_PART = 0.6
FONT_DISPL_PART = 0.02
BTN_DISPL_PART = 0.02

class AlgoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()
        self.screen_width, self.screen_height = screen_geometry.width(), screen_geometry.height()
        self.screen_base = min(self.screen_width, self.screen_height)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Window)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.vis_layout = QtWidgets.QHBoxLayout()
        self.play_layout = QtWidgets.QHBoxLayout()
        self.sort_graphic_scene = QtWidgets.QGraphicsScene()
        self.sort_graphic_view = QtWidgets.QGraphicsView(self.sort_graphic_scene)
        #   Play buttons
        left_dummy = QtWidgets.QWidget(self)
        right_dummy = QtWidgets.QWidget(self)
        buttons_size = QtCore.QSize(self.screen_base * BTN_DISPL_PART, self.screen_base * BTN_DISPL_PART)
        self.play_button = QtWidgets.QPushButton(self)
        self.play_button.clicked.connect(self.change_play_states_wait_event)
        play_image = QtGui.QPixmap("res/play.png")
        play_icon = QtGui.QIcon(play_image)
        self.play_button.setIcon(play_icon)
        self.play_button.setIconSize(buttons_size)
        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.clicked.connect(self.next_state)
        next_image = QtGui.QPixmap("res/next.png")
        next_icon = QtGui.QIcon(next_image)
        self.next_button.setIcon(next_icon)
        self.next_button.setIconSize(buttons_size)
        self.prev_button = QtWidgets.QPushButton(self)
        self.prev_button.clicked.connect(self.prev_state)
        prev_image = next_image.transformed(QtGui.QTransform().scale(-1, 1))
        prev_icon = QtGui.QIcon(prev_image)
        self.prev_button.setIcon(prev_icon)
        self.prev_button.setIconSize(buttons_size)
        self.play_layout.addWidget(left_dummy, 1)
        self.play_layout.addWidget(self.prev_button)
        self.play_layout.addWidget(self.play_button)
        self.play_layout.addWidget(self.next_button)
        self.play_layout.addWidget(right_dummy, 1)
        #   States slider
        self.states_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.states_slider.valueChanged.connect(self.slider_changed)
        self.states_slider.sliderPressed.connect(self.slider_pressed)
        self.states_slider.sliderReleased.connect(self.slider_released)
        #   Horizontal line
        h_line_top = QtWidgets.QFrame(self)
        h_line_top.setFrameShape(QtWidgets.QFrame.HLine)
        h_line_top.setFrameShadow(QtWidgets.QFrame.Sunken)
        h_line_bottom = QtWidgets.QFrame(self)
        h_line_bottom.setFrameShape(QtWidgets.QFrame.HLine)
        h_line_bottom.setFrameShadow(QtWidgets.QFrame.Sunken)
        #   Description and pseudocode widget
        self.description = QtWidgets.QLabel(self)
        self.pseudocode = QtWidgets.QLabel(self)
        self.vis_layout.addWidget(self.sort_graphic_view)
        self.vis_layout.addWidget(self.pseudocode)        
        #   States initialization
        self.states_list = []
        self.current_state = 0
        self.max_state = 0
        self.play_states_event = threading.Event()
        self.play_states_event.clear()
        self.current_change_state_timer = 0
        self.main_layout.addLayout(self.vis_layout)
        self.main_layout.addWidget(self.states_slider)
        self.main_layout.addLayout(self.play_layout)
        self.main_layout.addWidget(h_line_top)
        self.main_layout.addWidget(self.description)
        self.main_layout.addWidget(h_line_bottom)
        self.setLayout(self.main_layout)
        self.resize(self.screen_width * WIN_DISPL_PART, self.screen_height * WIN_DISPL_PART)
        self.setGeometry(QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight, 
            QtCore.Qt.AlignCenter, 
            self.size(), 
            screen_geometry
            ))

    def set_states(self):
        raise NotImplementedError("set_states method not implemented")

    def set_by_states(self):
        raise NotImplementedError("set_by_states method not implemented")

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
        if (self.states_slider.value() >= 0):
            self.current_state = self.states_slider.value()
        else:
            self.current_state = 0
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
