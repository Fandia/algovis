import random
import math
import json
from queue import Queue

from algorithms.algo import AlgoWidget
from PyQt5 import QtCore, QtGui, QtWidgets

#	CONSTANTS
NODE_COLOR = (0, 128, 255)
EDGE_COLOR = (0, 0, 0)
SELECT_COLOR = (234, 184, 4)
SOURCE_COLOR = (1, 178, 137)
TARGET_COLOR = SOURCE_COLOR
VISITED_COLOR = (50, 50, 50)

MATRIX_WIDTH = 5
MATRIX_HEIGHT = 5
NODES_COUNT = 10
MIN_MATRIX_WIDTH = 2
MIN_MATRIX_HEIGHT = MIN_MATRIX_WIDTH
MAX_MATRIX_WIDTH = 20
MAX_MATRIX_HEIGHT = MAX_MATRIX_WIDTH
MIN_NODES_COUNT = 3
MAX_NODES_COUNT = 400
NODE_PIXEL_WIDTH = 20
NODE_PEN_PIXEL_WIDTH = 1
EDGE_PEN_PIXEL_WIDTH = 3

BFS_ALG = r"""
<div style="overflow:auto;width:auto;border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;"><pre style="margin: 0; line-height: 125%"><span style="color: #cccccc">BFS(start_node,</span> <span style="color: #cccccc">goal_node)</span> <span style="color: #cccccc">{</span>
 <span style="color: #cdcd00">for</span><span style="color: #cccccc">(</span><span style="color: #cd00cd">all</span> <span style="color: #cccccc">nodes</span> <span style="color: #cccccc">i)</span> <span style="color: #cccccc">visited[i]</span> <span style="color: #3399cc">=</span> <span style="color: #cccccc">false;</span>
 <span style="color: #cccccc">queue</span><span style="color: #3399cc">.</span><span style="color: #cccccc">push(start_node);</span>
 <span style="color: #cccccc">visited[start_node]</span> <span style="color: #3399cc">=</span> <span style="color: #cccccc">true;</span>
 <span style="color: #cdcd00">while</span><span style="color: #cccccc">(</span><span style="color: #cccccc; border: 1px solid #FF0000">!</span> <span style="color: #cccccc">queue</span><span style="color: #3399cc">.</span><span style="color: #cccccc">empty()</span> <span style="color: #cccccc">)</span> <span style="color: #cccccc">{</span>
  <span style="color: #cccccc">node</span> <span style="color: #3399cc">=</span> <span style="color: #cccccc">queue</span><span style="color: #3399cc">.</span><span style="color: #cccccc">pop();</span>
  <span style="color: #cdcd00">if</span><span style="color: #cccccc">(node</span> <span style="color: #3399cc">==</span> <span style="color: #cccccc">goal_node)</span> <span style="color: #cccccc">{</span>
   <span style="color: #cdcd00">return</span> <span style="color: #cccccc">true;</span>
  <span style="color: #cccccc">}</span>
  <span style="color: #cccccc">foreach(child</span> <span style="color: #cdcd00">in</span> <span style="color: #cccccc">expand(node))</span> <span style="color: #cccccc">{</span>
   <span style="color: #cdcd00">if</span><span style="color: #cccccc">(visited[child]</span> <span style="color: #3399cc">==</span> <span style="color: #cccccc">false)</span> <span style="color: #cccccc">{</span>
    <span style="color: #cccccc">queue</span><span style="color: #3399cc">.</span><span style="color: #cccccc">push(child);</span>
    <span style="color: #cccccc">visited[child]</span> <span style="color: #3399cc">=</span> <span style="color: #cccccc">true;</span>
   <span style="color: #cccccc">}</span>
  <span style="color: #cccccc">}</span>
 <span style="color: #cccccc">}</span>
 <span style="color: #cdcd00">return</span> <span style="color: #cccccc">false;</span>
<span style="color: #cccccc">}</span>
</pre></div>
"""

class GraphNode(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, i, j, parent=None):
        super().__init__(parent)
        self.index = (i, j)
        self.used = False
        self.nghbrs_list_shifts = []
        self.edges_list_shifts = []
        self.id = 0
        self.visited = False

    def __str__(self):
        return str((self.index, self.id))


class GraphEdge(QtWidgets.QGraphicsLineItem):
    def __init__(self, first_nghbr, second_nghbr, parent=None):
        super().__init__(parent)
        self.first_nghbr = first_nghbr
        self.second_nghbr = second_nghbr


