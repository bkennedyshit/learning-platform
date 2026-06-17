---
title: "Computer Vision Cnns Vits"
subject: "AI & Machine Learning Systems"
catalog: advanced
audience_tier: higher-education
chapter: "23.3"
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [09 - Learning Index](09---Learning-Index)*

# 23.3 — Computer Vision: CNNs & Vision Transformers

> *"In vision, the first layers learn edges, the middle layers learn textures and parts, and the final layers learn objects — this hierarchy emerges automatically from data."*
> — **Yann LeCun**, *Gradient-Based Learning Applied to Document Recognition* (1998)

Convolutional Neural Networks exploit the spatial structure of images through local connectivity, weight sharing, and translation equivariance. This chapter derives the convolution operation mathematically, traces gradients through conv layers, and extends to modern Vision Transformers (ViTs) that apply self-attention to image patches.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Define the discrete 2D convolution operation with explicit index notation.
2. Compute output dimensions for conv layers given input size, kernel size, stride, and padding.
3. Derive the backward pass through a convolutional layer (gradient w.r.t. input and kernel).
4. Explain pooling operations and their effect on spatial dimensions and gradient flow.
5. Describe the architecture of LeNet, AlexNet, VGG, ResNet, and their key innovations.
6. Explain how Vision Transformers (ViT) tokenize images into patches and apply self-attention.
7. Compare inductive biases of CNNs (locality, translation equivariance) vs ViTs (global attention).

---

## 🖼️ Visual Anchor — Convolution Operation

![track-10__10.3-fig1](track-10__10.3-fig1.svg)

---

## 📚 1. Definitions

### Definition 23.3.1 — Discrete 2D Convolution (Cross-Correlation)

For input $I \in \mathbb{R}^{H \times W}$ and kernel $K \in \mathbb{R}^{k_H \times k_W}$, the **convolution** (technically cross-correlation in deep learning) is:

$$
(I * K)[i, j] = \sum_{m=0}^{k_H-1}\sum_{n=0}^{k_W-1} I[i+m, j+n] \cdot K[m, n]
$$

Output dimensions: $(I * K) \in \mathbb{R}^{(H-k_H+1) \times (W-k_W+1)}$.

### Definition 23.3.2 — Multi-Channel Convolution

For input $I \in \mathbb{R}^{C_{in} \times H \times W}$ and kernel $K \in \mathbb{R}^{C_{out} \times C_{in} \times k_H \times k_W}$:

$$
O[c_{out}, i, j] = b[c_{out}] + \sum_{c=0}^{C_{in}-1}\sum_{m=0}^{k_H-1}\sum_{n=0}^{k_W-1} I[c, i\cdot s+m, j\cdot s+n] \cdot K[c_{out}, c, m, n]
$$

where $s$ is the stride. Output: $O \in \mathbb{R}^{C_{out} \times H_{out} \times W_{out}}$.

### Definition 23.3.3 — Output Dimension Formula

$$
H_{out} = \left\lfloor\frac{H + 2P - k_H}{s}\right\rfloor + 1, \quad W_{out} = \left\lfloor\frac{W + 2P - k_W}{s}\right\rfloor + 1
$$

where $P$ = padding, $s$ = stride.

### Definition 23.3.4 — Pooling Operations

**Max pooling** with kernel $k$ and stride $s$:

$$
\text{MaxPool}(I)[i,j] = \max_{0 \leq m,n < k} I[i\cdot s + m, j\cdot s + n]
$$

**Average pooling:**

$$
\text{AvgPool}(I)[i,j] = \frac{1}{k^2}\sum_{m=0}^{k-1}\sum_{n=0}^{k-1} I[i\cdot s + m, j\cdot s + n]
$$

### Definition 23.3.5 — Receptive Field

The **receptive field** of a neuron in layer $\ell$ is the region of the input image that influences its activation. For a stack of $L$ conv layers with kernel size $k$ and stride 1:

$$
\text{RF} = 1 + L(k - 1)
$$

### Definition 23.3.6 — Vision Transformer (ViT) Patch Embedding

An image $I \in \mathbb{R}^{3 \times H \times W}$ is split into $N = HW/P^2$ non-overlapping patches of size $P \times P$. Each patch is flattened and linearly projected:

$$
\mathbf{z}_i = \mathbf{E}\text{vec}(\text{patch}_i) + \mathbf{e}_{pos}^i, \quad \mathbf{E} \in \mathbb{R}^{D \times (3P^2)}, \quad i = 1, \ldots, N
$$

These patch embeddings are then processed by a standard Transformer encoder.



---

## 📐 2. Axioms / Postulates

**Postulate 10.3.P1 (Translation Equivariance):** Convolution is equivariant to translation: if the input shifts by $(dx, dy)$, the output shifts by the same amount. Formally: $T_{dx,dy}(I) * K = T_{dx,dy}(I * K)$.

**Postulate 10.3.P2 (Locality Inductive Bias):** Natural images have local spatial correlations — nearby pixels are more related than distant ones. Convolution exploits this by restricting each neuron's receptive field to a local patch.

**Postulate 10.3.P3 (Hierarchical Feature Composition):** Complex visual features (faces, objects) are composed of simpler features (edges → textures → parts → objects). Deep CNNs learn this hierarchy layer by layer.

---

## 🛡️ 3. Lemmas

### Lemma 23.3.1 — Parameter Efficiency of Convolution

A conv layer with $C_{out}$ filters of size $C_{in} \times k \times k$ has:

$$
\text{Parameters} = C_{out} \times (C_{in} \times k^2 + 1)
$$

Compare to a fully-connected layer mapping the same spatial dimensions: $C_{out}H_{out}W_{out} \times C_{in}HW$ parameters — orders of magnitude more.

