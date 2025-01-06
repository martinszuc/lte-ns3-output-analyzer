# analyzer/metrics/packet_loss.py

import os
import pandas as pd
import matplotlib.pyplot as plt

def calculate_average_packet_loss(df):
    """
    Calculates the average packet loss rate.

    Args:
        df (pd.DataFrame): DataFrame containing simulation metrics.

    Returns:
        float: Average packet loss percentage.
    """
    packet_loss_cols = [col for col in df.columns if 'PacketLoss(%)' in col]
    return df[packet_loss_cols].mean().mean()

def plot_average_packet_loss(avg_packet_loss, plots_dir):
    """
    Plots the average packet loss.

    Args:
        avg_packet_loss (float): Average packet loss percentage.
        plots_dir (str): Directory to save the plot.
    """
    plt.figure(figsize=(6, 6))
    plt.bar(['Avg Packet Loss'], [avg_packet_loss], color='red')
    plt.title('Average Packet Loss')
    plt.ylabel('Packet Loss (%)')
    plt.tight_layout()
    plot_path = os.path.join(plots_dir, 'average-packet-loss.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"[+] Average packet loss plot saved to '{plot_path}'.")
