from pathlib import Path
import sys
import json

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import parser


def test_analyze_empty_packets(tmp_path: Path):
    """
    Edge/negative-ish case:
    - no packets captured
    - JSON/CSV still produced, but with empty data
    """
    packets = []  # simulate capture failure / no traffic

    json_path = tmp_path / "summary_empty.json"
    csv_path = tmp_path / "summary_empty.csv"

    parser.write_json(packets, json_path)
    parser.write_csv(packets, csv_path)

    assert json_path.exists()
    assert csv_path.exists()

    # --- JSON checks ---
    data = json.loads(json_path.read_text())

    # meta should indicate zero packets and no protocols
    assert data["meta"]["total_packets"] == 0
    assert data["meta"]["unique_protocols"] == []
    assert data["meta"]["protocol_counts"] == {}

    # packets list should be empty
    assert data["packets"] == []

    # --- CSV checks ---
    csv_text = csv_path.read_text()
    lines = [line.strip() for line in csv_text.splitlines() if line.strip()]

    # Only header row should be present
    assert lines == ["protocol,count"]
