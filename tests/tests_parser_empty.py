from pathlib import Path
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

    json_text = json_path.read_text()
    csv_text = csv_path.read_text()

    # JSON should contain an empty packets list
    assert '"packets": []' in json_text.replace("\n", "").replace(" ", "")

    # CSV should have only the header
    lines = [line.strip() for line in csv_text.splitlines() if line.strip()]
    assert lines == ["protocol,count"]
