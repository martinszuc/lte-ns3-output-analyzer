import os
import pandas as pd
import matplotlib.pyplot as plt

# Define paths
INPUT_DIR = "input"
OUTPUT_DIR = "output"


def ensure_directories():
    """Ensure input and output directories exist."""
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_simulation_data(run_dirs):
    """Load simulation data from the given run directories."""
    data = {}
    for run_dir in run_dirs:
        csv_path = os.path.join(INPUT_DIR, run_dir, "simulation_metrics.csv")
        if os.path.exists(csv_path):
            data[run_dir] = pd.read_csv(csv_path)
        else:
            print(f"Warning: {csv_path} not found. Skipping {run_dir}.")
    return data


def plot_metric(data, metric, output_file):
    """Plot the given metric for multiple runs."""
    plt.figure()
    for run, df in data.items():
        if metric in df.columns:
            plt.plot(df["Time(s)"], df[metric], label=run)
        else:
            print(f"Warning: Metric '{metric}' not found in run '{run}'. Skipping.")

    plt.title(f"{metric} Comparison Across Runs")
    plt.xlabel("Time (s)")
    plt.ylabel(metric)
    plt.legend()
    plt.grid()
    plt.savefig(output_file)
    plt.close()
    print(f"Saved plot: {output_file}")


def compare_runs(run_dirs, metrics, output_folder):
    """Compare specified metrics across multiple runs."""
    data = load_simulation_data(run_dirs)
    os.makedirs(output_folder, exist_ok=True)

    for metric in metrics:
        output_file = os.path.join(output_folder, f"{metric.replace('/', '_')}_comparison.png")
        plot_metric(data, metric, output_file)


def main():
    ensure_directories()

    # User input: runs to compare
    print("Enter the run directories to compare (comma-separated):")
    run_dirs_input = input("> ")
    run_dirs = [run.strip() for run in run_dirs_input.split(",")]

    # User input: metrics to compare
    print("Enter the metrics to compare (comma-separated):")
    metrics_input = input("> ")
    metrics = [metric.strip() for metric in metrics_input.split(",")]

    # Compare runs and generate comparative graphs
    output_folder = os.path.join(OUTPUT_DIR, "comparison_plots")
    compare_runs(run_dirs, metrics, output_folder)

    print(f"Comparative plots saved in: {output_folder}")


if __name__ == "__main__":
    main()
