# Hyperspectral Crop Disease Forecasting: Phase 3 & 4 Architectural Design

## 1. 3D Spatial-Spectral Convolutional Kernels

Hyperspectral Images (HSI) are essentially 3D data cubes $X \in \mathbb{R}^{C \times D \times H \times W}$ where $D$ represents the spectral bands. Standard 2D CNNs treat the spectral dimension strictly as channels, failing to capture the contiguous local structural relationships across adjacent wavelengths. 3D CNNs apply three-dimensional kernels $W \in \mathbb{R}^{C_{out} \times C_{in} \times k_d \times k_h \times k_w}$.

### Mathematical Formulation
A 3D convolution operation at spatial position $(x, y)$ and spectral depth $z$ is formulated as:
$$ V^{(l)}_{i, x, y, z} = f\left(b_{i}^{(l)} + \sum_{m} \sum_{p=0}^{P_i-1} \sum_{q=0}^{Q_i-1} \sum_{r=0}^{R_i-1} W^{(l)}_{i, m, p, q, r} \cdot V^{(l-1)}_{m, x+p, y+q, z+r}\right) $$
Where $V^{(l)}$ is the feature map at layer $l$, $P_i, Q_i, R_i$ represent the kernel dimensions (height, width, spectral depth).

### PyTorch Pseudocode
```python
import torch
import torch.nn as nn

class SpatialSpectralConv3D(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=(7, 3, 3)):
        super().__init__()
        # kernel_size = (spectral_depth, height, width)
        self.conv3d = nn.Conv3d(
            in_channels=in_channels, 
            out_channels=out_channels,
            kernel_size=kernel_size,
            stride=(2, 1, 1),
            padding=(kernel_size[0]//2, kernel_size[1]//2, kernel_size[2]//2)
        )
        self.bn = nn.BatchNorm3d(out_channels)
        self.relu = nn.GELU()

    def forward(self, x):
        # Input shape: (Batch, Channels, Spectral, H, W)
        return self.relu(self.bn(self.conv3d(x)))
```

## 2. Vision Transformer (ViT) Multi-Head Self-Attention for Spectral Bands

To capture long-range dependencies across distant spectral signatures (e.g., correlations between the visible green band and near-infrared (NIR) which dictate chlorophyll health / NDVI), Multi-Head Self-Attention (MHSA) treats spectral bands (or spectral-spatial tokens) as a sequence.

### Mathematical Formulation
The input sequence is mapped into Query ($Q$), Key ($K$), and Value ($V$) matrices. 
$$ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V $$
For spectral attention, the tokens represent non-overlapping spectral band groupings. Multi-head splits the embedding dimension $D$ into $h$ heads:
$$ \text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V) $$
$$ \text{MHSA} = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O $$

## 3. Hybrid PyTorch Architecture: 3D-CNN + ViT

