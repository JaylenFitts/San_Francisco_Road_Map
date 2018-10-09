#!/bin/python
#github-rest-api made by Jaylen, with help from StackOverflow, Wikipedia and other urls which I will include later

import urllib.request
import json
import math
from collections import namedtuple, deque
from pprint import pprint as pp

edges_data = dict() # dictionary where edge values will be loaded from json
nodes_data = dict() # dictionary where node values will be loaded from json
road_map = dict()   # dictionary representing nodes and edges

try:    # tries to load text file from url to parse into json for edge values
    edges_url = "https://gist.githubusercontent.com/BenjaminMalley/9eadf45dbe11ba9c3ac34c45f905cfe8/raw/2c363711b601fa39a5d0071f10158b86217e530f/edges.json"
    edges_f = urllib.request.urlopen(edges_url)
    my_edges_file = edges_f.read()
    edges_data = json.loads(my_edges_file.decode())
except ValueError:
    print("Edges JSON File Wouldn't Load")

try:    # tries to load text file from url to parse into json for node values
    nodes_url = "https://gist.githubusercontent.com/BenjaminMalley/9eadf45dbe11ba9c3ac34c45f905cfe8/raw/2c363711b601fa39a5d0071f10158b86217e530f/nodes.json"
    nodes_f = urllib.request.urlopen(nodes_url)
    my_nodes_file = nodes_f.read()
    nodes_data = json.loads(my_nodes_file.decode())
except ValueError:
    print("Nodes JSON File Wouldn't Load")


def createMap(edges_dict, nodes_dict):    # uses node and edge dicts to combine into a single map dict
    tup_edges = []

    for node in range(len(nodes_dict)): # creates adjacency dict of nodes at each node
        for edge in range(len(edges_dict)):    # fills tuple with nodes
            if str(edge) in edges_dict:
                if edges_dict.get(str(edge))['StartNodeId'] == node:
                    tup_edges.append((node, edges_dict[str(edge)]['EndNodeId'], edges_dict[str(edge)]['L2Distance']))

    return tup_edges


Edge = namedtuple('Edge', 'start, end, cost')


class Graph:
    def __init__(self, edges):
        self.edges = edges2 = [Edge(*edge) for edge in edges]
        self.vertices = set(sum(([e.start, e.end] for e in edges2), []))

    def dijkstra(self, source, goal):
        dist = {vertex: math.inf for vertex in self.vertices}
        previous = {vertex: None for vertex in self.vertices}
        dist[source] = 0
        q = self.vertices.copy()
        neighbours = {vertex: set() for vertex in self.vertices}
        for start, end, cost in self.edges:
            neighbours[start].add((end, cost))
        #pp(neighbours)

        while q:
            u = min(q, key=lambda vertex: dist[vertex])
            q.remove(u)
            if dist[u] == math.inf:
                print("\n***No connection between nodes***\n")
                break
            elif u == goal:
                break
            for v, cost in neighbours[u]:
                alt = dist[u] + cost
                if alt < dist[v]:                                  # Relax (u,v,a)
                    dist[v] = alt
                    previous[v] = u
        #pp(previous)
        s, u = deque(), goal
        while previous[u]:
            s.appendleft(u)
            u = previous[u]
        s.appendleft(u)
        s.appendleft(source)
        return s


road_map = Graph(createMap(edges_data, nodes_data))
pp(road_map.dijkstra(0, 5))
#distance = dijkstra(19, 21, road_map)

#print(distance)