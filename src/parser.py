# src/parser.py

import argparse
import json
import logging
import os
from pathlib import Path


def fake_echo(pcap_path: str) -> str:
    """
    ECHO stage
    In a real system this might receive or generate traffic.
    For now we just log that we're 'echoing' a synthetic pcap path.
    """
    logging.info("ECHO: preparing synthetic traffic using pcap path %s", pcap_path)
    return pcap_path


def fake_encrypt(pcap_path: str) -> str:
    """
    ENCRYPT stage
    In a real system this would encrypt payloads.
    For now we just log that encryption would happen here.
    """
    logging.info("ENCRYPT: applying demo encryption step (placeholder) for %s", pcap_path)
    # We could return a different path or metadata later; for now, just return the same.
    return pcap_path


def fake_capture_packets(pcap_path: str):
    """
    CAPTURE stage
    In a real system this would capture packets from the network or read from a pcap file.
    For now we just fake 3 packets with the same protocol stack.
    """
    logging.info("CAPTURE: parsing packets from %s (simulated)", pcap_path)
    packets = []
    for i in range(3):
        protocols = ["ETH", "IP", "TCP", "HTTP"]
        packets.append({
            "packet_idx": i,
            "protocols": protocols
        })
    logging.info("CAPTURE: produced %d synthetic packets", len(packets))
    return packets


def write_json(packets, out_json_path: Path):
    logging.info("ANALYZE: writing JSON summary to %s", out_json_path)

    # Compute simple metrics
    total_packets = len(packets)
    protocol_counts = {}
    for p in packets:
        for proto in p["protocols"]:
            protocol_counts[proto] = protocol_counts.get(proto, 0) + 1

    data = {
        "meta": {
            "total_packets": total_packets,
            "unique_protocols": sorted(protocol_counts.keys()),
            "protocol_counts": protocol_counts,
        },
        "packets": [],
    }

    for p in packets:
        data["packets"].append({
            "packet_idx": p["packet_idx"],
            "protocols": [{"protocol": proto} for proto in p["protocols"]],
        })

    out_json_path.parent.mkdir(parents=True, exist_ok=True)
    with out_json_path.open("w") as f:
        json.dump(data, f, indent=2)



def write_csv(packets, out_csv_path: Path):
    logging.info("ANALYZE: computing protocol counts and writing CSV to %s", out_csv_path)
    # Simple metric: count how many times each protocol appears
    counts = {}
    for p in packets:
        for proto in p["protocols"]:
            counts[proto] = counts.get(proto, 0) + 1

    out_csv_path.parent.mkdir(parents=True, exist_ok=True)
    with out_csv_path.open("w") as f:
        f.write("protocol,count\n")
        for proto, count in sorted(counts.items()):
            f.write(f"{proto},{count}\n")
    logging.info("ANALYZE: protocol counts = %s", counts)


def main():
    parser = argparse.ArgumentParser(description="OSI Encapsulation Explorer demo parser")
    parser.add_argument(
        "--pcap",
        help="Path to synthetic pcap file (not used yet, but reserved for later).",
        default="artifacts/pcaps/sample.pcap"
    )
    parser.add_argument(
        "--out-json",
        help="Path to JSON summary output.",
        default="artifacts/release/summary.json"
    )
    parser.add_argument(
        "--out-csv",
        help="Path to CSV metrics output.",
        default="artifacts/release/summary.csv"
    )
    parser.add_argument(
        "--log",
        help="Path to log file.",
        default="artifacts/release/run.log"
    )
    args = parser.parse_args()

    # Setup logging
    log_path = Path(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    logging.info("Starting OSI demo parser.")
    logging.info("PCAP (placeholder) path: %s", args.pcap)

    # ----- Vertical slice pipeline: echo -> encrypt -> capture -> analyze -----

    # ECHO stage
    echoed_pcap = fake_echo(args.pcap)

    # ENCRYPT stage (placeholder)
    encrypted_pcap = fake_encrypt(echoed_pcap)

    # CAPTURE stage (simulated packet parsing)
    packets = fake_capture_packets(encrypted_pcap)

    # ANALYZE stage (write JSON + CSV summaries)
    json_path = Path(args.out_json)
    csv_path = Path(args.out_csv)
    write_json(packets, json_path)
    write_csv(packets, csv_path)

    print("=== OSI Encapsulation Explorer (demo) ===")
    print("Pipeline: echo -> encrypt -> capture -> analyze")
    for p in packets:
        stack = " -> ".join(p["protocols"])
        print(f"Packet {p['packet_idx']}: {stack}")
    print("JSON summary written to:", json_path)
    print("CSV summary written to:", csv_path)
    print("Log written to:", log_path)
    print("=========================================")

    logging.info("Finished OSI demo parser. Wrote JSON, CSV, and log.")


if __name__ == "__main__":
    main()
