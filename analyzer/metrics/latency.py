# analyzer/metrics/latency.py

import os
import pandas as pd
import matplotlib.pyplot as plt

def calculate_average_latency(df):
    """
    Calculates the average latency.

    Args:
        df (pd.DataFrame): DataFrame containing simulation metrics.

    Returns:
        float: Average latency in ms.
    """
    return df['AvgDelay(ms)'].mean()

def plot_average_latency(avg_latency, plots_dir):
    """
    Plots the average latency.

    Args:
        avg_latency (float): Average latency in ms.
        plots_dir (str): Directory to save the plot.
    """
    plt.figure(figsize=(6, 6))
    plt.bar(['Avg Latency'], [avg_latency], color='orange')
    plt.title('Average Latency')
    plt.ylabel('Latency (ms)')
    plt.tight_layout()
    plot_path = os.path.join(plots_dir, 'average-latency.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"[+] Average latency plot saved to '{plot_path}'.")
