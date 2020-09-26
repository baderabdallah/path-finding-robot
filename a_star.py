import os
from operator import add
from node import Node
from edge import Edge
from open_list_item import OpenNodeWithEstimation


class AStar:
    def __init__(self, node_list, edge_list):
        self.node_list = node_list
        self.edge_list = edge_list

        # open_node_with_estimation_list is updated throught the A* algorithm
        self.open_node_with_estimation_list = list()
        # closed_node_list is the final soltuion of the A* algorithm
        self.closed_node_list = list()

        # Initialize cost lists
        self.past_cost_list = list()
        self.heuristic_cost_to_go_list = list()
        self.estimated_total_cost = list()

        # initializing the goal node as the last node from the node_list
        self.goal_node = node_list[-1]

        # Definition of the lists that are the attributes of the algorithm i.e. final path = f(parentNodeList, self.past_cost_list, heuCostList, estimated_total_cost)
        self.past_cost_list = [0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
        for node in node_list:
            self.heuristic_cost_to_go_list.append(node.heuristic_cost_to_go)
        estimated_total_cost = list(
            map(add, self.past_cost_list, self.heuristic_cost_to_go_list)
        )

        # Extracting children information for each parent from edge_list, and connecting the children to their parents in node_list
        Node.add_children_nodes_to_nodeList(node_list, edge_list)

        # First node is appended
        self.open_node_with_estimation_list.append(
            OpenNodeWithEstimation(node_list[0], estimated_total_cost[0])
        )

    def update_open_node_with_estimation_list(self, child_node, child_node_cost):
        self.past_cost_list[child_node.id - 1] = child_node_cost
        self.estimated_total_cost = list(
            map(add, self.past_cost_list, self.heuristic_cost_to_go_list)
        )

        is_child_node_traversed = any(
            closed_node == child_node for closed_node in self.closed_node_list
        )

        any_open_node_is_the_child_node = any(
            open_node_with_estimation.node.id == child_node.id
            for open_node_with_estimation in self.open_node_with_estimation_list
        )

        if not is_child_node_traversed and any_open_node_is_the_child_node:
            # Remove node from list because it holds old estimation
            Node.remove_node_from_list(
                child_node.id, self.open_node_with_estimation_list
            )

        # add new node with new or updated cost estimation
        self.open_node_with_estimation_list.append(
            OpenNodeWithEstimation(
                child_node, self.estimated_total_cost[child_node.id - 1]
            )
        )

    def run_algorithm(self):
        # Go on if open list is not empty!
        while not (len(self.open_node_with_estimation_list) == 0):
            current_node_with_estimation = self.open_node_with_estimation_list[0]

            # add first node in the open list to the closed list
            self.closed_node_list.append(current_node_with_estimation.node)

            # Break out of loop if goal is reached!
            if current_node_with_estimation.node.id == self.goal_node.id:
                break

            # first node was added to closed list. it is not need now in the open list.
            self.open_node_with_estimation_list.pop(0)

            # Add child nodes to open list
            # If child node exist in open list remove it as it holds old cost
            for child_node, child_node_cost in zip(
                current_node_with_estimation.node.child_nodes,
                current_node_with_estimation.node.child_costs,
            ):
                self.update_open_node_with_estimation_list(child_node, child_node_cost)

            # Sort open list according to cost
            self.open_node_with_estimation_list.sort(
                key=lambda x: x.node_est_tot_cost, reverse=False
            )
            # Go back to the start of the loop to add the first element of the open list into the closed list
        return self.closed_node_list


if __name__ == "__main__":

    # Parsing information about the nodes
    nodesFileName = os.getcwdb()
    nodesFileName = nodesFileName.decode("utf-8") + u"\\Scene5_example\\nodes.csv"
    node_list = Node.parse_nodes_data(nodesFileName)

    # Parsing information about the edges
    edges_file_name = os.getcwdb()
    edges_file_name = edges_file_name.decode("utf-8") + u"\\Scene5_example\\edges.csv"
    edge_list = Edge.parse_edge_data(edges_file_name)

    a_star = AStar(node_list, edge_list)
    closed_node_list = a_star.run_algorithm()

    # Algorithm is done! Now write the solution path into disk
    closedNodeListFileName = "Scene5_example/path.csv"
    Node.write_closed_node_list(closedNodeListFileName, closed_node_list)
