---
title: "24.2 — Image Generation Experiments: SDXL, ControlNet & LoRA"
subject: "AI Experiments"
catalog: advanced
audience_tier: higher-education
chapter: "24.2"
type: experiment-chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 24.2 — Image Generation Experiments: SDXL, ControlNet & LoRA

> *"Diffusion models are the first generative models that actually work at scale — they produce images that are both diverse and high-fidelity."*
> — **Yang Song**, Stanford (co-inventor of score-based diffusion)

This chapter takes you from running your first SDXL inference to training custom LoRA adapters and applying ControlNet conditioning. You'll understand the practical knobs: CFG scale, schedulers, LoRA rank, training steps, and how they affect output quality.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Run SDXL and SDXL-Turbo inference with the `diffusers` library.
2. Compare schedulers (DDPM, DDIM, DPM++, Euler) and their speed/quality tradeoffs.
3. Train a style LoRA on 20-50 images in under 30 minutes on a 24GB GPU.
4. Apply ControlNet conditioning (Canny, Depth, Pose) for structural guidance.
5. Merge multiple LoRAs with weighted composition.
6. Benchmark inference speed: steps/second, time-to-first-image.
7. Export models for ComfyUI and A1111 workflows.

---

## 🖼️ Visual Anchor — Diffusion Pipeline Architecture

![aiexp__5.2-fig1](aiexp__5.2-fig1.svg)

---

## 📚 1. Concepts & Definitions

| Concept | Definition |
|---------|-----------|
| **Diffusion Model** | Generative model that learns to reverse a noise-adding process |
| **U-Net** | The denoising backbone — predicts noise at each timestep |
| **VAE** | Variational Autoencoder — compresses images to/from latent space |
| **CLIP Text Encoder** | Converts text prompts to conditioning embeddings |
| **CFG (Classifier-Free Guidance)** | Amplifies prompt adherence: `output = uncond + scale * (cond - uncond)` |
| **LoRA** | Low-Rank Adaptation — trains small rank-decomposed weight deltas |
| **ControlNet** | Adds structural conditioning (edges, depth, pose) to generation |
| **Scheduler** | Defines the noise schedule and sampling strategy |

### Model Landscape (2024-2026)

| Model | Resolution | Params | Latent Size | Speed (4090) |
|-------|-----------|--------|-------------|-------------|
| SD 1.5 | 512×512 | 860M | 64×64 | ~2.5s/img |
| SDXL | 1024×1024 | 3.5B | 128×128 | ~6s/img |
| SDXL-Turbo | 1024×1024 | 3.5B | 128×128 | ~1s/img (4 steps) |
| SD3 Medium | 1024×1024 | 2B | 128×128 | ~4s/img |
| Flux.1 Dev | 1024×1024 | 12B | 128×128 | ~12s/img |
| Flux.1 Schnell | 1024×1024 | 12B | 128×128 | ~3s/img (4 steps) |

---

## 🔬 2. Theory Briefing

> For full diffusion theory (score matching, ELBO, noise schedules), see [23.6 - Generative Models - GANs & Diffusion](23.6---Generative-Models---GANs-&-Diffusion).

### The Forward & Reverse Process (Minimal)

**Forward (add noise):** Given clean image $x_0$, produce noisy $x_t$ at timestep $t$:

$$
x_t = \sqrt{\bar\alpha_t}\, x_0 + \sqrt{1 - \bar\alpha_t}\, \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)
$$

**Reverse (denoise):** The U-Net $\epsilon_\theta(x_t, t, c)$ predicts the noise $\epsilon$ given noisy input, timestep, and conditioning $c$. Subtract predicted noise iteratively to recover $x_0$.

### Latent Diffusion (Stable Diffusion Architecture)

Instead of operating on pixel space (512×512×3 = 786K dims), operate in latent space:

```
Image (1024×1024×3) → VAE Encoder → Latent (128×128×4) → Diffusion → VAE Decoder → Image
```

This reduces computation by ~64× while preserving perceptual quality.

### LoRA Mathematics

Standard weight update: $W' = W + \Delta W$ where $\Delta W \in \mathbb{R}^{d \times d}$ has $d^2$ parameters.

LoRA decomposition: $\Delta W = BA$ where $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times d}$, rank $r \ll d$.

Parameters: $2dr$ instead of $d^2$. For $d=1024$, $r=16$: 32K vs 1M parameters (32× reduction).

---

## 🔧 3. Setup & Prerequisites

```bash
conda activate aiexp

# Core diffusion stack
pip install diffusers[torch] transformers accelerate safetensors

# LoRA training
pip install peft kohya-ss-sd-scripts

# ControlNet preprocessors
pip install controlnet-aux mediapipe opencv-python

# Image utilities
pip install Pillow compel  # compel for prompt weighting

# Optional: xformers for memory-efficient attention
pip install xformers
```

### Model Downloads

```python
# Pre-download models (avoid timeout during experiments)
from huggingface_hub import snapshot_download

# SDXL base (~6.5 GB)
snapshot_download("stabilityai/stable-diffusion-xl-base-1.0")

# SDXL-Turbo (~6.5 GB)  
snapshot_download("stabilityai/sdxl-turbo")

# ControlNet for SDXL (~2.5 GB each)
snapshot_download("diffusers/controlnet-canny-sdxl-1.0")
snapshot_download("diffusers/controlnet-depth-sdxl-1.0")
```

---

## 🧪 4. Experiment Walkthrough

### Experiment 4.1 — Basic SDXL Inference

