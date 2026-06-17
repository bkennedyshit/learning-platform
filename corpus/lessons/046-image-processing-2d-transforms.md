---
title: "04.6 — Image Processing & 2D Transforms"
subject: "Signal Processing & DSP"
catalog: advanced
audience_tier: higher-education
chapter: "04.6"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [00 - 09 - Learning Index](00---09---Learning-Index)*

# 04.6 — Image Processing & 2D Transforms

> *"An image is just a 2D signal. The Fourier Transform doesn't know the difference — but you do, because frequency means spatial frequency now: how rapidly pixel values change across space."*

The Fourier machinery of [04.2](04.2---Fourier-Series-&-Fourier-Transform) and [04.3](04.3---Discrete-Fourier-Transform-&-FFT) extends directly to two dimensions. Images become tractable with exactly the same tools: 2D DFT, 2D convolution, 2D filtering. This chapter also connects to [Track 23](Subject_Plan) — holographic wavefront propagation *is* 2D Fourier optics.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Write and interpret the **2D DFT** equation; locate DC and spatial frequency components in the 2D spectrum.
2. Apply the **2D Convolution Theorem** to understand image filtering as spectrum multiplication.
3. Implement **Gaussian blur**, **Sobel edge detection**, and **Laplacian sharpening** with 2D convolution kernels.
4. Compute the 2D DFT of an image in Python and visualise the **log-magnitude spectrum**.
5. Understand the connection between the 2D DFT and **Fourier optics / holographic propagation**.
6. Apply **separable filters** for efficient 2D convolution.

---

## 🖼️ Visual Anchor

![dsp__32.6-fig1](dsp__32.6-fig1.svg)

*Diagram: 2D DFT formula and interpretation (DC centre, low/high frequency regions). Image filtering pipeline: image → 2D FFT → multiply by H[u,v] → IFFT → filtered image. Common 3×3 kernels (Gaussian, Sobel X/Y, Laplacian). Bottom: checkerboard image → Sobel X response → Sobel Y response → combined edge map.*

---

## 📚 1. The 2D Discrete Fourier Transform

### 1.1 Definition

For an M×N image f[m,n] (m = row, n = column), the **2D DFT** is:

```
F[u, v] = Σ_{m=0}^{M−1} Σ_{n=0}^{N−1}  f[m,n] · e^{−j2π(um/M + vn/N)}
```

and the **Inverse 2D DFT**:

```
f[m, n] = (1/MN) Σ_{u=0}^{M−1} Σ_{v=0}^{N−1}  F[u,v] · e^{j2π(um/M + vn/N)}
```

### 1.2 Interpretation

| Location in F[u,v] | Meaning |
|--------------------|---------|
| **F[0, 0]** (DC) | Sum of all pixel values (mean brightness × MN) |
| **Center after fftshift** | DC component visible in the middle |
| **Low spatial frequencies** (near center) | Slowly varying regions: backgrounds, gradients |
| **High spatial frequencies** (near edges) | Rapidly varying: edges, sharp textures, noise |
| **Horizontal lines in image** | Vertical stripes in spectrum (perpendicular) |

### 1.3 Separability of the 2D DFT

The 2D DFT is **separable**: it can be computed as M 1D DFTs along rows, then N 1D DFTs along columns (or vice versa). This means `numpy.fft.fft2` internally calls `fft` twice, and the algorithm is O(MN log(MN)).

```python
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Load grayscale image
img = np.array(Image.open("image.png").convert("L"), dtype=float)

# 2D FFT with DC shifted to center
F = np.fft.fft2(img)
F_shifted = np.fft.fftshift(F)

# Log-magnitude spectrum (log to see wide dynamic range)
magnitude = 20 * np.log10(np.abs(F_shifted) + 1)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray'); plt.title("Original image"); plt.axis('off')
plt.subplot(1, 2, 2)
plt.imshow(magnitude, cmap='inferno')
plt.title("Log-Magnitude Spectrum (DC centered)")
plt.colorbar(label='dB'); plt.axis('off')
plt.tight_layout(); plt.show()
```

---

## 📚 2. Image Filtering via 2D Convolution

### 2.1 2D Convolution Theorem

Exactly as in 1D, convolution in the spatial domain equals multiplication in the frequency domain:

```
f[m,n] ** g[m,n]   ⟺   F[u,v] · G[u,v]
```

where ** denotes 2D convolution. This enables **fast image filtering**:

1. Compute F = 2D FFT of image.
2. Compute H = 2D FFT of kernel (zero-padded to image size).
3. Multiply element-wise: G = F · H.
4. Compute g = Inverse 2D FFT of G.

For large kernels (e.g., 100×100 Gaussian), this is much faster than direct convolution.

### 2.2 Small Kernel Convolution (scipy.signal.convolve2d)

For small kernels (3×3, 5×5, 7×7), direct 2D convolution is fast and preferred:

