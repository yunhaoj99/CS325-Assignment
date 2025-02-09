import sys
from itertools import combinations
import math
from a1_utils import read_input_from_cli, distance, write_output_to_file

def brute_force_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
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
    #Set the minimun distance to infinity for comparing
    min_dist = float('inf')
    #Use closest_pairs to store all the closest pairs
    closest_pairs = []
    n = len(points)
    #For all the points, compute the distance of two of them, then compare the distance to min_dist
    for i in range(n):
        for j in range(i+1,n):
            dist = distance(points[i],points[j])
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
        points = read_input_from_cli()
        min_dist, closest_pairs = brute_force_closest_pair(points)

        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'brute_force_output.txt')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
