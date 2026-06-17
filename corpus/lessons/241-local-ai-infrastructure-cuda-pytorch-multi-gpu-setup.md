---
title: "24.1 — Local AI Infrastructure: CUDA, PyTorch & Multi-GPU Setup"
subject: "AI Experiments"
catalog: advanced
audience_tier: higher-education
chapter: "24.1"
type: experiment-chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 24.1 — Local AI Infrastructure: CUDA, PyTorch & Multi-GPU Setup

> *"The biggest lesson that can be read from 70 years of AI research is that general methods that leverage computation are ultimately the most effective."*
> — **Rich Sutton**, *The Bitter Lesson* (2019)

Before you fine-tune a single weight or generate a single image, your GPU stack must be bulletproof. This chapter takes you from bare metal to a fully validated multi-GPU PyTorch environment with proper memory management, NCCL communication, and reproducible benchmarks.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Install and validate CUDA toolkit, cuDNN, and NCCL on Linux/WSL2.
2. Configure PyTorch with the correct CUDA version and verify GPU access.
3. Benchmark GPU compute (TFLOPS) and memory bandwidth.
4. Set up `accelerate` for multi-GPU training with FSDP or DeepSpeed.
5. Profile GPU memory usage and identify OOM bottlenecks.
6. Configure environment variables for deterministic training.
7. Monitor GPU utilization in real-time with `nvitop` and `nvidia-smi`.

---

## 🖼️ Visual Anchor — GPU Memory Hierarchy

![aiexp__5.1-fig1](aiexp__5.1-fig1.svg)

---

## 📚 1. Concepts & Definitions

### GPU Compute Architecture

| Concept | Definition |
|---------|-----------|
| **CUDA Core** | Single-precision floating-point execution unit on NVIDIA GPUs |
| **Tensor Core** | Specialized matrix-multiply-accumulate unit (4×4 FP16 → FP32) |
| **SM (Streaming Multiprocessor)** | Group of CUDA/Tensor cores sharing L1 cache and registers |
| **VRAM** | High-bandwidth GPU memory (HBM3 on A100/H100, GDDR6X on RTX 4090) |
| **NCCL** | NVIDIA Collective Communications Library — GPU-to-GPU data transfer |
| **FSDP** | Fully Sharded Data Parallel — shards model across GPUs |
| **DeepSpeed** | Microsoft's distributed training library (ZeRO stages 1-3) |

### Memory Math for a 24GB GPU (RTX 4090)

```
Model weights (FP16):     params × 2 bytes
Optimizer states (AdamW):  params × 8 bytes (FP32 weights + momentum + variance)
Gradients (FP16):         params × 2 bytes
Activations:              batch_size × seq_len × hidden_dim × num_layers × ~2 bytes

Example: Llama-3-8B in FP16
  Weights:     8B × 2 = 16 GB
  Remaining:   24 - 16 = 8 GB for activations + KV cache
  Conclusion:  Inference fits. Training does NOT fit without QLoRA/FSDP.
```

### Key Environment Variables

```bash
# Deterministic operations (slower but reproducible)
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export PYTHONHASHSEED=42

# Memory management
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Multi-GPU
export NCCL_P2P_DISABLE=0
export NCCL_IB_DISABLE=1  # if no InfiniBand

# HuggingFace cache
export HF_HOME=/data/hf_cache
export TRANSFORMERS_CACHE=/data/hf_cache/transformers
```

---

## 🔬 2. Theory Briefing

> For deep theory on GPU architectures and CUDA programming, see [08.15 - GPU Computing & CUDA Foundations](08.15---GPU-Computing-&-CUDA-Foundations).

### CUDA Execution Model (Minimal)

The GPU executes **kernels** — functions launched on thousands of threads organized in a grid:

```
Grid → Blocks → Threads
       (up to 1024 threads per block)
       (blocks scheduled across SMs)
```

PyTorch abstracts this entirely. You interact with CUDA through:
1. **Device placement:** `tensor.to('cuda:0')`
2. **Mixed precision:** `torch.autocast('cuda', dtype=torch.float16)`
3. **Memory management:** `torch.cuda.empty_cache()`

### Memory Bandwidth vs Compute Bound

| Regime | Bottleneck | Example Operations |
|--------|-----------|-------------------|
| **Compute-bound** | TFLOPS | Large matmuls, attention with FlashAttention |
| **Memory-bound** | GB/s bandwidth | Element-wise ops, small batch inference, KV cache reads |

RTX 4090 specs:
- **FP16 Tensor:** 330 TFLOPS (with sparsity: 661)
- **Memory bandwidth:** 1,008 GB/s
- **VRAM:** 24 GB GDDR6X

**Arithmetic intensity** = FLOPs / Bytes transferred. If your operation's arithmetic intensity exceeds the machine's compute-to-bandwidth ratio (~330 FLOPS/byte for 4090), you're compute-bound. Otherwise, memory-bound.

---

## 🔧 3. Setup & Prerequisites

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | RTX 3090 (24GB) | RTX 4090 (24GB) |
| CPU | 8-core | 16-core (Ryzen 9 / i9) |
| RAM | 32 GB | 64 GB |
| Storage | 500 GB NVMe | 2 TB NVMe |
| PSU | 850W | 1000W (for dual GPU) |

### Software Stack Installation

```bash
# 1. NVIDIA Driver (latest stable)
sudo apt install nvidia-driver-550

# 2. CUDA Toolkit 12.4
wget https://developer.download.nvidia.com/compute/cuda/12.4.0/local_installers/cuda_12.4.0_550.54.14_linux.run
sudo sh cuda_12.4.0_550.54.14_linux.run --toolkit --silent

# 3. Add to PATH
echo 'export PATH=/usr/local/cuda-12.4/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# 4. Verify
nvidia-smi          # Driver version, GPU info
nvcc --version      # CUDA compiler version

# 5. Conda environment
conda create -n aiexp python=3.11 -y
conda activate aiexp

# 6. PyTorch with CUDA 12.4
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# 7. Verify PyTorch CUDA
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

### WSL2 Specific Notes

```bash
# WSL2 uses the Windows NVIDIA driver — do NOT install nvidia-driver inside WSL
# Only install cuda-toolkit (no driver component)
sudo apt-get install -y cuda-toolkit-12-4

# Verify GPU passthrough
nvidia-smi  # Should show your Windows GPU
```

---

## 🧪 4. Experiment Walkthrough

### Experiment 4.1 — GPU Validation & Info Dump

```python
import torch
import sys

