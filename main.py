from point import Point
from star_polygon import generate_star_polygon, print_center, print_vertices, print_edges
from polygon_operations import polygon_clipping_and_intersection, find_reflex_vertices, minimum_distance_to_kernel
from visualization import plot_star_polygon, plot_polygon_and_kernel

center_point = Point(x=50, y=50)
star_polygon = generate_star_polygon(center=center_point, n_vertices=10, min_radius=3, max_radius=20)

print_center(center_point)
print_vertices(star_polygon.points)
print_edges(star_polygon.points)

plot_star_polygon(star_polygon)

center = (50, 50)
polygon_points = [(p.x, p.y) for p in star_polygon.points]
kernel = polygon_clipping_and_intersection(center, polygon_points)

if kernel:
    reflex_vertices = find_reflex_vertices(polygon_points)
    print(f'Reflex Vertices: {reflex_vertices}')
    distances_to_kernel = minimum_distance_to_kernel(reflex_vertices, kernel)
    for rv, (distance, edge, closest_point) in distances_to_kernel.items():
        print(f'Reflex Vertex: {rv}, Minimum Distance to Kernel: {distance}, Closest Edge: {edge}, Closest Point: {closest_point}')

    plot_polygon_and_kernel(np.array(polygon_points), kernel, reflex_vertices, distances_to_kernel)
