import time
import matplotlib.pyplot as plt
import numpy as np
from a1_utils import generate_random_input_file, read_file_to_list
from brute_force import brute_force_closest_pair
from divide_conquer import divide_and_conquer_closest_pair
from enhanced_dnc import enhanced_divide_and_conquer_closest_pair

def test_algorithm(algo, points, algo_name):
    start_time = time.time()
    min_dist, pairs = algo(points)
    end_time = time.time()
    return end_time - start_time

def plot_runtime_comparison(sizes, times_dict):
    plt.figure(figsize=(12, 7))
    
    # Plot for each algorithm
    markers = ['o', 's', '^']  # Different markers for each algorithm
    for (algo_name, times), marker in zip(times_dict.items(), markers):
        plt.plot(sizes, times, marker=marker, label=algo_name, linewidth=2, markersize=8)
    
    plt.xlabel('Input Size (n)', fontsize=12)
    plt.ylabel('Runtime (seconds)', fontsize=12)
    plt.title('Algorithm Runtime Comparison', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Use log scale for better visualization
    plt.xscale('log')
    plt.yscale('log')
    
    # Add grid
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('runtime_comparison.png')
    plt.show()

def main():
    # Define input sizes from 10 to 1000, incrementing by 50
    input_sizes = list(range(1000, 5000, 200))
    
    # Define algorithms to test
    algorithms = [
        (brute_force_closest_pair, "Brute Force"),
        (divide_and_conquer_closest_pair, "Divide & Conquer"),
        (enhanced_divide_and_conquer_closest_pair, "Enhanced D&C")
    ]
    
    # Dictionary to store runtimes for each algorithm
    runtime_results = {algo_name: [] for _, algo_name in algorithms}
    
    # Run tests for each input size
    for n in input_sizes:
        print(f"\nTesting input size n = {n}")
        print("-" * 40)
        
        # Generate test data
        input_file = f"input_{n}.txt"
        generate_random_input_file(n, input_file)
        points = read_file_to_list(input_file)
        
        # Test each algorithm
        for algo, algo_name in algorithms:
            try:
                runtime = test_algorithm(algo, points, algo_name)
                runtime_results[algo_name].append(runtime)
                print(f"{algo_name}: {runtime:.4f} seconds")
            except Exception as e:
                print(f"{algo_name}: Error - {str(e)}")
                runtime_results[algo_name].append(None)
    
    # Plot the results
    plot_runtime_comparison(input_sizes, runtime_results)

if __name__ == "__main__":
    main() 