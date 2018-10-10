#!/bin/python
# github-rest-api made by Jaylen during fellowship at Uber Hidden Genius Project with help from StackOverflow
# RosettaCode, Wikipedia and the University of Utah School of Computing's data set
# retrieved from SSTD 2005 (On Trip Planning Queries in Spatial Databases)

import urllib.request
import json
import math
from collections import namedtuple, deque
from pprint import pprint as pp

edges_data = dict()                                             # Dictionary where edge values will be loaded from json
nodes_data = dict()                                             # Dictionary where node values will be loaded from json
road_map = dict()                                               # Dictionary representing nodes and edges
Edge = namedtuple('Edge', 'start, end, weight')                 # Tuple representing edge object

try:                                            # Tries to load text file from url to parse into json for edge values
    edges_url = "https://gist.githubusercontent.com/BenjaminMalley/9eadf45dbe11ba9c3ac34c45f905cfe8/raw/2c363711b601fa39a5d0071f10158b86217e530f/edges.json"
    edges_f = urllib.request.urlopen(edges_url)
    my_edges_file = edges_f.read()
    edges_data = json.loads(my_edges_file.decode())
except ValueError:
    print("Edges JSON File Wouldn't Load")

try:                                            # Tries to load text file from url to parse into json for node values
    nodes_url = "https://gist.githubusercontent.com/BenjaminMalley/9eadf45dbe11ba9c3ac34c45f905cfe8/raw/2c363711b601fa39a5d0071f10158b86217e530f/nodes.json"
    nodes_f = urllib.request.urlopen(nodes_url)
    my_nodes_file = nodes_f.read()
    nodes_data = json.loads(my_nodes_file.decode())
except ValueError:
    print("Nodes JSON File Wouldn't Load")


def createMap(edges_dict, nodes_dict):    # Uses node and edge dicts to combine into a single list filled with tuples
    tup_edges = []

    for node in range(len(nodes_dict)):                                 # Creates adjacency dict of nodes at each node
        for edge in range(len(edges_dict)):                                 # Fills tuple with nodes
            if str(edge) in edges_dict:
                if edges_dict.get(str(edge))['StartNodeId'] == node:
                    tup_edges.append((node, edges_dict[str(edge)]['EndNodeId'], edges_dict[str(edge)]['L2Distance']))

    return tup_edges


class Graph:                                                            # Creates a graph filled with nodes and edges
    def __init__(self, edges):
        self.edges = edges2 = [Edge(*edge) for edge in edges]           # Creates an Edge tuple with each edge passed
        self.nodes = set(sum(([e.start, e.end] for e in edges2), []))       # Uses Edge tuples to find each start and
                                                                            # end, then combines them into set

    def dijkstra(self, source, goal):                                   # Search algorithm for finding path between
                                                                        # start and end
        dist = {node: math.inf for node in self.nodes}
        previous = {node: None for node in self.nodes}
        dist[source] = 0
        q = self.nodes.copy()                                           # Queue
        neighbours = {node: set() for node in self.nodes}
        for start, end, weight in self.edges:
            neighbours[start].add((end, weight))
            neighbours[end].add((start, weight))
        #pp(neighbours)

        while q:                                            # While queue has nodes, update shortest paths of neighbors
                                                            # of nodes in queue until goal is found
            u = min(q, key=lambda vertex: dist[vertex])
            q.remove(u)
            if dist[u] == math.inf:                                     # If infinity, there is no way to reach goal
                print("\n***No connection between nodes***\n")
                break
            elif u == goal:
                break
            for v, weight in neighbours[u]:                 # if new weight found is less than previous weight, replace
                alt = dist[u] + weight
                if alt < dist[v]:
                    dist[v] = alt
                    previous[v] = u
        #pp(previous)
        s, u = deque(), goal
        while previous[u]:                                          # Fill deque with path to goal
            s.appendleft(u)
            u = previous[u]
        s.appendleft(u)
        s.appendleft(source)
        return s


road_map = Graph(createMap(edges_data, nodes_data))
pp(road_map.dijkstra(0, 5)) 
