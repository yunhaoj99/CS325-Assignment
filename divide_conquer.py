import sys
from itertools import combinations
import math, time
from a1_utils import read_input_from_cli, distance, write_output_to_file, generate_random_input_file, sort_pairs

def divide_and_conquer_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
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
    # Base case: use brute force when points <= 3
    if len(points) <= 3:
        return brute_force(points)
    
    # Sort points by x coordinate
    points_sorted_x = sorted(points, key=lambda p: p[0])
    mid = len(points_sorted_x) // 2
    mid_x = points_sorted_x[mid][0]
    
    # Split points into left and right halves
    left_points = points_sorted_x[:mid]
    right_points = points_sorted_x[mid:]
    
    # Recursively solve left and right halves
    left_min_dist, left_pairs = divide_and_conquer_closest_pair(left_points)
    right_min_dist, right_pairs = divide_and_conquer_closest_pair(right_points)
    
    # Get current minimum distance and corresponding pairs
    if left_min_dist < right_min_dist:
        min_dist = left_min_dist
        closest_pairs = left_pairs
    elif right_min_dist < left_min_dist:
        min_dist = right_min_dist
        closest_pairs = right_pairs
    else:
        min_dist = left_min_dist
        closest_pairs = left_pairs + right_pairs
    
    # points that cross the middle line
    strip_points = []
    for point in points_sorted_x:
        if abs(point[0] - mid_x) < min_dist:
            strip_points.append(point)
    
    # Sort strip points by y coordinate
    strip_points.sort(key=lambda p: p[1])
    
    # Find potential closest pairs in the strip
    strip_min_dist = min_dist
    strip_pairs = []
    
    for i in range(len(strip_points)):
        # Only need to check next 7 points
        for j in range(i + 1, min(i + 8, len(strip_points))):
            dist = distance(strip_points[i], strip_points[j])
            if dist < strip_min_dist:
                strip_min_dist = dist
                strip_pairs = [(strip_points[i], strip_points[j])]
            elif dist == strip_min_dist:
                strip_pairs.append((strip_points[i], strip_points[j]))
    
    # Update final results
    if strip_min_dist < min_dist:
        return strip_min_dist, sort_pairs(strip_pairs)
    elif strip_min_dist == min_dist:
        # Merge results and remove duplicates
        all_pairs = closest_pairs + strip_pairs
        # ensure all points are tuple type
        unique_pairs = list({(tuple(p1), tuple(p2)) for p1, p2 in all_pairs})
        return min_dist, sort_pairs(unique_pairs)
    else:
        return min_dist, sort_pairs(closest_pairs)


def brute_force(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    """
    Find the closest pair of points using brute force.
    
    Args:
        points (list[tuple[float, float]]): A list of 2D points, where each point is represented 
                                            as a tuple of coordinates (x, y).
                                            
    Returns:
        tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
            - The updated minimum distance (float) between the closest pair(s) of points.
            - A list of tuples representing the closest point pairs, where each pair is a 
              tuple of two points ((x1, y1), (x2, y2)).
    """
    #This function is same as the brute_force.py
    min_dist = float('inf')
    closest_pairs = []

    n = len(points)
    #For all the points, compute the distance of two of them, then compare the distance to min_dist
    for i in range(n):
        for j in range(i+1, n):
            dist = distance(points[i], points[j])
            if dist < min_dist:
                #Update the min_dist
                min_dist = dist
                #Clear the previous closest_pairs list
                closest_pairs.clear()
                closest_pairs.append((points[i], points[j]))
            elif dist == min_dist:
                closest_pairs.append((points[i], points[j]))
    return min_dist, closest_pairs


if __name__ == "__main__":
    try:
        #the first num can control how many different points in this list
        #the second string can control write to which file
        #the third can control the random seed(if seed is the same, the generate random num will be same)
        generate_random_input_file(100, "sampleinput.txt", 42)
        points = read_input_from_cli()
        #store the start_time
        start_time = time.time()
        min_dist, closest_pairs = divide_and_conquer_closest_pair(points)
        #store the end_time
        end_time = time.time()
        process_time = start_time - end_time
        #print out the real time
        print(f"Time: {process_time}")

        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'ddnc_output.txt')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)