# Python image
FROM python:3.11-slim

# Create a non-root user for safety
RUN adduser --disabled-password --uid 1000 appuser

# Set working directory
WORKDIR /work

# Copy everything into the container
COPY . /work

# Switch to non-root user
USER appuser

# Default command
CMD ["python", "src/parser.py"]