```python
import torch
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler

# Load pipeline
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
).to("cuda")

# Use DPM++ 2M Karras scheduler (fast, high quality)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config, algorithm_type="dpmsolver++", use_karras_sigmas=True
)

# Enable memory optimizations
pipe.enable_vae_tiling()  # For high-res without OOM

# Generate
prompt = "A cyberpunk cityscape at sunset, neon lights reflecting on wet streets, 8k, detailed"
negative_prompt = "blurry, low quality, distorted, watermark"

image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=25,
    guidance_scale=7.5,
    width=1024,
    height=1024,
    generator=torch.Generator("cuda").manual_seed(42),
).images[0]

image.save("sdxl_output.png")
print(f"Generated: {image.size}")
```

### Experiment 4.2 — Scheduler Comparison

```python
import torch
import time
from diffusers import (
    StableDiffusionXLPipeline,
    DDPMScheduler, DDIMScheduler,
    DPMSolverMultistepScheduler, EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
)

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16, variant="fp16",
).to("cuda")

schedulers = {
    "DDPM (1000 steps)": (DDPMScheduler, 50),  # still slow even at 50
    "DDIM (25 steps)": (DDIMScheduler, 25),
    "DPM++ 2M Karras (25)": (DPMSolverMultistepScheduler, 25),
    "Euler (25)": (EulerDiscreteScheduler, 25),
    "Euler Ancestral (25)": (EulerAncestralDiscreteScheduler, 25),
}

prompt = "A majestic mountain landscape with aurora borealis, photorealistic"
results = {}

for name, (sched_cls, steps) in schedulers.items():
    pipe.scheduler = sched_cls.from_config(pipe.scheduler.config)
    
    # Warmup
    _ = pipe(prompt, num_inference_steps=steps, output_type="latent")
    torch.cuda.synchronize()
    
    start = time.perf_counter()
    image = pipe(
        prompt, num_inference_steps=steps,
        generator=torch.Generator("cuda").manual_seed(42)
    ).images[0]
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    
    results[name] = elapsed
    image.save(f"scheduler_{name.split()[0].lower()}.png")
    print(f"{name}: {elapsed:.2f}s")

# Print comparison table
print("\n| Scheduler | Time | Steps |")
print("|-----------|------|-------|")
for name, t in sorted(results.items(), key=lambda x: x[1]):
    steps = schedulers[name][1]
    print(f"| {name} | {t:.2f}s | {steps} |")
```

### Experiment 4.3 — ControlNet (Canny Edge Conditioning)

```python
import torch
import cv2
import numpy as np
from PIL import Image
from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel
from diffusers.utils import load_image

# Load ControlNet
controlnet = ControlNetModel.from_pretrained(
    "diffusers/controlnet-canny-sdxl-1.0",
    torch_dtype=torch.float16, variant="fp16",
)

pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    controlnet=controlnet,
    torch_dtype=torch.float16, variant="fp16",
).to("cuda")

# Prepare control image (Canny edges)
input_image = load_image("reference_photo.png")
input_array = np.array(input_image)

# Canny edge detection
edges = cv2.Canny(input_array, 100, 200)
control_image = Image.fromarray(edges).convert("RGB").resize((1024, 1024))

# Generate with structural guidance
image = pipe(
    prompt="A futuristic building, glass and steel, dramatic lighting",
    negative_prompt="blurry, distorted",
    image=control_image,
    controlnet_conditioning_scale=0.7,  # 0.0-1.0, lower = less strict
    num_inference_steps=25,
    guidance_scale=7.5,
).images[0]

image.save("controlnet_canny_output.png")
```

### Experiment 4.4 — Training a Style LoRA

```python
# Using diffusers training script (simplified version)
# Full script: https://github.com/huggingface/diffusers/blob/main/examples/dreambooth/train_dreambooth_lora_sdxl.py

# Step 1: Prepare dataset
# Place 20-50 images in ./training_data/
# All images should be consistent style/subject

# Step 2: Training command
TRAINING_CMD = """
accelerate launch train_dreambooth_lora_sdxl.py \
  --pretrained_model_name_or_path="stabilityai/stable-diffusion-xl-base-1.0" \
  --instance_data_dir="./training_data" \
  --instance_prompt="a photo in the style of sks" \
  --output_dir="./lora_output" \
  --resolution=1024 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=4 \
  --learning_rate=1e-4 \
  --lr_scheduler="cosine" \
  --lr_warmup_steps=100 \
  --max_train_steps=1000 \
  --rank=32 \
  --mixed_precision="fp16" \
  --seed=42 \
  --gradient_checkpointing \
  --use_8bit_adam
"""

# Step 3: Inference with trained LoRA
from diffusers import StableDiffusionXLPipeline
import torch

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
).to("cuda")

# Load LoRA weights
pipe.load_lora_weights("./lora_output", weight_name="pytorch_lora_weights.safetensors")

# Generate with LoRA style
image = pipe(
    "a cyberpunk city in the style of sks",
    num_inference_steps=25,
    guidance_scale=7.5,
    cross_attention_kwargs={"scale": 0.8},  # LoRA strength
).images[0]
image.save("lora_inference.png")
```

### Experiment 4.5 — Multi-LoRA Composition

