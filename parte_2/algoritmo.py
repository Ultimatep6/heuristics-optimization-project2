from collections.abc import Callable
from classes.Node import Node
from classes.Path import Path
from abierta import OpenList


def no_sqrt_euclidian(node1: Node, node2: Node) -> float:
    return (node1.long - node2.long) ** 2 + (node1.lat - node2.lat) ** 2


class AStarSearch:
    open_list = OpenList()
    closed_list = set()

    def __init__(
        self,
        node_dict: dict[int, Node],
        path_dict: dict[int, list[Path]],
        heuristic: Callable[[Node, Node], float] | None = None,
    ) -> None:
        self.node_dict = node_dict
        self.path_dict = path_dict
        self.heuristic = no_sqrt_euclidian if heuristic is None else heuristic

    def expand_node(self, node: Node, goal: Node) -> None:
        # find all children of node
        paths: list[Path] = self.path_dict[node.id]
        dst_nodes: list[Node] = [self.node_dict[path.dest] for path in paths]
        for i, dst_node in enumerate(dst_nodes):
            # no need to reevaluate node if in closed list
            if dst_node in self.closed_list:
                continue
            # for all others update values for cost, heuristic cost, parent
            dst_node.cost = node.cost + paths[i].cost
            dst_node.heuristic_cost = self.heuristic(dst_node, goal)
            dst_node.parent = node
            self.open_list.insert(dst_node)

    def add_to_closed_list(self, node: Node) -> None:
        self.closed_list.add(node)

    def create_node_path(self, node: Node) -> tuple[Node, ...]:
        ret_list: list[Node] = [node]
        while node.parent is not None:
            ret_list.append(node.parent)
            node = node.parent
        return tuple(reversed(ret_list))

    def run(self, start_id: int, goal_id: int) -> tuple[tuple[Node, ...], float]:
        start = self.node_dict[start_id]
        start.cost = 0
        goal = self.node_dict[goal_id]
        # reset lists between runs
        self.open_list = OpenList([start])
        self.closed_list = set()
        while True:
            # get min from open list
            selected_node = self.open_list.get_min()
            # check if selected_node is goal
            if selected_node == goal:
                self.add_to_closed_list(selected_node)
                break
            # "expand" selected Node
            self.expand_node(selected_node, goal)
            # add selected Node to closed list
            self.add_to_closed_list(selected_node)

        return (self.create_node_path(selected_node), selected_node.cost)
