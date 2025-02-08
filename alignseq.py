import random
import time
from statistics import mean, stdev
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def read_cost_matrix(filename):
    """
    Read cost matrix from file.

    Args:
        filename (str): Path to the cost matrix file. File should be in CSV format with
                       first line containing the alphabet and subsequent lines containing
                       the cost values for each character.

    Returns:
        tuple: Contains two elements:
            - effective_alphabet (list): List of alphabet excluding the first symbol
            - cost_matrix (dict): Cost matrix dictionary where keys are tuples of character
                                pairs and values are their corresponding costs
    """
    with open(filename, 'r') as f:
        # Read first line to get alphabet (*,-,A,T,G,C)
        alphabet = f.readline().strip().split(',')
        # Effective alphabet excludes the first item
        effective_alphabet = alphabet[1:]
        
        # Create cost matrix dictionary
        cost_matrix = {}
        for line in f:
            values = line.strip().split(',')
            char = values[0]
            for j, cost in enumerate(values[1:]):
                # j corresponds to effective_alphabet[j]
                cost_matrix[(char, effective_alphabet[j])] = int(cost)
                
    return effective_alphabet, cost_matrix


def sequence_alignment(seq1, seq2, cost_matrix):
    """
    Implement sequence alignment using dynamic programming.

    Args:
        seq1 (str): First input sequence to be aligned
        seq2 (str): Second input sequence to be aligned
        cost_matrix (dict): Cost matrix dictionary where keys are tuples of character 
                          pairs (char1, char2) and values are their corresponding costs

    Returns:
        tuple: Contains two elements:
            - min_cost (int): Minimum alignment cost
            - (aligned1, aligned2) (tuple): Tuple containing the two aligned sequences 
                                          with gaps marked by '-'
    """
    m, n = len(seq1), len(seq2)
    # dp[i][j] represents minimum alignment cost for seq1[0:i] and seq2[0:j]
    dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]
    # path[i][j] records operations:
    # 0: match/substitute, 1: delete, 2: insert
    path = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize first row and column (empty sequence aligned with non-empty sequence)
    dp[0][0] = 0
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] + cost_matrix.get((seq1[i-1], '-'), 0)
        path[i][0] = 1  # can only delete
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] + cost_matrix.get(('-', seq2[j-1]), 0)
        path[0][j] = 2  # can only insert
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate costs for three operations
            match = dp[i-1][j-1] + cost_matrix.get((seq1[i-1], seq2[j-1]), 0)
            delete = dp[i-1][j] + cost_matrix.get((seq1[i-1], '-'), 0)
            insert = dp[i][j-1] + cost_matrix.get(('-', seq2[j-1]), 0)
            
            # Choose minimum cost operation
            min_cost = min(match, delete, insert)
            dp[i][j] = min_cost
            
            # 1. Match/substitute when it equals min_cost and is optimal
            # 2. Delete when it's strictly better or equal with length preference
            # 3. Insert otherwise
            if match == min_cost and (
                seq1[i-1] == seq2[j-1] or
                cost_matrix.get((seq1[i-1], seq2[j-1]), 0) <= min(
                    cost_matrix.get((seq1[i-1], '-'), 0),
                    cost_matrix.get(('-', seq2[j-1]), 0)
                )
            ):
                path[i][j] = 0
            elif delete == min_cost and (
                insert > min_cost or
                cost_matrix.get((seq1[i-1], '-'), 0) < cost_matrix.get(('-', seq2[j-1]), 0) or
                (cost_matrix.get((seq1[i-1], '-'), 0) == cost_matrix.get(('-', seq2[j-1]), 0) and i > j)
            ):
                path[i][j] = 1
            else:
                path[i][j] = 2
    
    # Backtrack to build alignment result
    aligned1, aligned2 = [], []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and path[i][j] == 0:
            # Match or substitute
            aligned1.append(seq1[i-1])
            aligned2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or path[i][j] == 1):
            # Delete: keep seq1[i-1], create gap in seq2
            aligned1.append(seq1[i-1])
            aligned2.append('-')
            i -= 1
        else:
            # Insert: create gap in seq1, keep seq2[j-1]
            aligned1.append('-')
            aligned2.append(seq2[j-1])
            j -= 1
    # Reverse the aligned sequences to get the correct order
    aligned1 = ''.join(reversed(aligned1))
    aligned2 = ''.join(reversed(aligned2))
    
    return dp[m][n], aligned1, aligned2