```python
import torch
from diffusers import StableDiffusionXLPipeline

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
).to("cuda")

# Load multiple LoRAs with different weights
pipe.load_lora_weights("./lora_style_A", adapter_name="style_a")
pipe.load_lora_weights("./lora_style_B", adapter_name="style_b")

# Set adapter weights (must sum to reasonable range, typically 0.5-1.5 total)
pipe.set_adapters(["style_a", "style_b"], adapter_weights=[0.6, 0.4])

image = pipe(
    "a portrait with dramatic lighting",
    num_inference_steps=25,
).images[0]
image.save("multi_lora.png")

# Disable LoRAs for comparison
pipe.disable_lora()
baseline = pipe("a portrait with dramatic lighting", num_inference_steps=25).images[0]
baseline.save("no_lora_baseline.png")
```

### Experiment 4.6 — SDXL-Turbo (4-Step Generation)

```python
import torch
from diffusers import AutoPipelineForText2Image

# SDXL-Turbo uses adversarial distillation — only 1-4 steps needed
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16, variant="fp16",
).to("cuda")

# No CFG needed for turbo models (guidance_scale=0.0)
image = pipe(
    prompt="A cat astronaut floating in space, digital art",
    num_inference_steps=4,
    guidance_scale=0.0,  # Turbo doesn't need CFG
    width=512, height=512,  # Turbo trained at 512
).images[0]
image.save("turbo_output.png")

# Benchmark: time 100 generations
import time
torch.cuda.synchronize()
start = time.perf_counter()
for i in range(100):
    _ = pipe("test", num_inference_steps=4, guidance_scale=0.0, output_type="latent")
torch.cuda.synchronize()
elapsed = time.perf_counter() - start
print(f"SDXL-Turbo: {elapsed/100*1000:.0f} ms/image ({100/elapsed:.1f} img/s)")
```

---

## 📈 5. Expected Results & Evaluation

### Quality Metrics

| Metric | What It Measures | Tool |
|--------|-----------------|------|
| **FID** | Distribution similarity to real images | `torchmetrics.image.fid` |
| **CLIP Score** | Text-image alignment | `torchmetrics.multimodal.CLIPScore` |
| **Aesthetic Score** | Predicted human preference | LAION aesthetic predictor |
| **LPIPS** | Perceptual similarity (for ControlNet) | `lpips` library |

### LoRA Training Targets

| Metric | Good | Concern |
|--------|------|---------|
| Training loss | Decreasing, stabilizes ~0.05-0.1 | Increasing → LR too high |
| CLIP score | > 0.28 | < 0.22 → prompt not learned |
| Visual quality | Recognizable style transfer | Mode collapse → reduce steps |
| Training time (1000 steps) | 20-30 min on 4090 | > 60 min → check batch/grad accum |

---

## ⚠️ 6. Gotchas & Debugging

| Issue | Cause | Fix |
|-------|-------|-----|
| Black images | VAE NaN (FP16 instability) | Use `pipe.vae = pipe.vae.to(torch.float32)` |
| Blurry outputs | Too few steps or low CFG | Increase steps to 25+, CFG to 7-9 |
| LoRA not taking effect | Wrong adapter name or scale=0 | Check `pipe.get_active_adapters()` |
| OOM during LoRA training | Batch too large | Use `gradient_checkpointing`, reduce batch to 1 |
| Color shift after LoRA | Overfitting on small dataset | Reduce steps, increase rank, add regularization images |
| ControlNet too rigid | conditioning_scale too high | Reduce to 0.4-0.6 |

### Memory Budget (SDXL on 24GB)

```
SDXL U-Net (FP16):        ~3.5 GB
SDXL VAE (FP32):          ~0.3 GB
Text Encoders (FP16):     ~1.2 GB
ControlNet (FP16):        ~2.5 GB
Latents + intermediates:  ~2-4 GB
─────────────────────────────────
Total inference:           ~10 GB (fits easily)
LoRA training:            ~18-22 GB (tight but works)
```

---

## 🔬 7. Variations & Extensions

1. **IP-Adapter:** Condition generation on reference images (style transfer without training). Use `ip-adapter-sdxl` for image-prompted generation.

2. **Flux.1 Experiments:** Try the 12B parameter Flux model with quantization. Compare quality vs SDXL at same inference time.

3. **AnimateDiff:** Extend SDXL to video generation. Train temporal LoRAs for consistent motion.

4. **Inpainting & Outpainting:** Use SDXL-Inpainting for targeted edits. Combine with SAM (Segment Anything) for mask generation.

5. **Textual Inversion:** Alternative to LoRA — learn a new token embedding instead of weight deltas. Faster to train but less expressive.

---

## 🔗 8. Cross-links & Further Reading

### Internal Cross-links
- Diffusion theory & math: [23.6 - Generative Models - GANs & Diffusion](23.6---Generative-Models---GANs-&-Diffusion)
- GPU memory management: [24.1 - Local AI Infrastructure - CUDA, PyTorch & Multi-GPU Setup](24.1---Local-AI-Infrastructure---CUDA,-PyTorch-&-Multi-GPU-Setup)
- LoRA theory (shared with LLM fine-tuning): [24.3 - LLM Fine-tuning - LoRA, QLoRA & Full Fine-tuning](24.3---LLM-Fine-tuning---LoRA,-QLoRA-&-Full-Fine-tuning)
- Multimodal bridges: [24.7 - Multimodal Experiments - Vision-Language & Audio-Text Bridges](24.7---Multimodal-Experiments---Vision-Language-&-Audio-Text-Bridges)

