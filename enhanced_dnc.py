import sys
from itertools import combinations
import math
from a1_utils import read_input_from_cli, distance, write_output_to_file

def enhanced_divide_and_conquer_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    """
    Recursively find the closest pair of points using an enhanced divide-and-conquer approach.
    This version pre-sorts points and maintains sorted lists throughout recursion.
    
    Args:
        points (list[tuple[float, float]]): A list of 2D points where 
                                           each point is represented as a tuple (x, y).
                                            
    Returns:
        tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
            - The minimum distance between the closest pair(s) of points.
            - A list of tuples representing the closest point pairs.
    """
    # Pre-sort points based on x and y coordinates
    points_sorted_x = sorted(points, key=lambda point: point[0])
    points_sorted_y = sorted(points, key=lambda point: point[1])

    def _closest_pair_recursive(points_sorted_x, points_sorted_y) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
      n = len(points_sorted_x)

      if n <= 3:
        min_dist = float('inf')
        closest_pairs = []
        for p1, p2 in combinations(points_sorted_x, 2):
          dist = distance(p1, p2)
          if dist < min_dist:
            min_dist = dist
            closest_pairs = [(p1, p2)]
          elif dist == min_dist:
            closest_pairs.append((p1,p2))
        return min_dist, closest_pairs

      # Divide the points into two halves
      mid = n // 2
      mid_point = points_sorted_x[mid]

      left_points_x = points_sorted_x[:mid]
      right_points_x = points_sorted_x[mid:]

      # Use a set for efficient lookups
      left_set = set(points_sorted_x[:mid])
      left_points_y = []
      right_points_y = []
      for point in points_sorted_y:
          if point in left_set:
              left_points_y.append(point)
          else:
              right_points_y.append(point)

      # Recursively find the closest pairs in the left and right halves
      left_min_dist, left_closest_pairs = _closest_pair_recursive(left_points_x, left_points_y)
      right_min_dist, right_closest_pairs = _closest_pair_recursive(right_points_x, right_points_y)
      
      # Get the minimum distance from left and right results
      min_dist = min(left_min_dist, right_min_dist)
      
      # Initialize closest_pairs with closest pairs from left or right
      if left_min_dist < right_min_dist:
        closest_pairs = left_closest_pairs
      elif right_min_dist < left_min_dist:
        closest_pairs = right_closest_pairs
      else:
        closest_pairs = left_closest_pairs + right_closest_pairs


      # Create a strip of points close to the dividing line using pre-sorted y list
      strip = [point for point in points_sorted_y if abs(point[0] - mid_point[0]) < min_dist]

      # Check for closer pairs in the strip
      for i in range(len(strip)):
          for j in range(i + 1, min(i + 8, len(strip))):
              dist = distance(strip[i], strip[j])
              if dist < min_dist:
                  min_dist = dist
                  closest_pairs = [(strip[i], strip[j])]
              elif dist == min_dist:
                closest_pairs.append((strip[i],strip[j]))

      closest_pairs = list(set(tuple(sorted(pair)) for pair in closest_pairs))
      return min_dist, closest_pairs

    # Start the recursive process with pre-sorted lists
    min_dist, closest_pairs = _closest_pair_recursive(points_sorted_x, points_sorted_y)
    return min_dist, closest_pairs

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
