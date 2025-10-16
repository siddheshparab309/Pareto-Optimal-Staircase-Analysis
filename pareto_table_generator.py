# Pareto Table Generator
# This file runs experiments, calculates the theoretical values and scaling constants,
# and prints four distinct tables for each algorithm's analysis.

import time
import math
import numpy as np
import sys
import os

try:
    # Use direct import if file structure is flat
    from pareto_algorithm_functions import (
        generate_points,
        algorithm_O_nh,
        run_O_nlogn_dc,
        algorithm_O_nlogh,
        algorithm_O_n
    )
except ImportError:
    # If using complex environment, print an error
    print("Error: Could not find 'pareto_functions.py'.")
    print("Please ensure 'pareto_functions.py' is in the same directory.")
    sys.exit(1)


# --- 1. ANALYSIS AND CALCULATION LOGIC ---

def calculate_theoretical_function(N, H, complexity_str):
    """Maps complexity string to its mathematical function."""
    # O(N*H) uses N*H calculation as per problem statement
    if complexity_str == "O(N * H)":
        return N * H
    elif complexity_str == "O(N log N)":
        return N * math.log2(N) if N > 1 else 0
    elif complexity_str == "O(N log H)":
        return N * math.log2(H) if H > 1 and N > 1 else 0
    elif complexity_str == "O(N)":
        return N
    return 0


def calculate_k_avg(N_list, T_exp_list, h_list, complexity_str):
    """Calculates the average scaling constant K for a given theoretical function."""
    N_arr = np.array(N_list)
    T_exp_arr = np.array(T_exp_list)
    h_arr = np.array(h_list)

    # 1. Calculate raw theoretical values
    T_theo_raw_list = []
    for N, H in zip(N_arr, h_arr):
        T_theo_raw_list.append(calculate_theoretical_function(N, H, complexity_str))

    T_theo_arr = np.array(T_theo_raw_list)

    # 2. Calculate K = T_exp / T_theo, ignoring points where T_theo is near zero
    valid_indices = T_theo_arr > 1e-6
    if np.any(valid_indices):
        K_values = T_exp_arr[valid_indices] / T_theo_arr[valid_indices]
        return np.mean(K_values)
    return 1.0


# --- 2. EXPERIMENT RUNNER ---

def run_experiments(input_sizes):
    """Runs all four algorithms and collects execution times."""
    results = []

    print("--- Running Algorithms and Collecting Raw Data ---")
    print("-" * 75)
    print(f"{'N':<10}{'T_nh (us)':<15}{'T_nlogn (us)':<17}{'T_nlogh (us)':<17}{'T_n (us)':<15}")
    print("-" * 75)

    for N in input_sizes:
        # Generate points for testing (Worst case for nh: N=H)
        random_points_for_sort = generate_points(N, case="worst_case_nh")
        # Generate points for O(n) test (already sorted)
        presorted_points = generate_points(N, case="presorted")
        presorted_points.sort(key=lambda p: p.x)

        # --- Test 1: O(nh) / Simple Sweep ---
        start = time.perf_counter()
        result_nh = algorithm_O_nh(list(random_points_for_sort))
        end = time.perf_counter()
        time_nh = (end - start) * 1e6
        h_nh = len(result_nh)

        # --- Test 2: O(n log n) / Divide-and-Conquer ---
        start = time.perf_counter()
        points_for_dc = sorted(list(random_points_for_sort), key=lambda p: p.x)
        result_dc = run_O_nlogn_dc(points_for_dc)
        end = time.perf_counter()
        time_dc = (end - start) * 1e6

        # --- Test 3: O(n log h) / Log-Height Sweep ---
        start = time.perf_counter()
        result_nlogh = algorithm_O_nlogh(list(random_points_for_sort))
        end = time.perf_counter()
        time_nlogh = (end - start) * 1e6

        # --- Test 4: O(n) / Pre-Sorted Sweep ---
        start = time.perf_counter()
        result_n = algorithm_O_n(list(presorted_points))
        end = time.perf_counter()
        time_n = (end - start) * 1e6

        # Store results
        results.append({
            'N': N,
            'h': h_nh,
            'T_nh': time_nh,
            'T_nlogn': time_dc,
            'T_nlogh': time_nlogh,
            'T_n': time_n
        })

        # Print only N and experimental times (T_exp)
        print(f"{N:<10}{time_nh:<15.0f}{time_dc:<17.0f}{time_nlogh:<17.0f}{time_n:<15.0f}")

    print("-" * 75)
    return results


# --- 3. TABLE GENERATION AND OUTPUT ---

