---
title: "AI Experiments — Learning Path"
subject: "AI Experiments"
catalog: advanced
audience_tier: higher-education
chapter: "Chapter 1"
type: learning-path
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 05 — AI Experiments: Learning Path

> *"You don't learn to walk by following rules. You learn by doing, and by falling over."*
> — **Richard Branson**

---

## 🗺️ Recommended Progression

```
Week 1-2:  24.1 Infrastructure  ──→  Validate GPU, benchmark, multi-GPU
    │
    ▼
Week 3-4:  24.2 Image Gen       ──→  SDXL inference, LoRA training, ControlNet
    │
    ▼
Week 5-7:  24.3 LLM Fine-tuning ──→  QLoRA on Llama-3, DPO alignment
    │
    ▼
Week 8-9:  24.4 RAG Pipelines   ──→  Embeddings, Chroma, hybrid search
    │
    ▼
Week 10-11: 24.5 Agentic AI     ──→  ReAct loops, tool calling, multi-agent
    │
    ▼
Week 12:   24.6 Voice & Audio   ──→  Whisper, TTS, voice cloning
    │
    ▼
Week 13-14: 24.7 Multimodal     ──→  Vision-language, audio-text bridges
```

---

## ⏱️ Time Estimates Per Chapter

| Chapter | Reading | Hands-On | Total | Difficulty |
|---------|---------|----------|-------|-----------|
| 24.1 Infrastructure | 2h | 6h | 8h | ⭐⭐ |
| 24.2 Image Generation | 3h | 10h | 13h | ⭐⭐⭐ |
| 24.3 LLM Fine-tuning | 4h | 15h | 19h | ⭐⭐⭐⭐ |
| 24.4 RAG Pipelines | 3h | 8h | 11h | ⭐⭐⭐ |
| 24.5 Agentic AI | 3h | 10h | 13h | ⭐⭐⭐ |
| 24.6 Voice & Audio | 2h | 6h | 8h | ⭐⭐ |
| 24.7 Multimodal | 3h | 10h | 13h | ⭐⭐⭐⭐ |
| **Total** | **20h** | **65h** | **85h** | |

---

## 🏆 Milestones & Deliverables

### Milestone 1: Infrastructure Validated (End of Week 2)
- [ ] CUDA toolkit installed and verified
- [ ] PyTorch sees all GPUs, NCCL works
- [ ] Benchmark: measure TFLOPS on matmul, memory bandwidth
- [ ] `accelerate config` set up for multi-GPU

### Milestone 2: First Image LoRA (End of Week 4)
- [ ] Generated 512×512 images with SDXL pipeline
- [ ] Trained a style LoRA on 20+ images (< 30 min on 24GB)
- [ ] Applied ControlNet conditioning (depth, canny)
- [ ] Compared SDXL vs SDXL-Turbo vs Flux inference speed

### Milestone 3: Fine-tuned LLM (End of Week 7)
- [ ] QLoRA fine-tune of Llama-3-8B on custom dataset
- [ ] Evaluated perplexity, BLEU, human preference
- [ ] Ran DPO alignment on preference pairs
- [ ] Merged adapter weights and exported GGUF for local inference

### Milestone 4: Production RAG (End of Week 9)
- [ ] Chunked and embedded 1000+ documents
- [ ] Deployed Qdrant or Chroma with persistent storage
- [ ] Implemented hybrid search (dense + BM25)
- [ ] Measured retrieval precision@k and answer quality

### Milestone 5: Working Agent System (End of Week 11)
- [ ] Built ReAct agent with 3+ tools
- [ ] Implemented structured output with Pydantic
- [ ] Multi-agent orchestration with task delegation
- [ ] Evaluated on a benchmark task suite

### Milestone 6: Voice Pipeline (End of Week 12)
- [ ] Transcribed audio with Whisper (word-level timestamps)
- [ ] Generated speech with Bark/Coqui TTS
- [ ] Cloned a voice from 30s of reference audio
- [ ] Built end-to-end voice assistant prototype

### Milestone 7: Multimodal Integration (End of Week 14)
- [ ] Ran vision-language inference with LLaVA/Qwen2-VL
- [ ] Built image-to-text-to-speech pipeline
- [ ] Experimented with ImageBind cross-modal embeddings
- [ ] Evaluated on VQA benchmarks

---

## 🔄 Prerequisites Check

Before starting this track, ensure you have:

1. **Hardware:** NVIDIA GPU with ≥16GB VRAM (24GB recommended)
2. **Software:** Linux or WSL2, CUDA 12.x, conda/mamba
3. **Theory:** At minimum, skim [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs) and [23.6 - Generative Models - GANs & Diffusion](23.6---Generative-Models---GANs-&-Diffusion)
4. **Python:** Comfortable with PyTorch tensors, dataloaders, training loops
5. **Storage:** 500GB+ free disk for model weights and datasets

---

## 📖 Companion Theory (Track 10)

| Experiment Topic | Theory Chapter |
|---|---|
| GPU/CUDA | [08.15 - GPU Computing & CUDA Foundations](08.15---GPU-Computing-&-CUDA-Foundations) |
| Multi-GPU | [08.16 - Distributed Systems & Multi-GPU Training](08.16---Distributed-Systems-&-Multi-GPU-Training) |
| Transformers | [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs) |
| Diffusion | [23.6 - Generative Models - GANs & Diffusion](23.6---Generative-Models---GANs-&-Diffusion) |
| RLHF/DPO | [23.7 - Reinforcement Learning & RLHF](23.7---Reinforcement-Learning-&-RLHF) |
| CNNs/ViTs | [23.3 - Computer Vision - CNNs & ViTs](23.3---Computer-Vision---CNNs-&-ViTs) |
| Backprop | [23.2 - Deep Neural Networks - Backprop & Architecture](23.2---Deep-Neural-Networks---Backprop-&-Architecture) |

---

## Related Notes
- [24.1 - Local AI Infrastructure - CUDA, PyTorch & Multi-GPU Setup](24.1---Local-AI-Infrastructure---CUDA,-PyTorch-&-Multi-GPU-Setup) - Same AI Experiments folder
- [24.2 - Image Generation Experiments - SDXL, ControlNet & LoRA](24.2---Image-Generation-Experiments---SDXL,-ControlNet-&-LoRA) - Same AI Experiments folder
- [24.3 - LLM Fine-tuning - LoRA, QLoRA & Full Fine-tuning](24.3---LLM-Fine-tuning---LoRA,-QLoRA-&-Full-Fine-tuning) - Same AI Experiments folder
- [24.4 - RAG Pipelines - Embeddings, Vector DBs & Retrieval](24.4---RAG-Pipelines---Embeddings,-Vector-DBs-&-Retrieval) - Same AI Experiments folder
- [24.5 - Agentic AI - ReAct, Tool Calling & Multi-Agent Orchestration](24.5---Agentic-AI---ReAct,-Tool-Calling-&-Multi-Agent-Orchestration) - Same AI Experiments folder
