#!/usr/bin/env python3
"""
main.py

Main application to process NS-3 LTE simulation results.
Usage:
    python main.py --version v2
"""

import argparse
import os
import shutil
import sys
from datetime import datetime

from analyzer.parse_flowmon import parse_flowmon
from analyzer.plot_metrics import plot_all_metrics
from analyzer.utils import setup_version_directory, copy_input_files, generate_report

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="NS-3 LTE Simulation Analyzer")
    parser.add_argument('--version', type=str, required=True, help='Version identifier for the simulation run (e.g., v1, v2)')
    parser.add_argument('--input_dir', type=str, default='input/', help='Directory containing NS-3 simulation output files')
    args = parser.parse_args()

    version = args.version
    input_dir = args.input_dir
    base_dir = os.getcwd()
    versions_dir = os.path.join(base_dir, 'versions')
    version_dir = setup_version_directory(versions_dir, version)

    # Copy input files to version directory
    copy_input_files(input_dir, version_dir)

    # Define paths to input files
    flowmon_file = os.path.join(version_dir, 'flowmon.xml')
    simulation_metrics_file = os.path.join(version_dir, 'simulation_metrics.csv')

    # Check if required input files exist
    if not os.path.isfile(flowmon_file):
        print(f"[Error] {flowmon_file} does not exist.")
        sys.exit(1)
    if not os.path.isfile(simulation_metrics_file):
        print(f"[Error] {simulation_metrics_file} does not exist.")
        sys.exit(1)

    # Parse flowmon.xml
    parsed_flowmon_csv = os.path.join(version_dir, 'reports', 'flowmon_parsed.csv')
    parse_flowmon(flowmon_file, parsed_flowmon_csv)

    # Plot metrics
    plots_dir = os.path.join(version_dir, 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    plot_all_metrics(simulation_metrics_file, plots_dir)

    # Generate Markdown report
    report_file = os.path.join(version_dir, 'reports', 'simulation-report.md')
    generate_report(simulation_metrics_file, plots_dir, report_file)

    print(f"[+] Analysis for version '{version}' completed successfully.")

if __name__ == "__main__":
    main()