class GraphWidget(AlgoWidget):
    def __init__(self, width, height, max_nodes, parent=None):
        super().__init__(parent)
        self.matrix_width = width
        self.matrix_height = height
        self.nodes_matrix = [[GraphNode(i, j) for j in range(width)] for i in range(height)]
        self.max_nodes_count = max_nodes
        first_indx = (random.randint(0, height - 1), random.randint(0, width - 1))
        self.nodes_matrix[first_indx[0]][first_indx[1]].used = True
        self.nodes_list = [self.nodes_matrix[first_indx[0]][first_indx[1]]]
        self.edges_list = []
        self.crnt_nds_list_shift = 0
        self.neighbours_indxs = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]  
        self.init_graph()
        self.source_node = self.nodes_list[0]
        self.target_node = self.nodes_list[-1]
        node_pen = QtGui.QPen()
        node_pen.setWidth(NODE_PEN_PIXEL_WIDTH)
        node_pen.setColor(QtGui.QColor(*EDGE_COLOR))
        for id, node in enumerate(self.nodes_list, 0):
            node.id = id
            node.setBrush(QtGui.QColor(*NODE_COLOR))
            node.setPen(node_pen)
            self.graphic_scene.addItem(node)
            QtWidgets.QGraphicsTextItem(str(id), node)
        edge_pen = QtGui.QPen()
        edge_pen.setWidth(EDGE_PEN_PIXEL_WIDTH)
        edge_pen.setColor(QtGui.QColor(*EDGE_COLOR))
        for edge in self.edges_list:
            edge.setPen(edge_pen)
            self.graphic_scene.addItem(edge)
        self.set_states()
        self.set_by_states()
        self.states_slider.setMaximum(self.max_state)
        self.states_slider.setMinimum(0)
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
        #node_width = min(self.graphic_view.width(), self.graphic_view.height()) / self.matrix_width
        node_width = NODE_PIXEL_WIDTH
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

    def set_by_states(self):
        for i, node_state in enumerate(self.nodes_states_list[self.current_state], 0):
            self.nodes_list[i].setBrush(QtGui.QColor(*node_state["color"]))
        for i, edge_state in enumerate(self.edges_states_list[self.current_state], 0):
            edge_pen = self.edges_list[i].pen()
            edge_pen.setColor(QtGui.QColor(*edge_state["color"]))
            self.edges_list[i].setPen(edge_pen)
        self.update_graph_scene(None)
    
    def _get_edge_idx(self, src, dst):
        for i, nghbr in enumerate(src.nghbrs_list_shifts, 0):
            if nghbr == dst.id:
                return i


class BFS(GraphWidget):
    def __init__(self, width, height, max_nodes, parent=None):
        super().__init__(width, height, max_nodes, parent)
        self.setWindowTitle(self.tr("Breadth-first search"))
        self.set_description(self.tr(
        """
        <b>Breadth-first search</b> (<b>BFS</b>) is an algorithm for traversing or searching tree \
        or graph data structures. It starts at the tree root (or some arbitrary node \
        of a graph, sometimes referred to as a 'search key') and explores the neighbor \
        nodes first, before moving to the next level neighbours.
        BFS and its application in finding connected components of graphs were invented in \
        1945 by Michael Burke and Konrad Zuse, in his (rejected) Ph.D. thesis on the Plankalkül \
        programming language, but this was not published until 1972. It was reinvented in 1959 \
        by E. F. Moore, who used it to find the shortest path out of a maze, and discovered \
        independently by C. Y. Lee as a wire routing algorithm (published 1961).
        """), BFS_ALG)

    def set_states(self):
        self.nodes_states_list = [[{"color":NODE_COLOR} for _ in self.nodes_list]]
        self.edges_states_list = [[{"color":EDGE_COLOR} for _ in self.edges_list]]
        queue = Queue()
        self.source_node.visited = True
        queue.put_nowait((self.source_node, None))
        self.nodes_states_list[-1][self.source_node.id]["color"] = SOURCE_COLOR
        self.nodes_states_list[-1][self.target_node.id]["color"] = TARGET_COLOR
        while not queue.empty():
            node, prev_node = queue.get_nowait()
            self.nodes_states_list.append(json.loads(json.dumps(self.nodes_states_list[-1])))
            self.nodes_states_list[-1][node.id]["color"] = SELECT_COLOR
            self.edges_states_list.append(json.loads(json.dumps(self.edges_states_list[-1])))
            if prev_node != None:
                self.edges_states_list[-1][node.edges_list_shifts[self._get_edge_idx(node, prev_node)]]["color"] = SELECT_COLOR

            if node == self.target_node:
                break
            for nghbr_index in node.nghbrs_list_shifts:
                if not self.nodes_list[nghbr_index].visited:
                    queue.put_nowait((self.nodes_list[nghbr_index], node))
                    self.nodes_list[nghbr_index].visited = True
                    self.nodes_states_list.append(json.loads(json.dumps(self.nodes_states_list[-1])))
                    self.edges_states_list.append(json.loads(json.dumps(self.edges_states_list[-1])))
                    self.nodes_states_list[-1][nghbr_index]["color"] = VISITED_COLOR
                    self.edges_states_list[-1][node.edges_list_shifts[ \
                        self._get_edge_idx(node, self.nodes_list[nghbr_index])]]["color"] = VISITED_COLOR
        self.max_state = len(self.nodes_states_list) - 1
