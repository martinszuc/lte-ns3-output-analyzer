# analyzer/parse_flowmon.py

import os
import xml.etree.ElementTree as ET
import pandas as pd

def parse_flowmon(flowmon_file, output_csv, destination_port_start=5000, num_ue=5):
    """
    Parses the flowmon.xml file and extracts flow statistics, including DestinationPort.

    Args:
        flowmon_file (str): Path to the flowmon.xml file.
        output_csv (str): Path to save the parsed CSV.
        destination_port_start (int): Starting port number for UEs.
        num_ue (int): Number of User Equipments (UEs).
    """
    try:
        tree = ET.parse(flowmon_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"[Error] XML parsing error: {e}")
        return

    # Step 1: Parse FlowStats
    flows_stats = {}
    for flow in root.findall(".//FlowStats/Flow"):
        flow_id = flow.get('flowId')
        if flow_id is None:
            continue

        def safe_get(attr, default=0):
            return float(flow.get(attr, default))

        tx_bytes = safe_get('txBytes')
        rx_bytes = safe_get('rxBytes')
        tx_packets = int(float(flow.get('txPackets', 0)))
        rx_packets = int(float(flow.get('rxPackets', 0)))
        lost_packets = int(float(flow.get('lostPackets', 0)))
        delay_sum = float(flow.get('delaySum', 0.0))
        jitter_sum = float(flow.get('jitterSum', 0.0))
        duration = float(flow.get('timeLastRxPacket', 0.0)) - float(flow.get('timeFirstTxPacket', 0.0))
        throughput = (rx_bytes * 8.0) / (duration * 1e9) if duration > 0 else 0.0  # Gbps
        avg_delay_ms = (delay_sum / rx_packets) * 1e3 if rx_packets > 0 else 0.0  # ms

        flows_stats[flow_id] = {
            'FlowID': int(flow_id),
            'TxBytes': tx_bytes,
            'RxBytes': rx_bytes,
            'TxPackets': tx_packets,
            'RxPackets': rx_packets,
            'LostPackets': lost_packets,
            'DelaySum(ns)': delay_sum,
            'JitterSum(ns)': jitter_sum,
            'Duration(ns)': duration,
            'Throughput(Gbps)': throughput,
            'AvgDelay(ms)': avg_delay_ms
        }

    # Step 2: Parse Ipv4FlowClassifier to get DestinationPort
    flow_classifier = {}
    for flow in root.findall(".//Ipv4FlowClassifier/Flow"):
        flow_id = flow.get('flowId')
        if flow_id is None:
            continue
        destination_port = flow.get('destinationPort')
        if destination_port is not None:
            flow_classifier[flow_id] = int(destination_port)

    # Step 3: Merge FlowStats with DestinationPort
    for flow_id, stats in flows_stats.items():
        dest_port = flow_classifier.get(flow_id, 0)  # Default to 0 if not found
        stats['DestinationPort'] = dest_port
        # Map to UE Index
        if destination_port_start <= dest_port < destination_port_start + num_ue:
            ue_index = dest_port - destination_port_start
            stats['UE_Index'] = ue_index
            stats['UE'] = f'UE_{ue_index}'
        else:
            stats['UE_Index'] = -1
            stats['UE'] = 'Unknown'

    # Step 4: Create DataFrame
    df_flows = pd.DataFrame.from_dict(flows_stats, orient='index')

    # Step 5: Filter out Unknown UEs if necessary
    df_flows = df_flows[df_flows['UE'] != 'Unknown']

    # Step 6: Calculate Packet Loss Rate
    df_flows['PacketLossRate(%)'] = (df_flows['LostPackets'] / df_flows['TxPackets']) * 100.0
    df_flows['Throughput(Kbps)'] = df_flows['Throughput(Gbps)'] * 1e6  # Convert Gbps to Kbps

    # Step 7: Reorder and Select Columns
    columns_order = [
        'FlowID', 'UE', 'DestinationPort', 'TxBytes', 'RxBytes',
        'TxPackets', 'RxPackets', 'LostPackets', 'PacketLossRate(%)',
        'Throughput(Kbps)', 'DelaySum(ns)', 'AvgDelay(ms)', 'JitterSum(ns)',
        'Duration(ns)'
    ]
    df_flows = df_flows[columns_order]

    # Step 8: Save to CSV
    if df_flows.empty:
        print("[Warning] No flows matched the expected destination ports.")
    else:
        df_flows.to_csv(output_csv, index=False)
        print(f"[+] Parsed FlowMonitor data saved to '{output_csv}'.")

if __name__ == "__main__":
    # Example usage
    parse_flowmon('flowmon.xml', 'flowmon_parsed.csv')