```python
from scipy.signal import convolve2d
import numpy as np

# Define kernels
gaussian_3x3 = np.array([[1, 2, 1],
                          [2, 4, 2],
                          [1, 2, 1]], dtype=float) / 16.0

sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]], dtype=float)

sobel_y = np.array([[-1, -2, -1],
                    [ 0,  0,  0],
                    [ 1,  2,  1]], dtype=float)

laplacian = np.array([[ 0,  1,  0],
                      [ 1, -4,  1],
                      [ 0,  1,  0]], dtype=float)

# Apply to image
blur = convolve2d(img, gaussian_3x3, mode='same', boundary='reflect')
edges_x = convolve2d(img, sobel_x, mode='same', boundary='reflect')
edges_y = convolve2d(img, sobel_y, mode='same', boundary='reflect')
edges = np.hypot(edges_x, edges_y)    # gradient magnitude
sharpened = img + convolve2d(img, laplacian, mode='same', boundary='reflect')

# Visualise
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
for ax, data, title in zip(axes.flat,
                             [img, blur, edges_x, edges_y, edges, sharpened],
                             ["Original", "Gaussian Blur", "Sobel X", "Sobel Y",
                              "Edge Magnitude", "Sharpened"]):
    ax.imshow(np.clip(data, 0, 255), cmap='gray')
    ax.set_title(title); ax.axis('off')
plt.tight_layout(); plt.show()
```

---

## 📚 3. Common Image Kernels

### 3.1 Gaussian Blur Kernel

The Gaussian is the **optimal smoothing filter** — it minimises the product of spatial and frequency localisation (uncertainty principle).

```
G(m, n) = (1/2πσ²) · e^{−(m²+n²)/(2σ²)}
```

Discrete approximations for σ=1:

| 3×3 (σ≈0.85) | 5×5 (σ≈1.0) |
|---|---|
| [1,2,1; 2,4,2; 1,2,1]/16 | [1,4,6,4,1; 4,16,24,16,4; 6,24,36,24,6; 4,16,24,16,4; 1,4,6,4,1]/256 |

The Gaussian is **separable**: a 2D Gaussian filter = 1D horizontal Gaussian × 1D vertical Gaussian. This reduces an N×N kernel from O(N²) operations per pixel to O(2N) operations — a critical optimization for large kernels.

### 3.2 Sobel Edge Detection

The Sobel operator approximates the gradient of the image:

```
G_x = f ** K_x     (horizontal gradient — detects vertical edges)
G_y = f ** K_y     (vertical gradient   — detects horizontal edges)
|G| = √(G_x² + G_y²)   (gradient magnitude)
θ = arctan(G_y / G_x)   (gradient direction)
```

K_x = [-1, 0, 1], [-2, 0, 2], [-1, 0, 1](-1,-0,-1],-[-2,-0,-2],-[-1,-0,-1) — weighted average of horizontal differences.
K_y = [-1,-2,-1], [0, 0, 0], [1, 2, 1](-1,-2,-1],-[0,-0,-0],-[1,-2,-1) — transpose of K_x.

The factor of 2 in the center row/column of Sobel (vs. Prewitt) provides mild Gaussian smoothing, making it more robust to noise.

### 3.3 Laplacian (Second Derivative)

The Laplacian ∇²f detects regions of rapid intensity change (all edges simultaneously):

```
∇²f = ∂²f/∂x² + ∂²f/∂y²  ≈  [0,1,0; 1,-4,1; 0,1,0] or [1,1,1; 1,-8,1; 1,1,1]
```

The Laplacian is **zero at edges** and non-zero near edges — technically it detects zero-crossings. In practice, `Laplacian of Gaussian (LoG)` (blur then Laplacian) is more robust than raw Laplacian (too sensitive to noise).

### 3.4 Frequency-Domain Interpretation

| Filter type | Effect on spectrum | Effect on image |
|-------------|-------------------|-----------------|
| Gaussian (lowpass) | Attenuates high frequencies | Smoothing / blur |
| Ideal highpass | Keeps only high frequencies | Edges only, no background |
| Sobel (highpass variant) | Differentiator (~jω in 2D) | Edges |
| Laplacian | Second-order differentiator (~−ω²) | All edges, isotropic |
| Notch filter in 2D | Removes periodic patterns | Remove scanning lines, moiré |

---

## 📚 4. Frequency Domain Filtering

For large kernels or when you want precise control over the frequency response, design the filter in the frequency domain:

```python
def frequency_domain_lowpass(img, cutoff_fraction=0.1):
    """Ideal circular lowpass filter."""
    F = np.fft.fft2(img)
    F_shifted = np.fft.fftshift(F)
    
    M, N = img.shape
    cy, cx = M // 2, N // 2          # center (DC)
    
    # Circular mask
    y, x = np.ogrid[-cy:M-cy, -cx:N-cx]
    r = np.sqrt(x**2 + y**2)
    radius = cutoff_fraction * min(M, N) / 2
    mask = (r < radius).astype(float)
    
    # Apply filter
    G_shifted = F_shifted * mask
    G = np.fft.ifftshift(G_shifted)
    g = np.real(np.fft.ifft2(G))
    
    return np.clip(g, 0, 255)
```

