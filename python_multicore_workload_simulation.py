import matplotlib.pyplot as plt  # For visualization

def simulate_a(total_workloadtime, parallelizable_fraction, number_cores):
    """
  This function calculates how much faster a task will run on multiple computer cores based on Amdahl's Law.  
  It takes three things as input:
  total_workload_time: How long the task takes on one core.
  parallelizable_fraction: What part of the task can be split up and done at the same time on different cores (a number between 0 and 1).
  num_cores: How many cores are being used.
  It gives back two things:
  multi_core_time: How long the task will take using multiple cores. 
  speedup: How much faster it is compared to using just one core.
    """
    if not (0.0 <= parallelizable_fraction <= 1.0):
        raise ValueError("The parallelizable fraction must be between 0.0 and 1.0.")
    if number_cores < 1:
        raise ValueError("The number of cores must be at least 1.")
    if total_workloadtime <= 0:
        raise ValueError("Total workload time must be positive.")

    serial_fraction = 1.0 - parallelizable_fraction  # S = 1 - P

    # Calculate the execution times of serial and parallel parts
    serial_time = total_workloadtime * serial_fraction
    parallelizable_time = total_workloadtime * parallelizable_fraction

    # Calculate the total execution time on multiple cores
    # The serial part remains unchanged; the parallel part is divided by N
    if number_cores == 1:
        multicore_time = total_workloadtime
    else:
        multicore_time = serial_time + (parallelizable_time / number_cores)

    # Calculate the speedup
    speedup = total_workloadtime / multicore_time

    return multicore_time, speedup

# Run Simulation and Visualization

# Set parameters
total_time = 100.0  # Example total workload time on a single core
parallel_fractions = [0.50, 0.75, 0.90, 0.95, 0.99]  # Different P values (parallel fractions)
core_counts = range(1, 65)  # Core counts to test (from 1 to 64)

results = {}  # Dictionary to store the results

# Run simulation for different P values
for p_frac in parallel_fractions:
    speedups = []
    for n_cores in core_counts:
        _, speedup = simulate_a(total_time, p_frac, n_cores)
        speedups.append(speedup)
    results[f'P = {p_frac:.2f}'] = speedups  # Label results with P value

# Visualize the results using Matplotlib
plt.figure(figsize=(12, 6))
for label, speedup_list in results.items():
    # Add theoretical speedup limit line (1/S)
    p = float(label.split('=')[1])
    s = 1.0 - p
    theoreticalimit = 1 / s if s > 0 else float('inf')  # If S = 0, limit is infinite
    plt.plot(core_counts, speedup_list, marker='.', linestyle='-', label=f'{label} (Limit: {theoreticalimit:.2f})')

plt.title("Amdahl's Law Simulation: Speedup vs Number of Cores")
plt.xlabel("Number of Cores (N)")
plt.ylabel("Speedup")
plt.grid(True)
plt.legend()
plt.ylim(bottom=0)  # Speedup cannot be negative
plt.show()  # Display the plot
