import pygame
from typing import List, Tuple, Union


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.pos = (x, y)


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2


    def intercept(self, line: object) -> Union[Point, None]:
        def ccw(A, B, C):
            return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

        def intersect(A, B, C, D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
        
        if not (intersect(self.p1, self.p2, line.p1, line.p2)):
            return
        
        a1 = self.p2.y - self.p1.y
        b1 = self.p1.x - self.p2.x
        c1 = (a1 * (self.p1.x)) + (b1 * self.p1.y)

        a2 = line.p2.y - line.p1.y
        b2 = line.p1.x - line.p2.x
        c2 = (a2 * (line.p1.x)) + (b2 * line.p1.y)

        determinant = a1*b2 - a2*b1

        x = round((b2*c1 - b1*c2)/determinant)
        y = round((a1*c2 - a2*c1)/determinant)
        
        return Point(x, y)


class Block:
    def __init__(self, vertices: List[Line]) -> None:
        self._vertices = vertices


    def get_any_intercept(self, line: Line) -> Union[Point, None]:
        for block_line in self._vertices:
            point = line.intercept(block_line)
            if point is not None:
                return point


    def get_all_intercept(self, line: Line) -> List[Point]:
        collitions = []
        for block_line in self._vertices:
            point = line.intercept(block_line)

            if point is not None:
                collitions.append(point)
        
        return collitions
    

    def render(self, surface: pygame.Surface) -> None:
        for line in self._vertices:
            pygame.draw.line(
                surface,
                (255, 255, 255),
                line.p1.pos,
                line.p2.pos
            )