**Example:** Conv layer with $C_{in}=64$, $C_{out}=128$, $k=3$: $128 \times (64 \times 9 + 1) = 73,856$ parameters. Equivalent FC on $32\times32$ feature maps: $128 \times 32^2 \times 64 \times 32^2 \approx 5.4 \times 10^8$ parameters.

### Lemma 23.3.2 — Convolution as Matrix Multiplication (im2col)

The convolution $I * K$ can be expressed as matrix multiplication by rearranging input patches into columns:

$$
\text{im2col}(I) \in \mathbb{R}^{(C_{in} \cdot k^2) \times (H_{out} \cdot W_{out})}
$$

$$
K_{\text{reshaped}} \in \mathbb{R}^{C_{out} \times (C_{in} \cdot k^2)}
$$

$$
O_{\text{reshaped}} = K_{\text{reshaped}} \cdot \text{im2col}(I) \in \mathbb{R}^{C_{out} \times (H_{out} \cdot W_{out})}
$$

This is how cuDNN implements convolution efficiently on GPUs.

### Lemma 23.3.3 — Gradient of Max Pooling

For max pooling, the gradient routes entirely to the maximum element:

$$
\frac{\partial \text{MaxPool}(I)[i,j]}{\partial I[i\cdot s + m, j\cdot s + n]} = \begin{cases}1 & \text{if } (m,n) = \arg\max\\0 & \text{otherwise}\end{cases}
$$

---

## 👑 4. Theorems

### Theorem 23.3.1 — Convolution Theorem (Fourier Domain)

Convolution in the spatial domain equals element-wise multiplication in the frequency domain:

$$
\mathcal{F}(I * K) = \mathcal{F}(I) \odot \mathcal{F}(K)
$$

where $\mathcal{F}$ denotes the 2D Discrete Fourier Transform. This provides $O(N\log N)$ convolution for large kernels.

### Theorem 23.3.2 — ResNet Skip Connection Gradient Flow

In a residual block $\mathbf{y} = \mathbf{x} + F(\mathbf{x})$, the gradient satisfies:

$$
\frac{\partial \mathcal{L}}{\partial \mathbf{x}} = \frac{\partial \mathcal{L}}{\partial \mathbf{y}}\left(I + \frac{\partial F}{\partial \mathbf{x}}\right)
$$

The identity term $I$ ensures gradients flow directly from output to input without multiplicative decay, solving the vanishing gradient problem for very deep networks (100+ layers).

### Theorem 23.3.3 — ViT Computational Complexity

For an image with $N = H W / P^2$ patches and embedding dimension $D$:
- Self-attention: $O(N^2 D)$ — quadratic in number of patches
- CNN with kernel $k$: $O(N \cdot k^2 \cdot C^2)$ — linear in spatial size

ViTs are more expensive for high-resolution images but capture global dependencies from layer 1.

---

## ✍️ 5. Proofs / Derivations

### 5.1 Backward Pass Through Convolution

**Setup:** Input $I \in \mathbb{R}^{H \times W}$, kernel $K \in \mathbb{R}^{k \times k}$, output $O \in \mathbb{R}^{H_{out} \times W_{out}}$ where $O[i,j] = \sum_m\sum_n I[i+m, j+n]K[m,n]$.

Given upstream gradient $\frac{\partial\mathcal{L}}{\partial O} \in \mathbb{R}^{H_{out} \times W_{out}}$:

**Gradient w.r.t. kernel:**

$$
\frac{\partial\mathcal{L}}{\partial K[m,n]} = \sum_{i=0}^{H_{out}-1}\sum_{j=0}^{W_{out}-1} \frac{\partial\mathcal{L}}{\partial O[i,j]} \cdot I[i+m, j+n]
$$

This is itself a convolution: $\frac{\partial\mathcal{L}}{\partial K} = I * \frac{\partial\mathcal{L}}{\partial O}$ (with appropriate indexing).

**Gradient w.r.t. input:**

$$
\frac{\partial\mathcal{L}}{\partial I[p,q]} = \sum_{i,j: i+m=p, j+n=q} \frac{\partial\mathcal{L}}{\partial O[i,j]} \cdot K[m,n]
$$

$$
= \sum_{i=0}^{H_{out}-1}\sum_{j=0}^{W_{out}-1} \frac{\partial\mathcal{L}}{\partial O[i,j]} \cdot K[p-i, q-j]
$$

This is a **full convolution** (with zero-padding) of $\frac{\partial\mathcal{L}}{\partial O}$ with the **flipped** kernel $K_{\text{rot180}}$.

### 5.2 Derivation of Output Dimensions

**Step 1.** Input width $W$, kernel width $k$, stride $s$, padding $P$.

**Step 2.** After padding: effective width = $W + 2P$.

**Step 3.** The kernel can be placed at positions $j = 0, s, 2s, \ldots$ such that $j + k - 1 \leq W + 2P - 1$.

**Step 4.** Number of valid positions: $\lfloor(W + 2P - k)/s\rfloor + 1$.

**Example:** $W=32$, $k=5$, $s=2$, $P=2$: $\lfloor(32+4-5)/2\rfloor + 1 = \lfloor31/2\rfloor + 1 = 15 + 1 = 16$.

### 5.3 ResNet Residual Learning — Why It Works

**Problem:** Training a 56-layer plain CNN gives *higher* training error than a 20-layer CNN (not just overfitting — optimization failure).

**Key insight:** If the optimal function is close to identity, learning $F(x) = H(x) - x$ (the residual) is easier than learning $H(x)$ directly, because $F(x) \approx 0$ is a simpler target.

**Gradient analysis:** For a network with $L$ residual blocks:

$$
\frac{\partial\mathcal{L}}{\partial x_0} = \frac{\partial\mathcal{L}}{\partial x_L}\prod_{\ell=0}^{L-1}\left(1 + \frac{\partial F_\ell}{\partial x_\ell}\right)
$$

