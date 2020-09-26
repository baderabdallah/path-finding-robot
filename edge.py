from numpy import genfromtxt
import os


class Edge:
    def __init__(self, child_node_id, parent_node_id, cost):
        self.child_node_id = int(child_node_id)
        self.parent_node_id = int(parent_node_id)
        self.cost = float(cost)

    @staticmethod
    def parse_edge_data(edges_file_name):
        edge_list = list()
        edges_data = genfromtxt(edges_file_name, delimiter=",")
        for edge in edges_data:
            m = Edge(edge[0], edge[1], edge[2])
            edge_list.append(m)
        return edge_list
