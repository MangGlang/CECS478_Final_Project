# RUNBOOK – OSI Encapsulation Explorer (Vertical Slice)
- This runbook explains how to build, run, test, and inspect artifacts for the OSI Encapsulation Explorer vertical slice.

## 1. Environment Requirements
- Before running this project, ensure you have:
- WSL2 (Ubuntu)
- Docker Desktop installed and running
- Docker Desktop → Settings → Resources → WSL Integration → enabled for - 
Ubuntu
- make installed (default on Ubuntu)
- pytest (optional, for unit tests)

## 2. Clone the Repository
```
git clone https://github.com/MangGlang/CECS478_Final_Project.git
cd CECS478_Final_Project
```

## 3. Grading Command
```
make up && make demo
```
- make up: builds docker image for app
- make demo: runs vertical slice inside a container, executing:
> echo --> encrypt --> capture --> analyze
- The program prints the packet protocol stacks and writes summary artifacts.

## 4. Expected Console Output
```
=== OSI Encapsulation Explorer (demo) ===
Pipeline: echo -> encrypt -> capture -> analyze
Packet 0: ETH -> IP -> TCP -> HTTP
Packet 1: ETH -> IP -> TCP -> HTTP
Packet 2: ETH -> IP -> TCP -> HTTP
JSON summary written to: artifacts/release/summary.json
CSV summary written to: artifacts/release/summary.csv
Log written to: artifacts/release/run.log
=========================================
```

## 5. Artifact Locations
```
artifacts/release/
```
present in this folder is the following files:
- run.log (records every stage of OSI pipline)
- summary.json (contains protocol counts, packets counts, protocol stacks)
- summary.csv (a table of compiled results of packets)

## 6. Unit Tests
```
pip install pytest
pytest -vv
```

Expected output:
```
collected 2 items
tests/test_parser_empty.py .      [50%]
tests/test_parser_happy.py .      [100%]
```

## 7. Useful Make Commands
```
make up - builds docker image
make demo - runs vertical slice demo
make clean - removes containers, images, and volumes
make test - run pytest