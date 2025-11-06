# GlacierEQ/whisperX - ASTRONOMICAL POWER Dockerfile
# Multi-engine support with optimal GPU acceleration
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 python3-pip python3.11-dev \
    ffmpeg libsndfile1 git wget curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install PyTorch with CUDA support
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Copy and install requirements
COPY requirements_astronomical.txt .
RUN pip3 install --no-cache-dir -r requirements_astronomical.txt

# Install FlashAttention-2 (optional, compiled for CUDA 12.1)
# Uncomment if GPU supports it (significant speedup)
# RUN pip3 install flash-attn --no-build-isolation

# Download Whisper Turbo model (optional: pre-cache in image)
RUN python3 -c "import whisper; whisper.load_model('turbo')"

# Copy application
COPY . .

# Create directories
RUN mkdir -p intake processing cases output logs

ENV CUDA_VISIBLE_DEVICES=0
ENV TRANSFORMERS_CACHE=/app/.cache

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python3 -c "import torch; assert torch.cuda.is_available()"

EXPOSE 8000 9090

CMD ["python3", "multi_engine_orchestrator.py"]
