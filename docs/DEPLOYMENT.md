# Deployment Guide - GlacierEQ/whisperX ASTRONOMICAL POWER

**Version**: 3.0.0-ASTRONOMICAL  
**Updated**: November 6, 2025

---

## 🎯 Deployment Strategies

### **1. Cloud GPU Deployment (Maximum Power)**

**Recommended for**: High-volume processing, critical accuracy requirements

#### **Hardware Recommendations**

| GPU | RTFx (Whisper Turbo) | RTFx (Canary Qwen) | Throughput/Day | Cost/Hour |
|-----|---------------------|-------------------|----------------|----------|
| **RTX 4090** | 250-300x | 450-500x | 600-1200 hrs | ~$0.50 |
| **A100 40GB** | 350-400x | 600-700x | 850-1700 hrs | ~$3.00 |
| **H100** | 500+x | 800+x | 1200+ hrs | ~$5.00 |

#### **Configuration**

```yaml
# config/cloud_gpu.yaml
engines:
  primary: whisper_large_v3_turbo
  critical: nvidia_canary_qwen_2.5b
  streaming: kyutai_2.6b
  
diarization:
  standard: nvidia_sortformer_streaming
  complex: pyannote_audio_v3.1
  fast: picovoice_falcon

resources:
  gpu_memory_limit: 40GB
  batch_size_auto: true
  parallel_streams: 4

optimization:
  use_flash_attention: true
  fp16_precision: true
  vad_preprocessing: true
```

#### **Docker Deployment**

```bash
# Build production image
docker build -t whisperx-astronomical:latest .

# Run with GPU support
docker run -d \
  --name whisperx-prod \
  --gpus all \
  -v ./intake:/app/intake \
  -v ./output:/app/output \
  -v ./logs:/app/logs \
  -p 8000:8000 \
  -e CUDA_VISIBLE_DEVICES=0 \
  -e HF_TOKEN=your_huggingface_token \
  whisperx-astronomical:latest
```

#### **Kubernetes Deployment**

```yaml
# k8s/whisperx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: whisperx-astronomical
spec:
  replicas: 3
  selector:
    matchLabels:
      app: whisperx
  template:
    metadata:
      labels:
        app: whisperx
    spec:
      containers:
      - name: whisperx
        image: whisperx-astronomical:latest
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: 16Gi
          requests:
            nvidia.com/gpu: 1
            memory: 8Gi
        env:
        - name: CUDA_VISIBLE_DEVICES
          value: "0"
        volumeMounts:
        - name: intake
          mountPath: /app/intake
        - name: output
          mountPath: /app/output
      volumes:
      - name: intake
        persistentVolumeClaim:
          claimName: whisperx-intake-pvc
      - name: output
        persistentVolumeClaim:
          claimName: whisperx-output-pvc
```

---

### **2. Edge Deployment (Field Forensics)**

**Recommended for**: Mobile units, field operations, resource-constrained environments

#### **Hardware Recommendations**

| Device | Engine | RTFx | Memory | Use Case |
|--------|--------|------|--------|----------|
| **Raspberry Pi 5 (8GB)** | Distil-Whisper | 30-50x | 2GB | Basic transcription |
| **NVIDIA Jetson Orin Nano** | Distil-Whisper | 80-100x | 4GB | Field forensics |
| **Intel NUC + GPU** | Whisper Turbo | 150-200x | 8GB | Mobile command |

#### **Configuration**

```yaml
# config/edge.yaml
engines:
  primary: distil_whisper_large_v3
  fallback: whisper_tiny  # Ultra-low resource fallback
  
diarization:
  primary: picovoice_falcon  # 100x faster, on-device

resources:
  gpu_memory_limit: 2GB
  cpu_threads: 4
  batch_size: 4

optimization:
  int8_quantization: true
  model_pruning: true
  cache_models: true
```

#### **Installation**

```bash
# Install lightweight stack
pip install -r requirements_edge.txt

# Download quantized models
python scripts/download_edge_models.py

# Run edge orchestrator
python edge_orchestrator.py --config config/edge.yaml
```

---

### **3. Hybrid Architecture (Best of Both)**

**Recommended for**: Distributed operations with field + cloud processing

#### **Architecture**

```
┌───────────────────┐
│  Field Unit (Edge)  │
│  - Distil-Whisper   │
│  - Falcon Diarize   │
│  - Quick Preview    │
└───────────────────┘
         │
         │ Upload
         ↓
┌───────────────────┐
│  Cloud Hub (GPU)    │
│  - Canary Qwen      │
│  - Whisper Turbo    │
│  - Full Analytics   │
└───────────────────┘
```

#### **Processing Tiers**

1. **Edge Intake**: Distil-Whisper + Falcon for immediate field processing
2. **Cloud Upload**: Automatic sync to cloud for re-processing
3. **Cloud Enhancement**: Canary Qwen for critical cases
4. **Analytics**: Full NLP pipeline in cloud

---

## 🔧 Environment Setup

