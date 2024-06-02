import numpy as np
from shapely.geometry import Polygon, Point, LineString
import matplotlib.pyplot as plt

def polygon_clipping_and_intersection(center, polygon_points):
    center = np.array(center)
    polygon = np.array(polygon_points)

    def get_clipping_line(polygon, edge_index):
        p1 = polygon[edge_index]
        p2 = polygon[(edge_index + 1) % len(polygon)]
        direction = p2 - p1
        extension_factor = 2
        clip_line_end = p2 + direction * extension_factor
        return (p1, clip_line_end)

    def inside(p, cp1, cp2):
        return (cp2[0] - cp1[0]) * (p[1] - cp1[1]) > (cp2[1] - cp1[1]) * (p[0] - cp1[0])

    def intersection(cp1, cp2, s, e):
        dc = np.array([cp1[0] - cp2[0], cp1[1] - cp2[1]])
        dp = np.array([s[0] - e[0], s[1] - e[1]])
        n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
        n2 = s[0] * e[1] - s[1] * e[0]
        n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
        return [(n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3]

    def clip_polygon(subject_polygon, clip_edge, center):
        cp1, cp2 = clip_edge
        output_list = []
        input_list = subject_polygon
        s = input_list[-1]
        
        for e in input_list:
            if inside(e, cp1, cp2):
                if not inside(s, cp1, cp2):
                    output_list.append(intersection(cp1, cp2, s, e))
                output_list.append(e)
            elif inside(s, cp1, cp2):
                output_list.append(intersection(cp1, cp2, s, e))
            s = e
        
        output_polygon = np.array(output_list)
        if Polygon(output_polygon).contains(Point(center)):
            return output_polygon
        else:
            return subject_polygon

    x_limits = (min(polygon[:, 0]) - 10, max(polygon[:, 0]) + 10)
    y_limits = (min(polygon[:, 1]) - 10, max(polygon[:, 1]) + 10)
    intersection_polygon = None

    for edge_index in range(len(polygon)):
        clip_line = get_clipping_line(polygon, edge_index)
        clipped_polygon = clip_polygon(polygon, clip_line, center)

        print(f'Remaining Polygon Points for Edge {edge_index}:')
        for point in clipped_polygon:
            print(f'({point[0]}, {point[1]})')

        if len(clipped_polygon) > 2:
            remaining_shapely_poly = Polygon(clipped_polygon)
            if not remaining_shapely_poly.is_valid:
                remaining_shapely_poly = remaining_shapely_poly.buffer(0)

            if intersection_polygon is None:
                intersection_polygon = remaining_shapely_poly
            else:
                intersection_polygon = intersection_polygon.intersection(remaining_shapely_poly)

        plt.figure()
        plt.fill(polygon[:, 0], polygon[:, 1], 'b', alpha=0.3, label='Original Polygon')
        plt.plot(polygon[:, 0], polygon[:, 1], 'b')

        if clipped_polygon.size > 0:
            plt.fill(clipped_polygon[:, 0], clipped_polygon[:, 1], 'r', alpha=0.3, label='Clipped Polygon')
            plt.plot(clipped_polygon[:, 0], clipped_polygon[:, 1], 'r')

        clip_x, clip_y = zip(*clip_line)
        plt.plot(clip_x, clip_y, 'k--', label=f'Clipping Line (Edge {edge_index})')

        plt.xlim(x_limits)
        plt.ylim(y_limits)
        plt.legend()
        plt.title(f'Polygon Clipping (Edge {edge_index})')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    kernel = intersection_polygon

    if kernel and not kernel.is_empty:
        print('Kernel Points:')
        for x, y in kernel.exterior.coords:
            print(f'({x}, {y})')
        
        plt.figure()
        plt.fill(polygon[:, 0], polygon[:, 1], 'b', alpha=0.3, label='Original Polygon')
        plt.plot(polygon[:, 0], polygon[:, 1], 'b')
        
        x, y = kernel.exterior.xy
        plt.fill(x, y, 'm', alpha=0.3, label='Kernel')
        plt.plot(x, y, 'm')

        plt.xlim(x_limits)
        plt.ylim(y_limits)
        
        plt.legend()
        plt.title('Polygon and Kernel')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
    else:
        print('No intersection found among all remaining polygons.')

    return kernel

def find_reflex_vertices(polygon_points):
    polygon = Polygon(polygon_points)
    reflex_vertices = []
    for i, point in enumerate(polygon_points):
        p1 = polygon_points[i - 1]
        p2 = point
        p3 = polygon_points[(i + 1) % len(polygon_points)]
        v1 = np.array(p1) - np.array(p2)
        v2 = np.array(p3) - np.array(p2)
        angle = np.degrees(np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0]))
        if angle < 0:
            angle += 360
        if angle > 180:
            reflex_vertices.append(p2)
    return reflex_vertices

def minimum_distance_to_kernel(reflex_vertices, kernel):
    kernel_edges = [kernel.exterior.coords[i:i+2] for i in range(len(kernel.exterior.coords) - 1)]
    distances = {}
    for rv in reflex_vertices:
        rv_point = Point(rv)
        min_distance = float('inf')
        closest_edge = None
        closest_point = None
        for edge in kernel_edges:
            edge_line = LineString(edge)
            distance = rv_point.distance(edge_line)
            if distance < min_distance:
                min_distance = distance
                closest_edge = edge
                closest_point = np.array(edge_line.interpolate(edge_line.project(rv_point)).coords[0])
        distances[tuple(rv)] = (min_distance, closest_edge, closest_point)

        plt.plot([rv[0], closest_point[0]], [rv[1], closest_point[1]], 'g--')
    return distances