def gpu_info():
    """Print comprehensive GPU information."""
    print(f"Python: {sys.version}")
    print(f"PyTorch: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"CUDA version: {torch.version.cuda}")
    print(f"cuDNN version: {torch.backends.cudnn.version()}")
    print(f"Device count: {torch.cuda.device_count()}")
    
    for i in range(torch.cuda.device_count()):
        props = torch.cuda.get_device_properties(i)
        print(f"\n--- GPU {i}: {props.name} ---")
        print(f"  Compute capability: {props.major}.{props.minor}")
        print(f"  Total memory: {props.total_mem / 1024**3:.1f} GB")
        print(f"  SMs: {props.multi_processor_count}")
        print(f"  Max threads/SM: {props.max_threads_per_multi_processor}")
        
    # Memory snapshot
    if torch.cuda.is_available():
        torch.cuda.set_device(0)
        free, total = torch.cuda.mem_get_info(0)
        print(f"\n  Free memory: {free / 1024**3:.2f} GB")
        print(f"  Allocated: {(total - free) / 1024**3:.2f} GB")

gpu_info()
```

### Experiment 4.2 — TFLOPS Benchmark

```python
import torch
import time

def benchmark_matmul(M=4096, N=4096, K=4096, dtype=torch.float16, warmup=10, iters=100):
    """Benchmark matrix multiplication TFLOPS."""
    device = torch.device('cuda')
    A = torch.randn(M, K, dtype=dtype, device=device)
    B = torch.randn(K, N, dtype=dtype, device=device)
    
    # Warmup
    for _ in range(warmup):
        C = torch.mm(A, B)
    torch.cuda.synchronize()
    
    # Timed iterations
    start = time.perf_counter()
    for _ in range(iters):
        C = torch.mm(A, B)
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    
    # FLOPs for matmul: 2*M*N*K (multiply + accumulate)
    flops_per_iter = 2 * M * N * K
    total_flops = flops_per_iter * iters
    tflops = total_flops / elapsed / 1e12
    
    print(f"Matrix size: {M}×{K} @ {K}×{N} ({dtype})")
    print(f"Time: {elapsed/iters*1000:.2f} ms/iter")
    print(f"Throughput: {tflops:.1f} TFLOPS")
    return tflops

# Run benchmarks at different sizes
print("=" * 60)
print("GPU TFLOPS BENCHMARK")
print("=" * 60)
for size in [1024, 2048, 4096, 8192]:
    benchmark_matmul(M=size, N=size, K=size)
    print()

# FP32 comparison
print("\n--- FP32 ---")
benchmark_matmul(M=4096, N=4096, K=4096, dtype=torch.float32)
```

### Experiment 4.3 — Memory Bandwidth Test

```python
import torch
import time

def benchmark_bandwidth(size_gb=1.0, dtype=torch.float16, iters=50):
    """Measure effective memory bandwidth with copy operations."""
    device = torch.device('cuda')
    num_elements = int(size_gb * 1024**3 / torch.tensor([], dtype=dtype).element_size())
    
    src = torch.randn(num_elements, dtype=dtype, device=device)
    dst = torch.empty_like(src)
    
    # Warmup
    for _ in range(5):
        dst.copy_(src)
    torch.cuda.synchronize()
    
    start = time.perf_counter()
    for _ in range(iters):
        dst.copy_(src)
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    
    bytes_per_iter = 2 * src.nelement() * src.element_size()  # read + write
    bandwidth_gbs = (bytes_per_iter * iters) / elapsed / 1e9
    
    print(f"Transfer size: {size_gb:.1f} GB ({dtype})")
    print(f"Effective bandwidth: {bandwidth_gbs:.0f} GB/s")
    print(f"Theoretical max (4090): 1008 GB/s")
    print(f"Efficiency: {bandwidth_gbs/1008*100:.1f}%")
    return bandwidth_gbs

benchmark_bandwidth()
```

### Experiment 4.4 — Multi-GPU Communication (NCCL)

```python
import torch
import torch.distributed as dist
import os

def test_nccl():
    """Test NCCL all-reduce between GPUs. Run with: torchrun --nproc_per_node=2 script.py"""
    dist.init_process_group(backend='nccl')
    rank = dist.get_rank()
    world_size = dist.get_world_size()
    device = torch.device(f'cuda:{rank}')
    torch.cuda.set_device(device)
    
    # Each GPU creates a tensor with its rank value
    tensor = torch.tensor([rank + 1.0], device=device)
    print(f"[Rank {rank}] Before all-reduce: {tensor.item()}")
    
    # All-reduce: sum across all GPUs
    dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
    print(f"[Rank {rank}] After all-reduce: {tensor.item()}")
    # Expected: 1 + 2 = 3 for 2 GPUs
    
    # Bandwidth test
    import time
    size = 256 * 1024 * 1024  # 256M elements = 512MB in FP16
    data = torch.randn(size, dtype=torch.float16, device=device)
    
    # Warmup
    for _ in range(5):
        dist.all_reduce(data)
    torch.cuda.synchronize()
    
    start = time.perf_counter()
    for _ in range(20):
        dist.all_reduce(data)
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    
    # All-reduce transfers 2*(N-1)/N * data_size in ring algorithm
    bytes_transferred = 2 * (world_size - 1) / world_size * data.nelement() * 2 * 20
    bus_bandwidth = bytes_transferred / elapsed / 1e9
    
    if rank == 0:
        print(f"\nNCCL All-Reduce Bandwidth: {bus_bandwidth:.1f} GB/s")
        print(f"(PCIe 4.0 x16 theoretical: 32 GB/s per direction)")
    
    dist.destroy_process_group()

if __name__ == '__main__':
    test_nccl()
```

### Experiment 4.5 — HuggingFace Accelerate Configuration

```python
# accelerate config generates ~/.cache/huggingface/accelerate/default_config.yaml
# Here's what a multi-GPU config looks like:

ACCELERATE_CONFIG = """
compute_environment: LOCAL_MACHINE
distributed_type: MULTI_GPU
downcast_bf16: 'no'
gpu_ids: all
machine_rank: 0
main_training_port: 29500
mixed_precision: bf16
num_machines: 1
num_processes: 2
rdzv_backend: static
same_network: true
tpu_env: []
tpu_use_cluster: false
tpu_use_sudo: false
use_cpu: false
"""

# Usage in training script:
from accelerate import Accelerator

accelerator = Accelerator(mixed_precision="bf16")
model = accelerator.prepare(model)
optimizer = accelerator.prepare(optimizer)
dataloader = accelerator.prepare(dataloader)

# Training loop works identically to single-GPU
for batch in dataloader:
    outputs = model(**batch)
    loss = outputs.loss
    accelerator.backward(loss)
    optimizer.step()
    optimizer.zero_grad()
```

### Experiment 4.6 — Memory Profiling

```python
import torch
from contextlib import contextmanager

@contextmanager
def track_memory(label=""):
    """Context manager to track GPU memory delta."""
    torch.cuda.synchronize()
    torch.cuda.reset_peak_memory_stats()
    mem_before = torch.cuda.memory_allocated()
    yield
    torch.cuda.synchronize()
    mem_after = torch.cuda.memory_allocated()
    peak = torch.cuda.max_memory_allocated()
    print(f"[{label}]")
    print(f"  Allocated: {(mem_after - mem_before) / 1024**2:.1f} MB")
    print(f"  Peak: {peak / 1024**2:.1f} MB")

# Example: measure model loading
from transformers import AutoModelForCausalLM, AutoTokenizer

with track_memory("Load Llama-3-8B in 4-bit"):
    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Meta-Llama-3-8B",
        load_in_4bit=True,
        device_map="auto",
    )
