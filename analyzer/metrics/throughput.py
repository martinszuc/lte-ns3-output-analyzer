import pandas as pd
import matplotlib.pyplot as plt

def calculate_average_throughput(df):
    """
    Calculates the average throughput for each UE.

    Args:
        df (pd.DataFrame): DataFrame containing simulation metrics.

    Returns:
        pd.Series: Average throughput per UE.
    """
    throughput_cols = [col for col in df.columns if 'Throughput' in col]
    return df[throughput_cols].mean()

def plot_average_throughput(avg_throughput, plots_dir):
    """
    Plots the average throughput per UE.

    Args:
        avg_throughput (pd.Series): Average throughput per UE.
        plots_dir (str): Directory to save the plot.
    """
    plt.figure(figsize=(8, 6))
    avg_throughput.plot(kind='bar', color='skyblue')
    plt.title('Average Throughput per UE')
    plt.xlabel('User Equipment (UE)')
    plt.ylabel('Throughput (Kbps)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plot_path = os.path.join(plots_dir, 'average-throughput-per-ue.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"[+] Average throughput plot saved to '{plot_path}'.")
