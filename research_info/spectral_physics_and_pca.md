# Deep Theoretical Research: Hyperspectral Crop Disease Forecasting (Phases 1 & 4)

## 1. Spectral Physics & Wavelength Ranges
Hyperspectral imaging (HSI) in agriculture leverages narrow, contiguous spectral bands (typically 1-10 nm resolution) to capture detailed target reflectance across the electromagnetic spectrum. The primary ranges of interest include:
*   **Visible (VIS, 400–700 nm):** Dominated by pigment absorption (chlorophyll $a/b$, carotenoids, anthocyanins). Chlorophyll strongly absorbs in the blue (~450 nm) and red (~670 nm) regions, producing the green reflectance peak (~550 nm).
*   **Red Edge (680–750 nm):** The region of rapid transition from strong red absorption by chlorophyll to high NIR scattering. The Red Edge Inflection Point (REIP) is highly correlated with chlorophyll concentration and canopy biomass.
*   **Near-Infrared (NIR, 750–1300 nm):** Governed by leaf internal structure (mesophyll cellular scattering) and canopy architecture. Healthy foliage exhibits high reflectance due to multiple internal scattering events at the cell wall-air interfaces.
*   **Shortwave-Infrared (SWIR, 1300–2500 nm):** Dominated by molecular vibrations (overtones and combinations) of $O-H$, $C-H$, and $N-H$ bonds. This region is critical for estimating Equivalent Water Thickness (EWT) and detecting biochemical constituents like lignin, cellulose, and nitrogen.

## 2. Plant Pathology Biomarkers, Cellular Collapse, and the Red Edge Blue Shift
When a plant undergoes pathogenic stress, several biophysical and biochemical biomarkers manifest spectrally before visual symptoms appear:
*   **Cellular Collapse:** Pathogens (e.g., necrotrophic fungi) destroy the spongy mesophyll and palisade tissue. This structural degradation collapses the intercellular air spaces, drastically reducing NIR reflectance (750-1300 nm).
*   **Chlorophyll Degradation & Red Edge Blue Shift:** Pathogenesis accelerates the breakdown of chlorophyll $a/b$, causing the red absorption well (~670 nm) to narrow. Mathematically, the first derivative of the reflectance curve ($\frac{dR}{d\lambda}$) yields a maximum at the REIP. As chlorophyll concentration drops, the REIP shifts towards shorter wavelengths (from ~725 nm down to ~700 nm), a phenomenon known as the **"Blue Shift"**.
*   **Water Loss:** Pathogenic disruption of vascular tissue (xylem/phloem) leads to rapid leaf desiccation, manifesting as increased reflectance in the SWIR water absorption bands (1450 nm and 1940 nm).

## 3. Radiometric & Atmospheric Calibration (6S & FLAASH)
Raw hyperspectral data (Digital Numbers) must be converted to absolute surface reflectance. This requires removing atmospheric scattering (Rayleigh and Mie) and absorption (primarily $H_2O$, $O_3$, $CO_2$).
*   **FLAASH (Fast Line-of-sight Atmospheric Analysis of Spectral Hypercubes):** Based on the MODTRAN radiative transfer model. It utilizes the correlated-k method for atmospheric transmittance and computes surface reflectance ($\rho$) by solving the radiative transfer equation: 
    $$ L = \left( \frac{A \rho}{1 - \rho_e S} \right) + \left( \frac{B \rho_e}{1 - \rho_e S} \right) + L_a $$
    where $L$ is at-sensor radiance, $L_a$ is atmospheric path radiance, $S$ is spherical albedo, $\rho$ is target reflectance, $\rho_e$ is spatially averaged reflectance, and $A, B$ are atmospheric coefficients.
*   **6S (Second Simulation of the Satellite Signal in the Solar Spectrum):** Uses the successive orders of scattering (SOS) method to model radiative transfer. It accurately accounts for aerosol scattering phase functions and gaseous absorption.
*   **Water Vapor Noise Suppression:** Atmospheric water vapor absorbs heavily at ~940 nm, 1140 nm, 1380 nm, and 1880 nm. FLAASH estimates column water vapor on a pixel-by-pixel basis by measuring the depth of the 1135 nm or 940 nm absorption bands using a 3-band ratio technique, enabling precise inversion and suppression of $H_2O$ noise.

