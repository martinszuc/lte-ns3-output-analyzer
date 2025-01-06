import os
import xml.etree.ElementTree as ET
import pandas as pd
from tabulate import tabulate

def parse_flowmon(flowmon_file, output_csv):
    """
    Parses the flowmon.xml file and extracts flow statistics.

    Args:
        flowmon_file (str): Path to the flowmon.xml file.
        output_csv (str): Path to save the parsed CSV.
    """
    try:
        tree = ET.parse(flowmon_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"[Error] XML parsing error: {e}")
        return

    flows = []
    for flow in root.findall(".//Flow"):
        flow_id = flow.get('flowId')
        if flow_id is None:
            continue

        tx_node = flow.find('Tx')
        rx_node = flow.find('Rx')
        if tx_node is None or rx_node is None:
            continue

        tx_address_element = tx_node.find('Address')
        rx_address_element = rx_node.find('Address')
        tx_port_element    = tx_node.find('Port')
        rx_port_element    = rx_node.find('Port')
        tx_packets_element = tx_node.find('Packets')
        rx_packets_element = rx_node.find('Packets')
        tx_bytes_element   = tx_node.find('Bytes')
        rx_bytes_element   = rx_node.find('Bytes')
        tx_retx_element    = tx_node.find('ReTx')
        delay_sum_element  = rx_node.find('DelaySum')
        jitter_sum_element = rx_node.find('JitterSum')
        loss_element       = flow.find('Loss')
        protocol_element   = rx_node.find('Protocol')
        duration_element   = flow.find('Duration')

        if (tx_address_element is None or rx_address_element is None or
            tx_port_element is None or rx_port_element is None or
            protocol_element is None):
            continue

        source_address = tx_address_element.get('value')
        destination_address = rx_address_element.get('value')
        protocol = protocol_element.get('value')
        try:
            source_port = int(tx_port_element.get('value'))
            destination_port = int(rx_port_element.get('value'))
        except (TypeError, ValueError):
            continue

        def safe_int(elem):
            return int(elem.get('value')) if elem is not None and elem.get('value') else 0

        def safe_float(elem):
            return float(elem.get('value')) if elem is not None and elem.get('value') else 0.0

        tx_packets = safe_int(tx_packets_element)
        rx_packets = safe_int(rx_packets_element)
        tx_bytes   = safe_int(tx_bytes_element)
        rx_bytes   = safe_int(rx_bytes_element)
        tx_retransmissions = safe_int(tx_retx_element)
        delay_sum  = safe_float(delay_sum_element)
        jitter_sum = safe_float(jitter_sum_element)
        packet_loss = safe_float(loss_element)
        duration   = safe_float(duration_element)

        throughput = (rx_bytes * 8.0) / (duration * 1000.0) if duration > 0 else 0.0
        avg_delay_ms = (delay_sum / rx_packets) * 1000.0 if rx_packets > 0 else 0.0

        flows.append({
            'FlowID': int(flow_id),
            'Protocol': protocol,
            'SourceAddress': source_address,
            'DestinationAddress': destination_address,
            'SourcePort': source_port,
            'DestinationPort': destination_port,
            'TxPackets': tx_packets,
            'RxPackets': rx_packets,
            'TxBytes': tx_bytes,
            'RxBytes': rx_bytes,
            'TxRetransmissions': tx_retransmissions,
            'Duration(s)': duration,
            'Throughput(Kbps)': throughput,
            'AvgDelay(ms)': avg_delay_ms,
            'PacketLoss(%)': packet_loss
        })

    df_flows = pd.DataFrame(flows)

    # Map flows to UEs based on DestinationPort (e.g., 5000..5004 for 5 UEs)
    df_flows['UE_Index'] = df_flows['DestinationPort'] - 5000
    df_flows['UE'] = 'UE_' + df_flows['UE_Index'].astype(str)

    # Filter out any flows that do not match the expected port range
    df_flows = df_flows[
        (df_flows['DestinationPort'] >= 5000) &
        (df_flows['DestinationPort'] < 5000 + 5)  # Adjust if number of UEs varies
    ]

    if df_flows.empty:
        print("[Warning] No flows matched the expected destination ports.")
    else:
        df_flows.to_csv(output_csv, index=False)
        print(f"[+] Parsed FlowMonitor data saved to '{output_csv}'.")

