from dataclasses import dataclass


@dataclass
class Path:
    _src: int = None
    _dest: int = None
    _cost: int = 0

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, value):
        if not isinstance(value, int):
            raise TypeError("src must be a int")
        elif value == self.dest and value is not None:
            raise ValueError("src cannot be the dest")
        else:
            self._src = value

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, value: int):
        if not isinstance(value, int):
            raise TypeError("dest must be a int")
        elif value == self.src and value is not None:
            raise ValueError("src cannot be the dest")
        else:
            self._dest = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value: int):
        if not isinstance(value, int):
            raise TypeError("cost must be a int")
        elif value < 0:
            raise ValueError("cost must be a non-negative integer")
        else:
            self._cost = value
