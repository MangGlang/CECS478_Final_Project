# OSI Encapsulation Explorer – CECS 478 Final Project

### Vertical Slide Demo 
![Demo GIF](https://raw.githubusercontent.com/MangGlang/CECS478_Final_Project/main/assets/demo.gif)

### 1. Problem Statement

Understanding how data travels through the layers of the OSI model is one of the foundational concepts in networking. This process is often overlooked as students and analysts tend to observe the outcome of packets on a network rather than the layered transformations that occur along the way. The goal of this project is to design an **interactive system** that visually demonstrates how network packets are **encapsulated and decapsulated** as they pass through the OSI layers. The system will parse network data, show each encapsulation step, and optionally export these steps into a JSON or CSV format for further analysis. By building this tool, we aim to provide a clear and reproducible educational demonstration of OSI-layer encapsulation using real or simulated traffic.

### 2. Threat Model

#### **Assets**
- **Packet data:** The PCAP files or live captures (synthetic) used for demonstration.  
- **Visualization outputs:** The exported CSV or JSON files summarizing encapsulation steps.  
- **System integrity:** The accuracy and reliability of the parsing logic and visualization modules.  
- **Execution environment:** The Docker-based sandbox used to run the project and prevent unauthorized network access.  

#### **Threat Actors**
- **Input validation gaps:** If the parser accepts arbitrary PCAP files, malformed inputs could cause exceptions or crashes.  
- **File I/O operations:** Reading and writing artifacts (e.g., packet captures, exported summaries) without validation could risk overwriting or accessing unintended files.  
- **Visualization endpoints:** If the visualization component evolves into a lightweight web interface, it might introduce exposure via local ports or HTTP endpoints.  

#### **Assumptions**
- All data is synthetic, anonymized, or generated locally for demonstration purposes.  
- The tool will not be connected to any production or campus network.  
- Execution will take place inside a Docker container, isolated from the host machine.  

#### **Planned Defenses**
- **Environment isolation:** All components will run within Docker containers using non-root users and limited filesystem permissions.  
- **Error handling:** Implement safe parsing routines to prevent crashes on malformed inputs.  
- **Strict input validation:** Only allow reading `.pcap` or `.pcapng` files from the local directory.  
- **Logging and transparency:** Maintain logs of all parsed files and exports to ensure traceability.  



### 3. Success Metrics

Project success will be measured based on the following criteria:  
- Successfully parses and visualizes at least **five layers of the OSI model** from a packet capture (PCAP).  
- Demonstrates **correct encapsulation and decapsulation order** for sample traffic.  
- Generates **exportable summaries (CSV or JSON)** showing layer-by-layer information for at least three example packets.  



### 4. Dataset / PCAP Plan

The project will use **synthetic packet captures** generated through controlled local traffic, such as simple HTTP requests or ping commands, using tools like:  
- `scapy` (Python packet crafting)  
- `tcpdump` or `Wireshark` for small offline captures  

The datasets will be intentionally small to keep analysis simple and reproducible. Each capture will demonstrate specific OSI layer combinations, such as:  
- **ICMP echo requests** (Layer 3–4 focus)  
- **HTTP GET requests** (Layer 7 focus)  
- **DNS lookups** (showing UDP encapsulation)  



### 5. Risks and Ethics

This project carries **minimal risk**, as no live or third-party network monitoring is involved. All data will be synthetic or anonymized, and the purpose is strictly educational, adhering to responsible data handling principles. All captures will be restricted to **local Docker networks** to avoid unintentional interception of real traffic. Demonstration datasets will be self-generated within approved lab environments. Network inspection activities will be performed **responsibly, transparently, and with clear consent**, ensuring compliance with ethical and legal guidelines.


### Architecture Diagram

The OSI encapsulation Explorer will follow a modular design with three components:
- Packet Input Module – Imports or generates PCAPs (via scapy or tcpdump). Responsible for basic validation and safe handling of all input files.
- Encapsulation Parser – Extracts headers and reconstructs OSI layers using Python libraries such as dpkt or pyshark. This component will map protocols to OSI layers (e.g., IP = Layer 3, TCP = Layer 4) and provide structured data for visualization.
- Visualization & Exporter – Displays results in a simple terminal interface and exports summaries to CSV and JSON formats. 


![Architecture Diagram](assets/architecture_diagram.png)


## Quick Commands
| Command | Description |
|----------|-------------|
| `make bootstrap` | Build and start containers |
| `make up` | Start existing containers |
| `make down` | Stop containers |
| `make clean` | Remove all containers, images, and volumes |
| `make help` | List all available commands |
