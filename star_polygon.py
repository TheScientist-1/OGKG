import numpy as np
from pydantic import BaseModel
from point import Point

class StarPolygon(BaseModel):
    points: list[Point]
    center: Point | None = None
    
    def asarray(self) -> np.ndarray:
        return np.asarray([[point.x, point.y] for point in self.points])


def generate_star_polygon(center: Point, n_vertices: int = 5, min_radius: float = 10,
                          max_radius: float = 20) -> StarPolygon:
    distance = np.random.rand(n_vertices)
    alpha = np.sort((np.random.rand(n_vertices) * 360))
    params = np.stack([alpha, distance])
    parameters_rad = (params * np.asarray([[np.pi / 180], [max_radius - min_radius]]))
    parameters_rad = parameters_rad + np.asarray([[0], [min_radius]])
    delta_xs = np.cos(parameters_rad[0]) * parameters_rad[1]
    delta_ys = np.sin(parameters_rad[0]) * parameters_rad[1]
    points = [
        Point(x=int(center.x + delta_x), y=int(center.y + delta_y))
        for delta_x, delta_y in zip(delta_xs, delta_ys)
    ]
    points = sorted(points, key=lambda p: np.arctan2(p.y - center.y, p.x - center.x))
    return StarPolygon(points=points, center=center)


def print_center(center: Point):
    print(f'Center: ({center.x}, {center.y})')


def print_vertices(vertices: list[Point]):
    vertices_list = [[p.x, p.y] for p in vertices]
    print(f'Vertices: {vertices_list}')


def print_edges(points: list[Point]):
    edges = [(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
    for i, (p1, p2) in enumerate(edges):
        print(f'Edge {i + 1}: ({p1.x}, {p1.y}) -> ({p2.x}, {p2.y})')
