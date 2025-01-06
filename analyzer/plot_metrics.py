import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_throughput(df, plots_dir):
    """
    Plots Per-UE Throughput Over Time.

    Args:
        df (pd.DataFrame): DataFrame containing simulation metrics.
        plots_dir (str): Directory to save the plots.
    """
    throughput_cols = [col for col in df.columns if 'Throughput' in col]
    plt.figure(figsize=(10, 6))
    for col in throughput_cols:
        plt.plot(df['Time(s)'], df[col], label=col.replace('_', ' ').replace('(Kbps)', ''))
    plt.title('Per-UE Throughput Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Throughput (Kbps)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plot_path = os.path.join(plots_dir, 'ue-throughput-time-series.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"[+] Throughput plot saved to '{plot_path}'.")

def plot_latency(df, plots_dir):
    """
    Plots Aggregate Latency Over Time.

    Args:
        df (pd.DataFrame): DataFrame containing simulation metrics.
        plots_dir (str): Directory to save the plots.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df['Time(s)'], df['Avg_Latency(ms)'], marker='o', color='b')
    plt.title('Aggregate Latency Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Latency (ms)')
    plt.grid(True)
    plt.tight_layout()
    plot_path = os.path.join(plots_dir, 'aggregate-latency-time-series.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"[+] Latency plot saved to '{plot_path}'.")

def plot_packet_loss(df, plots_dir):
    """
    Plots Per-UE Packet Loss Over Time.

    Args:
        df (pd.DataFrame): DataFrame containing simulation metrics.
        plots_dir (str): Directory to save the plots.
    """
    packet_loss_cols = [col for col in df.columns if 'PacketLoss' in col]
    plt.figure(figsize=(10, 6))
    for col in packet_loss_cols:
        plt.plot(df['Time(s)'], df[col], label=col.replace('_', ' ').replace('(%)', ''))
    plt.title('Per-UE Packet Loss Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Packet Loss (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plot_path = os.path.join(plots_dir, 'ue-packetloss-time-series.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"[+] Packet Loss plot saved to '{plot_path}'.")

def plot_all_metrics(simulation_metrics_file, plots_dir):
    """
    Generates all required plots from simulation metrics.

    Args:
        simulation_metrics_file (str): Path to simulation_metrics.csv.
        plots_dir (str): Directory to save the plots.
    """
    df = pd.read_csv(simulation_metrics_file)
    plot_throughput(df, plots_dir)
    plot_latency(df, plots_dir)
    plot_packet_loss(df, plots_dir)
