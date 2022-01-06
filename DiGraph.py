import json
from collections import defaultdict
import string
import random

from typing import cast
from GraphInterface import GraphInterface

"""This class implements the interface "GraphInterface"."""
class DiGraph(GraphInterface):

    def __init__(self): #default constructor
        self.Edges = {}
        self.Nodes = {}
        self.nodeSize = 0
        self.edgeSize = 0
        self.MC = 0
        self.outEdges = {}
        self.inEdges = {}
        tmpIn = {}
        tmpOut = {}
        self.visited = []

        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
    def v_size(self) -> int:
        return self.nodeSize

    """
    Returns the number of edges in this graph
    @return: The number of edges in this graph
    """
    def e_size(self) -> int:
        return self.edgeSize

    """return a dictionary of all the nodes in the Graph, each node is represented using a pair
    (node_id, node_data)
    """
    def get_all_v(self) -> dict:
        return self.Nodes

    """return a dictionary of all the nodes connected to (into) node_id ,
    each node is represented using a pair (other_node_id, weight)
    """
    def all_in_edges_of_node(self, id) -> dict:
        tmp = {}
        tmp[id] = self.inEdges[id]
        return tmp

    """
    return a dictionary of all the nodes connected from node_id , each node is represented using a pair
    (other_node_id, weight)
    """
    def all_out_edges_of_node(self, id) -> dict:
        tmp = {}
        tmp[id] = self.outEdges[id]
        return tmp

    """
    Returns the current version of this graph,
    on every change in the graph state - the MC should be increased
    @return: The current version of this graph.
    """
    def get_mc(self) -> int:
        return self.MC

    """
    Adds an edge to the graph.
    @param id1: The start node of the edge
    @param id2: The end node of the edge
    @param weight: The weight of the edge
    @return: True if the edge was added successfully, False o.w.
    Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
    """
    def add_edge(self, src: int, dest: int, weight: float) -> bool:
        # check if the edge is already exists
        key = str(src) + "," + str(dest)
        try:
            self.Edges[key]
            return False
        except:
            try:
                self.Nodes[src]
                self.Nodes[dest]
                e = {}
                e['src'] = src
                e['w'] = weight
                e['dest'] = dest
                self.Edges[key] = e
                self.inEdges[e['dest']].append(e)
                self.outEdges[e['src']].append(e)
                self.MC += 1
                self.edgeSize += 1
                return True
            except:
                return False

    """
    Adds a node to the graph.
    @param node_id: The node ID
    @param pos: The position of the node
    @return: True if the node was added successfully, False o.w.
    Note: if the node id already exists the node will not be added
    """
    def add_node(self, node_id: int, pos: tuple = None) -> bool:  # O(n) n = nodeSize
        try:
            self.Nodes[node_id]
            return False
        except:
            if not pos:
                n = {}
                x = 35 + random.random()
                y = 32 + random.random()
                z = 0.0
                pos = str(x) + "," + str(y) + "," + str(z)
                n["pos"] = pos
                n["id"] = node_id
                self.Nodes[node_id] = n
                self.MC += 1
                self.nodeSize += 1
            else:
                n = {}
                n["pos"] = pos
                n["id"] = node_id
                self.Nodes[node_id] = n
                self.MC += 1
                self.nodeSize += 1
            self.inEdges[node_id] = []
            self.outEdges[node_id] = []
            return True

    """
    Removes a node from the graph.
    @param node_id: The node ID
    @return: True if the node was removed successfully, False o.w.
    Note: if the node id does not exists the function will do nothing
    """
    def remove_node(self, node_id: int) -> bool:
        rm = self.Nodes.pop(node_id, None)
        if (rm != None):
            for e in self.inEdges[node_id]:
                key = str(e['src']) + "," + str(e['dest'])
                self.Edges.pop(key)
            for e in self.outEdges[node_id]:
                key = str(e['src']) + "," + str(e['dest'])
                self.Edges.pop(key)
            self.nodeSize -= 1
            self.edgeSize -= len(self.inEdges[node_id]) + len(self.outEdges[node_id])
            self.MC = 1 + len(self.inEdges[node_id]) + len(self.outEdges[node_id])
            del self.inEdges[node_id]
            del self.outEdges[node_id]
            return True
        return False

    """
    Removes an edge from the graph.
    @param node_id1: The start node of the edge
    @param node_id2: The end node of the edge
    @return: True if the edge was removed successfully, False o.w.
    Note: If such an edge does not exists the function will do nothing
    """
    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        key = str(node_id1) + "," + str(node_id2)
        rm = self.Edges.pop(key, None)
        if (rm != None):
            i = 0
            for n in self.outEdges[node_id1]:
                i += 1
                if n['dest'] == node_id2:
                    self.outEdges[node_id1].remove(n)
            i = 0
            for n in self.inEdges[node_id2]:
                if n['src'] == node_id1:
                    self.inEdges[node_id2].remove(n)
            self.MC += 1
            return True
        return False

# this function prints the Digraph
    def __repr__(self):
        return f'DiGraph\nEdges:\n{self.Edges}\nNodes:\n{self.Nodes}'

    def get_node(self, node_id: int):
        return self.get_all_v().get(node_id)

    def get_pos(self, node_id: int):
        return self.get_node(node_id).get('pos')

    def get_x(self, node_id: int):
        s = self.get_pos(node_id)
        s: cast(string, s)
        s = s.split(',')
        return float(s[0])

    def get_y(self, node_id: int):
        s = self.get_pos(node_id)
        s: cast(string, s)
        s = s.split(',')
        return float(s[1])

    def get_z(self, node_id: int):
        s = self.get_pos(node_id)
        s: cast(string, s)
        s = s.split(',')
        return float(s[2])

    def load(self, file): # only for testing
        with open(file) as b1:
            f = json.load(b1)
        tmpEdges = f['Edges']
        tmpNodes = f['Nodes']
        self.Edges = {}
        self.Nodes = {}
        self.nodeSize = len(tmpNodes)
        self.edgeSize = len(tmpEdges)
        self.MC = 0
        self.outEdges = []
        self.inEdges = []
        for n in tmpNodes:
            self.outEdges.insert(0, [])
            self.inEdges.insert(0, [])
            self.Nodes[n['id']] = n
        for e in tmpEdges:
            key = str(e['src']) + "," + str(e['dest'])
            self.inEdges[e['dest']].insert(0, e)
            self.outEdges[e['src']].insert(0, e)
            self.Edges[key] = e