def main():
    # Read cost matrix
    alphabet, cost_matrix = read_cost_matrix('imp2cost.txt')
    
    # Read sequence pairs, each line format: "sequence1,sequence2"
    with open('imp2input.txt', 'r') as f:
        sequences = [line.strip().split(',') for line in f]
    
    # Process each pair and write results to output.txt
    with open('imp2output.txt', 'w') as f:
        for seq1, seq2 in sequences:
            cost, aligned1, aligned2 = sequence_alignment(seq1, seq2, cost_matrix)
            f.write(f"{aligned1},{aligned2}:{cost}\n")


if __name__ == "__main__":
    main()

def generate_random_sequence(length):
    """Generate random DNA sequence of given length
    
    Args:
        length (int): The desired length of the DNA sequence to generate
        
    Returns:
        str: A randomly generated DNA sequence containing only A, G, T, C nucleotides
    """
    # Define the possible nucleotides in DNA sequence
    nucleotides = ['A', 'G', 'T', 'C']
    
    # Generate random sequence using random.choices
    random_sequence = random.choices(nucleotides, k=length)
    
    # Join the nucleotides into a single string
    return ''.join(random_sequence)

def run_time_analysis():
    """
    Conduct runtime analysis and create plots for sequence alignment algorithm
    """
    # Read cost matrix first
    alphabet, cost_matrix = read_cost_matrix('imp2cost.txt')
    
    # Sequence lengths to test (more data points for better analysis)
    lengths = [100, 200, 500, 1000, 1500, 2000, 2500, 3000]
    
    # Store results
    results = {length: [] for length in lengths}
    avg_times = []
    
    # Run experiments
    for length in lengths:
        print(f"\nTesting sequences of length {length}")
        
        # Run 5 trials for each length
        for i in range(5):
            seq1 = generate_random_sequence(length)
            seq2 = generate_random_sequence(length)
            
            start_time = time.time()
            sequence_alignment(seq1, seq2, cost_matrix)
            execution_time = time.time() - start_time
            
            results[length].append(execution_time)
            print(f"Trial {i+1}: {execution_time:.4f} seconds")
        
        avg_time = mean(results[length])
        avg_times.append(avg_time)
        print(f"Average time for length {length}: {avg_time:.4f} seconds")

    # Create plots
    plt.figure(figsize=(12, 8))
    
    # Plot 1: Regular runtime plot
    plt.subplot(2, 1, 1)
    plt.plot(lengths, avg_times, 'bo-', label='Actual runtime')
    plt.xlabel('Sequence Length (n)')
    plt.ylabel('Time (seconds)')
    plt.title('Sequence Alignment Runtime Analysis')
    plt.grid(True)
    plt.legend()

    # Plot 2: Log-log plot to determine polynomial order
    plt.subplot(2, 1, 2)
    log_lengths = np.log(lengths)
    log_times = np.log(avg_times)
    
    # Linear regression on log-log data
    slope, intercept, r_value, p_value, std_err = linregress(log_lengths, log_times)
    
    plt.plot(log_lengths, log_times, 'ro-', label=f'Log-log plot (slope ≈ {slope:.2f})')
    plt.plot(log_lengths, slope * log_lengths + intercept, 'g--', 
             label=f'Fitted line (R² = {r_value**2:.3f})')
    plt.xlabel('log(Sequence Length)')
    plt.ylabel('log(Time)')
    plt.title(f'Log-Log Plot (Empirical Order: O(n^{slope:.2f}))')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig('runtime_analysis.png')
    plt.close()

    # Print numerical results
    print("\nNumerical Results:")
    print("Length\tAvg Time (s)\tStd Dev (s)")
    for length in lengths:
        avg = mean(results[length])
        std = stdev(results[length]) if len(results[length]) > 1 else 0
        print(f"{length}\t{avg:.4f}\t{std:.4f}")

    print(f"\nEmpirical complexity: O(n^{slope:.2f})")
    print(f"R-squared value: {r_value**2:.3f}")

if __name__ == "__main__":
    run_time_analysis()
