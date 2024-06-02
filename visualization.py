import matplotlib.pyplot as plt
import numpy as np
from star_polygon import StarPolygon

def plot_star_polygon(star_polygon: StarPolygon):
    points_array = star_polygon.asarray()
    
    plt.figure(figsize=(6, 6))
    plt.plot(*zip(*points_array, points_array[0]), 'o-')
    plt.fill(points_array[:, 0], points_array[:, 1], alpha=0.3)
    plt.scatter(star_polygon.center.x, star_polygon.center.y, color='red')
    plt.title("Star Polygon")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def plot_polygon_and_kernel(polygon, kernel, reflex_vertices=None, distances_to_kernel=None):
    x_limits = (min(polygon[:, 0]) - 10, max(polygon[:, 0]) + 10)
    y_limits = (min(polygon[:, 1]) - 10, max(polygon[:, 1]) + 10)
    
    plt.figure()
    
    plt.fill(polygon[:, 0], polygon[:, 1], 'b', alpha=0.3, label='Original Polygon')
    plt.plot(polygon[:, 0], polygon[:, 1], 'b')
    
    if kernel and not kernel.is_empty:
        x, y = kernel.exterior.xy
        plt.fill(x, y, 'm', alpha=0.3, label='Kernel')
        plt.plot(x, y, 'm')
    
    if reflex_vertices and distances_to_kernel:
        for rv, (distance, edge, closest_point) in distances_to_kernel.items():
            plt.plot([rv[0], closest_point[0]], [rv[1], closest_point[1]], 'g--')

    plt.xlim(x_limits)
    plt.ylim(y_limits)
    plt.legend()
    plt.title('Polygon and Kernel with Reflex Vertex Distances')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