This hybrid architecture leverages 3D convolutions for localized spatial-spectral feature extraction (mitigating the ViT's lack of inductive bias) and passes the refined feature maps into a Transformer encoder for global spectral modeling.

### PyTorch Pseudocode
```python
class HybridHSIAttention(nn.Module):
    def __init__(self, bands=200, num_classes=5, dim=256, depth=4, heads=8):
        super().__init__()
        # 1. 3D CNN Feature Extractor
        self.feature_extractor = nn.Sequential(
            nn.Conv3d(1, 16, kernel_size=(7, 3, 3), padding=(3, 1, 1)),
            nn.BatchNorm3d(16),
            nn.GELU(),
            nn.MaxPool3d(kernel_size=(2, 2, 2)),
            nn.Conv3d(16, 32, kernel_size=(5, 3, 3), padding=(2, 1, 1)),
            nn.BatchNorm3d(32),
            nn.GELU(),
            nn.MaxPool3d(kernel_size=(2, 2, 2))
        )
        
        # 2. Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(d_model=dim, nhead=heads, dim_feedforward=dim*2, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=depth)
        
        # 3. Projection & Classification
        self.proj = nn.Linear(32 * (bands // 4), dim)
        self.classifier = nn.Linear(dim, num_classes)
        
    def forward(self, x):
        # x: (B, 1, Bands, H, W)
        features = self.feature_extractor(x) 
        # Output features: (B, Channels=32, B', H', W')
        
        B, C, Depth, H, W = features.shape
        # Flatten spatial dimensions and treat Depth*Channels as embedding per spatial patch
        features = features.view(B, C * Depth, H * W).permute(0, 2, 1) # (B, Seq=H*W, Emb=C*Depth)
        
        features = self.proj(features)
        attn_out = self.transformer(features)
        
        # Global Average Pooling
        pooled = attn_out.mean(dim=1)
        return self.classifier(pooled)
```

## 4. CUDA GPU Memory Allocation & Tensor Tiling Mechanics

Hyperspectral cubes often exceed standard GPU memory limits (e.g., a single $1000 \times 1000 \times 224$ float32 cube is ~896MB, a batch of 16 is ~14GB, before intermediate gradient allocations).

**Tiling Strategy**:
1. **Spatial Patching**: The HSI cube is cropped into overlapping 3D patches (e.g., $1 \times 224 \times 15 \times 15$) during the DataLoader phase.
2. **Gradient Accumulation**: To maintain large effective batch sizes without OOM errors.
3. **Mixed Precision (AMP)**: Leveraging `torch.cuda.amp.autocast()` to reduce memory bandwidth by 50% using FP16/BF16 without precision loss.

```python
# Tiling Data Loader snippet
def extract_overlapping_patches(hsi_tensor, patch_size=15, stride=10):
    # hsi_tensor: (Bands, H, W)
    patches = hsi_tensor.unfold(1, patch_size, stride).unfold(2, patch_size, stride)
    return patches.reshape(hsi_tensor.size(0), -1, patch_size, patch_size).permute(1, 0, 2, 3)
```

## 5. Explainable AI (XAI): Integrated Gradients Spectral Attribution

To trust the model, we must know *which* spectral bands led to a disease prediction (e.g., early rust detection at 750nm). Integrated Gradients (IG) accumulates gradients interpolated between a baseline (zero-tensor) and the input HSI cube.

### Mathematical Formulation
$$ IG_i(x) = (x_i - x'_i) \times \int_{\alpha=0}^{1} \frac{\partial F(x' + \alpha(x - x'))}{\partial x_i} d\alpha $$

### Application to HSI
Using the `captum` library, we calculate attribution across the spectral dimension $D$ and spatially average the scores to output a 1D "Band Importance" vector.

```python
from captum.attr import IntegratedGradients

ig = IntegratedGradients(model)
# Calculate attribution for the predicted class
attributions, delta = ig.attribute(input_tensor, target=predicted_class, return_convergence_delta=True)
# Aggregate spatially to get spectral importance (B, Bands)
spectral_importance = attributions.squeeze(1).mean(dim=(2, 3)) 
```

## 6. MLOps: Seasonal Illumination & Concept Drift Monitoring

In agricultural HSI, the data distribution $P(X)$ changes due to varying solar azimuth angles, atmospheric scattering, and seasonal phenology (crop maturity), causing **Covariate Shift / Concept Drift**.

**Monitoring Strategy**:
1. **Latent Space Monitoring**: Extract features from the `HybridHSIAttention` global average pooling layer.
2. **Drift Metric Calculation**: Use Population Stability Index (PSI) or Maximum Mean Discrepancy (MMD) to compare the production latent distribution against the baseline training distribution.
3. **Illumination Normalization Loop**: Implement an automated shadow/illumination correction step (e.g., using Empirical Line Method with reference panels) if MMD crosses a predefined critical threshold ($\tau$), triggering a retraining pipeline.
