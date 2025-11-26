from dataclasses import dataclass
import math


@dataclass
class Node:
    id: int
    _lat: int = 0
    _long: int = 0
    _cost: float = math.inf
    _heuristic_cost: float = 0
    _parent: "Node" = None

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Node):
            return self.id == value.id
        raise NotImplementedError

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.cost + self._heuristic_cost < other.cost + other._heuristic_cost
        raise NotImplementedError

    def __str__(self) -> str:
        return str(self.id)

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value: int):
        if not isinstance(value, int):
            raise TypeError("lat must be a int")
        else:
            self._lat = value

    @property
    def long(self):
        return self._long

    @long.setter
    def long(self, value: int):
        if not isinstance(value, int):
            raise TypeError("long must be a int")
        else:
            self._long = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if not isinstance(value, Node):
            raise TypeError("parent must be a Node")
        elif value == self:
            raise ValueError("parent cannot be self")
        else:
            self._parent = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value: float):
        if value < 0:
            raise ValueError("cost must be a non-negative integer")
        self._cost = value

    @property
    def heuristic_cost(self):
        return self._heuristic_cost

    @heuristic_cost.setter
    def heuristic_cost(self, value: float):
        if value < 0:
            raise ValueError("heuristic cost must be a non-negative integer")
        self._heuristic_cost = value
