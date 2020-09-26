class OpenNodeWithEstimation:
    def __init__(self, node, node_est_tot_cost):
        self.node = node
        self.node_est_tot_cost = node_est_tot_cost

    def __repr__(self):
        return "OpenNode({},{})".format(self.node.id, self.node_est_tot_cost)
