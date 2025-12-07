# ============================================================
# Final Project - OSI Encapsulation Explorer
# CECS478 Final Project - "OSI Encapsulation Visualization Tool"
# Authors: Minhlee Lam & Hoa Nguyen
# ============================================================

PROJECT_NAME ?= OSI_Encapsulation_Explorer
COMPOSE      ?= docker compose       # use 'docker-compose' if using v1 CLI
SERVICE      ?= app                  # <-- MUST MATCH docker-compose.yml
PCAP_OUT     ?= ./captures/osi_traffic.pcap

.PHONY: bootstrap up down logs ps rebuild clean pcap demo help
.DEFAULT_GOAL := help

## bootstrap: Build Docker images and start containers
bootstrap:
	@echo "Bootstrapping $(PROJECT_NAME)..."
	$(COMPOSE) build
	$(COMPOSE) up -d
	@echo "Containers for $(PROJECT_NAME) are up and running."

## up: Start existing containers (build images if needed)
up:
	$(COMPOSE) build

## down: Stop all running containers
down:
	$(COMPOSE) down

## logs: View logs from all services
logs:
	$(COMPOSE) logs -f

## ps: List running containers
ps:
	$(COMPOSE) ps

## rebuild: Force rebuild images without cache
rebuild:
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d

## clean: Stop containers and remove all images, volumes, and orphans
clean:
	$(COMPOSE) down --rmi all --volumes --remove-orphans
	@echo "Cleaned up containers, images, and volumes for $(PROJECT_NAME)."

## pcap: Capture Docker network traffic for OSI visualization (controlled use only)
pcap:
	@mkdir -p $(dir $(PCAP_OUT))
	@echo "Capturing traffic inside $(SERVICE) container..."
	$(COMPOSE) exec -T $(SERVICE) sh -c 'command -v tcpdump >/dev/null || (echo "tcpdump missing" && exit 1); tcpdump -i any -w /tmp/osi_traffic.pcap' &
	@sleep 3
	@echo "Press Ctrl+C when done capturing. The pcap file will be copied out."
	@trap '$(COMPOSE) cp $(SERVICE):/tmp/osi_traffic.pcap $(PCAP_OUT); echo "Saved to $(PCAP_OUT)";' INT; while :; do sleep 1; done

## demo: Run the vertical slice demo inside the container
demo:
	@echo "Running demo (vertical slice) in $(SERVICE) container..."
	$(COMPOSE) run --rm $(SERVICE)
	@echo "Demo complete."

## test: Run unit tests
test:
	pytest -vv

## help: Show available make commands
help:
	@echo "Available make commands:"
	@grep -E '^## ' Makefile | sed -e 's/^## //'
