import numpy as np
import matplotlib.pyplot as plt
import time
import subprocess
import glob
import os
from scipy.spatial import ConvexHull

# --- 1. CONFIGURATION ---

# Command for your original algorithm
MY_ALGO_COMMAND = ["./monotone_chain"]

# Command for your new optimized algorithm
MY_OPTIMIZED_ALGO_COMMAND = ["./optimized_monotone_chain"] # <--- NEW

# The folder where your test cases are
DATASET_DIR = "datasets"

# --- 2. THE BENCHMARKING FUNCTION ---

def run_benchmarks():
    # Find all .txt files in the dataset directory
    dataset_files = glob.glob(os.path.join(DATASET_DIR, "*.txt"))
    dataset_files.sort()
    
    if not dataset_files:
        print(f"Error: No datasets found in '{DATASET_DIR}'.")
        print("Run 'python generate_cases.py' first.")
        return

    results = []

    print("--- Starting Benchmark ---")

    for filepath in dataset_files:
        filename = os.path.basename(filepath)
        print(f"Benchmarking: {filename}...")
        
        # Load points into memory for SciPy
        try:
            points = np.loadtxt(filepath)
            if points.ndim == 1:
                points = points.reshape(1, -1)
            is_runnable = points.shape[0] >= 3
        except Exception as e:
            print(f"  Skipping (empty or corrupt file): {e}")
            is_runnable = False
            continue

        # --- A: Time Your (Base) Monotone Chain ---
        command_base = MY_ALGO_COMMAND + [filepath] # <--- MODIFIED
        
        try:
            start_time_c = time.perf_counter()
            subprocess.run(command_base, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # <--- MODIFIED
            end_time_c = time.perf_counter()
            time_c = end_time_c - start_time_c
        except Exception as e:
            print(f"  ERROR running your BASE algorithm: {e}") # <--- MODIFIED
            print(f"  Please check the command: {' '.join(command_base)}") # <--- MODIFIED
            time_c = None 

        # --- B: Time Your (Optimized) Monotone Chain ---  # <--- NEW BLOCK
        command_optimized = MY_OPTIMIZED_ALGO_COMMAND + [filepath]
        
        try:
            start_time_c_opt = time.perf_counter()
            subprocess.run(command_optimized, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            end_time_c_opt = time.perf_counter()
            time_c_optimized = end_time_c_opt - start_time_c_opt
        except Exception as e:
            print(f"  ERROR running your OPTIMIZED algorithm: {e}")
            print(f"  Please check the command: {' '.join(command_optimized)}")
            time_c_optimized = None # Mark as failed

        # --- C: Time SciPy (Quickhull) ---
        if is_runnable:
            try:
                start_time_scipy = time.perf_counter()
                hull = ConvexHull(points) 
                end_time_scipy = time.perf_counter()
                time_scipy = end_time_scipy - start_time_scipy
            except Exception as e:
                time_scipy = time.perf_counter() - start_time_scipy 
                print(f"  Note: SciPy raised an error (e.g., collinear): {e}")
        else:
            time_scipy = None 

        results.append({
            "name": filename.replace("case_", "").replace(".txt", ""),
            "my_algo_time": time_c,
            "my_optimized_algo_time": time_c_optimized, # <--- NEW
            "scipy_time": time_scipy
        })

    print("--- Benchmark Complete ---")
    return results

# --- 3. THE PLOTTING FUNCTION ---

def plot_results(results):
    # Filter out any failed runs
    valid_results = [r for r in results if 
                     r["my_algo_time"] is not None and 
                     r["my_optimized_algo_time"] is not None and # <--- NEW
                     r["scipy_time"] is not None]
    
    if not valid_results:
        print("No valid results to plot. Did all runs fail?")
        return

    labels = [r["name"] for r in valid_results]
    my_times = [r["my_algo_time"] for r in valid_results]
    my_optimized_times = [r["my_optimized_algo_time"] for r in valid_results] # <--- NEW
    scipy_times = [r["scipy_time"] for r in valid_results]

    x = np.arange(len(labels))  # the label locations
    width = 0.25  # the width of the bars # <--- MODIFIED (was 0.35)

    fig, ax = plt.subplots(figsize=(17, 8)) # <--- MODIFIED (made wider)
    
    # --- MODIFIED bar positions for three bars ---
    rects1 = ax.bar(x - width, my_times, width, label='My Algo (Base)')
    rects2 = ax.bar(x, my_optimized_times, width, label='My Algo (Optimized)') # <--- NEW
    rects3 = ax.bar(x + width, scipy_times, width, label='SciPy (Quickhull)')

    # Add some text for labels, title and axes ticks
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Algorithm Performance: Monotone Chain (Base vs. Optimized) vs. SciPy (Quickhull)') # <--- MODIFIED
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()

    ax.bar_label(rects1, padding=3, fmt='%.4f', rotation=90, fontsize=8)
    ax.bar_label(rects2, padding=3, fmt='%.4f', rotation=90, fontsize=8) # <--- NEW
    ax.bar_label(rects3, padding=3, fmt='%.4f', rotation=90, fontsize=8) # <--- MODIFIED (was rects2)
    
    ax.set_yscale('log')
    ax.set_ylabel('Time (seconds, log scale)')

    fig.tight_layout()
    plt.savefig("benchmark_plot.png")
    print("\nBenchmark plot saved to 'benchmark_plot.png'")
    plt.show()


# --- 4. MAIN EXECUTION ---
if __name__ == "__main__":
    benchmark_results = run_benchmarks()
    if benchmark_results:
        plot_results(benchmark_results)