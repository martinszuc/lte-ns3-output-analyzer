import os
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime
import shutil


# Define paths
INPUT_DIR = "input"
OUTPUT_DIR = "output"


def ensure_directories():
    """Ensure input and output directories exist."""
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_csv_file(file_path):
    """Load the simulation_metrics.csv file into a DataFrame."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: {file_path} not found!")
        return None


def parse_flowmon_xml(file_path):
    """Parse the flowmon.xml file and extract statistics."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        flow_stats = []

        def parse_time_with_units(value):
            """Parse time with units like 'ns', 'ms', or 's'."""
            if value.endswith("ns"):
                return float(value[:-2]) * 1e-6  # Convert ns to ms
            elif value.endswith("ms"):
                return float(value[:-2])  # Already in ms
            elif value.endswith("s"):
                return float(value[:-1]) * 1e3  # Convert s to ms
            else:
                return float(value)  # Assume it's already in ms

        for flow in root.findall("FlowStats/Flow"):
            flow_id = int(flow.get("flowId", -1))
            tx_packets = int(flow.get("txPackets", 0))
            rx_packets = int(flow.get("rxPackets", 0))
            lost_packets = tx_packets - rx_packets

            # Parse delaySum and jitterSum, converting to milliseconds
            delay_sum = parse_time_with_units(flow.get("delaySum", "0ms"))
            jitter_sum = parse_time_with_units(flow.get("jitterSum", "0ms"))

            flow_stats.append({
                "FlowId": flow_id,
                "TxPackets": tx_packets,
                "RxPackets": rx_packets,
                "LostPackets": lost_packets,
                "DelaySum": delay_sum,
                "JitterSum": jitter_sum,
            })

        return pd.DataFrame(flow_stats)
    except FileNotFoundError:
        print(f"Error: {file_path} not found!")
        return None
    except ET.ParseError:
        print(f"Error: Failed to parse {file_path}!")
        return None


def generate_plots(csv_df, output_folder):
    """Generate throughput, latency, packet loss, jitter, and average throughput graphs."""
    os.makedirs(output_folder, exist_ok=True)

    # Time Series (X-axis: Time, Y-axis: Metrics per UE)
    time_series = csv_df["Time(s)"]

    # Throughput per UE
    throughput_columns = [col for col in csv_df.columns if "Throughput" in col and "Avg" not in col]
    for col in throughput_columns:
        plt.plot(time_series, csv_df[col], label=col)
    plt.title("Per-UE Throughput Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Throughput (Kbps)")
    plt.legend()
    plt.savefig(os.path.join(output_folder, "throughput_time_series.png"))
    plt.clf()

    # Average Throughput
    if "Avg_Throughput(Kbps)" in csv_df.columns:
        plt.plot(time_series, csv_df["Avg_Throughput(Kbps)"], label="Avg Throughput")
        plt.title("Average Throughput Over Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Throughput (Kbps)")
        plt.legend()
        plt.savefig(os.path.join(output_folder, "avg_throughput_time_series.png"))
        plt.clf()

    # Latency
    plt.plot(time_series, csv_df["Avg_Latency(ms)"], label="Avg Latency")
    plt.title("Average Latency Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Latency (ms)")
    plt.legend()
    plt.savefig(os.path.join(output_folder, "latency_time_series.png"))
    plt.clf()

    # Packet Loss
    packet_loss_columns = [col for col in csv_df.columns if "PacketLoss" in col]
    for col in packet_loss_columns:
        plt.plot(time_series, csv_df[col], label=col)
    plt.title("Per-UE Packet Loss Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Packet Loss (%)")
    plt.legend()
    plt.savefig(os.path.join(output_folder, "packet_loss_time_series.png"))
    plt.clf()

    # Jitter
    jitter_columns = [col for col in csv_df.columns if "Jitter" in col]
    for col in jitter_columns:
        plt.plot(time_series, csv_df[col], label=col)
    plt.title("Per-UE Jitter Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Jitter (ms)")
    plt.legend()
    plt.savefig(os.path.join(output_folder, "jitter_time_series.png"))
    plt.clf()


def generate_summary_documentation(csv_df, flowmon_df, output_folder):
    """Generate a Markdown summary of simulation results."""
    summary_path = os.path.join(output_folder, "simulation_summary.md")
    with open(summary_path, "w") as md_file:
        md_file.write("# Simulation Summary\n\n")
        md_file.write(f"**Output Directory**: {output_folder}\n\n")
        md_file.write("## Key Metrics\n\n")

        # Aggregate metrics
        if csv_df is not None:
            avg_throughput = csv_df[[col for col in csv_df.columns if "Throughput" in col]].mean()
            avg_latency = csv_df["Avg_Latency(ms)"].mean()
            avg_packet_loss = csv_df[[col for col in csv_df.columns if "PacketLoss" in col]].mean()
            avg_jitter = csv_df[[col for col in csv_df.columns if "Jitter" in col]].mean()

            md_file.write(f"- **Average Throughput**: {avg_throughput.mean():.2f} Kbps\n")
            md_file.write(f"- **Average Latency**: {avg_latency:.2f} ms\n")
            md_file.write(f"- **Average Packet Loss**: {avg_packet_loss.mean():.2f}%\n")
            md_file.write(f"- **Average Jitter**: {avg_jitter.mean():.2f} ms\n")

        # Flow-specific metrics
        if flowmon_df is not None:
            total_tx = flowmon_df["TxPackets"].sum()
            total_rx = flowmon_df["RxPackets"].sum()
            packet_loss_rate = (1 - (total_rx / total_tx)) * 100 if total_tx > 0 else 0
            avg_delay = flowmon_df["DelaySum"].mean() / flowmon_df["RxPackets"].mean() if flowmon_df["RxPackets"].mean() > 0 else 0
            avg_jitter = flowmon_df["JitterSum"].mean() / flowmon_df["RxPackets"].mean() if flowmon_df["RxPackets"].mean() > 0 else 0

            md_file.write("\n### Flow Monitor Metrics\n")
            md_file.write(f"- **Total Transmitted Packets**: {total_tx}\n")
            md_file.write(f"- **Total Received Packets**: {total_rx}\n")
            md_file.write(f"- **Packet Loss Rate**: {packet_loss_rate:.2f}%\n")
            md_file.write(f"- **Average Delay**: {avg_delay:.2f} ms\n")
            md_file.write(f"- **Average Jitter**: {avg_jitter:.2f} ms\n")


def process_run_directory(run_dir, output_folder):
    """Process a single run directory."""
    csv_file = os.path.join(run_dir, "simulation_metrics.csv")
    xml_file = os.path.join(run_dir, "flowmon.xml")

    csv_df = load_csv_file(csv_file)
    flowmon_df = parse_flowmon_xml(xml_file)

    if csv_df is not None:
        generate_plots(csv_df, output_folder)

    generate_summary_documentation(csv_df, flowmon_df, output_folder)


def main():
    ensure_directories()

    # Process each run directory
    for run_dir in sorted(os.listdir(INPUT_DIR)):
        run_path = os.path.join(INPUT_DIR, run_dir)
        if os.path.isdir(run_path):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_folder = os.path.join(OUTPUT_DIR, f"{run_dir}_output_{timestamp}")
            os.makedirs(output_folder, exist_ok=True)

            print(f"Processing: {run_path}")
            process_run_directory(run_path, output_folder)

    print(f"Analysis complete. Results saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
