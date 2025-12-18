from collections.abc import Callable
from classes.Node import Node
from classes.Path import Path
from abierta import OpenList
import math
from statistics import mean


def no_sqrt_euclidian(node1: Node, node2: Node) -> float:
    # Length in km of 1° of longitude = 40075 km * cos( latitude ) / 360
    # Length in km of 1° of latitude = always 111.32 km
    # euclidean distance over a sphere, isn't perfect but is admissible
    return (
        (40075000 * math.cos(math.radians(mean([node1.lat * 10e-7, node2.lat * 10e-7]))) / 360 * (node1.long * 10e-7 - node2.long * 10e-7)) ** 2
        + ((node1.lat - node2.lat) * 10e-7 * 111320) ** 2
    )

def haversine(node1: Node, node2: Node) -> float:
    R = 6371e3
    phi_1 = node1.lat * 10e-7 * math.pi / 180
    phi_2 = node2.lat * 10e-7 * math.pi / 180
    delta_phi = (node2.lat - node1.lat) * 10e-7 * math.pi / 180
    delta_lambda = (node2.long - node1.long) * 10e-7 * math.pi / 180

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


class AStarSearch:
    open_list = OpenList()
    closed_list = set()

    base_scores = {}

    def __init__(
        self,
        node_dict: dict[int, Node],
        path_dict: dict[int, list[Path]],
        heuristic: Callable[[Node, Node], float] | None = None,
    ) -> None:
        self.node_dict = node_dict
        self.path_dict = path_dict
        self.heuristic = no_sqrt_euclidian if heuristic is None else heuristic

    def get_num_expanded_nodes(self) -> int:
        return len(self.closed_list)

    def expand_node(self, node: Node, goal: Node) -> None:
        # find all children of node
        paths: list[Path] = self.path_dict[node.id]
        dst_nodes: list[Node] = [self.node_dict[path.dest] for path in paths]
        for i, dst_node in enumerate(dst_nodes):
            # no need to reevaluate node if in closed list
            if dst_node in self.closed_list:
                continue
            # update values for cost, heuristic cost, parent if new cost is best
            temp_cost = node.cost + paths[i].cost
            if temp_cost < self.base_scores.get(dst_node.id, math.inf):
                self.base_scores[dst_node.id] = temp_cost
                dst_node.cost = temp_cost
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
        self.base_scores = {}
        self.heuristic_scores = {}

        while True:
            # get min from open list
            selected_node = self.open_list.get_min()
            # check if selected_node isn't outdated
            if selected_node.cost > self.base_scores.get(selected_node.id, math.inf):
                continue
            # check if selected_node is goal
            if selected_node == goal:
                self.add_to_closed_list(selected_node)
                break
            # "expand" selected Node
            self.expand_node(selected_node, goal)
            # add selected Node to closed list
            self.add_to_closed_list(selected_node)

        return (self.create_node_path(selected_node), selected_node.cost)
