import matplotlib.pyplot as plt  # For visualization

def simulate_amdahl(total_workload_time, parallelizable_fraction, num_cores):
    """
    Simulates execution time and speedup on a multicore system according to Amdahl's Law.

    Args:
        total_workload_time (float): Total execution time on a single core.
        parallelizable_fraction (float): Fraction of the workload that can be parallelized (between 0.0 and 1.0).
        num_cores (int): Number of cores used (N >= 1).

    Returns:
        tuple: (multi_core_time, speedup)
               multi_core_time: Computed execution time on multiple cores.
               speedup: Computed speedup compared to single-core execution.
    """
    if not (0.0 <= parallelizable_fraction <= 1.0):
        raise ValueError("The parallelizable fraction must be between 0.0 and 1.0.")
    if num_cores < 1:
        raise ValueError("The number of cores must be at least 1.")
    if total_workload_time <= 0:
        raise ValueError("Total workload time must be positive.")

    serial_fraction = 1.0 - parallelizable_fraction  # S = 1 - P

    # Calculate the execution times of serial and parallel parts
    serial_time = total_workload_time * serial_fraction
    parallelizable_time = total_workload_time * parallelizable_fraction

    # Calculate the total execution time on multiple cores
    # The serial part remains unchanged; the parallel part is divided by N
    if num_cores == 1:
        multi_core_time = total_workload_time
    else:
        multi_core_time = serial_time + (parallelizable_time / num_cores)

    # Calculate the speedup
    speedup = total_workload_time / multi_core_time

    return multi_core_time, speedup

# --- Run Simulation and Visualization ---

# Set parameters
total_time = 100.0  # Example total workload time on a single core
parallel_fractions = [0.50, 0.75, 0.90, 0.95, 0.99]  # Different P values (parallel fractions)
core_counts = range(1, 65)  # Core counts to test (from 1 to 64)

results = {}  # Dictionary to store the results

# Run simulation for different P values
for p_frac in parallel_fractions:
    speedups = []
    for n_cores in core_counts:
        _, speedup = simulate_amdahl(total_time, p_frac, n_cores)
        speedups.append(speedup)
    results[f'P = {p_frac:.2f}'] = speedups  # Label results with P value

# Visualize the results using Matplotlib
plt.figure(figsize=(10, 6))
for label, speedup_list in results.items():
    # Add theoretical speedup limit line (1/S)
    p = float(label.split('=')[1])
    s = 1.0 - p
    theoretical_limit = 1 / s if s > 0 else float('inf')  # If S = 0, limit is infinite
    plt.plot(core_counts, speedup_list, marker='.', linestyle='-', label=f'{label} (Limit: {theoretical_limit:.2f})')

plt.title("Amdahl's Law Simulation: Speedup vs Number of Cores")
plt.xlabel("Number of Cores (N)")
plt.ylabel("Speedup")
plt.grid(True)
plt.legend()
plt.ylim(bottom=0)  # Speedup cannot be negative
plt.show()  # Display the plot
