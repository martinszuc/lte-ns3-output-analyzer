import os
import pandas as pd
import matplotlib.pyplot as plt
import logging

# Define paths
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# Configure logging
logging.basicConfig(
    filename="comparison_analysis.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def ensure_directories():
    """Ensure input and output directories exist."""
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_simulation_data(run_numbers):
    """
    Load Avg_Throughput(Kbps), Avg_Latency(ms), and compute Avg_PacketLoss(%) from the given run numbers.

    Parameters:
        run_numbers (list of str): List of run numbers as strings.

    Returns:
        dict: Dictionary mapping run numbers to their respective DataFrames.
    """
    data = {}
    for run_number in run_numbers:
        run_dir = f"run{run_number}"
        csv_path = os.path.join(INPUT_DIR, run_dir, "simulation_metrics.csv")
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
                # Check required columns
                required_columns = ["Time(s)", "Avg_Throughput(Kbps)", "Avg_Latency(ms)"]
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    logging.warning(f"Missing columns {missing_columns} in {csv_path}. Skipping run{run_number}.")
                    continue

                # Compute Avg_PacketLoss(%)
                packet_loss_cols = [col for col in df.columns if "PacketLoss(%)" in col]
                if packet_loss_cols:
                    df["Avg_PacketLoss(%)"] = df[packet_loss_cols].mean(axis=1)
                    logging.info(f"Computed Avg_PacketLoss(%) for run{run_number}.")
                else:
                    logging.warning(f"No PacketLoss(%) columns found in {csv_path}. Setting Avg_PacketLoss(%) to 0.")
                    df["Avg_PacketLoss(%)"] = 0

                # Keep only required columns
                data[run_number] = df[["Time(s)", "Avg_Throughput(Kbps)", "Avg_Latency(ms)", "Avg_PacketLoss(%)"]]
                logging.info(f"Loaded data for run{run_number}.")
            except Exception as e:
                logging.error(f"Error loading {csv_path}: {e}")
        else:
            logging.warning(f"{csv_path} not found. Skipping run{run_number}.")
    return data


def plot_metric(data, metric, output_file):
    """
    Plot the given metric for multiple runs.

    Parameters:
        data (dict): Dictionary mapping run numbers to their DataFrames.
        metric (str): The metric column to plot.
        output_file (str): Path to save the generated plot.
    """
    try:
        plt.figure(figsize=(12, 8))

        # Define a list of markers and cycle through them
        markers = ['o', 's', '^', 'D', 'v', '>', '<', 'p', '*', 'h', 'H', 'X', 'd']
        marker_cycle = (markers[i % len(markers)] for i in range(len(data)))

        for (run_number, df), marker in zip(data.items(), marker_cycle):
            plt.plot(df["Time(s)"], df[metric],
                     label=f"Simulation {run_number}",
                     marker=marker,
                     linestyle='-',
                     markersize=5)

        plt.title(f"{metric} Comparison Across Runs", fontsize=16)
        plt.xlabel("Time (s)", fontsize=14)
        plt.ylabel(metric, fontsize=14)
        plt.legend(title="Runs", fontsize=12)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        logging.info(f"Saved plot: {output_file}")
    except Exception as e:
        logging.error(f"Error plotting metric '{metric}': {e}")


def compare_runs(run_numbers, metrics=None, output_folder=None):
    """
    Compare specified metrics across multiple runs.

    Parameters:
        run_numbers (list of str): List of run numbers as strings.
        metrics (list of str, optional): List of metric column names to plot.
        output_folder (str, optional): Directory to save the generated plots.
    """
    data = load_simulation_data(run_numbers)

    if not data:
        logging.error("No valid data loaded. Exiting plotting function.")
        print("No valid data loaded. Please check the log for details.")
        return

    # Specify default metrics if not provided
    if not metrics:
        metrics = ["Avg_Throughput(Kbps)", "Avg_Latency(ms)", "Avg_PacketLoss(%)"]

    # Create output folder
    output_folder = output_folder or os.path.join(OUTPUT_DIR, "comparison_plots")
    os.makedirs(output_folder, exist_ok=True)

    # Generate comparative plots
    for metric in metrics:
        output_file = os.path.join(output_folder, f"{metric.replace('/', '_')}_comparison.png")
        plot_metric(data, metric, output_file)


def main():
    ensure_directories()

    # User input: runs to compare
    print("Enter the run numbers to compare (comma-separated, e.g., 27,28,29):")
    run_numbers_input = input("> ")
    run_numbers = [num.strip() for num in run_numbers_input.split(",") if num.strip().isdigit()]

    if not run_numbers:
        print("No valid run numbers entered. Exiting.")
        logging.error("No valid run numbers entered by the user.")
        return

    # Compare runs and generate comparative plots
    compare_runs(run_numbers)

    print(f"Comparative plots saved in: {os.path.join(OUTPUT_DIR, 'comparison_plots')}")
    logging.info(f"Comparative plots generated for runs: {run_numbers}")


if __name__ == "__main__":
    main()
