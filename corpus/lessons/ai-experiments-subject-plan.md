---
title: "AI Experiments — Subject Plan"
subject: "AI Experiments"
catalog: advanced
audience_tier: higher-education
chapter: "24"
type: subject-plan
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [09 - Learning Index](09---Learning-Index)*

# 24 — AI Experiments: Subject Plan

> *"The best way to understand deep learning is to code it from scratch."*
> — **Andrej Karpathy**

---

## 🎯 Track Mission

This track is **pure execution**. Theory lives in [Track 23 — AI & Machine Learning Systems](Subject_Plan). Here we:

- Set up real GPU infrastructure and benchmark it
- Run image generation experiments with SDXL, ControlNet, LoRA
- Fine-tune LLMs with LoRA, QLoRA, and full fine-tuning
- Build RAG pipelines with vector databases
- Orchestrate multi-agent systems with tool calling
- Clone voices and run ASR/TTS pipelines
- Bridge modalities: vision-language, audio-text

**Target hardware:** Single workstation with 1–2× RTX 4090 (24GB VRAM each).

---

## 📚 Chapter Index

| # | Chapter | Focus | Key Tools |
|---|---------|-------|-----------|
| 24.1 | [24.1 - Local AI Infrastructure - CUDA, PyTorch & Multi-GPU Setup](24.1---Local-AI-Infrastructure---CUDA,-PyTorch-&-Multi-GPU-Setup) | GPU setup, CUDA, benchmarking | PyTorch, CUDA, nvitop, accelerate |
| 24.2 | [24.2 - Image Generation Experiments - SDXL, ControlNet & LoRA](24.2---Image-Generation-Experiments---SDXL,-ControlNet-&-LoRA) | Diffusion models, LoRA training | diffusers, kohya_ss, ComfyUI |
| 24.3 | [24.3 - LLM Fine-tuning - LoRA, QLoRA & Full Fine-tuning](24.3---LLM-Fine-tuning---LoRA,-QLoRA-&-Full-Fine-tuning) | Adapter training, full FT | peft, trl, transformers, unsloth |
| 24.4 | [24.4 - RAG Pipelines - Embeddings, Vector DBs & Retrieval](24.4---RAG-Pipelines---Embeddings,-Vector-DBs-&-Retrieval) | Retrieval-augmented generation | Chroma, Qdrant, FAISS, LlamaIndex |
| 24.5 | [24.5 - Agentic AI - ReAct, Tool Calling & Multi-Agent Orchestration](24.5---Agentic-AI---ReAct,-Tool-Calling-&-Multi-Agent-Orchestration) | Agent loops, tool use, orchestration | LangChain, smolagents, Pydantic-AI |
| 24.6 | [24.6 - Voice & Audio - TTS, ASR & Voice Cloning](24.6---Voice-&-Audio---TTS,-ASR-&-Voice-Cloning) | Speech synthesis & recognition | Whisper, Coqui, ElevenLabs, Bark |
| 24.7 | [24.7 - Multimodal Experiments - Vision-Language & Audio-Text Bridges](24.7---Multimodal-Experiments---Vision-Language-&-Audio-Text-Bridges) | Cross-modal AI | LLaVA, Qwen2-VL, ImageBind |

---

## 🔗 Cross-Track Dependencies

| This Chapter | Requires Theory From |
|---|---|
| 24.1 | [08.15 - GPU Computing & CUDA Foundations](08.15---GPU-Computing-&-CUDA-Foundations), [08.16 - Distributed Systems & Multi-GPU Training](08.16---Distributed-Systems-&-Multi-GPU-Training) |
| 24.2 | [23.6 - Generative Models - GANs & Diffusion](23.6---Generative-Models---GANs-&-Diffusion) |
| 24.3 | [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs), [23.7 - Reinforcement Learning & RLHF](23.7---Reinforcement-Learning-&-RLHF) |
| 24.4 | [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs) |
| 24.5 | [23.7 - Reinforcement Learning & RLHF](23.7---Reinforcement-Learning-&-RLHF) |
| 24.6 | [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs) |
| 24.7 | [23.3 - Computer Vision - CNNs & ViTs](23.3---Computer-Vision---CNNs-&-ViTs), [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs) |

---

## 🛠️ Global Prerequisites

```bash
# Core environment (conda recommended)
conda create -n aiexp python=3.11 -y
conda activate aiexp

# PyTorch with CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# HuggingFace ecosystem
pip install transformers accelerate peft trl datasets diffusers bitsandbytes

# Vector DBs & agents
pip install chromadb qdrant-client faiss-gpu langchain llama-index

# Audio
pip install openai-whisper TTS bark

# Utilities
pip install wandb nvitop einops safetensors sentencepiece
```

---

## 📂 Practice Scripts

All runnable scripts live in `_practice/scripts/`. Each script:
- Has a `--demo` flag for quick local validation
- Has a `--config` flag for YAML/JSON experiment configs
- Emits metrics to a markdown report
- Targets a single 24GB GPU

---

## 📊 Progress Tracker

| Chapter | Status | Last Updated |
|---------|--------|-------------|
| 24.1 | ✅ Written | 2026-05-24 |
| 24.2 | ✅ Written | 2026-05-24 |
| 24.3 | ✅ Written | 2026-05-24 |
| 24.4 | ✅ Written | 2026-05-24 |
| 24.5 | ✅ Written | 2026-05-24 |
| 24.6 | ✅ Written | 2026-05-24 |
| 24.7 | ✅ Written | 2026-05-24 |

---

## Related Notes
