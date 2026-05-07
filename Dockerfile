FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# System deps
RUN apt-get update && apt-get install -y \
    python3-pip \
    espeak-ng \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
RUN pip3 install --no-cache-dir \
    torch \
    kokoro>=0.19 \
    soundfile \
    runpod \
    numpy

# Copy app
COPY app /app

# Start handler
CMD ["python3", "handler.py"]
