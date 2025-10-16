# Pareto Core Functions
# This file holds the Point data structure, input generation, and all four algorithm implementations.

import random
import math

# --- 1. Point Data Structure ---

class Point:
    """Represents a 2D point with X and Y coordinates."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"


# --- 2. Input Data Generation ---

def generate_points(n, case="random"):
    """Generates a list of n points."""
    points = []
    if case == "worst_case_nh":
        # Worst case for O(nh) where h = n (downward slope: x increases, y decreases)
        for i in range(n):
            points.append(Point(i, n - i))
    elif case == "presorted":
        # Already sorted by X, simulating O(n) scenario input
        for i in range(n):
            # Use random Y values to get variable h but preserve X order
            points.append(Point(i, random.uniform(0, n)))
    else:
        # Random distribution (Average Case)
        for _ in range(n):
            points.append(Point(random.uniform(0, n * 2), random.uniform(0, n * 2)))
    return points


# --- 3. Algorithm Implementations ---

# ALGORITHM 1: O(nh) / Simple Right-to-Left Sweep
# Note: Implemented with initial sort, making the actual time O(n log n) due to the sort.
# This is tested against the O(N*H) function in the generator for academic comparison.
def algorithm_O_nh(points):
    """
    Implements the Simple Sweep. Sorts by X, then sweeps right-to-left
    to filter based on Max Y found so far.
    """
    points.sort(key=lambda p: p.x)
    pareto_set = []
    max_y_found = -float('inf')
    for point in reversed(points):
        if point.y > max_y_found:
            pareto_set.append(point)
            max_y_found = point.y
    return pareto_set[::-1]


# ALGORITHM 2: O(n log n) / Divide-and-Conquer
def combine_results(left_staircase, right_staircase):
    """Merges two pre-sorted staircases in O(n) time."""
    if not right_staircase:
        return left_staircase

    # Find the tallest wall in the Right Staircase
    max_y_right = -float('inf')
    for p in right_staircase:
        if p.y > max_y_right:
            max_y_right = p.y

    merged_staircase = []

    # Filter the Left Staircase: keep only points taller than the right-side wall
    for p in left_staircase:
        if p.y > max_y_right:
            merged_staircase.append(p)

    # Combine the filtered Left Staircase with the entire Right Staircase
    merged_staircase.extend(right_staircase)
    return merged_staircase


def algorithm_O_nlogn_dc(points):
    """Recursive Divide-and-Conquer function."""
    n = len(points)
    if n <= 1:
        return points

    mid = n // 2
    left_result = algorithm_O_nlogn_dc(points[:mid])
    right_result = algorithm_O_nlogn_dc(points[mid:])

    return combine_results(left_result, right_result)


def run_O_nlogn_dc(points):
    """Entry point for O(n log n) algorithm: performs initial sort then calls recursive function."""
    points.sort(key=lambda p: p.x)
    return algorithm_O_nlogn_dc(points)


# ALGORITHM 3: O(n log h) / Log-Height BST Sweep
def algorithm_O_nlogh(points):
    """
    Simulated O(n log h) approach using a sweep line.
    The internal filtering loop simulates the BST deletion process.
    """
    points.sort(key=lambda p: p.x)
    pareto_set = []

    # We sweep right-to-left
    for point in reversed(points):
        is_dominated = False

        # Check against the first point in the current optimal set (log h check)
        # Simplified: Check if point is clearly dominated by the closest optimal point
        if pareto_set and point.y < pareto_set[0].y:
            is_dominated = True

        if not is_dominated:
            temp_set = [point]
            current_max_y = point.y

            # Simulate removing dominated points from the set
            # The inner loop iterates over current optimal set (h points),
            # but in a true BST this would be faster, O(log h) amortized.
            for p in pareto_set:
                if p.y > current_max_y:
                    temp_set.append(p)
                    current_max_y = p.y

            pareto_set = temp_set

    return pareto_set[::-1]


# ALGORITHM 4: O(n) / Pre-Sorted Sweep
def algorithm_O_n(points):
    """
    Implements the Simple Sweep assuming points are already sorted by X.
    This is the O(n) solution because the O(n log n) sort is skipped.
    """
    pareto_set = []
    max_y_found = -float('inf')

    # Sweep right-to-left
    for point in reversed(points):
        if point.y > max_y_found:
            pareto_set.append(point)
            max_y_found = point.y

    return pareto_set[::-1]