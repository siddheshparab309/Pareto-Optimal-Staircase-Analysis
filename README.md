# **Pareto-Optimal-Staircase-Java-Analysis (O(N log N))**

## **Project Goal**

This project implements the **Divide-and-Conquer** algorithm to compute the **Pareto-Optimal Points** (the "Staircase") in a set of 2D points. The goal is to verify the algorithm's efficient theoretical time complexity of  through numerical experiments.

## **Core Solution**

The algorithm uses an initial  sort by \-coordinate, followed by a recursive divide-and-conquer approach. The efficiency comes from the linear-time **Merge Step** which correctly combines two pre-sorted "staircases".

## **Project Structure (Java)**

The solution is split into three files:

| File | Purpose | Complexity |
| :---- | :---- | :---- |
| Point.java | Data Structure | Defines the x and y coordinates. |
| ParetoFinder.java | Core Algorithm | Implements the  Divide-and-Conquer logic, including the recursive splitting and the  merging step. |
| ExperimentRunner.java | **Execution & Analysis** | Contains the main method. It generates random test data, runs the Pareto Finder, measures execution time in nanoseconds, and performs the theoretical complexity analysis. |