# Expected: ~4.5 GB for 8B params in 4-bit quantization
```

---

## 📈 5. Expected Results & Evaluation

### Benchmark Targets (RTX 4090)

| Metric | Expected | Concern If Below |
|--------|----------|-----------------|
| FP16 matmul (4096³) | 280-330 TFLOPS | < 200 → driver/thermal issue |
| FP32 matmul (4096³) | 70-82 TFLOPS | < 50 → check power limit |
| Memory bandwidth | 850-950 GB/s | < 700 → PCIe bottleneck |
| NCCL all-reduce (2 GPU) | 20-28 GB/s | < 10 → check PCIe lanes |

### Validation Checklist

- [ ] `torch.cuda.is_available()` returns `True`
- [ ] `torch.cuda.device_count()` matches physical GPUs
- [ ] FP16 TFLOPS within 85% of theoretical peak
- [ ] Memory bandwidth within 85% of spec
- [ ] NCCL all-reduce completes without timeout
- [ ] `accelerate` config validated with `accelerate test`

---

## ⚠️ 6. Gotchas & Debugging

### OOM (Out of Memory) Strategies

```python
# 1. Reduce batch size (most common fix)
# 2. Enable gradient checkpointing
model.gradient_checkpointing_enable()

# 3. Use mixed precision
with torch.autocast('cuda', dtype=torch.bfloat16):
    output = model(input_ids)

# 4. Clear cache between experiments
torch.cuda.empty_cache()
import gc; gc.collect()

# 5. Use memory-efficient attention
# pip install flash-attn
model = AutoModelForCausalLM.from_pretrained(
    model_name, attn_implementation="flash_attention_2"
)
```

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `CUDA out of memory` | Batch too large or memory leak | Reduce batch, check for tensor accumulation |
| `NCCL timeout` | Firewall or wrong NCCL version | Set `NCCL_SOCKET_IFNAME=eth0`, rebuild |
| `RuntimeError: CUDA error: device-side assert` | Index out of bounds in kernel | Run with `CUDA_LAUNCH_BLOCKING=1` for stack trace |
| Low TFLOPS | Power throttling | Check `nvidia-smi -q -d PERFORMANCE`, set power limit |
| `torch.cuda.is_available()` False | Wrong PyTorch build | Reinstall with correct CUDA version |

### Power & Thermal Management

```bash
# Check current power draw and limits
nvidia-smi -q -d POWER

# Set power limit (requires root)
sudo nvidia-smi -pl 450  # RTX 4090 max TDP

# Monitor temperature
watch -n 1 nvidia-smi --query-gpu=temperature.gpu,power.draw,clocks.sm --format=csv
```

---

## 🔬 7. Variations & Extensions

1. **DeepSpeed ZeRO-3 Setup:** Configure DeepSpeed for training models larger than single-GPU VRAM. Shard optimizer states, gradients, AND parameters across GPUs.

2. **CUDA Graphs:** Capture and replay GPU operations to eliminate CPU launch overhead. Critical for inference serving with small batch sizes.

3. **Custom CUDA Kernels with Triton:** Write fused kernels in Python using OpenAI's Triton compiler. Example: fused attention + dropout + residual.

4. **NVLink vs PCIe Benchmarking:** If you have NVLink (A100/H100), compare inter-GPU bandwidth: NVLink delivers 600 GB/s vs PCIe 4.0's 32 GB/s.

5. **Docker + NVIDIA Container Toolkit:** Containerize your environment for reproducibility:
   ```bash
   docker run --gpus all -it nvcr.io/nvidia/pytorch:24.04-py3
   ```

---

## 🔗 8. Cross-links & Further Reading

### Internal Cross-links
- CUDA programming model: [08.15 - GPU Computing & CUDA Foundations](08.15---GPU-Computing-&-CUDA-Foundations)
- Distributed training patterns: [08.16 - Distributed Systems & Multi-GPU Training](08.16---Distributed-Systems-&-Multi-GPU-Training)
- Transformer memory requirements: [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs)
- Next experiment: [24.2 - Image Generation Experiments - SDXL, ControlNet & LoRA](24.2---Image-Generation-Experiments---SDXL,-ControlNet-&-LoRA)

### External References
- **NVIDIA CUDA Toolkit Documentation** — [docs.nvidia.com/cuda](https://docs.nvidia.com/cuda/)
- **PyTorch CUDA Semantics** — [pytorch.org/docs/stable/notes/cuda.html](https://pytorch.org/docs/stable/notes/cuda.html)
- **HuggingFace Accelerate** — [huggingface.co/docs/accelerate](https://huggingface.co/docs/accelerate)
- **DeepSpeed** — [deepspeed.ai](https://www.deepspeed.ai/)
- **nvitop** — Real-time GPU monitoring — [github.com/XuehaiPan/nvitop](https://github.com/XuehaiPan/nvitop)
- **FlashAttention-2** — [github.com/Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention)



---

## 🧠 9. Extended Experiments & Variations

### Experiment 9.1 — Multi-GPU NVLink Topology Benchmarks

Measure actual inter-GPU bandwidth under different topologies (PCIe vs NVLink) and communication patterns (all-reduce, all-gather, reduce-scatter). This reveals whether your multi-GPU setup is bottlenecked by interconnect.

```python
import torch
import torch.distributed as dist
import os
import time
import json
from dataclasses import dataclass

@dataclass
class BandwidthResult:
    operation: str
    size_mb: float
    time_ms: float
    bandwidth_gbps: float
    
