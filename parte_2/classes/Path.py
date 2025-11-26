from dataclasses import dataclass
from .Node import Node

@dataclass
class Path:
    _src : Node = None
    _dest : Node = None
    _cost : int = 0

    @property
    def src(self):
        return self._src
    
    @src.setter
    def src(self, value):
        if not isinstance(value, Node):
            raise TypeError('src must be a Node')
        elif value == self.dest and value is not None:
            raise ValueError('src cannot be the dest')
        else:
            self._src = value

    @property
    def dest(self):
        return self._dest
    
    @dest.setter
    def dest(self, value:Node):
        if not isinstance(value,Node):
            raise TypeError('dest must be a Node')
        elif value == self.src and value is not None:
            raise ValueError('src cannot be the dest')
        else:
            self._dest = value        
    
    @property
    def cost(self):
        return self._cost
    
    @cost.setter
    def cost(self, value:int):
        if not isinstance(value,int):
            raise TypeError('cost must be a int')
        elif value < 0:
            raise ValueError('cost must be a non-negative integer')
        else:
            self._cost = value



    