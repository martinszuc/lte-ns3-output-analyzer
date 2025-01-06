import os
import shutil
from datetime import datetime

def setup_version_directory(base_dir, version):
    """
    Creates a version-specific directory to store simulation results.

    Args:
        base_dir (str): Base directory where 'versions' folder resides.
        version (str): Version identifier (e.g., v1, v2).

    Returns:
        str: Path to the created version directory.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_dir = os.path.join(base_dir, version)
    if os.path.exists(version_dir):
        print(f"[Warning] Version directory '{version_dir}' already exists. It will be overwritten.")
        shutil.rmtree(version_dir)
    os.makedirs(version_dir, exist_ok=True)
    os.makedirs(os.path.join(version_dir, 'plots'), exist_ok=True)
    os.makedirs(os.path.join(version_dir, 'reports'), exist_ok=True)
    print(f"[+] Created version directory at '{version_dir}'.")
    return version_dir

def copy_input_files(input_dir, version_dir):
    """
    Copies relevant simulation output files from input directory to version directory.

    Args:
        input_dir (str): Source directory containing simulation output files.
        version_dir (str): Destination version-specific directory.
    """
    files_to_copy = ['flowmon.xml', 'simulation_metrics.csv']
    for file in files_to_copy:
        src = os.path.join(input_dir, file)
        dst = os.path.join(version_dir, file)
        if os.path.isfile(src):
            shutil.copy(src, dst)
            print(f"[+] Copied '{file}' to version directory.")
        else:
            print(f"[Warning] '{file}' not found in input directory '{input_dir}'.")

def generate_report(simulation_metrics_file, plots_dir, report_file):
    """
    Generates a Markdown report summarizing the simulation results.

    Args:
        simulation_metrics_file (str): Path to simulation_metrics.csv.
        plots_dir (str): Directory containing generated plot images.
        report_file (str): Path to the output Markdown report.
    """
    import pandas as pd

    df = pd.read_csv(simulation_metrics_file)
    avg_throughput = df.filter(like='Throughput').mean().mean()
    avg_latency = df['Avg_Latency(ms)'].mean()
    packet_loss = df.filter(like='PacketLoss').mean().mean()

    with open(report_file, 'w') as md:
        md.write("# Simulation Report\n\n")
        md.write(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        md.write("## Summary\n")
        md.write(f"- **Average Throughput:** {avg_throughput:.2f} Kbps\n")
        md.write(f"- **Average Latency:** {avg_latency:.2f} ms\n")
        md.write(f"- **Average Packet Loss:** {packet_loss:.2f} %\n\n")

        md.write("## Plots\n")
        for plot in os.listdir(plots_dir):
            if plot.endswith('.png'):
                md.write(f"### {plot.replace('-', ' ').replace('.png', '').title()}\n")
                md.write(f"![{plot}](../plots/{plot})\n\n")

        md.write("## Detailed Metrics\n")
        md.write("See `flowmon_parsed.csv` for detailed flow statistics.\n")

    print(f"[+] Generated Markdown report at '{report_file}'.")
