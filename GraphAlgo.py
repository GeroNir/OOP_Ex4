import math
import random
from queue import Queue
from typing import List

from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface
import json
import matplotlib.pyplot as gui


class GraphAlgo(GraphAlgoInterface):
    """This class implements "GraphAlgoInterface"."""

    # constructor with a DiGraph and without, up to user
    def __init__(self, other = None):
        if not other:
            self.graph = DiGraph()
        else:
            self.graph = other

        """
        :return: the directed graph on which the algorithm works on.
        """
    def get_graph(self):
        return self.graph

    """
    Loads a graph from a json file.
    @param file_name: The path to the json file
    @returns True if the loading was successful, False o.w.
    """
    def load_from_json(self, file_name: str) -> bool:

        try:
            with open(file_name) as b1:
                f = json.load(b1)
            tmpEdges = f['Edges']
            tmpNodes = f['Nodes']
            self.graph.Edges = {}
            self.graph.Nodes = {}
            self.graph.nodeSize = len(tmpNodes)
            self.graph.edgeSize = len(tmpEdges)
            self.graph.MC = 0
            self.graph.outEdges = {}
            self.graph.inEdges = {}
            for n in tmpNodes:
                self.graph.outEdges[n['id']] = []
                self.graph.inEdges[n['id']] = []
                try:
                    tmpNodes[n['id']]['pos'] #check if there is attribute 'pos', if not, randomly added a 'pos'
                except:
                    node = {}
                    x = 35 + random.random()
                    y = 32 + random.random()
                    z = 0.0
                    pos = str(x) + "," + str(y) + "," + str(z)
                    node["pos"] = pos
                    node["id"] = n['id']
                    del tmpNodes[n['id']]
                    tmpNodes.insert(n['id'], node)
                    n = node
                self.graph.Nodes[n['id']] = n
            for e in tmpEdges:
                key = str(e['src']) + "," + str(e['dest'])
                self.graph.inEdges[e['dest']].append(e)
                self.graph.outEdges[e['src']].append(e)
                self.graph.Edges[key] = e
        except IOError as err:
            print(err)
            return False

        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        """
    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if id1 == id2:
            return 0, [id1, id2]
        dist, prev = self.dijkstra(id1)
        shortest_path = dist[id2]
        if shortest_path == float('inf'): # it means that you cant reach to id2, then return 'inf', []
            return float('inf'), []
        tmp = prev[id2]
        ans = []
        ans.insert(0, id2)
        ans.insert(0, tmp)
        while tmp != id1: # for extract all the nodes that you should go
            tmp = prev[tmp]
            ans.insert(0, tmp)
        return shortest_path, ans

    '''
    This function check if you can reach from one node to every other node. called Connectivity on Graph theory.
    For more info: https://en.wikipedia.org/wiki/Connectivity_(graph_theory)
    The logic goes like this: BFS -> Transpose -> BFS the graph is connected iff BFS reach all the nodes
    '''
    def isConnected(self) -> bool:
        bool = self.BFS_check()
        if bool:
            self.getTranspose()
            bool = self.BFS_check()
            if bool:
                self.getTranspose()
                return True
            else:
                self.getTranspose()
        return False

    '''
    This function find the shortest path for all the nodes in the graph.
    For more info: https://en.wikipedia.org/wiki/Dijkstra's_algorithm
    '''
    def dijkstra(self, src):
        visited = {}
        prev = {}
        queue = Queue()
        dist = {}
        for n in self.get_graph().get_all_v(): # set the dist for 'inf' except the src that = 0
            dist[n] = float('inf')
            visited[n] = False
        dist[src] = 0
        queue.put(src)
        while not queue.empty():
            curr = queue.get()
            if visited.get(curr) is False:
                try:
                    for i in range(len(self.get_graph().all_out_edges_of_node(curr)[curr])):
                        currDict = self.get_graph().all_out_edges_of_node(curr)[curr][i]
                        distance = dist[curr] + float(currDict['w'])
                        if distance < dist[int(currDict['dest'])] and currDict['src'] == curr:
                            dist[int(currDict['dest'])] = distance
                            prev[currDict['dest']] = int(currDict['src'])
                            queue.put(int(currDict['dest']))
                except:
                    pass
            visited[curr] = True
        return dist, prev

    '''
    This function is a method to check if from a given node you can reach all the nodes.
    BFS is a method to go through a Graph.
    For more info: https://en.wikipedia.org/wiki/Breadth-first_search  
    '''
    def BFS_check (self) -> bool:
        queue = Queue()
        queue.put(self.graph.Nodes[0]['id'])
        visited = []
        visited.append(self.graph.Nodes[0]['id'])
        while not queue.empty():
            check = queue.get()
            for e in self.graph.Edges: # go through all the edges and mark the nodes that he visit
                if self.get_graph().Edges[e]['src'] == check:
                    dest = self.graph.Edges[e]['dest']
                    if dest in visited:
                        pass
                    else:
                        queue.put(dest)
                        visited.append(dest)
        if len(visited) == self.graph.nodeSize: # check if the BFS go through all the graph
            return True
        else:
            return False

    '''
    This helper function, did a regular dijkstra, but return the max value, using for cenetrPoint()
    '''
    def dijkstra_max(self, src):
        dist, prev = self.dijkstra(src)
        max = -1
        i = 0
        indx = 0
        for d in dist.values():
            if max < d:
                max = d
                indx = i
                i += 1
        return indx, max

    '''
    This helper function, did a regular dijkstra, but return the distance list, using for TSP()
    '''
    def dijkstra_dist(self, src):
        dist, prev = self.dijkstra(src)
        return dist

    '''
    This function gets a list with an nodes, and the function returns the "best" order that you can go through all of them.
    For more info: https://en.wikipedia.org/wiki/Travelling_salesman_problem
    '''
    def TSP(self, node_lst: List[int]) -> (List[int], float):
        node_lst.sort()
        for i in range(len(node_lst)-1):
            if node_lst[i] == node_lst[i+1]:
                node_lst.pop(i)
        if len(node_lst) == 1:
            return node_lst
        dist = []
        min_dist = float('inf')
        for n in self.get_graph().get_all_v().values():
            tmp, prev = self.dijkstra(int(n['id']))
            dist.insert(int(n['id']), tmp) # check all the distances
        for n1 in node_lst: # find the first 2 nodes
            for n2 in node_lst:
                last_val = dist[n1][n2]
                if (last_val < min_dist and last_val != 0):
                    min_dist = last_val
                    src = n1
                    dest = n2
        ans = []
        node_lst_copy = node_lst.copy()
        ans.append(src)
        ans.append(dest)
        node_lst_copy.remove(src)
        node_lst_copy.remove(dest)
        last = dest
        while len(node_lst_copy) > 0: # check the min dist in a greedy way
            min_dist = float('inf')
            for n in node_lst_copy:
                last_val = dist[last][n]
                if (last_val <= min_dist and last_val != 0):
                    min_dist = last_val
                    indx = n
            if min_dist == float('inf'):
                return ans
            node_lst_copy.remove(indx)
            ans.append(indx)
            last = indx
        return ans

    """
    Saves the graph in JSON format to a file
    @param file_name: The path to the out file
    @return: True if the save was successful, False o.w.
    """
    def save_to_json(self, file_name: str) -> bool:
        try:
            Edges = []
            Nodes = []
            graph = {}
            for e in self.get_graph().Edges.values():
                Edges.append(e)
            for n in self.get_graph().Nodes.values():
                Nodes.append(n)
            graph['Edges'] = Edges
            graph['Nodes'] = Nodes
            with open(file_name, 'w') as outfile:
                json.dump(graph, outfile, indent=2)
            return True
        except:
            return False

    '''
    This function returns the Transpose Graph. it mean that is switch the source and the dest of all the edged. 
    '''
    def getTranspose(self) -> DiGraph:
        new = {}
        for e in self.get_graph().Edges.values():
            tmp = e['src']
            e['src'] = e['dest']
            e['dest'] = tmp
            new[str(e['src']) + "," + str(e['dest'])] = e
        del self.get_graph().Edges
        self.get_graph().Edges = new
        return self.get_graph()

    """
    Finds the node that has the shortest distance to it's farthest node.
    :return: The nodes id, min-maximum distance
    """
    def centerPoint(self) -> (int, float):
        if self.isConnected(): # check if the Graph is connected
            cen = []
            for n in self.graph.Nodes:
                cen.append(self.dijkstra_max(n)) # returns the max distance value
            min = float('inf')
            indx = 0
            for i in cen: # choose the minimum from all the max values
                if i[1] < min:
                    min = i[1]
                    indx = i[0]
            return indx, min
        else:
            return -1, float('inf')

    """
    Plots the graph.
    If the nodes have a position, the nodes will be placed there.
    Otherwise, they will be placed in a random but elegant manner.
    @return: None
    """
    def plot_graph(self) -> None:
        graph = self.graph
        for node in graph.get_all_v().keys():
            if graph.get_pos(node) is None:
                node.pos = (random.uniform(0, 5), random.uniform(0, 5), 0)
            gui.text(graph.get_x(node), graph.get_y(node), str(node), horizontalalignment='center',
                     verticalalignment='center',
                     bbox=dict(facecolor='green', edgecolor='black', boxstyle='circle, pad=0.1'))

        for src in graph.get_all_v().keys():
            for dest in graph.outEdges[src]:
                        radius = 0.0001
                        x_src = graph.get_x(src)
                        y_src = graph.get_y(src)
                        x_dest = graph.get_x(dest.get('dest'))
                        y_dest = graph.get_y(dest.get('dest'))
                        distance = math.sqrt((x_src - x_dest) ** 2 + (y_src - y_dest) ** 2)
                        direction_x = (x_src - x_dest) / distance
                        direction_y = (y_src - y_dest) / distance
                        x_dest = direction_x * radius + x_dest
                        y_dest = direction_y * radius + y_dest
                        x_src = direction_x * (-radius) + x_src
                        y_src = direction_y * (-radius) + y_src
                        gui.arrow(x_src, y_src, (x_dest - x_src), (y_dest - y_src), length_includes_head=True,
                                  width=0.000003, head_width=0.00025, color="black")
        gui.show()


