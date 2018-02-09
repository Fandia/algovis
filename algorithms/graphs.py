import random
import math

from algorithms.algo import AlgoWidget
from PyQt5 import QtCore, QtGui, QtWidgets

#	CONSTANTS
NODE_COLOR = (0, 128, 255)
SELECT_COLOR = (255, 190, 0)
PIVOT_COLOR = (240, 0, 20)

class GraphNode(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, i, j, parent=None):
        super().__init__(parent)
        self.index = (i, j)
        self.used = False
        self.nghbrs_list_shifts = []
        self.edges_list_shifts = []
        self.id = 0

    def __str__(self):
        return str((self.index, self.id))


class GraphEdge(QtWidgets.QGraphicsLineItem):
    def __init__(self, first_nghbr, second_nghbr, parent=None):
        super().__init__(parent)
        self.first_nghbr = first_nghbr
        self.second_nghbr = second_nghbr


class GraphWidget(AlgoWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.matrix_width = width
        self.matrix_height = height
        self.nodes_matrix = [[GraphNode(i, j) for j in range(width)] for i in range(height)]
        self.max_nodes_count = random.randint(3, height * width)
        first_indx = (random.randint(0, height - 1), random.randint(0, width - 1))
        self.nodes_matrix[first_indx[0]][first_indx[1]].used = True
        self.nodes_list = [self.nodes_matrix[first_indx[0]][first_indx[1]]]
        self.edges_list = []
        self.crnt_nds_list_shift = 0
        #   4 neighbours: top, right, bottom and left
        self.neighbours_indxs = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]  
        self.init_graph()
        node_pen = QtGui.QPen()
        node_pen.setWidth(4)
        for id, node in enumerate(self.nodes_list, 0):
            node.id = id
            node.setBrush(QtGui.QColor(*NODE_COLOR))
            node.setPen(node_pen)
            self.graphic_scene.addItem(node)
            QtWidgets.QGraphicsTextItem(str(id), node)
        edge_pen = QtGui.QPen()
        edge_pen.setWidth(8)
        for edge in self.edges_list:
            edge.setPen(edge_pen)
            self.graphic_scene.addItem(edge)
        self.paintEvent = self.update_graph_scene
        self.resizeEvent = self.update_graph_scene

    def init_graph(self):
        crnt_node = self.nodes_list[self.crnt_nds_list_shift]
        crnt_node_indx = crnt_node.index
        rnd_neighbours_flg = [bool(random.randint(0,1)) for _ in range(len(self.neighbours_indxs))]
        if not any(rnd_neighbours_flg):            
            rnd_neighbours_flg[random.randint(0,len(rnd_neighbours_flg) - 1)] = True
        for indx, neighbour_flg in enumerate(rnd_neighbours_flg, 0):
            if len(self.nodes_list) < self.max_nodes_count:                        
                neighbour_index = (crnt_node_indx[0] + self.neighbours_indxs[indx][0], \
                    crnt_node_indx[1] + self.neighbours_indxs[indx][1])
                if neighbour_index[0] < self.matrix_height and neighbour_index[0] >= 0 and \
                    neighbour_index[1] < self.matrix_width and neighbour_index[1] >= 0:
                    crnt_neighbour = self.nodes_matrix[neighbour_index[0]][neighbour_index[1]]
                    if neighbour_flg and not crnt_neighbour.used:
                        crnt_neighbour.used = True
                        crnt_neighbour.nghbrs_list_shifts.append(self.crnt_nds_list_shift)
                        self.nodes_list.append(crnt_neighbour)
                        crnt_node.nghbrs_list_shifts.append(len(self.nodes_list) - 1)
                        self.edges_list.append(GraphEdge(self.crnt_nds_list_shift, len(self.nodes_list) - 1))
                        crnt_neighbour.edges_list_shifts.append(len(self.edges_list) - 1)
                        crnt_node.edges_list_shifts.append(len(self.edges_list) - 1)

        if len(self.nodes_list) < self.max_nodes_count and len(self.nodes_list) - 1 > self.crnt_nds_list_shift:
            self.crnt_nds_list_shift += 1
            self.init_graph()

    def update_graph_scene(self, event):
        node_width = min(self.graphic_view.width(), self.graphic_view.height()) / self.matrix_width
        distance = node_width
        for node in self.nodes_list:
            x = node.index[0] * (node_width + distance)
            y = node.index[1] * (node_width + distance)
            node.setRect(x, y, node_width, node_width)
            node.setZValue(1)
            current_font = node.childItems()[0].font()
            current_font.setPixelSize(node_width / 2.5)
            text_width = node.childItems()[0].boundingRect().width()
            text_height = node.childItems()[0].boundingRect().height()
            node.childItems()[0].setFont(current_font)
            node.childItems()[0].setPos(x + (node_width - text_width) / 2, y + (node_width - text_height) / 2)
        for edge in self.edges_list:
            first_node = self.nodes_list[edge.first_nghbr]
            second_node = self.nodes_list[edge.second_nghbr]
            frst_pnt_x = first_node.rect().x() + first_node.rect().width() / 2
            frst_pnt_y = first_node.rect().y() + first_node.rect().height() / 2
            scnd_pnt_x = second_node.rect().x() + second_node.rect().width() / 2
            scnd_pnt_y = second_node.rect().y() + second_node.rect().height() / 2
            edge.setLine(frst_pnt_x, frst_pnt_y, scnd_pnt_x, scnd_pnt_y)
        new_rect = self.graphic_scene.itemsBoundingRect()
        border = 0.1 * min(new_rect.width(), new_rect.height())
        new_rect.setRect(new_rect.x() - border, new_rect.y() - border,
            new_rect.width() + border * 2, new_rect.height() + border * 2)
        self.graphic_scene.setSceneRect(new_rect)
        self.graphic_view.fitInView(new_rect, QtCore.Qt.KeepAspectRatio)


class BFS(GraphWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(width, height, parent)
        self.setWindowTitle(self.tr("Breadth-first search"))
