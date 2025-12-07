FROM python:3.11-slim

RUN adduser --disabled-password --uid 1000 appuser

WORKDIR /work

COPY . /work

# Create artifacts folder and give ownership to appuser
RUN mkdir -p /work/artifacts/release && chown -R appuser:appuser /work/artifacts

USER appuser

CMD ["python", "src/parser.py"]