---

## 📚 5. Holographic Wavefront Propagation (Connection to Track 23)

The most surprising application of 2D Fourier analysis is in **Fourier optics** — the physics of how light propagates.

### 5.1 The Angular Spectrum Method

A coherent wavefront E(x,y,0) at z=0 propagates to z=d via:

```
E(x, y, d) = IFFT2D[ FFT2D(E(x,y,0)) · H(u,v) ]
```

where H(u,v) is the **transfer function of free-space propagation** (angular spectrum):

```
H(u, v) = e^{jkd·√(1 − λ²u² − λ²v²)}
```

k = 2π/λ (wave number), λ = wavelength, u,v = spatial frequencies.

This is just the 2D Convolution Theorem: **multiplication in the frequency domain = convolution in the spatial domain**. Free-space propagation *is* a 2D filter.

**Why this appears in Track 23 (Holographics):** Computing the propagated holographic wavefront for display on a spatial light modulator (SLM) requires computing this transform for a 4K (3840×2160) complex array, potentially at real-time rates. GPUs run 2D FFTs using `cuFFT` (CUDA) or `torch.fft.fft2`.

```python
# Angular spectrum propagation (simplified)
import numpy as np

def angular_spectrum_propagate(field, wavelength, pixel_size, z):
    """Propagate a 2D complex field by distance z."""
    M, N = field.shape
    
    # Spatial frequencies
    fx = np.fft.fftfreq(N, d=pixel_size)
    fy = np.fft.fftfreq(M, d=pixel_size)
    FX, FY = np.meshgrid(fx, fy)
    
    # Transfer function H(fx, fy)
    k = 2 * np.pi / wavelength
    sq = 1 - (wavelength * FX)**2 - (wavelength * FY)**2
    sq = np.where(sq >= 0, sq, 0)    # evanescent waves → zero
    H = np.exp(1j * k * z * np.sqrt(sq))
    
    # Apply
    F = np.fft.fft2(field)
    return np.fft.ifft2(F * H)
```

This is the bridge between [this chapter](04.6---Image-Processing-&-2D-Transforms) and [Track 23](Subject_Plan).

---

## 📚 6. Common Misconceptions

- **"Convolution and correlation are the same."** Convolution flips the kernel before sliding; correlation does not. `scipy.signal.convolve2d` convolves; `scipy.ndimage.correlate` correlates. For symmetric kernels (e.g., Gaussian), they give the same result.
- **"Larger kernel = better smoothing."** Only if you want more blur. Larger Gaussian kernel = more smoothing and more computation. Use `scipy.ndimage.gaussian_filter(sigma=2)` which automatically selects kernel size.
- **"The 2D DFT output has the DC at corner [0,0]."** After `numpy.fft.fft2`, DC is at [0,0]. Apply `numpy.fft.fftshift` to move it to the center for visualisation.
- **"2D FFT is much harder than 1D FFT."** It's identical in structure — just apply 1D FFT to each row, then each column. `numpy.fft.fft2` does exactly this.
- **"Edge artefacts in convolution are always a problem."** They are mitigated with correct boundary handling: `mode='reflect'` wraps values; `mode='constant'` (zero-padding) introduces DC error; `mode='wrap'` assumes periodic extension (like DFT).

---

## 🔗 7. Cross-links & Further Reading

### Internal
- [04.2 - Fourier Series & Fourier Transform](04.2---Fourier-Series-&-Fourier-Transform) — 1D theory extended here to 2D
- [04.3 - Discrete Fourier Transform & FFT](04.3---Discrete-Fourier-Transform-&-FFT) — the algorithm behind `numpy.fft.fft2`
- [04.4 - Digital Filters - FIR & IIR](04.4---Digital-Filters---FIR-&-IIR) — 2D kernels are 2D FIR filters
- [Track 23](Subject_Plan) — angular spectrum method, SLM wavefronts
- [Track 09](Subject_Plan) — texture filtering (mipmaps = lowpass filtering)
- [Subject_Plan](Subject_Plan) — resource catalog

### External
- [scipy.ndimage documentation](https://docs.scipy.org/doc/scipy/reference/ndimage.html) — Gaussian filter, Sobel, etc.
- [scipy.signal.convolve2d](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve2d.html)
- [numpy.fft.fft2](https://numpy.org/doc/stable/reference/generated/numpy.fft.fft2.html)
- [Gonzalez & Woods — Digital Image Processing (Pearson)](https://www.imageprocessingplace.com/) — the standard textbook
- [OpenCV-Python Tutorials — Image Filtering](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html) — practical computer vision filtering
- [dspguide.com — Chapter 24: Linear Image Processing](https://www.dspguide.com/ch24.htm) — free

---

*Next: [04.7 - Speech & Voice Processing (ASR-TTS Foundations)](04.7---Speech-&-Voice-Processing-(ASR-TTS-Foundations)) — How audio signals become text (Whisper) and text becomes speech (XTTS).*
