import heapq
from classes.Node import Node


class OpenList:
    def __init__(self, li: list[Node] | None = None) -> None:
        self.li: list[Node] = li if li is not None else []
        heapq.heapify(self.li)

    def insert(self, item: Node) -> None:
        heapq.heappush(self.li, item)

    def get_min(self) -> Node:
        return heapq.heappop(self.li)
