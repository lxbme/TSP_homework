from numbers import Real
from math import sqrt
from typing import Iterable, List


class Point:
    def __init__(self, x: Real, y: Real, name=None):
        self.x = x
        self.y = y
        self.name = name

    def __sub__(self, other):
        return Point(self.x - other[0], self.y - other[1])

    def __rsub__(self, other):
        return Point(other[0] - self.x, other[1] - self.y)

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __getitem__(self, item: int):
        return [self.x, self.y][item]

    @staticmethod
    def from_sequence(seq, offset=0) -> List:
        return [Point(*seq[i], i + offset) for i in range(len(seq))]


class Routine:
    def __init__(self, points: Iterable[Point]):
        self.points = list(points)

    def __getitem__(self, index: int) -> Point:
        return self.points[index]

    def __setitem__(self, index: int, point: Point):
        self.points[index] = point

    def __len__(self):
        return len(self.points)

    def __str__(self):
        string = 'Routine(\n'
        for point in self.points:
            string += f'{point.name}: ({point[0]}, {point[1]}) \n'
        string += ")"
        return string

    def append(self, point: Point):
        self.points.append(point)

    def length(self):
        return sum([abs(pre - after) for pre, after in zip(self.points[0:-1], self.points[1:])])

    def exchange(self, index_1: int, index_2: int):
        self.points[index_1], self.points[index_2] = self.points[index_2], self.points[index_1]

