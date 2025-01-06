# analyzer/plot_metrics.py

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
    throughput_cols = [col for col in df.columns if 'Throughput(Kbps)' in col]
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
    plt.plot(df['Time(s)'], df['AvgDelay(ms)'], marker='o', color='b')
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
    packet_loss_cols = [col for col in df.columns if 'PacketLoss(%)' in col]
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


def plot_all_metrics(parsed_flowmon_csv, plots_dir):
    """
    Generates all required plots from parsed FlowMonitor data.

    Args:
        parsed_flowmon_csv (str): Path to flowmon_parsed.csv.
        plots_dir (str): Directory to save the plots.
    """
    df = pd.read_csv(parsed_flowmon_csv)

    # Assuming 'Time(s)' is available. If not, you might need to aggregate differently.
    # Since flowmon_parsed.csv contains flow-specific data without time, you may need to adjust.

    # For demonstration, we'll calculate average metrics per UE
    # Modify this section based on actual requirements

    # Plot Average Throughput per UE
    avg_throughput = calculate_average_throughput(df)
    plot_average_throughput(avg_throughput, plots_dir)

    # Plot Average Latency
    avg_latency = calculate_average_latency(df)
    plot_average_latency(avg_latency, plots_dir)

    # Plot Average Packet Loss
    avg_packet_loss = calculate_average_packet_loss(df)
    plot_average_packet_loss(avg_packet_loss, plots_dir)


def calculate_average_throughput(df):
    """
    Calculates the average throughput for each UE.

    Args:
        df (pd.DataFrame): DataFrame containing simulation metrics.

    Returns:
        pd.Series: Average throughput per UE.
    """
    throughput_cols = [col for col in df.columns if 'Throughput(Kbps)' in col]
    return df[throughput_cols].mean()


def plot_average_throughput(avg_throughput, plots_dir):
    """
    Plots the average throughput per UE.

    Args:
        avg_throughput (pd.Series): Average throughput per UE.
        plots_dir (str): Directory to save the plot.
    """
    plt.figure(figsize=(10, 6))
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
