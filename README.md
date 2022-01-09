# Object Oriented Programming - Pokemon game
**By:**
*Hagai Hen 313414872* 

*Nir Geron 315874925*

![Pokemon](https://upload.wikimedia.org/wikipedia/commons/9/98/International_Pok%C3%A9mon_logo.svg)

 
 This project is used for an implementation of a directed Weighted Graph in python language.
 
# Literature:
#### `1.Dijkstra's Algorithm`:
	https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/
#### `2.Depth First Search or DFS`:
https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/
#### `3.Traveling Salesman Problem (TSP)`:
	https://www.geeksforgeeks.org/traveling-salesman-problem-tsp-implementation/
#### `4.graph using Dictionary`:
https://www.geeksforgeeks.org/generate-graph-using-dictionary-python/

### **how to start?**
first clone this repository using this following command:
 ```
$git clone https://github.com/GeroNir/OOP_Ex04.git
 ```
 
# Running Time
#### [click here to see our Wiki 	:smiley: ](https://github.com/GeroNir/OOP_Ex4/wiki)

# Algorithm Explaining 
This time we've been asked to build an algorithm for graphs and make an interface that shows the best solution for the "Travelling Salesman Problem", which gave us a list of place that we must visit and returns the quickest way to pass the whole places.

# About the Game
The game consists of 16 stages [0-15].

At each stage a different number of Pokemon and agents.

The main goal at each stage is to catch as many Pokemon as possible by the agents. When the game scene actually a strongly weighted (directed) graph.

Every Pokemon has a "weight". The same "weight" is summed up after the capture of the Pokemon.

The goal of the game is to accumulate the maximum number of points ("score") in the smallest number of steps and in the shortest time (each game has a fixed time - usually 30-120 seconds).

At the end of each game we will get the score and the number of steps performed.

![Pokemon](https://github.com/GeroNir/OOP_Ex4/blob/master/graphics/screenshot.png)


# Algorithm Classes
**GraphAlgo :**

This class implements the interface `GraphAlgoInterface`, For solving the `Travelling Salesman Problem` we need to find 
the quickest and most efficient way for planning the route, we were assisted Dijkstra's algorithm in greedily.
Dijkstra's algorithm is an algorithm for finding the shortest paths between nodes in a graph.
To find which point will be the best place for start we checked each couple of points to find the fastest start,
and after that we checked the whole other points with the second point, and so on.
In def `isConnected` we check if the graph is connected so we check if the graph is connected with `Depth first search algorithm` 
that help us to make sure we can reach each node and then we transpose the graph with the def `getTranspose` and check again with DFS if the graph is connected
In def `getCenter` we check the shortest path (by using Dijkstra Algo) for each node, and than we choose the longest path. 
from all the longest values, we choose the minimum to be the center.
In def `ShortestPath`" we use Dijkstra Algo for find the shortest path for the src node.

* `get_graph()` method simply returns the graph 

* `load_from_json(file_name)` method simply load the the graph from the given json file, if there is no such file in the memory then the graph will remain with no differences. the method returns `true` or `false` depends on if the process succeeded

* `save_to_json(file_name)` method simply save the graph to a json format, the method returns `true` or `false` depends on if the process succeeded 

* `connected_component(id)` method returns a list of the Strongly Connected Component(SCC) that the given node is a part of. this method using `dfs` algorithm 2 times, the first time is on the regular graph, the second time is on the transpose of this graph   

* `connected_components()` method returns a list of lists, represents all the SCC of this graph this method using `connected_component()` method 

* `shortestPath(src, dest)` method, this method using in Dijkstra's algorithm. it returns a Tuple with the distance of the path and the actual path between `src` to `dest` via List of keys. if `src` or `dest` are not in the graph or one of them does not exist in the graph, than the method returns `(float('inf',[])`.
if `src` is equal to `dest` then the method returns a list 

* `plot_graph()` method simply plot this graph, the nodes will be in there given position.

**DiGraph :**

This class implements the interface GraphInterface, the main function it's Digraph that implements JSON and copy the data into two dicts (Nodes and Edges).
And we have another function calls "connect" that make an edge between two nodes and give them a weight.

* `get_all_v()`-  returns all the vertex of this graph as dictionary format

* `all_in_edges_of_node(key)`- returns all the nodes connected to (into) the given node 

* `all_out_edges_of_node(key)`- returns all the nodes connected from the given node


* `add_edge(key1,key2,weight)`-  connect between the given nodes with the given weight. if there is alredy an edge between the nodes or one of the nodes does not exist in the graph, or the weight is negative then the method returns false o.w return true

* `addNode(key, pos:None)`- adds the node with the given id and pos to the graph, if the node already exist in the graph, the function does not add this node again, if the pos is none then the positiion will be a random position

* `hasEdge(key1,key2)`- method, check if the given nodes has edge who connect them


* `get_weight(node1,node2)`- method uses `hasEdge()` method to check if there is an edge between the given nodes, if not the method returns -1. if yes then the method returns the weight between the given nodes

* `remove_node(key)`- removes the node from the graph and all of his edges, returns true if the node removed successfully, false o.w


* `remove_edge(key1,key2)`- method uses `hasEdge()` method to check if there is an edge between the given nodes. if yes then the method removes the edge between the given nodes. else the method return false

* `get_node(key)`-  returns the node with the given id if this node exist in this graph

# UML diagram

 ![Alt text](https://github.com/GeroNir/OOP_Ex4/blob/master/data/graphics/UML.png?raw=true)
 