def benchmark_nccl_operation(op_name, tensor_size_mb, num_iters=100, warmup=10):
    """Benchmark a single NCCL collective operation."""
    rank = dist.get_rank()
    world_size = dist.get_world_size()
    device = torch.device(f"cuda:{rank}")
    
    # Allocate tensor
    num_elements = int(tensor_size_mb * 1024 * 1024 / 4)  # float32
    tensor = torch.randn(num_elements, device=device)
    
    # Warmup
    for _ in range(warmup):
        if op_name == "all_reduce":
            dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
        elif op_name == "all_gather":
            output = [torch.zeros_like(tensor) for _ in range(world_size)]
            dist.all_gather(output, tensor)
        elif op_name == "reduce_scatter":
            chunk_size = num_elements // world_size
            input_list = [torch.randn(chunk_size, device=device) for _ in range(world_size)]
            output = torch.zeros(chunk_size, device=device)
            dist.reduce_scatter(output, input_list)
        elif op_name == "broadcast":
            dist.broadcast(tensor, src=0)
    
    torch.cuda.synchronize()
    
    # Timed iterations
    start = time.perf_counter()
    for _ in range(num_iters):
        if op_name == "all_reduce":
            dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
        elif op_name == "all_gather":
            output = [torch.zeros_like(tensor) for _ in range(world_size)]
            dist.all_gather(output, tensor)
        elif op_name == "reduce_scatter":
            chunk_size = num_elements // world_size
            input_list = [torch.randn(chunk_size, device=device) for _ in range(world_size)]
            output = torch.zeros(chunk_size, device=device)
            dist.reduce_scatter(output, input_list)
        elif op_name == "broadcast":
            dist.broadcast(tensor, src=0)
    
    torch.cuda.synchronize()
    elapsed_ms = (time.perf_counter() - start) * 1000 / num_iters
    
    # Bandwidth calculation (algorithm bandwidth)
    # all_reduce: 2 * (n-1)/n * size (ring algorithm)
    # all_gather: (n-1)/n * size
    # reduce_scatter: (n-1)/n * size
    n = world_size
    if op_name == "all_reduce":
        algo_bytes = 2 * (n - 1) / n * tensor_size_mb * 1024 * 1024
    elif op_name in ("all_gather", "reduce_scatter"):
        algo_bytes = (n - 1) / n * tensor_size_mb * 1024 * 1024
    else:
        algo_bytes = tensor_size_mb * 1024 * 1024
    
    bandwidth_gbps = (algo_bytes / (elapsed_ms / 1000)) / 1e9
    
    return BandwidthResult(
        operation=op_name,
        size_mb=tensor_size_mb,
        time_ms=elapsed_ms,
        bandwidth_gbps=bandwidth_gbps,
    )

def run_full_benchmark():
    """Run complete NCCL benchmark suite."""
    dist.init_process_group(backend="nccl")
    rank = dist.get_rank()
    torch.cuda.set_device(rank)
    
    sizes_mb = [1, 4, 16, 64, 256, 512, 1024]
    operations = ["all_reduce", "all_gather", "reduce_scatter", "broadcast"]
    
    results = []
    for op in operations:
        for size in sizes_mb:
            result = benchmark_nccl_operation(op, size)
            results.append(result)
            if rank == 0:
                print(f"{op:15s} | {size:6.0f} MB | {result.time_ms:8.2f} ms | {result.bandwidth_gbps:6.1f} GB/s")
    
    if rank == 0:
        # Save results
        with open("nccl_benchmark_results.json", "w") as f:
            json.dump([vars(r) for r in results], f, indent=2)
        
        # Print topology info
        print("\n=== GPU Topology ===")
        os.system("nvidia-smi topo -m")
    
    dist.destroy_process_group()

if __name__ == "__main__":
    run_full_benchmark()
```

```bash
# Launch with torchrun (2 GPUs)
torchrun --nproc_per_node=2 nccl_benchmark.py

# Launch with 4 GPUs
torchrun --nproc_per_node=4 nccl_benchmark.py
```

**Expected output:**

| Topology | all_reduce 256MB | all_reduce 1GB | Peak BW |
|----------|-----------------|----------------|---------|
| 2× 4090 PCIe 4.0 x16 | ~25 GB/s | ~28 GB/s | ~30 GB/s |
| 2× A100 NVLink | ~250 GB/s | ~280 GB/s | ~300 GB/s |
| 2× H100 NVLink | ~450 GB/s | ~500 GB/s | ~600 GB/s |
| 4× 4090 PCIe (via switch) | ~18 GB/s | ~22 GB/s | ~25 GB/s |

**Gotchas:**
- PCIe bandwidth is shared with CPU↔GPU transfers; running data loading concurrently halves effective NCCL bandwidth.
- NVLink bandwidth is bidirectional — 600 GB/s means 300 GB/s in each direction simultaneously.
- `nvidia-smi topo -m` shows `NV#` for NVLink connections, `PIX`/`PHB`/`SYS` for PCIe paths.
- If you see `SYS` (cross-socket), bandwidth drops ~40% vs `PIX` (same PCIe switch).

### Experiment 9.2 — vLLM vs TensorRT-LLM vs llama.cpp Inference Comparison

Benchmark the three dominant inference engines on identical hardware with the same model, measuring throughput (tokens/sec), latency (time-to-first-token, inter-token latency), and memory efficiency.

