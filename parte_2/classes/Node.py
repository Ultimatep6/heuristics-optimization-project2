from dataclasses import dataclass

@dataclass
class Node:
    _lat : int = 0
    _long : int = 0
    _cost : int = 0
    _parent : 'Node' = None

    def __le__(self, other:'Node'):
        return self.cost < other.cost

    @property
    def lat(self):
        return self._lat
    
    @lat.setter
    def lat(self, value:int):
        if not isinstance(value,int):
            raise TypeError('lat must be a int')
        else:
            self._lat = value

    @property
    def long(self):
        return self._long
    @long.setter
    def long(self, value:int):
        if not isinstance(value,int):
            raise TypeError('long must be a int')
        else:
            self._long = value

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, value):
        if not isinstance(value, 'Node'):
            raise TypeError('parent must be a Node')
        elif value == self:
            raise ValueError('parent cannot be self')
        else:
            self._parent = value
    
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


    