### **Environment Variables**

```bash
# .env
CUDA_VISIBLE_DEVICES=0
TRANSFORMERS_CACHE=/app/.cache
HF_TOKEN=your_huggingface_token
PYANNOTE_AUTH_TOKEN=your_pyannote_token

# Optional: NVIDIA NeMo
NEMO_CACHE_DIR=/app/.nemo_cache

# Optional: Picovoice Falcon
PICOVOICE_ACCESS_KEY=your_picovoice_key

# Performance tuning
OMP_NUM_THREADS=8
CUDA_LAUNCH_BLOCKING=0
```

### **System Requirements**

**Minimum**:
- GPU: 4GB VRAM (Whisper Turbo)
- RAM: 16GB
- Storage: 50GB SSD
- CUDA: 11.8+

**Recommended**:
- GPU: 24GB+ VRAM (Multi-engine)
- RAM: 32GB+
- Storage: 500GB NVMe SSD
- CUDA: 12.1+

---

## 📊 Monitoring & Observability

### **Health Checks**

```python
# health_check.py
import torch
from multi_engine_orchestrator import AstronomicalOrchestrator

def health_check():
    checks = {
        "cuda_available": torch.cuda.is_available(),
        "gpu_count": torch.cuda.device_count(),
        "gpu_memory": torch.cuda.get_device_properties(0).total_memory / 1e9,
        "orchestrator": True
    }
    
    try:
        orchestrator = AstronomicalOrchestrator()
        checks["orchestrator"] = True
    except Exception as e:
        checks["orchestrator"] = False
        checks["error"] = str(e)
    
    return checks
```

### **Prometheus Metrics**

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge

processing_duration = Histogram(
    'whisperx_processing_duration_seconds',
    'Time spent processing audio',
    ['engine', 'quality_tier']
)

processing_count = Counter(
    'whisperx_processing_total',
    'Total number of audio files processed',
    ['engine', 'status']
)

gpu_memory_usage = Gauge(
    'whisperx_gpu_memory_bytes',
    'Current GPU memory usage'
)
```

---

## 🔒 Security Considerations

### **Chain of Custody**

```python
# chain_of_custody.py
import hashlib
import json
from datetime import datetime

def create_custody_record(file_path: str, processing_config: dict) -> dict:
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    
    record = {
        "file_hash_sha256": file_hash,
        "timestamp": datetime.utcnow().isoformat(),
        "processing_config": processing_config,
        "system_info": {
            "gpu": torch.cuda.get_device_name(0),
            "cuda_version": torch.version.cuda
        }
    }
    
    return record
```

### **Access Control**

```yaml
# rbac.yaml
roles:
  analyst:
    - read:transcriptions
    - write:annotations
  
  supervisor:
    - read:transcriptions
    - write:annotations
    - approve:critical_cases
  
  admin:
    - all:permissions
```

---

## 🚀 Performance Tuning

### **Batch Size Optimization**

```python
# batch_optimizer.py
def calculate_optimal_batch_size(gpu_memory_gb: float, audio_duration: float) -> int:
    """Calculate optimal batch size based on available GPU memory"""
    
    if gpu_memory_gb >= 40:  # A100
        return 24 if audio_duration < 60 else 16
    elif gpu_memory_gb >= 24:  # RTX 4090
        return 16 if audio_duration < 60 else 12
    elif gpu_memory_gb >= 12:  # RTX 3080
        return 12 if audio_duration < 60 else 8
    else:  # < 12GB
        return 8 if audio_duration < 60 else 4
```

### **Caching Strategy**

```python
# caching.py
import redis
import pickle

class ResultCache:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.client = redis.from_url(redis_url)
    
    def get_cached_result(self, file_hash: str) -> Optional[dict]:
        cached = self.client.get(f"result:{file_hash}")
        return pickle.loads(cached) if cached else None
    
    def cache_result(self, file_hash: str, result: dict, ttl: int = 86400):
        self.client.setex(
            f"result:{file_hash}",
            ttl,
            pickle.dumps(result)
        )
```

---

## 📝 Troubleshooting

### **Common Issues**

**Issue**: Out of GPU memory
```bash
Solution: Reduce batch size or use smaller engine
export WHISPERX_BATCH_SIZE=4
python multi_engine_orchestrator.py
```

**Issue**: Slow processing
```bash
Solution: Enable FlashAttention-2
pip install flash-attn --no-build-isolation
```

**Issue**: Poor accuracy on noisy audio
```python
# Use Canary Qwen for critical/noisy cases
profile = AudioProfile(
    quality_tier="critical",
    is_noisy=True
)
config = orchestrator.select_optimal_engines(profile)
```

---

## 📚 Additional Resources

- [Performance Benchmarks](./BENCHMARKS.md)
- [API Reference](./API_REFERENCE.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [GitHub Issues](https://github.com/GlacierEQ/whisperX/issues)

---

*Updated: November 6, 2025 | Version: 3.0.0-ASTRONOMICAL*