### External References
- **Stable Diffusion XL Paper** — [arXiv:2307.01952](https://arxiv.org/abs/2307.01952)
- **LoRA Paper** — Hu et al. (2021) [arXiv:2106.09685](https://arxiv.org/abs/2106.09685)
- **ControlNet Paper** — Zhang et al. (2023) [arXiv:2302.05543](https://arxiv.org/abs/2302.05543)
- **HuggingFace Diffusers** — [huggingface.co/docs/diffusers](https://huggingface.co/docs/diffusers)
- **ComfyUI** — Node-based workflow — [github.com/comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- **CivitAI** — Community LoRA/model hub — [civitai.com](https://civitai.com)



---

## 🧠 9. Extended Experiments & Variations

### Experiment 9.1 — SDXL + ControlNet + IP-Adapter Combined Stack

Layer multiple conditioning signals: structural guidance from ControlNet (Canny edges) plus style guidance from IP-Adapter (reference image). This is the production workflow for consistent, controllable generation.

```python
import torch
from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel, AutoencoderKL
from diffusers.utils import load_image
from transformers import CLIPVisionModelWithProjection
from PIL import Image
import numpy as np
import cv2
import time

def setup_sdxl_controlnet_ipadapter():
    """Load SDXL with ControlNet + IP-Adapter stack."""
    # Load ControlNet (Canny edge detection)
    controlnet = ControlNetModel.from_pretrained(
        "diffusers/controlnet-canny-sdxl-1.0",
        torch_dtype=torch.float16,
        variant="fp16",
    )
    
    # Load SDXL pipeline with ControlNet
    pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        controlnet=controlnet,
        torch_dtype=torch.float16,
        variant="fp16",
    )
    
    # Load IP-Adapter
    pipe.load_ip_adapter(
        "h94/IP-Adapter",
        subfolder="sdxl_models",
        weight_name="ip-adapter-plus_sdxl_vit-h.safetensors",
    )
    pipe.set_ip_adapter_scale(0.6)  # Balance between prompt and reference image
    
    # Optimizations for 24GB GPU
    pipe.enable_model_cpu_offload()
    pipe.enable_vae_slicing()
    
    return pipe

def extract_canny_edges(image_path, low_threshold=100, high_threshold=200):
    """Extract Canny edges from an image for ControlNet conditioning."""
    image = np.array(Image.open(image_path).resize((1024, 1024)))
    edges = cv2.Canny(image, low_threshold, high_threshold)
    edges = np.stack([edges] * 3, axis=-1)  # Convert to 3-channel
    return Image.fromarray(edges)

def generate_with_full_stack(pipe, prompt, structure_image_path, style_image_path,
                             num_images=4, controlnet_scale=0.7):
    """Generate images with ControlNet structure + IP-Adapter style."""
    # Prepare conditioning
    canny_image = extract_canny_edges(structure_image_path)
    style_image = load_image(style_image_path).resize((1024, 1024))
    
    results = []
    for i in range(num_images):
        start = time.perf_counter()
        
        image = pipe(
            prompt=prompt,
            negative_prompt="blurry, low quality, distorted, deformed",
            image=canny_image,
            ip_adapter_image=style_image,
            controlnet_conditioning_scale=controlnet_scale,
            num_inference_steps=30,
            guidance_scale=7.5,
            generator=torch.Generator("cuda").manual_seed(42 + i),
        ).images[0]
        
        elapsed = time.perf_counter() - start
        image.save(f"output_combined_{i:02d}.png")
        results.append({"seed": 42 + i, "time_s": elapsed})
        print(f"Image {i}: {elapsed:.1f}s")
    
    return results

# Run experiment
pipe = setup_sdxl_controlnet_ipadapter()
results = generate_with_full_stack(
    pipe,
    prompt="A futuristic cityscape at sunset, cyberpunk architecture, neon lights",
    structure_image_path="reference_building.png",
    style_image_path="style_reference_artstation.png",
)
```

**Expected output:**
- Generation time: 8-12s per image on RTX 4090 (ControlNet + IP-Adapter adds ~40% overhead vs base SDXL)
- VRAM usage: ~18 GB with CPU offload, ~22 GB without
- Images maintain structural layout from Canny edges while adopting color palette and artistic style from reference

**Gotchas:**
- IP-Adapter scale > 0.8 causes the output to become a near-copy of the reference (loss of prompt adherence).
- ControlNet conditioning_scale > 0.9 produces artifacts at edge boundaries.
- The combined stack requires careful balancing: start with controlnet_scale=0.5, ip_adapter_scale=0.4, then adjust.
- CPU offload adds ~3s latency per image but saves ~6 GB VRAM.

### Experiment 9.2 — LoRA Training on Custom Dataset (Full Pipeline)

Train a style LoRA from scratch on 20-50 images of a specific art style, character, or object. Includes dataset preparation, captioning, training, and evaluation.

```python
import torch
import os
import json
from pathlib import Path
from diffusers import StableDiffusionXLPipeline, AutoencoderKL
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# === STEP 1: Auto-caption dataset with BLIP-2 ===
def caption_dataset(image_dir, output_dir):
    """Generate captions for training images using BLIP-2."""
    processor = BlipProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16, device_map="auto"
    )
    
    image_dir = Path(image_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    metadata = []
    for img_path in sorted(image_dir.glob("*.png")) + sorted(image_dir.glob("*.jpg")):
        image = Image.open(img_path).convert("RGB")
        inputs = processor(image, return_tensors="pt").to("cuda", torch.float16)
        
        generated_ids = model.generate(**inputs, max_new_tokens=50)
        caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        
        # Add trigger word
        caption = f"in the style of sks_artstyle, {caption}"
        
        # Save caption file (same name, .txt extension)
        caption_path = output_dir / f"{img_path.stem}.txt"
        caption_path.write_text(caption)
        
        # Copy image to output
        image.save(output_dir / img_path.name)
        metadata.append({"file_name": img_path.name, "text": caption})
        print(f"{img_path.name}: {caption}")
    
    # Save metadata.jsonl
    with open(output_dir / "metadata.jsonl", "w") as f:
        for item in metadata:
            f.write(json.dumps(item) + "\n")
    
    return metadata

# === STEP 2: Training configuration ===
TRAINING_CONFIG = """
# train_lora_sdxl.yaml
pretrained_model_name_or_path: "stabilityai/stable-diffusion-xl-base-1.0"
instance_data_dir: "./training_data"
output_dir: "./lora_output"
resolution: 1024
train_batch_size: 1
gradient_accumulation_steps: 4
learning_rate: 1e-4
lr_scheduler: "cosine"
lr_warmup_steps: 100
max_train_steps: 1000
rank: 32
text_encoder_lr: 5e-5
train_text_encoder: true
mixed_precision: "bf16"
seed: 42
validation_prompt: "a landscape in the style of sks_artstyle, mountains at sunset"
validation_epochs: 100
"""

# === STEP 3: Launch training with diffusers script ===
def get_training_command(config_path="train_lora_sdxl.yaml"):
    """Generate the training command."""
    cmd = """
accelerate launch diffusers/examples/dreambooth/train_dreambooth_lora_sdxl.py \\
  --pretrained_model_name_or_path="stabilityai/stable-diffusion-xl-base-1.0" \\
  --instance_data_dir="./training_data" \\
  --output_dir="./lora_output" \\
  --instance_prompt="in the style of sks_artstyle" \\
  --resolution=1024 \\
  --train_batch_size=1 \\
  --gradient_accumulation_steps=4 \\
  --learning_rate=1e-4 \\
  --lr_scheduler="cosine" \\
  --lr_warmup_steps=100 \\
  --max_train_steps=1000 \\
  --rank=32 \\
  --train_text_encoder \\
  --mixed_precision="bf16" \\
  --seed=42 \\
  --validation_prompt="a landscape in the style of sks_artstyle" \\
  --validation_epochs=200 \\
  --gradient_checkpointing \\
  --use_8bit_adam
"""
    return cmd.strip()

# === STEP 4: Evaluate trained LoRA ===
def evaluate_lora(lora_path, prompts, num_images_per_prompt=4):
    """Generate images with trained LoRA and compute CLIP scores."""
    from torchmetrics.multimodal import CLIPScore
    
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        variant="fp16",
    ).to("cuda")
    
    pipe.load_lora_weights(lora_path)
    pipe.fuse_lora(lora_scale=0.8)
    
    clip_metric = CLIPScore(model_name_or_path="openai/clip-vit-large-patch14").to("cuda")
    
    all_scores = []
    for prompt in prompts:
        for i in range(num_images_per_prompt):
            image = pipe(
                prompt=prompt,
                num_inference_steps=25,
                guidance_scale=7.0,
                generator=torch.Generator("cuda").manual_seed(i),
            ).images[0]
            
            # CLIP score
            image_tensor = torch.tensor(np.array(image)).permute(2, 0, 1).unsqueeze(0).to("cuda")
            score = clip_metric(image_tensor, prompt)
            all_scores.append(score.item())
            
            image.save(f"eval_{prompt[:20]}_{i}.png")
    
    print(f"Average CLIP Score: {np.mean(all_scores):.4f}")
    print(f"Score range: [{min(all_scores):.4f}, {max(all_scores):.4f}]")
    return all_scores

print(get_training_command())
```

```bash
# Full training pipeline
# Step 1: Prepare dataset
python caption_dataset.py --input ./raw_images --output ./training_data

# Step 2: Train (takes ~25 min on RTX 4090 for 1000 steps)
accelerate launch train_dreambooth_lora_sdxl.py \
  --pretrained_model_name_or_path="stabilityai/stable-diffusion-xl-base-1.0" \
  --instance_data_dir="./training_data" \
  --output_dir="./lora_output" \
  --instance_prompt="in the style of sks_artstyle" \
  --resolution=1024 --train_batch_size=1 \
  --gradient_accumulation_steps=4 --learning_rate=1e-4 \
  --max_train_steps=1000 --rank=32 \
  --mixed_precision="bf16" --gradient_checkpointing --use_8bit_adam

# Step 3: Convert to safetensors for ComfyUI/A1111
python convert_lora_to_safetensors.py --input ./lora_output --output ./my_style.safetensors
```

**Expected output:**
- Training time: 20-30 minutes for 1000 steps on RTX 4090
- VRAM usage: 18-22 GB (with gradient checkpointing + 8-bit Adam)
- LoRA file size: 50-150 MB (rank 32, all layers)
- CLIP score improvement: +0.02-0.05 on style-specific prompts vs base model

**Gotchas:**
- Too many steps (>2000) on small datasets (<30 images) causes overfitting — outputs become copies of training images.
- The trigger word (`sks_artstyle`) must be unique and not a real word to avoid conflicting with pretrained knowledge.
- Training the text encoder (`--train_text_encoder`) improves prompt adherence but doubles training time.
- Always use `gradient_checkpointing` — without it, SDXL LoRA training OOMs on 24GB.

### Experiment 9.3 — ComfyUI vs Automatic1111 Workflow Comparison

Build equivalent generation pipelines in both interfaces and compare flexibility, speed, and reproducibility.

```python
# ComfyUI workflow as Python (using ComfyUI's API)
import json
import requests
import websocket
import uuid

COMFYUI_URL = "http://127.0.0.1:8188"

def build_comfyui_workflow(prompt, negative_prompt, steps=25, cfg=7.0, 
                           seed=42, width=1024, height=1024,
                           lora_name=None, lora_strength=0.8,
                           controlnet_image=None):
    """Build a ComfyUI workflow programmatically via API."""
    workflow = {
        "3": {  # KSampler
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "denoise": 1.0,
                "model": ["4", 0],  # from CheckpointLoader
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0],
            }
        },
        "4": {  # CheckpointLoader
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}
        },
        "5": {  # EmptyLatentImage
            "class_type": "EmptyLatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1}
        },
        "6": {  # CLIP Text Encode (positive)
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt, "clip": ["4", 1]}
        },
        "7": {  # CLIP Text Encode (negative)
            "class_type": "CLIPTextEncode",
            "inputs": {"text": negative_prompt, "clip": ["4", 1]}
        },
        "8": {  # VAE Decode
            "class_type": "VAEDecode",
            "inputs": {"samples": ["3", 0], "vae": ["4", 2]}
        },
        "9": {  # Save Image
            "class_type": "SaveImage",
            "inputs": {"images": ["8", 0], "filename_prefix": "comfyui_output"}
        },
    }
    
    # Add LoRA node if specified
    if lora_name:
        workflow["10"] = {
            "class_type": "LoraLoader",
            "inputs": {
                "lora_name": lora_name,
                "strength_model": lora_strength,
                "strength_clip": lora_strength,
                "model": ["4", 0],
                "clip": ["4", 1],
            }
        }
        # Rewire KSampler to use LoRA model
        workflow["3"]["inputs"]["model"] = ["10", 0]
        workflow["6"]["inputs"]["clip"] = ["10", 1]
        workflow["7"]["inputs"]["clip"] = ["10", 1]
    
    return workflow

def queue_comfyui_prompt(workflow):
    """Submit workflow to ComfyUI and wait for result."""
    client_id = str(uuid.uuid4())
    
    # Queue prompt
    response = requests.post(f"{COMFYUI_URL}/prompt", json={
        "prompt": workflow,
        "client_id": client_id,
    })
    prompt_id = response.json()["prompt_id"]
    
    # Wait for completion via websocket
    ws = websocket.WebSocket()
    ws.connect(f"ws://127.0.0.1:8188/ws?clientId={client_id}")
    
    while True:
        msg = json.loads(ws.recv())
        if msg["type"] == "executing" and msg["data"]["node"] is None:
            break
    
    ws.close()
    
    # Get output images
    history = requests.get(f"{COMFYUI_URL}/history/{prompt_id}").json()
    return history[prompt_id]["outputs"]

# Comparison benchmark
def compare_interfaces():
    """Compare ComfyUI vs A1111 API for same generation task."""
    import time
    
    prompt = "A majestic dragon perched on a crystal mountain, fantasy art, detailed scales"
    negative = "blurry, low quality, watermark"
    
    # ComfyUI timing
    workflow = build_comfyui_workflow(prompt, negative, steps=25, cfg=7.0)
    
    start = time.perf_counter()
    for _ in range(10):
        queue_comfyui_prompt(workflow)
    comfyui_time = (time.perf_counter() - start) / 10
    
    # A1111 API timing
    a1111_url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    payload = {
        "prompt": prompt,
        "negative_prompt": negative,
        "steps": 25,
        "cfg_scale": 7.0,
        "width": 1024,
        "height": 1024,
        "sampler_name": "DPM++ 2M Karras",
    }
    
    start = time.perf_counter()
    for _ in range(10):
        requests.post(a1111_url, json=payload)
    a1111_time = (time.perf_counter() - start) / 10
    
    print(f"ComfyUI: {comfyui_time:.2f}s/image")
    print(f"A1111:   {a1111_time:.2f}s/image")
    print(f"Speedup: {a1111_time/comfyui_time:.2f}×")

compare_interfaces()
```

**Expected output:**

| Feature | ComfyUI | Automatic1111 |
|---------|---------|---------------|
| Speed (SDXL, 25 steps) | ~5.5s | ~6.2s |
| Node-based workflow | ✅ Visual graph | ❌ Linear UI |
| API automation | ✅ Full workflow JSON | ✅ REST API |
| LoRA hot-swap | ✅ Instant | ⚠️ Requires reload |
| ControlNet stacking | ✅ Multiple in parallel | ✅ Via extension |
| Memory efficiency | Better (lazy loading) | Higher baseline |
| Custom nodes ecosystem | 2000+ community nodes | 500+ extensions |
| Batch processing | ✅ Queue system | ✅ Batch count |

**Gotchas:**
- ComfyUI workflows are JSON — version control them in git for reproducibility.
- A1111 extensions can conflict; use `--no-half-vae` if you see black images.
- ComfyUI's node execution is topologically sorted — circular dependencies crash silently.
- For production serving, neither is ideal — use `diffusers` directly with a FastAPI wrapper.

### Experiment 9.4 — Flux Model Variants: Dev vs Schnell vs Pro

Compare the Flux model family (Black Forest Labs) against SDXL for quality, speed, and controllability.

```python
import torch
from diffusers import FluxPipeline, FluxTransformer2DModel
from optimum.quanto import quantize, freeze, qfloat8
import time
import numpy as np
from PIL import Image

def setup_flux_schnell_quantized():
    """Load Flux.1 Schnell with FP8 quantization to fit on 24GB."""
    # Flux.1 is 12B params — needs quantization for 24GB GPU
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-schnell",
        torch_dtype=torch.bfloat16,
    )
    
    # Quantize transformer to FP8 (saves ~6GB)
    quantize(pipe.transformer, weights=qfloat8)
    freeze(pipe.transformer)
    
    pipe.enable_model_cpu_offload()
    pipe.vae.enable_slicing()
    pipe.vae.enable_tiling()
    
    return pipe

def setup_flux_dev_quantized():
    """Load Flux.1 Dev with FP8 quantization."""
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        torch_dtype=torch.bfloat16,
    )
    quantize(pipe.transformer, weights=qfloat8)
    freeze(pipe.transformer)
    pipe.enable_model_cpu_offload()
    return pipe

def benchmark_flux_vs_sdxl(prompts, num_runs=5):
    """Compare Flux variants against SDXL."""
    from diffusers import StableDiffusionXLPipeline
    
    results = {}
    
    # SDXL baseline
    sdxl = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16, variant="fp16",
    ).to("cuda")
    
    times = []
    for prompt in prompts:
        start = time.perf_counter()
        for _ in range(num_runs):
            _ = sdxl(prompt, num_inference_steps=25, guidance_scale=7.0,
                     generator=torch.Generator("cuda").manual_seed(42)).images[0]
        times.append((time.perf_counter() - start) / num_runs)
    results["SDXL (25 steps)"] = np.mean(times)
    del sdxl; torch.cuda.empty_cache()
    
    # Flux Schnell (4 steps)
    flux_schnell = setup_flux_schnell_quantized()
    times = []
    for prompt in prompts:
        start = time.perf_counter()
        for _ in range(num_runs):
            _ = flux_schnell(prompt, num_inference_steps=4, guidance_scale=0.0,
                            generator=torch.Generator("cuda").manual_seed(42)).images[0]
        times.append((time.perf_counter() - start) / num_runs)
    results["Flux Schnell (4 steps, FP8)"] = np.mean(times)
    del flux_schnell; torch.cuda.empty_cache()
    
    # Flux Dev (20 steps)
    flux_dev = setup_flux_dev_quantized()
    times = []
    for prompt in prompts:
        start = time.perf_counter()
        for _ in range(num_runs):
            _ = flux_dev(prompt, num_inference_steps=20, guidance_scale=3.5,
                        generator=torch.Generator("cuda").manual_seed(42)).images[0]
        times.append((time.perf_counter() - start) / num_runs)
    results["Flux Dev (20 steps, FP8)"] = np.mean(times)
    del flux_dev; torch.cuda.empty_cache()
    
    # Print comparison
    print(f"\n{'Model':<35} {'Time/Image':<12} {'Relative':<10}")
    print("-" * 57)
    baseline = results["SDXL (25 steps)"]
    for name, t in results.items():
        print(f"{name:<35} {t:.2f}s        {t/baseline:.2f}×")
    
    return results

test_prompts = [
    "A photorealistic portrait of an elderly fisherman, golden hour lighting",
    "An abstract painting of consciousness, vibrant colors, museum quality",
    "A technical diagram of a fusion reactor, blueprint style, detailed labels",
]
benchmark_flux_vs_sdxl(test_prompts)
```

**Expected output (RTX 4090):**

| Model | Steps | Time/Image | Quality (subjective) | VRAM |
|-------|-------|-----------|---------------------|------|
| SDXL Base | 25 | 5.8s | Good | 7 GB |
| SDXL Turbo | 4 | 1.2s | Decent | 7 GB |
| Flux Schnell (FP8) | 4 | 3.5s | Very Good | 18 GB |
| Flux Dev (FP8) | 20 | 14s | Excellent | 20 GB |
| Flux Dev (FP16) | 20 | OOM | — | >24 GB |

**Key findings:**
- Flux produces significantly better text rendering and spatial understanding than SDXL.
- Flux Schnell at 4 steps rivals SDXL at 25 steps in quality (rectified flow > DDPM).
- FP8 quantization is essential for Flux on 24GB — quality loss is imperceptible.
- Flux lacks ControlNet ecosystem maturity (fewer community models vs SDXL).

**Gotchas:**
- Flux uses T5-XXL text encoder (4.7B params) — this alone takes 10 GB in FP16. Use FP8 or CPU offload.
- Flux Schnell is Apache-2.0 licensed (commercial use OK); Flux Dev is non-commercial.
- `guidance_scale=0.0` for Schnell (it's distilled for zero-CFG); Dev uses 3.0-4.0.
- Flux's rectified flow scheduler is incompatible with DDPM/DDIM schedulers — don't swap them.


---

## 📘 10. Appendix: Production Considerations & Theory Bridges

### 10.1 Classifier-Free Guidance — Full Derivation

Classifier-Free Guidance (CFG) is the mechanism that controls how strongly the generated image adheres to the text prompt. Understanding its derivation explains why `guidance_scale=7.5` works and what happens at extreme values.

**Background:** In classifier guidance (Dhariwal & Nichol, 2021), a pretrained classifier $p(y|x_t)$ guides diffusion:

$$
\nabla_{x_t} \log p(x_t | y) = \nabla_{x_t} \log p(x_t) + s \cdot \nabla_{x_t} \log p(y | x_t)
$$

where $s$ is the guidance scale. Problem: requires training a separate classifier on noisy images.

**Classifier-Free Guidance (Ho & Salimans, 2022):** Train a single model that can operate both conditionally and unconditionally by randomly dropping the conditioning during training (e.g., replacing text embedding with null embedding 10% of the time).

At inference, the guided noise prediction is:

$$
\hat{\epsilon}_\theta(x_t, c) = \epsilon_\theta(x_t, \varnothing) + s \cdot (\epsilon_\theta(x_t, c) - \epsilon_\theta(x_t, \varnothing))
$$

where:
- $\epsilon_\theta(x_t, c)$ = conditional prediction (with text prompt)
- $\epsilon_\theta(x_t, \varnothing)$ = unconditional prediction (null prompt)
- $s$ = guidance scale (typically 5-15 for SDXL)

**Interpretation:** CFG amplifies the "direction" from unconditional to conditional. At $s=1$, it's standard conditional generation. At $s>1$, it exaggerates prompt-relevant features. At $s=0$, it ignores the prompt entirely.

**Why it works (implicit classifier):**

$$
s \cdot (\epsilon_\theta(x_t, c) - \epsilon_\theta(x_t, \varnothing)) \propto s \cdot \nabla_{x_t} \log p(c | x_t)
$$

The difference between conditional and unconditional predictions implicitly estimates the gradient of a classifier — no separate classifier needed.

**Practical effects of guidance scale:**

| Scale | Effect | Use Case |
|-------|--------|----------|
| 1.0 | No guidance (pure conditional) | Rarely used |
| 3.0-24.0 | Soft guidance, more diverse | Artistic exploration |
| 7.0-8.0 | Standard (SDXL sweet spot) | General purpose |
| 10.0-15.0 | Strong adherence, less diversity | Precise prompts |
| 20.0+ | Over-saturated, artifacts | Avoid |

**Computational cost:** CFG requires TWO forward passes per denoising step (conditional + unconditional), doubling inference time. Distilled models (SDXL-Turbo, Flux Schnell) eliminate this by training without CFG.

### 10.2 Rectified Flow vs DDPM — Theory Bridge

> **Cross-reference:** [23.6 - Generative Models - GANs & Diffusion](23.6---Generative-Models---GANs-&-Diffusion) for full diffusion theory.

**DDPM (Denoising Diffusion Probabilistic Models):**

The forward process adds Gaussian noise over $T$ timesteps with a variance schedule $\beta_t$:

$$
q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t}\, x_{t-1}, \beta_t I)
$$

The reverse process learns to denoise:

$$
p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \sigma_t^2 I)
$$

Problem: The noise schedule creates curved paths in latent space. Sampling requires many steps (20-50) to follow these curves accurately.

**Rectified Flow (Liu et al., 2022 — used in Flux):**

Instead of a curved noise schedule, rectified flow learns straight-line paths between noise and data:

$$
x_t = (1 - t) \cdot x_0 + t \cdot \epsilon, \quad t \in [0, 1]
$$

The model predicts the velocity (direction from noise to data):

$$
v_\theta(x_t, t) \approx x_0 - \epsilon = \frac{x_0 - x_t}{1 - t}
$$

**Why fewer steps work:** Straight paths can be traversed in 1-4 Euler steps:

$$
x_{t-\Delta t} = x_t + \Delta t \cdot v_\theta(x_t, t)
$$

DDPM's curved paths require 20+ steps because large step sizes cause the trajectory to deviate from the true reverse path.

**Reflow (straightening):** The initial learned paths aren't perfectly straight. Reflow iteratively straightens them:
1. Sample pairs $(x_0, x_1)$ from the learned flow
2. Retrain the model on these straight-line pairs
3. Repeat — each iteration produces straighter paths

After 2-3 reflow iterations, 1-step generation becomes viable (this is how Flux Schnell achieves 4-step generation).

**Comparison:**

| Property | DDPM | Rectified Flow |
|----------|------|---------------|
| Path shape | Curved (variance schedule) | Straight (linear interpolation) |
| Min steps for quality | 20-50 | 1-4 (after distillation) |
| Training objective | Predict noise $\epsilon$ | Predict velocity $v$ |
| CFG required | Yes (2× cost) | Optional (can distill without) |
| Theory basis | Markov chain | ODE flow matching |

### 10.3 LoRA Rank Selection — Mathematical Justification

The LoRA decomposition replaces a weight update $\Delta W \in \mathbb{R}^{d \times k}$ with:

$$
\Delta W = BA, \quad B \in \mathbb{R}^{d \times r}, \; A \in \mathbb{R}^{r \times k}
$$

where $r \ll \min(d, k)$ is the rank.

**Information capacity:** The rank-$r$ approximation can represent at most $r(d + k - r)$ degrees of freedom (the dimension of the Grassmannian manifold of rank-$r$ matrices). For SDXL's U-Net with typical layer sizes $d = k = 1280$:

| Rank | Parameters | % of Full | Capacity |
|------|-----------|-----------|----------|
| 4 | 10,240 | 0.6% | Minimal style shift |
| 16 | 40,960 | 2.5% | Good style transfer |
| 32 | 81,920 | 5.0% | Strong adaptation |
| 64 | 163,840 | 10.0% | Near full fine-tune |
| 128 | 327,680 | 20.0% | Diminishing returns |

**The alpha/rank ratio:** The effective learning rate for LoRA is scaled by $\alpha/r$:

$$
W' = W + \frac{\alpha}{r} \cdot BA
$$

Common choices: $\alpha = 2r$ (aggressive), $\alpha = r$ (standard), $\alpha = r/2$ (conservative). Higher $\alpha/r$ means the LoRA has more influence per training step.

---