## 4. Continuum Removal (Convex Hull Normalization)
Continuum removal normalizes reflectance spectra to isolate specific absorption features, removing the effects of albedo and background scattering.
*   **Convex Hull Normalization:** A convex hull (continuum line) is fitted over the top of the spectrum by connecting the local reflectance maxima. The continuum $R_c(\lambda)$ acts as a baseline.
*   **Band Depth Isolation:** The continuum-removed spectrum $CR(\lambda)$ is calculated as the ratio of the original reflectance $R(\lambda)$ to the continuum curve:
    $$ CR(\lambda) = \frac{R(\lambda)}{R_c(\lambda)} $$
*   **Band Depth (BD):** Computed as $BD = 1 - CR(\lambda)$. This isolates the precise mathematical depth of pathogenic absorption features (e.g., localized chlorophyll degradation at 680 nm or water loss at 970 nm).

## 5. PCA Band Reduction Math
Hyperspectral data contains massive redundancy (multicollinearity). Principal Component Analysis (PCA) provides orthogonal linear transformation to extract the most informative variance.
*   **1. Spatial Tensor Reshaping (3D to 2D):** The hypercube $X \in \mathbb{R}^{H \times W \times B}$ (where $H$=height, $W$=width, $B$=bands) is unfolded into a 2D matrix $X_{2D} \in \mathbb{R}^{N \times B}$, where $N = H \times W$ (total pixels).
*   **2. Mean Centering:** The empirical mean $\mu_j = \frac{1}{N} \sum_{i=1}^N x_{i,j}$ is subtracted from each band: 
    $$ X_c = X_{2D} - \mu $$
*   **3. Covariance Matrix Computation:** The $B \times B$ covariance matrix $\Sigma$ is calculated:
    $$ \Sigma = \frac{1}{N-1} X_c^T X_c $$
*   **4. Eigenvalue Decomposition:** $\Sigma$ is decomposed into eigenvectors $V$ and a diagonal matrix of eigenvalues $\Lambda$:
    $$ \Sigma V = V \Lambda $$
    The eigenvectors represent the new orthogonal axes (Principal Components), and eigenvalues ($\lambda_i$) represent the variance captured by each PC.
*   **5. Cumulative Explained Variance ($\ge$ 98.5%):** PCs are sorted by descending $\lambda_i$. The number of retained components $k$ is chosen such that the cumulative explained variance exceeds 0.985:
    $$ \frac{\sum_{i=1}^k \lambda_i}{\sum_{j=1}^B \lambda_j} \ge 0.985 $$
    The data is then projected: $X_{reduced} = X_c V_k$, transforming $\mathbb{R}^{N \times B} \rightarrow \mathbb{R}^{N \times k}$.

## 6. Vegetation Indices
Narrowband Vegetation Indices amplify specific pathogenic signals while normalizing structural/illumination variables:
*   **Photochemical Reflectance Index (PRI):** 
    $$ PRI = \frac{R_{531} - R_{570}}{R_{531} + R_{570}} $$
    *Utility:* Measures changes in the xanthophyll cycle (zeaxanthin/violaxanthin ratio). It is a highly sensitive, early indicator of photosynthetic light-use efficiency drops due to pathogenic stress.
*   **Water Band Index (WBI):**
    $$ WBI = \frac{R_{900}}{R_{970}} $$
    *Utility:* Tracks canopy water status. The 970 nm band corresponds to a minor water absorption feature. Pathogen-induced desiccation causes a decrease in the WBI ratio.
*   **Structure Insensitive Pigment Index (SIPI):**
    $$ SIPI = \frac{R_{800} - R_{445}}{R_{800} - R_{680}} $$
    *Utility:* Maximizes sensitivity to the ratio of carotenoids to chlorophyll $a$ while minimizing the confounding effects of canopy structure and Leaf Area Index (LAI). Elevated SIPI is a strong biomarker for necrosis and senescence.
