import sys
from itertools import combinations
import math
from a1_utils import read_input_from_cli, distance, write_output_to_file


def enhanced_divide_and_conquer_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    """
    Recursively find the closest pair of points using a divide-and-conquer approach.
    
    Args:
        points (list[tuple[float, float]]): A list of 2D points where 
                                            each point is represented as a tuple (x, y).
                                            
    Returns:
        tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
            - The minimum distance between the closest pair(s) of points.
            - A list of tuples representing the closest point pairs, where each pair is a 
              tuple of two points ((x1, y1), (x2, y2)).
    """
    # Handle empty input
    if not points:
        return float('inf'), []
        
    # Pre-sort points by x and y coordinates, avoid sorting the points again
    px = sorted(points, key=lambda p: p[0])  # Sort by x-coordinate
    py = sorted(points, key=lambda p: p[1])  # Sort by y-coordinate
    
    # Find all pairs with minimum distance
    min_dist, min_pairs = closest_pair_rec(px, py)
    
    # Final check to ensure we have all pairs with minimum distance
    all_pairs = []
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(px[i], px[j])
            if abs(dist - min_dist) < 1e-6:  # Using epsilon for float comparison
                all_pairs.append((px[i], px[j]))

    return min_dist, all_pairs

def closest_pair_rec(px: list[tuple[float, float]], py: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    """
    Recursive helper function that works with pre-sorted point lists.
    
    Args:
        px: Points sorted by x-coordinate
        py: Points sorted by y-coordinate
        
    Returns:
        tuple containing minimum distance and list of point pairs with that distance
    """
    n = len(px)
    
    # Base cases
    if n <= 1:
        return float('inf'), []
    if n == 2:
        dist = distance(px[0], px[1])
        return dist, [(px[0], px[1])]
        
    # Find median x-coordinate
    mid = n // 2
    median_x = px[mid][0]
    
    # Divide points into left and right halves based on x-coordinate
    px_left = px[:mid]
    px_right = px[mid:]
    
    # Split py into left and right while maintaining y-sort order
    py_left = []
    py_right = []
    for point in py:
        if point[0] <= median_x and len(py_left) < mid:
            py_left.append(point)
        else:
            py_right.append(point)
            
    # Recursively find closest pairs in left and right halves
    left_dist, left_pairs = closest_pair_rec(px_left, py_left)
    right_dist, right_pairs = closest_pair_rec(px_right, py_right)
    
    # Get minimum distance and pairs from recursive calls
    if left_dist < right_dist:
        min_dist = left_dist
        min_pairs = left_pairs
    elif right_dist < left_dist:
        min_dist = right_dist
        min_pairs = right_pairs
    else:
        min_dist = left_dist
        min_pairs = left_pairs + right_pairs
        
    # Build strip of points within min_dist of median
    strip = [p for p in py if abs(p[0] - median_x) < min_dist]
    
    # Check for closer pairs in strip
    for i in range(len(strip)):
        # Only need to check 7 points ahead (proved in literature)
        j = i + 1
        while j < len(strip) and strip[j][1] - strip[i][1] < min_dist:
            dist = distance(strip[i], strip[j])
            if dist < min_dist:
                min_dist = dist
                min_pairs = [(strip[i], strip[j])]
            elif dist == min_dist:
                min_pairs.append((strip[i], strip[j]))
            j += 1
            
    return min_dist, min_pairs


if __name__ == "__main__":
    try:
        points = read_input_from_cli()
        min_dist, closest_pairs = enhanced_divide_and_conquer_closest_pair(points)

        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'enhance_ddnc_output.txt')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