def print_single_algorithm_table(N_list, T_exp_list, h_list, title, complexity_str):
    """Generates a single, complete analysis table for one algorithm and returns plot data."""

    N_arr = np.array(N_list)
    T_exp_arr = np.array(T_exp_list)
    h_arr = np.array(h_list)

    # 1. Calculate K_avg
    K_avg = calculate_k_avg(N_list, T_exp_list, h_list, complexity_str)

    # 2. Calculate raw theoretical values and adjusted results
    T_theo_raw_list = []
    T_theo_adjusted_list = []

    for N, H in zip(N_arr, h_arr):
        T_raw = calculate_theoretical_function(N, H, complexity_str)
        T_theo_raw_list.append(T_raw)
        # Use K_avg to scale the raw theoretical value
        T_theo_adjusted_list.append(K_avg * T_raw)

    # 3. Print Table
    print("\n" + "=" * 105)
    print(f"--- Algorithm: {title} ({complexity_str} Analysis) ---")
    # Use 8 decimal places for K_avg to show precision, which explains small values
    print(f"Calculated Average Scaling Constant (K_avg): {K_avg:.8f}")
    print("-" * 105)

    header = f"{'N':<10}{'H':<10}{'Exp. Time (us)':<25}{'Theoretical Value':<25}{'Adj. Theoretical Result (us)':<30}"
    print(header)
    print("-" * 105)

    total_exp_time = 0
    total_theo_value = 0

    for i in range(len(N_arr)):
        N = N_arr[i]
        H = h_arr[i]
        T_exp = T_exp_arr[i]
        T_theo_raw = T_theo_raw_list[i]
        T_theo_adjusted = T_theo_adjusted_list[i]

        # Print row data (using .2f for adjusted result fixes the rounding issue)
        print(f"{N:<10}{H:<10}{T_exp:<25.0f}{T_theo_raw:<25.2f}{T_theo_adjusted:<30.2f}")

        total_exp_time += T_exp
        total_theo_value += T_theo_raw

    # Print Averages
    N_count = len(N_arr)
    avg_exp_time = total_exp_time / N_count
    avg_theo_value = total_theo_value / N_count

    print("-" * 105)
    print(f"{'Average ->':<10}{'':<10}{avg_exp_time:<25.0f}{avg_theo_value:<25.2f}{'':<30}")
    print("=" * 105)

    # Return data needed for plotting
    return N_arr, T_exp_arr, np.array(T_theo_adjusted_list), title, complexity_str


# --- 4. MAIN EXECUTION ---

if __name__ == "__main__":
    # Input sizes for testing
    input_sizes = [100, 500, 1000, 2000, 4000, 8000, 16000, 32000]

    # 1. Run Experiments
    experimental_results = run_experiments(input_sizes)

    # Extract data lists
    N_list = [r['N'] for r in experimental_results]
    h_list = [r['h'] for r in experimental_results]
    T_nh_list = [r['T_nh'] for r in experimental_results]
    T_dc_list = [r['T_nlogn'] for r in experimental_results]
    T_nlogh_list = [r['T_nlogh'] for r in experimental_results]
    T_n_list = [r['T_n'] for r in experimental_results]

    all_plot_data = []

    # 2. Print Tables & Prepare Plot Data for each Algorithm

    # Algorithm 1: O(nh) - Calculated against O(N * H)
    N_data, T_exp_data, T_adj_data, title, comp = print_single_algorithm_table(
        N_list, T_nh_list, h_list, "Algorithm 1: Simple Right-to-Left Sweep", "O(N * H)"
    )
    all_plot_data.append((N_data, T_exp_data, T_adj_data, title, comp))

    # Algorithm 2: O(n log n)
    N_data, T_exp_data, T_adj_data, title, comp = print_single_algorithm_table(
        N_list, T_dc_list, h_list, "Algorithm 2: Divide-and-Conquer", "O(N log N)"
    )
    all_plot_data.append((N_data, T_exp_data, T_adj_data, title, comp))

    # Algorithm 3: O(n log h)
    N_data, T_exp_data, T_adj_data, title, comp = print_single_algorithm_table(
        N_list, T_nlogh_list, h_list, "Algorithm 3: Log-Height BST Sweep", "O(N log H)"
    )
    all_plot_data.append((N_data, T_exp_data, T_adj_data, title, comp))

    # Algorithm 4: O(n)
    N_data, T_exp_data, T_adj_data, title, comp = print_single_algorithm_table(
        N_list, T_n_list, h_list, "Algorithm 4: Pre-Sorted Sweep", "O(N)"
    )
    all_plot_data.append((N_data, T_exp_data, T_adj_data, title, comp))

    # 3. Import and Run Plotting Logic
    try:
        from pareto_plotting_analysis import plot_single_analysis
    except ImportError:
        print("\nError: Could not find 'pareto_analysis.py'. Ensure it is saved in the same directory.")
        sys.exit(1)

    print("\nGenerating 4 separate comparative plots...")
    for N_data, T_exp_data, T_adj_data, title, comp in all_plot_data:
        plot_single_analysis(N_data, T_exp_data, T_adj_data, title, comp)

    print("\nAnalysis complete. Four tables and four plots have been generated.")