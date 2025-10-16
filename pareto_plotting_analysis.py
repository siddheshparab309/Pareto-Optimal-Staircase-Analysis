# Pareto Analysis and Plotting
# This file contains the plotting logic to visualize the comparison between
# Experimental Time and Adjusted Theoretical Time for all four algorithms.

import matplotlib.pyplot as plt
import numpy as np

def plot_single_analysis(N_data, T_exp_data, T_adj_data, title, complexity_str):
    """
    Generates and displays a comparison plot for a single algorithm.
    Compares experimental time vs. the scaled theoretical curve.
    """

    plt.figure(figsize=(10, 6))

    # Plot Experimental Results
    plt.plot(N_data, T_exp_data, 'o-', label='Experimental Time ($\mu$s)', color='red', linewidth=2)

    # Plot Adjusted Theoretical Curve
    # Use a dashed line for the theoretical curve for clear distinction
    plt.plot(N_data, T_adj_data, '--', label=f'Adjusted Theoretical ({complexity_str})', color='blue', alpha=0.7)

    plt.title(f'{title}: Experimental vs. Theoretical Runtime', fontsize=14)
    plt.xlabel('Input Size (N)', fontsize=12)
    plt.ylabel('Execution Time ($\mu$s)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()