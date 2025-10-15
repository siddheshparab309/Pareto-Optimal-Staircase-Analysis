# **Pareto-Optimal Staircase Analysis**

This project implements and analyzes the time complexity of four algorithms designed to compute the **Pareto-Optimal Staircase** (also known as the maximum vector or skyline problem) in a 2-dimensional point set. 

The code is modularized into three Python files to separate logic, analysis, and plotting.

## 

## **Project Structure**

| File | Purpose |
| :---- | :---- |
| pareto\_functions.py | Contains the Point class, input generation, and the core implementation for all four algorithms. |
| pareto\_table\_generator.py | **MAIN RUNNER.** Executes the experiments, calculates the average scaling constant (), and prints all four analysis tables. |
| pareto\_analysis.py | Contains the plotting logic (plot\_single\_analysis) used to generate the comparative graphs. |

## 

## **How to Run the Analysis**

1. **Install Dependencies:** Ensure you have Python 3, NumPy, and Matplotlib installed.  
   pip install numpy matplotlib

2. **Save Files:** Place all three Python files (pareto\_algorithm\_functions.py, pareto\_table\_generator.py, pareto\_plotting\_analysis.py) in the same directory.

3. **Execute:** Run the table generator script from your terminal.  
   python3 pareto\_table\_generator.py

## 

## **Output**

Running the main script generates two primary outputs:

1. **Console Output:** Four separate, detailed tables showing the **Experimental Time**, the **Theoretical Value**, the **Average Scaling Constant (K)** and the **Adjusted Theoretical Result** for each of the four algorithms.

2. **Visual Output:** Four distinct graphs comparing the Experimental time against the Adjusted Theoretical curve for visual proof of the time complexity.
