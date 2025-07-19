from time import sleep
from math import cos, sin, radians, dist
from threading import Thread
from typing import List, Tuple, Union

import pygame

from space import Point, Line, Block


RAY_LENGTH = 1000
RAY_SEGMENT = 100
RESOLUTION = (1280, 720)

raw_vertices = [
    [
        ((50, 50), (150, 50)),
        ((150, 50), (150, 550)),
        ((150, 550), (50, 550)),
        ((50, 550), (50, 50))
    ],
    [
        ((1000, 200), (1100, 200)),
        ((1100, 200), (1100, 600)),
        ((1100, 600), (1000, 600)),
        ((1000, 600), (1000, 200))
    ],
    [
        ((400, 550), (800, 550)),
        ((800, 550), (800, 650)),
        ((800, 650), (400, 650)),
        ((400, 650), (400, 550))
    ],
]


def create_block_map(verticies: List[List[Tuple[Tuple[int, int], Tuple[int, int]]]]) -> List[Block]:
    block_map = []
    for verticy_list in verticies:
        
        verticy_map = []

        for verticy in verticy_list:
            p1 = Point(verticy[0][0], verticy[0][1])
            p2 = Point(verticy[1][0], verticy[1][1])
            
            line = Line(p1, p2)

            verticy_map.append(line)

        block_map.append(Block(verticy_map))
    
    return block_map


def create_ray(ray_src: Point, angle: int, distance: int) -> Line:
    x_des = ray_src.x + (distance * cos(radians(angle)))
    y_des = ray_src.y + (distance * sin(radians(angle)))

    ray_dest = Point(x_des, y_des)

    return Line(ray_src, ray_dest)


def get_distance(p1: Point, p2: Point) -> float:
    return dist(p1.pos, p2.pos)


def show_fps(clock: object):
    while True:
        print(clock.get_fps())
        sleep(1)


def main() -> None:
    block_map = create_block_map(raw_vertices)
    
    mouse_pos = Point(
        round(RESOLUTION[0] / 2),
        round(RESOLUTION[0] / 2)
    )
    
    pygame.init()
    
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Raycasting")

    screen = pygame.display.set_mode(RESOLUTION)
    clock = pygame.time.Clock()
    

    clock_t = Thread(
        target=show_fps,
        args=(clock,),
        daemon=True
    )
    clock_t.start()

    running = True
    
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = Point(*event.pos)

        ray_map = []
        for a in range(360):
            ray_line_full = create_ray(mouse_pos, a, RAY_LENGTH)

            ray_any_collition = False
            for block in block_map:
                if block.get_any_intercept(ray_line_full) is not None:
                    ray_any_collition = True
                    break

            if not ray_any_collition:
                ray_map.append((
                    round(ray_line_full.p2.x),
                    round(ray_line_full.p2.y)
                ))
                continue

            for lenght in range(0, RAY_LENGTH + RAY_SEGMENT, RAY_SEGMENT):
                ray_line_segment = create_ray(mouse_pos, a, lenght)

                collitions = []
                for block in block_map:
                    collitions.extend(block.get_all_intercept(ray_line_segment))

                if collitions:
                    closest_point = None
                    closest_point_dist = None
                    
                    for point in collitions:
                        distance = get_distance(mouse_pos, point)

                        if closest_point is None or distance < closest_point_dist:
                            closest_point = point
                            closest_point_dist = distance
                    
                    ray_map.append((
                        round(closest_point.x),
                        round(closest_point.y)
                    ))

                    break
        
        # Render The Light casting and source
        pygame.draw.polygon(screen, (255, 255, 100), ray_map)
        pygame.draw.circle(screen, (255, 0, 0), mouse_pos.pos, 10)

        for block in block_map:
            block.render(screen)

        pygame.display.update()
        clock.tick()


if __name__ == "__main__":
    main()