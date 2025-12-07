from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import parser


def test_analyze_packets_with_no_protocols(tmp_path: Path):
    """
    Edge/negative test:
    - packets list is non-empty, but a packet has no protocols
    - JSON/CSV should still be created and protocol metrics should be empty
    """
    packets = [
        {"packet_idx": 0, "protocols": []},
    ]

    json_path = tmp_path / "summary_no_protocols.json"
    csv_path = tmp_path / "summary_no_protocols.csv"

    parser.write_json(packets, json_path)
    parser.write_csv(packets, csv_path)

    assert json_path.exists()
    assert csv_path.exists()

    # --- JSON checks ---
    data = json.loads(json_path.read_text())
    assert data["meta"]["total_packets"] == 1
    assert data["meta"]["unique_protocols"] == []
    assert data["meta"]["protocol_counts"] == {}
    assert data["packets"][0]["packet_idx"] == 0
    assert data["packets"][0]["protocols"] == []

    # --- CSV checks ---
    csv_text = csv_path.read_text()
    lines = [line.strip() for line in csv_text.splitlines() if line.strip()]
    # Only header row, no protocol lines
    assert lines == ["protocol,count"]
