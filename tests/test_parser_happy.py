from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import parser

def test_capture_and_analyze_happy(tmp_path: Path):
    """
    Happy path:
    - simulate packets via fake_capture_packets
    - write JSON + CSV to temporary directory
    - assert files exist and contain expected content
    """
    # Arrange
    pcap_path = "artifacts/pcaps/sample.pcap"  # just a string; function doesn't actually read it
    packets = parser.fake_capture_packets(pcap_path)

    json_path = tmp_path / "summary.json"
    csv_path = tmp_path / "summary.csv"

    # Act
    parser.write_json(packets, json_path)
    parser.write_csv(packets, csv_path)

    # Assert
    assert json_path.exists()
    assert csv_path.exists()

    json_text = json_path.read_text()
    csv_text = csv_path.read_text()

    # We know we create 3 packets with the same 4 protocols
    assert '"packet_idx": 0' in json_text
    assert '"protocol": "ETH"' in json_text

    # CSV has header + 4 lines (ETH, HTTP, IP, TCP)
    lines = [line.strip() for line in csv_text.splitlines() if line.strip()]
    assert lines[0] == "protocol,count"
    assert len(lines) == 1 + 4  # header + 4 protocols
    assert "ETH,3" in lines
    assert "IP,3" in lines
    assert "TCP,3" in lines
    assert "HTTP,3" in lines
