# LTE-Sim-Analyzer

**LTE-Sim-Analyzer** is a Python-based tool designed to process, analyze, and visualize NS-3 LTE network simulation results. It automates the parsing of FlowMonitor data, generates insightful plots, and organizes results systematically by simulation versions.

## Usage

1. **Prepare Simulation Output**  
   Place the following files in the `input/` directory:  
   - `flowmon.xml`  
   - `simulation_metrics.csv`  

2. **Run the Analyzer**  
   Use the following command to analyze the simulation results:  

   ```bash
   python analyzer.py --version <version_name> --input_dir <input_directory>
   ```

   **Arguments**:  
   - `--version`: Identifier for the simulation run (e.g., `v1`, `v2`).  
   - `--input_dir`: Directory containing NS-3 simulation output files. Default is `input/`.  

3. **View Results**  
   The analyzer will create a new directory under `versions/` with the specified version name. This directory will contain:  
   - Plots: Throughput, latency, and packet loss over time.  
   - Reports: A Markdown summary of the simulation results.  
   - Processed data: Parsed `flowmon.xml` and other detailed statistics.  

4. **Example**  

   To analyze version `v2` with files in the default `input/` directory:  

   ```bash
   python analyzer.py --version v2
   ```

   Results will be stored in `versions/v2/`.

