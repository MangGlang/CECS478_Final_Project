# What Works / What’s Next

## What Works

- `echo → encrypt → capture → analyze`
- Shown in `src/parser.py`.

## Synthetic packet generation
- `fake_capture_packets()` produces 3 packets with the stack  
    `ETH -> IP -> TCP -> HTTP`

## Analysis & Metrics
- `write_json()` writes `summary.json` with:
- `write_csv()` writes `summary.csv` with protocol counts.

## Artifacts
- artifacts/release/run.log
- artifacts/release/summary.json
- artifacts/release/summary.csv

## Runs in Docker
- 'make up && make demo'  runs the vertical slice inside Docker.

## Happy and Negative tests
- tests/test_parser_happy.py
- tests/test_parser_empty.py
- tests/test_parser_no_protocols.py

## What's next

- **Real PCAP support (future Feature)**:
 - Replace fake packet with real parsing using library

- **Richer visualization**:
 - Generate charts, possibly UI for exploring packets

- **More test coverage**:
 - Add tests for malformed packet list
 - Verify logging content

- **Extended protocol mapping**:
 - Add support for UDP, DNS, ICMP, and IPv6 when real pcaps introduced