```python
import subprocess
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

@dataclass
class InferenceResult:
    engine: str
    model: str
    prompt_tokens: int
    output_tokens: int
    ttft_ms: float          # time to first token
    itl_ms: float           # inter-token latency
    throughput_tps: float   # tokens per second (generation)
    vram_gb: float
    
def benchmark_vllm(model_name="meta-llama/Meta-Llama-3.1-8B-Instruct",
                   num_prompts=50, max_tokens=256):
    """Benchmark vLLM server (must be running)."""
    # Start server: python -m vllm.entrypoints.openai.api_server \
    #   --model meta-llama/Meta-Llama-3.1-8B-Instruct --dtype float16
    
    url = "http://localhost:8000/v1/completions"
    prompt = "Explain the theory of general relativity in detail, covering spacetime curvature, "
    
    results = []
    for i in range(num_prompts):
        start = time.perf_counter()
        response = requests.post(url, json={
            "model": model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "stream": False,
        })
        elapsed = time.perf_counter() - start
        
        data = response.json()
        output_tokens = data["usage"]["completion_tokens"]
        results.append({
            "elapsed_s": elapsed,
            "output_tokens": output_tokens,
            "tps": output_tokens / elapsed,
        })
    
    avg_tps = sum(r["tps"] for r in results) / len(results)
    avg_latency = sum(r["elapsed_s"] for r in results) / len(results) * 1000
    
    return InferenceResult(
        engine="vLLM",
        model=model_name,
        prompt_tokens=len(prompt.split()) * 1.3,  # approximate
        output_tokens=max_tokens,
        ttft_ms=avg_latency * 0.1,  # approximate TTFT
        itl_ms=avg_latency / max_tokens,
        throughput_tps=avg_tps,
        vram_gb=16.5,  # Llama-3.1-8B FP16
    )

def benchmark_llamacpp(model_path, num_prompts=50, max_tokens=256):
    """Benchmark llama.cpp server."""
    # Start: ./llama-server -m model.gguf -ngl 99 -c 4096 --port 8080
    
    url = "http://localhost:8080/completion"
    prompt = "Explain the theory of general relativity in detail, covering spacetime curvature, "
    
    results = []
    for i in range(num_prompts):
        start = time.perf_counter()
        response = requests.post(url, json={
            "prompt": prompt,
            "n_predict": max_tokens,
            "temperature": 0.7,
        })
        elapsed = time.perf_counter() - start
        
        data = response.json()
        tokens_predicted = data.get("tokens_predicted", max_tokens)
        results.append({
            "elapsed_s": elapsed,
            "output_tokens": tokens_predicted,
            "tps": tokens_predicted / elapsed,
        })
    
    avg_tps = sum(r["tps"] for r in results) / len(results)
    return avg_tps

# Comparison table generator
def generate_comparison_report():
    """Generate markdown comparison table."""
    # These are representative results for RTX 4090
    results = {
        "vLLM (FP16)": {"tps": 95, "ttft_ms": 45, "vram_gb": 16.5, "batch_tps": 2400},
        "vLLM (AWQ 4-bit)": {"tps": 130, "ttft_ms": 35, "vram_gb": 24.5, "batch_tps": 3200},
        "TensorRT-LLM (FP16)": {"tps": 110, "ttft_ms": 38, "vram_gb": 17.0, "batch_tps": 2800},
        "TensorRT-LLM (INT8)": {"tps": 145, "ttft_ms": 30, "vram_gb": 9.0, "batch_tps": 3500},
        "llama.cpp (Q4_K_M)": {"tps": 85, "ttft_ms": 55, "vram_gb": 24.0, "batch_tps": 85},
        "llama.cpp (Q8_0)": {"tps": 65, "ttft_ms": 60, "vram_gb": 8.5, "batch_tps": 65},
    }
    
    print("| Engine | Tokens/s (single) | TTFT (ms) | VRAM | Batch Throughput |")
    print("|--------|-------------------|-----------|------|-----------------|")
    for engine, metrics in results.items():
        print(f"| {engine} | {metrics['tps']} | {metrics['ttft_ms']} | "
              f"{metrics['vram_gb']:.1f} GB | {metrics['batch_tps']} t/s |")

generate_comparison_report()
```

**Expected output (RTX 4090, Llama-3.1-8B):**

| Engine | Tokens/s (single) | TTFT (ms) | VRAM | Batch Throughput |
|--------|-------------------|-----------|------|-----------------|
| vLLM (FP16) | 95 | 45 | 16.5 GB | 2400 t/s |
| vLLM (AWQ 4-bit) | 130 | 35 | 24.5 GB | 3200 t/s |
| TensorRT-LLM (FP16) | 110 | 38 | 17.0 GB | 2800 t/s |
| TensorRT-LLM (INT8) | 145 | 30 | 9.0 GB | 3500 t/s |
| llama.cpp (Q4_K_M) | 85 | 55 | 24.0 GB | 85 t/s |
| llama.cpp (Q8_0) | 65 | 60 | 8.5 GB | 65 t/s |

**Key insights:**
- **vLLM** excels at batched serving (PagedAttention enables high batch throughput).
- **TensorRT-LLM** wins on single-stream latency due to kernel fusion and custom CUDA kernels.
- **llama.cpp** has no batching but lowest VRAM and simplest deployment (single binary).
- Quantization (4-bit) gives 1.4-1.5× speedup with minimal quality loss on most benchmarks.

**Gotchas:**
- vLLM requires model fits in GPU memory in chosen precision (no CPU offload).
- TensorRT-LLM requires engine compilation per GPU architecture — not portable.
- llama.cpp GGUF quantization quality varies: Q4_K_M > Q4_0 > Q4_1 for most models.
- Batch throughput numbers assume continuous batching with 32+ concurrent requests.


### Experiment 9.3 — Quantization Overhead: FP16 vs BF16 vs FP8 vs INT8 vs INT4

Systematically measure the quality-speed-memory tradeoff across all major quantization formats for inference. This experiment reveals the Pareto frontier for your specific hardware.

```python
import torch
import time
import json
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from datasets import load_dataset
import numpy as np

def measure_perplexity(model, tokenizer, dataset_texts, max_length=512, stride=256):
    """Compute perplexity on a text dataset."""
    model.eval()
    nlls = []
    
    for text in dataset_texts[:100]:  # 100 samples
        encodings = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_length)
        input_ids = encodings.input_ids.to(model.device)
        
        with torch.no_grad():
            outputs = model(input_ids, labels=input_ids)
            nlls.append(outputs.loss.item())
    
    return np.exp(np.mean(nlls))

def benchmark_quantization(model_name="meta-llama/Meta-Llama-3.1-8B"):
    """Benchmark model across quantization levels."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Load evaluation dataset
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="test")
    texts = [t for t in dataset["text"] if len(t) > 100][:100]
    
    configs = {
        "FP16": {"torch_dtype": torch.float16},
        "BF16": {"torch_dtype": torch.bfloat16},
        "INT8 (bitsandbytes)": {"quantization_config": BitsAndBytesConfig(load_in_8bit=True)},
        "INT4 (NF4)": {"quantization_config": BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )},
    }
    
    results = {}
    for name, kwargs in configs.items():
        print(f"\n{'='*60}")
        print(f"Loading {name}...")
        
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name, device_map="auto", **kwargs
        )
        
        # Memory measurement
        vram_gb = torch.cuda.max_memory_allocated() / 1024**3
        
        # Perplexity
        ppl = measure_perplexity(model, tokenizer, texts)
        
        # Throughput (tokens/sec for generation)
        prompt = tokenizer("The meaning of life is", return_tensors="pt").to(model.device)
        
        torch.cuda.synchronize()
        start = time.perf_counter()
        num_runs = 20
        for _ in range(num_runs):
            with torch.no_grad():
                _ = model.generate(**prompt, max_new_tokens=128, do_sample=False)
        torch.cuda.synchronize()
        elapsed = time.perf_counter() - start
        
        tokens_per_sec = (128 * num_runs) / elapsed
        
        results[name] = {
            "vram_gb": round(vram_gb, 2),
            "perplexity": round(ppl, 3),
            "tokens_per_sec": round(tokens_per_sec, 1),
            "quality_retention": None,  # filled below
        }
        
        del model
        torch.cuda.empty_cache()
    
    # Compute quality retention relative to FP16
    fp16_ppl = results["FP16"]["perplexity"]
    for name in results:
        # Lower perplexity = better; retention = how close to FP16
        results[name]["quality_retention"] = round(fp16_ppl / results[name]["perplexity"] * 100, 1)
    
    # Print results table
    print("\n" + "="*80)
    print(f"{'Format':<25} {'VRAM (GB)':<12} {'PPL':<10} {'Tok/s':<10} {'Quality %':<10}")
    print("-"*80)
    for name, r in results.items():
        print(f"{name:<25} {r['vram_gb']:<12} {r['perplexity']:<10} "
              f"{r['tokens_per_sec']:<10} {r['quality_retention']:<10}")
    
    return results

if __name__ == "__main__":
    results = benchmark_quantization()
    with open("quantization_benchmark.json", "w") as f:
        json.dump(results, f, indent=2)
```

