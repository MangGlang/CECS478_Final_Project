# src/parser.py

import argparse
import json
import logging
import os
from pathlib import Path


def fake_parse_packets():
    """
    Fake parser for now:
    Pretends we have 3 packets with the same protocol stack.
    Later we will replace this with real pcap parsing.
    """
    packets = []
    for i in range(3):
        protocols = ["ETH", "IP", "TCP", "HTTP"]
        packets.append({
            "packet_idx": i,
            "protocols": protocols
        })
    return packets


def write_json(packets, out_json_path: Path):
    data = {"packets": []}
    for p in packets:
        data["packets"].append({
            "packet_idx": p["packet_idx"],
            "protocols": [{"protocol": proto} for proto in p["protocols"]]
        })
    out_json_path.parent.mkdir(parents=True, exist_ok=True)
    with out_json_path.open("w") as f:
        json.dump(data, f, indent=2)


def write_csv(packets, out_csv_path: Path):
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

    # For now, we do NOT actually read the pcap.
    # We just simulate packets.
    packets = fake_parse_packets()

    # Write outputs
    json_path = Path(args.out_json)
    csv_path = Path(args.out_csv)
    write_json(packets, json_path)
    write_csv(packets, csv_path)

    # Also print to console for your demo
    print("=== OSI Encapsulation Explorer (demo) ===")
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