Expanding the product: every term contains a direct path (product of 1's) plus correction terms. The gradient never vanishes completely because the "1" terms provide a gradient highway.

### 5.4 ViT: From Pixels to Patch Tokens

**Step 1.** Split image $I \in \mathbb{R}^{3 \times 224 \times 224}$ into $14 \times 14 = 196$ patches of size $16 \times 16$.

**Step 2.** Flatten each patch: $\text{patch}_i \in \mathbb{R}^{3 \times 16 \times 16} \to \mathbb{R}^{768}$.

**Step 3.** Linear projection: $\mathbf{z}_i = \mathbf{E}\text{patch}_i + \mathbf{e}_{pos}^i$, $\mathbf{E} \in \mathbb{R}^{D \times 768}$.

**Step 4.** Prepend [CLS] token: sequence = $[\mathbf{z}_{cls}, \mathbf{z}_1, \ldots, \mathbf{z}_{196}] \in \mathbb{R}^{197 \times D}$.

**Step 5.** Process through $L$ Transformer encoder layers (see [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs)).

**Step 6.** Classification head on [CLS] output: $\hat{y} = \text{MLP}(\mathbf{z}_{cls}^{(L)})$.



---

## 💻 6. Code Examples

### Manual Conv2D Forward Pass

```python
import numpy as np

def conv2d_manual(input: np.ndarray, kernel: np.ndarray, stride: int = 1, padding: int = 0) -> np.ndarray:
    """
    Manual 2D convolution (single channel).
    input: (H, W), kernel: (kH, kW) -> output: (H_out, W_out)
    """
    H, W = input.shape          # e.g., (5, 5)
    kH, kW = kernel.shape       # e.g., (3, 3)
    
    # Apply padding
    if padding > 0:
        input = np.pad(input, padding, mode='constant')  # (H+2P, W+2P)
    
    H_pad, W_pad = input.shape
    H_out = (H_pad - kH) // stride + 1
    W_out = (W_pad - kW) // stride + 1
    output = np.zeros((H_out, W_out))  # shape: (H_out, W_out)
    
    for i in range(H_out):
        for j in range(W_out):
            # Extract receptive field
            patch = input[i*stride:i*stride+kH, j*stride:j*stride+kW]  # (kH, kW)
            output[i, j] = np.sum(patch * kernel)  # element-wise multiply and sum
    
    return output

# Example: Sobel edge detection
image = np.array([
    [1, 0, 2, 3, 1],
    [1, 1, 0, 1, 0],
    [3, 0, 1, 2, 1],
    [0, 2, 1, 0, 3],
    [1, 1, 0, 1, 2]
], dtype=float)

sobel_x = np.array([-1, 0, 1], [-2, 0, 2], [-1, 0, 1](-1,-0,-1],-[-2,-0,-2],-[-1,-0,-1), dtype=float)
edges = conv2d_manual(image, sobel_x)
print(f"Input shape: {image.shape}")       # (5, 5)
print(f"Kernel shape: {sobel_x.shape}")    # (3, 3)
print(f"Output shape: {edges.shape}")      # (3, 3)
print(f"Output:\n{edges}")
```

### PyTorch CNN Forward Pass with Shape Annotations

```python
import torch
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # Conv layers
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)   # (1,28,28) -> (16,28,28)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)  # (16,14,14) -> (32,14,14)
        self.pool = nn.MaxPool2d(2, 2)                             # halves spatial dims
        self.fc1 = nn.Linear(32 * 7 * 7, 128)                     # (32*7*7,) -> (128,)
        self.fc2 = nn.Linear(128, 10)                              # (128,) -> (10,)
    
    def forward(self, x):
        # x: (B, 1, 28, 28) — batch of MNIST images
        x = self.pool(torch.relu(self.conv1(x)))  # (B,1,28,28) -> (B,16,28,28) -> (B,16,14,14)
        x = self.pool(torch.relu(self.conv2(x)))  # (B,16,14,14) -> (B,32,14,14) -> (B,32,7,7)
        x = x.view(x.size(0), -1)                 # (B, 32*7*7) = (B, 1568)
        x = torch.relu(self.fc1(x))               # (B, 128)
        x = self.fc2(x)                            # (B, 10)
        return x

model = SimpleCNN()
dummy = torch.randn(4, 1, 28, 28)  # batch of 4 MNIST images
out = model(dummy)
print(f"Output shape: {out.shape}")  # torch.Size([4, 10])
print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
```

> **See also:** `_practice/scripts/10.3_cnn_vit.py` for conv2d math worked out by hand.

---

## 🧮 7. Worked Examples

### Example 23.3.E1 — Manual Convolution Computation

<details>
<summary>🔍 Full Solution: 3×3 kernel on 4×4 input</summary>

**Input:**

$$
I = \begin{pmatrix}1&2&0&1\\3&1&2&0\\0&1&3&2\\2&0&1&1\end{pmatrix}, \quad K = \begin{pmatrix}1&0&-1\\1&0&-1\\1&0&-1\end{pmatrix}
$$

**Output size:** $(4-3+1) \times (4-3+1) = 2 \times 2$.

**Position (0,0):**

$$
O[0,0] = 1(1)+2(0)+0(-1)+3(1)+1(0)+2(-1)+0(1)+1(0)+3(-1) = 1+0+0+3+0-2+0+0-3 = -1
$$

**Position (0,1):**

$$
O[0,1] = 2(1)+0(0)+1(-1)+1(1)+2(0)+0(-1)+1(1)+3(0)+2(-1) = 2+0-1+1+0+0+1+0-2 = 1
$$

**Position (1,0):**

$$
O[1,0] = 3(1)+1(0)+2(-1)+0(1)+1(0)+3(-1)+2(1)+0(0)+1(-1) = 3+0-2+0+0-3+2+0-1 = -1
$$

**Position (1,1):**

$$
O[1,1] = 1(1)+2(0)+0(-1)+1(1)+3(0)+2(-1)+0(1)+1(0)+1(-1) = 1+0+0+1+0-2+0+0-1 = -1
$$

$$
O = \begin{pmatrix}-1&1\\-1&-1\end{pmatrix}
$$

</details>

### Example 23.3.E2 — Output Dimension Calculation

<details>
<summary>🔍 Full Solution: VGG-style conv stack</summary>

**Problem:** Input $224 \times 224 \times 3$. Apply: Conv(64, 3×3, pad=1) → Conv(64, 3×3, pad=1) → MaxPool(2×2) → Conv(128, 3×3, pad=1) → MaxPool(2×2).

**After Conv1:** $\lfloor(224+2-3)/1\rfloor+1 = 224$. Shape: $224 \times 224 \times 64$.

**After Conv2:** Same padding → $224 \times 224 \times 64$.

**After Pool1:** $224/2 = 112$. Shape: $112 \times 112 \times 64$.

**After Conv3:** $\lfloor(112+2-3)/1\rfloor+1 = 112$. Shape: $112 \times 112 \times 128$.

**After Pool2:** $112/2 = 56$. Shape: $56 \times 56 \times 128$.

**Parameter count:**
- Conv1: $64 \times (3 \times 3^2 + 1) = 1,792$
- Conv2: $64 \times (64 \times 9 + 1) = 36,928$
- Conv3: $128 \times (64 \times 9 + 1) = 73,856$
- Total: $112,576$

</details>

### Example 23.3.E3 — Receptive Field Calculation

<details>
<summary>🔍 Full Solution: 3 conv layers with stride</summary>

**Problem:** Three conv layers: Conv(3×3, s=1) → Conv(3×3, s=2) → Conv(3×3, s=1). What is the receptive field of a single output neuron?

**Layer 1 (s=1, k=3):** Each output neuron sees a 3×3 region.

**Layer 2 (s=2, k=3):** Each neuron sees 3 neurons from layer 1, but stride 2 means they're spaced 2 apart. RF at input: $3 + (3-1) \times 2 = 7$ (each of the 3 layer-1 positions covers 3 pixels, spaced by stride 2).

More precisely, using the recursive formula: $RF_\ell = RF_{\ell-1} + (k_\ell - 1) \times \prod_{i=1}^{\ell-1} s_i$:

- $RF_1 = 3$
- $RF_2 = 3 + (3-1) \times 1 = 5$... 

Actually the standard formula: $RF_L = 1 + \sum_{\ell=1}^L (k_\ell - 1)\prod_{i=1}^{\ell-1}s_i$:

- $RF = 1 + (3-1)\cdot1 + (3-1)\cdot1 + (3-1)\cdot2 = 1 + 2 + 2 + 4 = 9$

Wait — let me reorder. Layers from input to output: L1(k=3,s=1), L2(k=3,s=2), L3(k=3,s=1).

$RF = 1 + (k_1-1)s_0 + (k_2-1)s_0 s_1 + ... $ — working backwards:

$RF = 1 + \sum_{\ell=1}^3 (k_\ell - 1)\prod_{j=1}^{\ell-1}s_j = 1 + 2\cdot1 + 2\cdot1 + 2\cdot2 = 1+2+2+4 = 9$

**Answer:** Receptive field = $9 \times 9$ pixels.

</details>

### Example 23.3.E4 — ViT Patch Count and Sequence Length

<details>
<summary>🔍 Full Solution: ViT-Base on ImageNet</summary>

**Problem:** ViT-Base with image size 224×224, patch size 16×16, embedding dim 768.

**Patch count:** $N = (224/16)^2 = 14^2 = 196$ patches.

**Sequence length:** $196 + 1 = 197$ (including [CLS] token).

**Patch embedding parameters:** $E \in \mathbb{R}^{768 \times (3 \times 16^2)} = \mathbb{R}^{768 \times 768}$: $768^2 = 589,824$ params.

**Positional embedding:** $197 \times 768 = 151,296$ params.

**Self-attention FLOPs per layer:** $O(N^2 D) = O(197^2 \times 768) \approx 30M$ multiply-adds.

**Total ViT-Base params (12 layers, 12 heads):** ~86M parameters.

</details>

---

## 🔗 8. Cross-links & Further Reading

### Internal Cross-links
- Convolution as linear operation: [2.2 - Matrix Operations & Algebra](2.2---Matrix-Operations-&-Algebra)
- Fourier transform for convolution theorem: [1.5 - Integral Calculus & Techniques](1.5---Integral-Calculus-&-Techniques)
- Backpropagation through conv layers: [23.2 - Deep Neural Networks - Backprop & Architecture](23.2---Deep-Neural-Networks---Backprop-&-Architecture)
- Self-attention in ViT: [23.5 - Transformer Architectures & LLMs](23.5---Transformer-Architectures-&-LLMs)
- Optimization for training CNNs: [23.1 - Statistical Learning & Optimization](23.1---Statistical-Learning-&-Optimization)

### External References
- **LeCun et al. (1998)** — *Gradient-Based Learning Applied to Document Recognition* (LeNet)
- **He et al. (2016)** — *Deep Residual Learning for Image Recognition* ([arXiv:1512.03385](https://arxiv.org/abs/1512.03385))
- **Dosovitskiy et al. (2021)** — *An Image is Worth 16x16 Words* (ViT, [arXiv:2010.11929](https://arxiv.org/abs/2010.11929))
- **Stanford CS231n** — Convolutional Neural Networks for Visual Recognition ([cs231n.stanford.edu](https://cs231n.stanford.edu/))
- **Goodfellow et al.** — *Deep Learning*, Chapter 9: Convolutional Networks

---

## ⚠️ Common Pitfalls

### Pitfall 1 — Forgetting to Account for Padding in Output Size

With "same" padding ($P = \lfloor k/2 \rfloor$) and stride 1, output size equals input size. But with stride > 1, even "same" padding reduces dimensions. Always use the formula explicitly.

### Pitfall 2 — Channel Dimension Confusion

PyTorch uses NCHW (batch, channels, height, width). TensorFlow uses NHWC by default. Transposing between them is a common source of bugs. Always annotate tensor shapes in comments.

### Pitfall 3 — Receptive Field vs. Effective Receptive Field

The theoretical receptive field grows linearly with depth, but the **effective** receptive field (where gradients actually flow significantly) is much smaller — typically Gaussian-shaped and concentrated in the center. Deep networks need many layers to truly "see" the full input.

### Pitfall 4 — ViT Data Hunger

ViTs lack the inductive biases of CNNs (locality, translation equivariance). They need much more training data to match CNN performance. ViT-Base trained on ImageNet-1K alone underperforms ResNet-50. It only excels when pre-trained on ImageNet-21K or JFT-300M.

---

## 📝 CNN Architecture Evolution

| Model | Year | Depth | Key Innovation | Top-5 Error |
|-------|------|-------|---------------|-------------|
| LeNet-5 | 1998 | 5 | First practical CNN | — |
| AlexNet | 2012 | 8 | ReLU, dropout, GPU training | 16.4% |
| VGG-16 | 2014 | 16 | 3×3 convs only, depth matters | 7.3% |
| GoogLeNet | 2014 | 22 | Inception modules (multi-scale) | 6.7% |
| ResNet-152 | 2015 | 152 | Skip connections | 3.6% |
| EfficientNet | 2019 | — | Compound scaling (depth×width×resolution) | 2.9% |
| ViT-L/16 | 2021 | 24 | Pure attention, no convolutions | 2.5% |

**Key insight:** The progression shows that depth (with proper gradient flow via skip connections) and scale (with proper data) are the dominant factors in vision performance.



---

## 🧠 9. Extended Worked Examples & Deep Dives

### Example 9.1 — Conv2D Output Shape Arithmetic with Stride, Padding, and Dilation

**Problem:** Compute the output spatial dimensions for a Conv2D layer with:
- Input: $H_{in} = 32, W_{in} = 32, C_{in} = 3$
- Kernel: $k = 5 \times 5$
- Stride: $s = 2$
- Padding: $p = 2$
- Dilation: $d = 3$
- Number of filters: $C_{out} = 64$

Also compute the total number of parameters and FLOPs.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: The General Output Dimension Formula

$$
H_{out} = \left\lfloor \frac{H_{in} + 2p - d(k-1) - 1}{s} + 1 \right\rfloor
$$

This formula accounts for:
- $2p$: padding adds $p$ pixels on each side
- $d(k-1) + 1$: the effective kernel size with dilation (dilation inserts $d-1$ zeros between kernel elements)
- $s$: stride determines how many positions the kernel visits

#### Step 2: Compute Effective Kernel Size

With dilation $d = 3$ and kernel size $k = 5$:

$$
k_{eff} = d(k - 1) + 1 = 3(5 - 1) + 1 = 3(4) + 1 = 13
$$

The $5 \times 5$ kernel with dilation 3 has the same receptive field as a $13 \times 13$ kernel, but with only 25 non-zero weights.

#### Step 3: Apply the Formula

$$
H_{out} = \left\lfloor \frac{32 + 2(2) - 13 - 1}{2} + 1 \right\rfloor = \left\lfloor \frac{32 + 4 - 13 - 1}{2} + 1 \right\rfloor
$$

$$
= \left\lfloor \frac{22}{2} + 1 \right\rfloor = \left\lfloor 11 + 1 \right\rfloor = 12
$$

By symmetry (square input, square kernel): $W_{out} = 12$.

Output tensor shape: $(64, 12, 12)$ — that is, 64 channels each of spatial size $12 \times 12$.

#### Step 4: Parameter Count

Each filter has shape $(C_{in}, k, k)$ plus one bias:

$$
\text{Params} = C_{out} \times (C_{in} \times k \times k + 1) = 64 \times (3 \times 5 \times 5 + 1) = 64 \times 76 = 4{,}864
$$

#### Step 5: FLOPs (Multiply-Accumulate Operations)

Each output pixel requires $C_{in} \times k \times k$ multiplications and the same number of additions:

$$
\text{FLOPs} = 2 \times C_{out} \times H_{out} \times W_{out} \times C_{in} \times k \times k
$$

$$
= 2 \times 64 \times 12 \times 12 \times 3 \times 5 \times 5 = 2 \times 64 \times 144 \times 75 = 1{,}382{,}400
$$

**Final Answer:**

$$
\text{Output shape: } (64, 12, 12), \quad \text{Params: } 4{,}864, \quad \text{FLOPs: } 1.38\text{M}
$$

</details>

### Example 9.2 — Im2col: Reformulating Convolution as Matrix Multiplication

**Problem:** Show how a $3 \times 3$ convolution on a $4 \times 4$ single-channel input with stride 1 and no padding can be expressed as a matrix multiplication using the im2col transformation. Construct the explicit matrices.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Define the Input and Kernel

Input $X$ ($4 \times 4$, single channel):

$$
X = \begin{bmatrix} 1 & 2 & 3 & 4 \\ 5 & 6 & 7 & 8 \\ 9 & 10 & 11 & 12 \\ 13 & 14 & 15 & 16 \end{bmatrix}
$$

Kernel $K$ ($3 \times 3$):

$$
K = \begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}
$$

Output size: $H_{out} = W_{out} = 4 - 3 + 1 = 2$, so output is $2 \times 2$.

#### Step 2: Standard Convolution Output

$$
Y_{11} = a(1) + b(2) + c(3) + d(5) + e(6) + f(7) + g(9) + h(10) + i(11)
$$

$$
Y_{12} = a(2) + b(3) + c(4) + d(6) + e(7) + f(8) + g(10) + h(11) + i(12)
$$

$$
Y_{21} = a(5) + b(6) + c(7) + d(9) + e(10) + f(11) + g(13) + h(14) + i(15)
$$

$$
Y_{22} = a(6) + b(7) + c(8) + d(10) + e(11) + f(12) + g(14) + h(15) + i(16)
$$

#### Step 3: Im2col Transformation

The im2col operation extracts each receptive field patch and lays it as a column (or row). Each patch is a $k^2 = 9$ element vector. With 4 output positions, we get a $(9 \times 4)$ matrix:

$$
\text{Im2col}(X) = \begin{bmatrix} 1 & 2 & 5 & 6 \\ 2 & 3 & 6 & 7 \\ 3 & 4 & 7 & 8 \\ 5 & 6 & 9 & 10 \\ 6 & 7 & 10 & 11 \\ 7 & 8 & 11 & 12 \\ 9 & 10 & 13 & 14 \\ 10 & 11 & 14 & 15 \\ 11 & 12 & 15 & 16 \end{bmatrix}
$$

Each column corresponds to one output position's receptive field, read row-by-row from the input.

#### Step 4: Reshape Kernel to Row Vector

Flatten the kernel into a $(1 \times 9)$ row vector:

$$
\text{vec}(K)^T = \begin{bmatrix} a & b & c & d & e & f & g & h & i \end{bmatrix}
$$

#### Step 5: Matrix Multiplication Gives Convolution Output

$$
Y_{\text{flat}} = \text{vec}(K)^T \cdot \text{Im2col}(X)
$$

This is a $(1 \times 9) \times (9 \times 4) = (1 \times 4)$ matrix, which we reshape to $(2 \times 2)$.

#### Step 6: Multi-Channel and Multi-Filter Extension

For $C_{in}$ input channels and $C_{out}$ filters:
- Im2col matrix: $(C_{in} \cdot k^2) \times (H_{out} \cdot W_{out})$
- Weight matrix: $C_{out} \times (C_{in} \cdot k^2)$
- Output: $C_{out} \times (H_{out} \cdot W_{out})$, reshaped to $(C_{out}, H_{out}, W_{out})$

**Why this matters:** GPUs are optimized for large matrix multiplications (GEMM). Im2col trades memory (the column matrix has redundant copies of input values) for compute efficiency by leveraging highly optimized BLAS routines.

**Final Answer:**

$$
\text{Conv2D}(X, K) = \text{reshape}\left( W_{\text{flat}} \cdot \text{Im2col}(X), \; (C_{out}, H_{out}, W_{out}) \right)
$$

</details>


### Example 9.3 — Receptive Field Calculation Across Multiple Layers

**Problem:** Compute the receptive field of a neuron in the final feature map of a network with the following architecture:
- Layer 1: Conv $3 \times 3$, stride 1, padding 1
- Layer 2: Conv $3 \times 3$, stride 1, padding 1
- Layer 3: MaxPool $2 \times 2$, stride 2
- Layer 4: Conv $3 \times 3$, stride 1, padding 1
- Layer 5: Conv $3 \times 3$, stride 1, padding 1

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Receptive Field Recurrence Formula

The receptive field $r_l$ at layer $l$ is computed backwards from the output:

$$
r_{l-1} = r_l + (k_l - 1) \times j_{l-1}
$$

where $j_l$ is the **jump** (product of all strides up to layer $l$):

$$
j_l = \prod_{i=1}^{l} s_i
$$

We start with $r_L = 1$ (a single output pixel) and work backwards.

#### Step 2: Compute Jumps (Forward)

$$
j_0 = 1 \quad \text{(input pixel spacing)}
$$

$$
j_1 = j_0 \times s_1 = 1 \times 1 = 1
$$

$$
j_2 = j_1 \times s_2 = 1 \times 1 = 1
$$

$$
j_3 = j_2 \times s_3 = 1 \times 2 = 2
$$

$$
j_4 = j_3 \times s_4 = 2 \times 1 = 2
$$

$$
j_5 = j_4 \times s_5 = 2 \times 1 = 2
$$

#### Step 3: Compute Receptive Field (Backward from output)

Starting with $r_5 = 1$:

$$
r_4 = r_5 + (k_5 - 1) \times j_4 = 1 + (3-1) \times 2 = 1 + 4 = 5
$$

$$
r_3 = r_4 + (k_4 - 1) \times j_3 = 5 + (3-1) \times 2 = 5 + 4 = 9
$$

$$
r_2 = r_3 + (k_3 - 1) \times j_2 = 9 + (2-1) \times 1 = 9 + 1 = 10
$$

$$
r_1 = r_2 + (k_2 - 1) \times j_1 = 10 + (3-1) \times 1 = 10 + 2 = 12
$$

$$
r_0 = r_1 + (k_1 - 1) \times j_0 = 12 + (3-1) \times 1 = 12 + 2 = 14
$$

#### Step 4: Interpretation

Each neuron in the final feature map "sees" a $14 \times 14$ pixel region of the original input. The pooling layer doubles the effective stride, causing subsequent convolutions to cover more input space per layer.

**Final Answer:**

$$
\text{Receptive field} = 14 \times 14 \text{ pixels}
$$

</details>

### Example 9.4 — Max-Pool and Average-Pool Backward Pass

**Problem:** Given a $4 \times 4$ feature map that undergoes $2 \times 2$ max-pooling and average-pooling (stride 2), compute the backward pass gradient routing for both operations given a $2 \times 2$ upstream gradient.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Define Input Feature Map

$$
F = \begin{bmatrix} 1 & 3 & 2 & 4 \\ 5 & 6 & 7 & 8 \\ 3 & 2 & 1 & 0 \\ 9 & 4 & 6 & 3 \end{bmatrix}
$$

#### Step 2: Max-Pool Forward Pass

Partition into $2 \times 2$ blocks and take the maximum:

- Block $(1,1)$: $\max(1, 3, 5, 6) = 6$ at position $(2,2)$
- Block $(1,2)$: $\max(2, 4, 7, 8) = 8$ at position $(2,4)$
- Block $(2,1)$: $\max(3, 2, 9, 4) = 9$ at position $(4,1)$
- Block $(2,2)$: $\max(1, 0, 6, 3) = 6$ at position $(3,3)$

$$
\text{MaxPool}(F) = \begin{bmatrix} 6 & 8 \\ 9 & 6 \end{bmatrix}
$$

#### Step 3: Max-Pool Backward Pass

Given upstream gradient:

$$
\frac{\partial \mathcal{L}}{\partial Y} = \begin{bmatrix} g_{11} & g_{12} \\ g_{21} & g_{22} \end{bmatrix}
$$

The gradient is routed **only to the position that achieved the maximum** (winner-take-all):

$$
\frac{\partial \mathcal{L}}{\partial F} = \begin{bmatrix} 0 & 0 & 0 & 0 \\ 0 & g_{11} & 0 & g_{12} \\ 0 & 0 & g_{22} & 0 \\ g_{21} & 0 & 0 & 0 \end{bmatrix}
$$

All non-maximum positions receive zero gradient. This is why max-pool creates sparse gradients.

#### Step 4: Average-Pool Forward Pass

$$
\text{AvgPool}(F) = \begin{bmatrix} \frac{1+3+5+6}{4} & \frac{2+4+7+8}{4} \\ \frac{3+2+9+4}{4} & \frac{1+0+6+3}{4} \end{bmatrix} = \begin{bmatrix} 3.75 & 5.25 \\ 4.5 & 2.5 \end{bmatrix}
$$

#### Step 5: Average-Pool Backward Pass

Each input in a block contributed equally ($\frac{1}{4}$) to the output, so the gradient is distributed uniformly:

$$
\frac{\partial \mathcal{L}}{\partial F} = \begin{bmatrix} g_{11}/4 & g_{11}/4 & g_{12}/4 & g_{12}/4 \\ g_{11}/4 & g_{11}/4 & g_{12}/4 & g_{12}/4 \\ g_{21}/4 & g_{21}/4 & g_{22}/4 & g_{22}/4 \\ g_{21}/4 & g_{21}/4 & g_{22}/4 & g_{22}/4 \end{bmatrix}
$$

**Final Answer:** Max-pool routes gradients to argmax positions (sparse); average-pool distributes gradients uniformly (dense). Max-pool preserves stronger signals but loses spatial precision; average-pool preserves all spatial information equally.

</details>

### Example 9.5 — ViT Patch Embedding: Sequence Length and Dimensionality

**Problem:** For a Vision Transformer (ViT-B/16) processing a $224 \times 224 \times 3$ RGB image with patch size $P = 16$ and embedding dimension $D = 768$, derive: (a) the number of patches (sequence length), (b) the patch embedding projection dimensions, (c) total parameters in the embedding layer, and (d) the effect of adding a [CLS] token and positional embeddings.

<details>
<summary>🔍 Full step-by-step solution</summary>

#### Step 1: Number of Patches (Sequence Length)

The image is divided into a grid of non-overlapping $P \times P$ patches:

$$
N = \frac{H}{P} \times \frac{W}{P} = \frac{224}{16} \times \frac{224}{16} = 14 \times 14 = 196
$$

Each patch is a $16 \times 16 \times 3 = 768$-dimensional vector when flattened.

#### Step 2: Patch Embedding Projection

Each flattened patch $\mathbf{p}_i \in \mathbb{R}^{P^2 \cdot C}$ is linearly projected to dimension $D$:

$$
\mathbf{z}_i = E \mathbf{p}_i + \mathbf{b}_E, \quad E \in \mathbb{R}^{D \times (P^2 \cdot C)}
$$

$$
E \in \mathbb{R}^{768 \times 768}
$$

In this specific case, the input dimension $P^2 \cdot C = 16^2 \times 3 = 768$ happens to equal the embedding dimension $D = 768$, so $E$ is a square matrix. This is a coincidence of ViT-B/16's design.

#### Step 3: Parameters in the Embedding Layer

$$
\text{Params}(E) = D \times (P^2 \cdot C) + D = 768 \times 768 + 768 = 590{,}592 + 768 = 591{,}360
$$

This is equivalent to a Conv2D with kernel size $16 \times 16$, stride 16, and 768 output channels:

$$
\text{Conv2D}(C_{in}=3, C_{out}=768, k=16, s=16): \quad 768 \times (3 \times 16 \times 16) + 768 = 591{,}360 \; \checkmark
$$

#### Step 4: Adding [CLS] Token

A learnable classification token $\mathbf{z}_{\text{cls}} \in \mathbb{R}^D$ is prepended to the sequence:

$$
\mathbf{Z}_0 = [\mathbf{z}_{\text{cls}}; \; \mathbf{z}_1; \; \mathbf{z}_2; \; \ldots; \; \mathbf{z}_{196}] \in \mathbb{R}^{197 \times 768}
$$

Total sequence length becomes $N + 1 = 197$.

#### Step 5: Positional Embeddings

Learnable positional embeddings $E_{pos} \in \mathbb{R}^{(N+1) \times D}$ are added element-wise:

$$
\mathbf{Z}_0' = \mathbf{Z}_0 + E_{pos}
$$

$$
\text{Params}(E_{pos}) = 197 \times 768 = 151{,}296
$$

#### Step 6: Total Embedding Parameters

$$
\text{Total} = \underbrace{591{,}360}_{\text{patch proj}} + \underbrace{768}_{\text{[CLS] token}} + \underbrace{151{,}296}_{\text{pos embed}} = 743{,}424
$$

#### Step 7: Memory and Compute for Self-Attention

The self-attention in each transformer block operates on the $(197 \times 768)$ sequence. The attention matrix is:

$$
A \in \mathbb{R}^{197 \times 197} \quad \text{(per head)}
$$

Memory for attention scores (float32, 12 heads): $12 \times 197 \times 197 \times 4 \text{ bytes} = 1.87 \text{ MB per image}$

**Final Answer:**

$$
N = 196 \text{ patches}, \quad \text{Sequence length} = 197 \text{ (with [CLS])}, \quad \text{Embedding params} = 743{,}424
$$

</details>



---

## 📘 10. Appendix: Extended Derivations & Special Cases

### 23.1 Translation Equivariance vs Invariance: Formal Proofs

**Definition (Equivariance):** A function $f$ is equivariant to a transformation $T$ if applying $T$ to the input produces the same transformation in the output:

$$
f(T(x)) = T(f(x))
$$

**Definition (Invariance):** A function $f$ is invariant to $T$ if the output is unchanged:

$$
f(T(x)) = f(x)
$$

**Theorem:** Convolution is translation-equivariant.

**Proof:** Let $T_\tau$ denote translation by $\tau$: $(T_\tau x)(t) = x(t - \tau)$.

The convolution of $x$ with kernel $k$ is:

$$
(x * k)(t) = \int x(s) k(t - s) \, ds
$$

Applying translation to the input:

$$
(T_\tau x * k)(t) = \int x(s - \tau) k(t - s) \, ds
$$

Substituting $u = s - \tau$ (so $s = u + \tau$, $ds = du$):

$$
= \int x(u) k(t - u - \tau) \, du = (x * k)(t - \tau) = T_\tau(x * k)(t)
$$

Therefore: $\text{Conv}(T_\tau(x)) = T_\tau(\text{Conv}(x))$ — convolution is translation-equivariant. $\square$

**Corollary:** Global average pooling converts equivariance to invariance. If $f$ is equivariant and $g(y) = \frac{1}{|y|}\sum_i y_i$, then $g(f(T_\tau(x))) = g(T_\tau(f(x))) = g(f(x))$ since the mean is translation-invariant.

**Why ViTs lack built-in equivariance:** Self-attention computes $\text{softmax}(QK^T/\sqrt{d})V$. Permuting the input sequence permutes $Q$, $K$, $V$ identically, making attention permutation-equivariant but NOT translation-equivariant in the spatial sense. Positional embeddings break even permutation equivariance. ViTs must learn translation equivariance from data, which is why they require more training data than CNNs.

### 23.2 Depthwise-Separable Convolution: Efficiency Derivation

**Standard convolution** with $C_{in}$ input channels, $C_{out}$ output channels, kernel $k \times k$:

$$
\text{Params}_{\text{std}} = C_{out} \times C_{in} \times k^2
$$

$$
\text{FLOPs}_{\text{std}} = C_{out} \times C_{in} \times k^2 \times H_{out} \times W_{out}
$$

**Depthwise-separable convolution** decomposes this into:

1. **Depthwise conv:** One $k \times k$ filter per input channel (no cross-channel mixing):

$$
\text{Params}_{\text{dw}} = C_{in} \times k^2
$$

2. **Pointwise conv:** $1 \times 1$ convolution to mix channels:

$$
\text{Params}_{\text{pw}} = C_{out} \times C_{in}
$$

**Total:**

$$
\text{Params}_{\text{sep}} = C_{in} \times k^2 + C_{out} \times C_{in} = C_{in}(k^2 + C_{out})
$$

**Reduction ratio:**

$$
\frac{\text{Params}_{\text{sep}}}{\text{Params}_{\text{std}}} = \frac{C_{in}(k^2 + C_{out})}{C_{out} \times C_{in} \times k^2} = \frac{1}{C_{out}} + \frac{1}{k^2}
$$

For typical values ($C_{out} = 256$, $k = 3$):

$$
\text{Ratio} = \frac{1}{256} + \frac{1}{9} \approx 0.004 + 0.111 = 0.115
$$

Depthwise-separable convolutions use approximately **8.7× fewer parameters and FLOPs** than standard convolutions. This is the foundation of MobileNet's efficiency.

### 23.3 FLOPs and Parameters: ResNet-50 vs ViT-B/16

**ResNet-50:**
- Total parameters: ~25.6M
- FLOPs (224×224 input): ~4.1 GFLOPs
- Dominated by the $3 \times 3$ convolutions in bottleneck blocks
- Parameter formula for one bottleneck block (channels $c$, bottleneck ratio 4):

$$
\text{Params}_{\text{block}} = 1 \times 1 \times c \times \frac{c}{4} + 3 \times 3 \times \frac{c}{4} \times \frac{c}{4} + 1 \times 1 \times \frac{c}{4} \times c = \frac{c^2}{4} + \frac{9c^2}{16} + \frac{c^2}{4} = \frac{17c^2}{16}
$$

**ViT-B/16:**
- Total parameters: ~86M
- FLOPs (224×224 input): ~17.6 GFLOPs
- Dominated by self-attention and MLP blocks
- Per transformer block (dimension $D = 768$, MLP ratio 4):

$$
\text{Params}_{\text{attn}} = 4D^2 = 4(768)^2 = 2{,}359{,}296 \quad \text{(Q, K, V, output projections)}
$$

$$
\text{Params}_{\text{MLP}} = 2 \times D \times 4D = 8D^2 = 8(768)^2 = 4{,}718{,}592
$$

$$
\text{Params per block} = 12D^2 = 7{,}077{,}888
$$

$$
\text{Total (12 blocks)} = 12 \times 12D^2 = 144D^2 \approx 84.9\text{M}
$$

**Key insight:** ViT has 3.4× more parameters and 4.3× more FLOPs than ResNet-50, yet achieves better accuracy when pre-trained on large datasets (JFT-300M). The quadratic attention cost $O(N^2 D)$ with $N = 197$ is manageable for $224 \times 224$ images but becomes prohibitive for high-resolution inputs without windowed attention (Swin Transformer).

---