**Expected output (Llama-3.1-8B on RTX 4090):**

| Format | VRAM | Perplexity | Tokens/s | Quality Retention |
|--------|------|-----------|----------|-------------------|
| FP16 | 16.2 GB | 6.14 | 65 | 100.0% |
| BF16 | 16.2 GB | 6.15 | 68 | 99.8% |
| INT8 (bnb) | 8.8 GB | 6.18 | 55 | 99.4% |
| INT4 (NF4) | 4.8 GB | 6.42 | 72 | 95.6% |
| GPTQ 4-bit | 4.5 GB | 6.35 | 95 | 96.7% |
| AWQ 4-bit | 4.5 GB | 6.32 | 105 | 97.1% |

**Gotchas:**
- BF16 is slightly faster than FP16 on Ampere+ GPUs (native BF16 tensor cores) but has less precision in the mantissa (8-bit exponent, 7-bit mantissa vs FP16's 5/10).
- INT8 via bitsandbytes is actually *slower* than FP16 due to dequantization overhead — it's a memory saver, not a speed booster.
- AWQ and GPTQ are pre-quantized formats that use optimized CUDA kernels (exllama, marlin) — much faster than on-the-fly bitsandbytes quantization.
- FP8 (available on H100/4090 Ada) requires `transformer-engine` library and shows ~1.5× speedup over FP16 with <0.1% quality loss.

### Experiment 9.4 — Memory Bandwidth Saturation Analysis

LLM inference is memory-bandwidth-bound (not compute-bound) for single-batch generation. This experiment proves it by measuring the arithmetic intensity and comparing against the roofline model.

```python
import torch
import time
import numpy as np

def roofline_analysis(model_params_B, batch_size, seq_len, dtype_bytes=2):
    """
    Compute arithmetic intensity and determine if workload is
    compute-bound or memory-bound using the roofline model.
    
    RTX 4090 specs:
      - FP16 compute: 330 TFLOPS (with sparsity) / 165 TFLOPS (dense)
      - Memory bandwidth: 1008 GB/s
      - Arithmetic intensity crossover: 165 TFLOPS / 1008 GB/s ≈ 164 FLOP/byte
    """
    # For autoregressive generation (single token, batch_size=1):
    # Each layer: read all weights once, do 2*params FLOPs
    # Arithmetic intensity = FLOPs / Bytes_read
    
    total_params = model_params_B * 1e9
    bytes_read = total_params * dtype_bytes  # read all weights
    flops = 2 * total_params * batch_size    # 2 FLOPs per param per token
    
    arithmetic_intensity = flops / bytes_read  # FLOP/byte
    
    # RTX 4090 roofline
    peak_compute_tflops = 165  # dense FP16
    peak_bandwidth_gbs = 1008
    crossover_intensity = (peak_compute_tflops * 1e12) / (peak_bandwidth_gbs * 1e9)
    
    is_memory_bound = arithmetic_intensity < crossover_intensity
    
    # Achievable performance
    if is_memory_bound:
        achievable_tflops = arithmetic_intensity * peak_bandwidth_gbs * 1e9 / 1e12
    else:
        achievable_tflops = peak_compute_tflops
    
    # Theoretical max tokens/sec (memory-bound case)
    time_per_token_s = bytes_read / (peak_bandwidth_gbs * 1e9)
    max_tokens_per_sec = 1.0 / time_per_token_s
    
    return {
        "arithmetic_intensity": arithmetic_intensity,
        "crossover_intensity": crossover_intensity,
        "is_memory_bound": is_memory_bound,
        "achievable_tflops": achievable_tflops,
        "theoretical_max_tps": max_tokens_per_sec,
        "bytes_per_token": bytes_read,
        "time_per_token_ms": time_per_token_s * 1000,
    }

# Analyze different models on RTX 4090
models = [
    ("Llama-3.1-8B (FP16)", 8.0, 2),
    ("Llama-3.1-8B (INT4)", 8.0, 0.5),
    ("Llama-3.1-70B (INT4)", 70.0, 0.5),
    ("Mistral-7B (FP16)", 7.2, 2),
    ("Phi-3-mini (FP16)", 3.8, 2),
    ("Qwen2.5-72B (INT4)", 72.0, 0.5),
]

print(f"{'Model':<28} {'AI (F/B)':<10} {'Bound':<8} {'Max t/s':<10} {'ms/tok':<8}")
print("-" * 72)
for name, params_B, dtype_bytes in models:
    result = roofline_analysis(params_B, batch_size=1, seq_len=1, dtype_bytes=dtype_bytes)
    bound = "MEM" if result["is_memory_bound"] else "COMPUTE"
    print(f"{name:<28} {result['arithmetic_intensity']:<10.1f} {bound:<8} "
          f"{result['theoretical_max_tps']:<10.0f} {result['time_per_token_ms']:<8.1f}")

print(f"\nRTX 4090 crossover: {roofline_analysis(8, 1, 1)['crossover_intensity']:.0f} FLOP/byte")
print("Batch size needed to become compute-bound: ~164 (for FP16 models)")
```

**Expected output:**

| Model | Arith. Intensity | Bound | Max Tokens/s | ms/token |
|-------|-----------------|-------|-------------|----------|
| Llama-3.1-8B (FP16) | 1.0 | MEM | 63 | 15.9 |
| Llama-3.1-8B (INT4) | 4.0 | MEM | 252 | 4.0 |
| Llama-3.1-70B (INT4) | 4.0 | MEM | 29 | 34.7 |
| Mistral-7B (FP16) | 1.0 | MEM | 70 | 14.3 |
| Phi-3-mini (FP16) | 1.0 | MEM | 133 | 7.5 |

**Key insight:** Single-batch LLM inference is *always* memory-bandwidth-bound. The arithmetic intensity is 1.0 FLOP/byte for FP16 (far below the 164 FLOP/byte crossover). This is why:
- Quantization helps speed (fewer bytes to read per token)
- Batching helps utilization (more FLOPs per byte read)
- Faster memory (HBM3 on H100: 3.35 TB/s) directly translates to faster inference

**Gotchas:**
- Real throughput is 60-80% of theoretical max due to kernel launch overhead, KV cache reads, and non-matmul operations.
- Prefill (processing the prompt) IS compute-bound because batch_size = seq_len tokens processed in parallel.
- The roofline model assumes perfect memory access patterns; cache misses reduce effective bandwidth.

### Experiment 9.5 — PCIe Bandwidth Budget for Multi-GPU Inference

When a model is split across GPUs via tensor parallelism, activations must be transferred between GPUs at every layer. This experiment quantifies the PCIe tax and determines when model parallelism becomes worthwhile.

```python
import torch
import time

def measure_pcie_bandwidth(src_device=0, dst_device=1, sizes_mb=None):
    """Measure actual GPU-to-GPU transfer bandwidth over PCIe."""
    if sizes_mb is None:
        sizes_mb = [1, 4, 16, 64, 128, 256, 512, 1024]
    
    results = []
    for size_mb in sizes_mb:
        num_elements = int(size_mb * 1024 * 1024 / 2)  # float16
        src_tensor = torch.randn(num_elements, dtype=torch.float16, device=f"cuda:{src_device}")
        
        # Warmup
        for _ in range(5):
            dst_tensor = src_tensor.to(f"cuda:{dst_device}")
        
        torch.cuda.synchronize()
        
        # Timed transfer
        num_iters = 50
        start = time.perf_counter()
        for _ in range(num_iters):
            dst_tensor = src_tensor.to(f"cuda:{dst_device}")
        torch.cuda.synchronize()
        elapsed = time.perf_counter() - start
        
        time_per_transfer_ms = elapsed / num_iters * 1000
        bandwidth_gbs = (size_mb / 1024) / (time_per_transfer_ms / 1000)
        
        results.append({
            "size_mb": size_mb,
            "time_ms": round(time_per_transfer_ms, 3),
            "bandwidth_gbs": round(bandwidth_gbs, 2),
        })
        
        del src_tensor, dst_tensor
        torch.cuda.empty_cache()
    
    return results

def tensor_parallel_overhead(model_params_B, hidden_dim, num_layers, 
                             num_gpus, pcie_bw_gbs=25):
    """
    Calculate tensor parallelism communication overhead.
    
    In tensor parallelism, each layer requires 2 all-reduce operations
    (one after attention, one after FFN). Each all-reduce transfers
    batch_size × seq_len × hidden_dim × dtype_bytes.
    """
    # Per all-reduce: transfer hidden activations
    # For ring all-reduce: 2*(n-1)/n * message_size
    batch_size = 1
    seq_len = 1  # per-token during generation
    dtype_bytes = 2  # FP16
    
    message_size_bytes = batch_size * seq_len * hidden_dim * dtype_bytes
    # Ring all-reduce factor
    allreduce_bytes = 2 * (num_gpus - 1) / num_gpus * message_size_bytes
    
    # 2 all-reduces per layer (attention + FFN)
    total_comm_bytes = 2 * num_layers * allreduce_bytes
    
    # Communication time
    comm_time_ms = (total_comm_bytes / (pcie_bw_gbs * 1e9)) * 1000
    
    # Compute time (memory-bound: read params/num_gpus)
    params_per_gpu = model_params_B * 1e9 / num_gpus
    mem_bw_gbs = 1008  # RTX 4090
    compute_time_ms = (params_per_gpu * dtype_bytes / (mem_bw_gbs * 1e9)) * 1000
    
    overhead_pct = comm_time_ms / (compute_time_ms + comm_time_ms) * 100
    
    return {
        "compute_time_ms": round(compute_time_ms, 2),
        "comm_time_ms": round(comm_time_ms, 4),
        "overhead_pct": round(overhead_pct, 2),
        "effective_speedup": round((compute_time_ms + comm_time_ms) / 
                                   (model_params_B * 1e9 * dtype_bytes / (mem_bw_gbs * 1e9) * 1000), 2),
    }

# Analyze overhead for different configurations
configs = [
    ("Llama-3.1-70B, 2 GPU PCIe", 70, 8192, 80, 2, 25),
    ("Llama-3.1-70B, 4 GPU PCIe", 70, 8192, 80, 4, 25),
    ("Llama-3.1-70B, 2 GPU NVLink", 70, 8192, 80, 2, 300),
    ("Llama-3.1-8B, 2 GPU PCIe", 8, 4096, 32, 2, 25),
]

print(f"{'Config':<35} {'Compute':<12} {'Comm':<10} {'Overhead':<10} {'Speedup':<8}")
print("-" * 75)
for name, params, hidden, layers, gpus, bw in configs:
    r = tensor_parallel_overhead(params, hidden, layers, gpus, bw)
    print(f"{name:<35} {r['compute_time_ms']:<12} {r['comm_time_ms']:<10} "
          f"{r['overhead_pct']:<10}% {r['effective_speedup']:<8}×")
```

**Expected output:**

| Config | Compute (ms) | Comm (ms) | Overhead | Effective Speedup |
|--------|-------------|-----------|----------|-------------------|
| 70B, 2 GPU PCIe | 69.4 | 0.05 | 0.07% | 1.99× |
| 70B, 4 GPU PCIe | 34.7 | 0.07 | 0.20% | 3.96× |
| 70B, 2 GPU NVLink | 69.4 | 0.004 | 0.006% | 2.00× |
| 8B, 2 GPU PCIe | 7.9 | 0.03 | 0.33% | 1.99× |

**Key insight:** For single-token generation, tensor parallelism communication overhead is negligible (<1%) even over PCIe because the activation tensors are tiny (hidden_dim × dtype = 8192 × 2 = 16 KB per transfer). The real benefit is splitting model weights across GPUs to fit larger models. The overhead becomes significant only during prefill with long sequences (seq_len × hidden_dim can be megabytes).

**Gotchas:**
- Pipeline parallelism (splitting by layers) has *zero* communication during generation but introduces pipeline bubbles during prefill.
- PCIe latency (~5μs per transfer) dominates over bandwidth for small messages — this matters for pipeline parallelism with many micro-batches.
- With 4× GPUs on consumer motherboards, check that all slots are x16 electrical — many boards drop to x8 with 4 GPUs populated.


---

## 📘 10. Appendix: Production Considerations & Theory Bridges

### 10.1 PCIe Bandwidth Budgets for Inference Serving

In production inference serving, PCIe bandwidth becomes critical in three scenarios:

**Scenario 1: CPU↔GPU Data Transfer (Tokenization Pipeline)**

Tokenized input must travel from CPU to GPU. For a batch of 32 sequences at 2048 tokens each:
- Data size: 32 × 2048 × 4 bytes (int32 token IDs) = 256 KB
- PCIe 4.0 x16 bandwidth: 32 GB/s
- Transfer time: 256 KB / 32 GB/s = 8 μs (negligible)

**Scenario 2: KV-Cache Offloading**

When serving many concurrent users, KV-cache can exceed GPU memory. Offloading to CPU:
- KV-cache per token per layer: 2 × d_model × dtype_bytes = 2 × 4096 × 2 = 16 KB (Llama-8B)
- Full cache for 2048 tokens, 32 layers: 2048 × 32 × 16 KB = 1 GB
- Swapping 1 GB at 32 GB/s: 31 ms — this is the latency penalty per swap

**Scenario 3: Multi-GPU Tensor Parallelism (Prefill Phase)**

During prefill, the full sequence is processed in parallel:
- Activation size: batch × seq_len × hidden_dim × 2 bytes
- For batch=1, seq=4096, hidden=8192: 64 MB per all-reduce
- At 25 GB/s effective PCIe: 2.6 ms per all-reduce × 2 per layer × 80 layers = 410 ms overhead
- This is why NVLink matters for large-batch prefill

**Production bandwidth budget table (RTX 4090, PCIe 4.0 x16):**

| Transfer Type | Size | Time | Impact |
|--------------|------|------|--------|
| Token IDs (batch=32) | 256 KB | 8 μs | None |
| KV-cache swap (1 user) | 1 GB | 31 ms | High latency spike |
| TP all-reduce (generation) | 16 KB | 5 μs | Negligible |
| TP all-reduce (prefill, seq=4K) | 64 MB | 2.6 ms | Significant at scale |
| Model loading (8B FP16) | 16 GB | 500 ms | One-time startup |

**Optimization strategies:**
1. **Overlap communication with computation** — while GPU computes layer N, transfer layer N+1's activations.
2. **PagedAttention (vLLM)** — manages KV-cache like virtual memory pages, avoiding full swaps.
3. **Speculative decoding** — draft model generates candidates on one GPU while main model verifies, hiding latency.

### 10.2 Memory Bandwidth Math for Inference — Theory Bridge

> **Cross-reference:** [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs) §4 (Theorem 10.5.2) for attention complexity analysis.

The fundamental equation governing LLM inference speed on a single GPU:

$$
\text{Tokens/sec} = \frac{\text{Memory Bandwidth (bytes/sec)}}{\text{Model Size (bytes)}}
$$

**Derivation:** During autoregressive generation, each token requires reading the entire model's weights once (for the matrix multiplications in each layer). The computation (2 FLOPs per parameter) is trivial compared to the memory read.

**For RTX 4090 (1008 GB/s bandwidth):**

$$
\text{Llama-8B FP16: } \frac{1008 \text{ GB/s}}{16 \text{ GB}} = 63 \text{ tokens/sec (theoretical max)}
$$

$$
\text{Llama-8B INT4: } \frac{1008 \text{ GB/s}}{4 \text{ GB}} = 252 \text{ tokens/sec (theoretical max)}
$$

$$
\text{Llama-70B INT4: } \frac{1008 \text{ GB/s}}{35 \text{ GB}} = 29 \text{ tokens/sec (theoretical max)}
$$

**Why batching helps:** With batch size $B$, you read weights once but compute $B$ tokens:

$$
\text{Tokens/sec} = \frac{B \times \text{Memory Bandwidth}}{\text{Model Size} + B \times \text{KV-cache per token}}
$$

The system becomes compute-bound when:

$$
B > \frac{\text{Peak FLOPS}}{\text{Memory Bandwidth}} \times \frac{\text{bytes per param}}{2} = \frac{165 \times 10^{12}}{1008 \times 10^9} \times \frac{2}{2} = 164
$$

So batch size ~164 saturates the RTX 4090's compute for FP16 models. In practice, KV-cache memory limits batch size to 32-64 for 8B models on 24GB.

**Comparison across GPU generations:**

| GPU | Bandwidth | 8B FP16 (t/s) | 8B INT4 (t/s) | 70B INT4 (t/s) |
|-----|-----------|---------------|---------------|----------------|
| RTX 3090 | 936 GB/s | 59 | 234 | 27 |
| RTX 4090 | 1008 GB/s | 63 | 252 | 29 |
| A100 80GB | 2039 GB/s | 127 | 510 | 58 |
| H100 80GB | 3350 GB/s | 209 | 838 | 96 |

> **See also:** [24.1 - Local AI Infrastructure - CUDA, PyTorch & Multi-GPU Setup](24.1---Local-AI-Infrastructure---CUDA,-PyTorch-&-Multi-GPU-Setup) §9.4 for the roofline model experiment that validates these calculations empirically.

### 10.3 CUDA Memory Allocator Internals

Understanding PyTorch's CUDA memory allocator explains why `torch.cuda.memory_allocated()` and `nvidia-smi` show different numbers:

**PyTorch's caching allocator:**
1. First allocation: requests memory from CUDA driver (shows in `nvidia-smi`)
2. After `del tensor`: memory returns to PyTorch's free pool (still shows in `nvidia-smi`)
3. `torch.cuda.empty_cache()`: returns free pool to CUDA driver
4. New allocation: checks free pool first, only requests from driver if needed

**Memory fragmentation:** The allocator uses a best-fit strategy with block splitting. Over time, the free pool becomes fragmented — many small free blocks that can't satisfy a large allocation. This is why you get OOM even when `nvidia-smi` shows free memory.

**The `expandable_segments` fix (PyTorch 2.1+):**

```bash
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```

This uses CUDA virtual memory to create expandable allocations that can grow without fragmentation. Reduces OOM errors by 30-50% in long-running training jobs.

**Memory pool statistics:**

```python
# Detailed memory stats
stats = torch.cuda.memory_stats()
print(f"Active allocations: {stats['active.all.current']}")
print(f"Active memory: {stats['active_bytes.all.current'] / 1024**3:.2f} GB")
print(f"Reserved (cached): {stats['reserved_bytes.all.current'] / 1024**3:.2f} GB")
print(f"Num alloc retries: {stats['num_alloc_retries']}")  # fragmentation indicator
print(f"Num OOMs: {stats['num_ooms']}")
```

---
