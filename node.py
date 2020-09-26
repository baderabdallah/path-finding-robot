from numpy import genfromtxt
import os
import csv


class Node:
    def __init__(self, id, x, y, heuristic_cost_to_go):
        self.id = int(id)
        self.x = float(x)
        self.y = float(y)
        self.heuristic_cost_to_go = float(heuristic_cost_to_go)
        self.child_nodes = list()
        self.child_costs = list()

    def __repr__(self):
        return "Node({},{},{},{})".format(
            self.id, self.x, self.y, self.heuristic_cost_to_go
        )

    @staticmethod
    def parse_nodes_data(nodes_file_name):
        node_list = list()
        nodes_data = genfromtxt(nodes_file_name, delimiter=",")
        for node in nodes_data:
            n = Node(node[0], node[1], node[2], node[3])
            node_list.append(n)
        return node_list

    @staticmethod
    def write_closed_node_list(closed_node_list_file_name, closed_node_list):
        path = list()
        for node in closed_node_list:
            path.append(node.id)
        path_folder = os.path.abspath(closed_node_list_file_name)

        with open(path_folder, "w", newline="") as fp:
            wr = csv.writer(fp, dialect="excel")
            wr.writerow(path)

    @staticmethod
    def add_children_nodes_to_nodeList(node_list, edge_list):
        for edge in edge_list:
            # Child nodes
            parent_node = node_list[edge.parent_node_id - 1]
            child_node = node_list[edge.child_node_id - 1]
            parent_node.child_nodes.append(child_node)
            # Child costs.
            parent_node.child_costs.append(edge.cost)

    @staticmethod
    def remove_node_from_list(id, node_with_Estimation_list):
        popOut = next(
            (
                open_node_with_estimation
                for open_node_with_estimation in node_with_Estimation_list
                if open_node_with_estimation.node.id == id
            ),
            None,
        )
        node_with_Estimation_list.pop(node_with_Estimation_list.index(popOut))
