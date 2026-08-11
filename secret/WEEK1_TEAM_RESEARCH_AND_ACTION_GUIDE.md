# 📚 TerraSpectra (Project 1): Complete Team Research, Preparation & Action Guide

This guide details **everything your 4-member team needs to research, study, collect, and execute** for Week 1 of **Project 1: TerraSpectra (Hyperspectral Crop Disease Forecasting)**.

---

# 🔍 SECTION 1: Theoretical Research & Background Study (What to Learn)

All team members should read and understand these core concepts before writing code:

### 1.1 Remote Sensing & Hyperspectral Physics
* **Why RGB/NDVI Fails:** Standard 3-band RGB and 4-band NDVI imagery only detect plant stress after leaves turn yellow or brown (chlorosis/necrosis). At this point, plant cell structures are permanently destroyed.
* **The Hyperspectral Advantage:** Hyperspectral sensors capture **200+ contiguous narrow bands** (400 nm – 2500 nm).
* **Key Spectral Regions to Study:**
  * **Visible (400 nm – 700 nm):** Absorbed by Chlorophyll-a (675 nm) and Chlorophyll-b (650 nm).
  * **Red Edge (680 nm – 750 nm):** Steep incline zone. When fungal blight infects a crop, cell wall damage causes a **leftward shift** (toward shorter wavelengths) **3 weeks before visual symptoms manifest**.
  * **Near-Infrared / NIR (700 nm – 1100 nm):** Reflects off leaf spongy mesophyll. Infection causes reflection collapse.
  * **Short-Wave Infrared / SWIR (1100 nm – 2500 nm):** Detects plant moisture. Absorption troughs occur at 1450 nm and 1940 nm.

### 1.2 Data File Formats & GIS Coordinates
* **HDF5 (`.h5` / `.hdf5`):** Stores multi-dimensional arrays (tensors) with metadata. Learn `h5py` in Python to inspect dataset keys, attributes, and slicing.
* **GeoTIFF (`.tif`):** Raster image tagged with geospatial parameters (GeoKeys). Maps pixel $(x, y)$ to real-world Longitude/Latitude.
* **Coordinate Reference Systems (CRS):**
  * **EPSG:4326 (WGS 84):** Decimal degrees (Latitude, Longitude). Used for GPS & backend payloads.
  * **EPSG:3857 (Web Mercator):** Coordinates in meters. Used by web mapping engines (Mapbox, Google Maps).

---

# 📐 SECTION 2: Mathematical Research & Formulas to Master

### 2.1 Principal Component Analysis (PCA) on 3D Cubes
Hyperspectral data has extreme redundancy between adjacent bands. PCA reduces 224 bands down to 32 principal components while retaining **>98.5% of variance**.

1. **Reshape 3D Data Cube:**
   $$C \in \mathbb{R}^{H \times W \times B} \longrightarrow X \in \mathbb{R}^{(H \cdot W) \times B}$$
2. **Mean Centering & Standardization:**
   $$\bar{X} = X - \mu$$
3. **Covariance Matrix:**
   $$\Sigma = \frac{1}{N - 1} \bar{X}^T \bar{X} \in \mathbb{R}^{B \times B}$$
4. **Eigenvalue Decomposition:**
   $$\Sigma V = V \Lambda \quad (\text{Eigenvalues } \lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_B)$$
5. **Cumulative Explained Variance Ratio:**
   $$\text{EVR}(k) = \frac{\sum_{i=1}^k \lambda_i}{\sum_{j=1}^B \lambda_j} \ge 0.985$$
6. **Projection Back to 3D Tensor:**
   $$Z = \bar{X} V_k \in \mathbb{R}^{(H \cdot W) \times k} \longrightarrow C_{\text{reduced}} \in \mathbb{R}^{H \times W \times k}$$

---

# 🌐 SECTION 3: Data Assets, Accounts & API Keys to Collect

Before building, the team must acquire the following items:

1. **Mapbox Access Token (Free Developer Account):**
   * Register at [mapbox.com](https://www.mapbox.com/).
   * Copy the default public access token (`pk.eyJ1...`).
   * Add to `frontend/.env` file as `VITE_MAPBOX_ACCESS_TOKEN`.

2. **Satellite Datasets & Sample Files (To Research & Download):**
   * **NASA AVIRIS-NG Airborne Data:** Download sample `.hdr` / binary spectral cubes from [aviris.jpl.nasa.gov](https://aviris.jpl.nasa.gov/).
   * **USGS EarthExplorer EO-1 Hyperion:** Access spaceborne 222-band satellite scenes via [earthexplorer.usgs.gov](https://earthexplorer.usgs.gov/).
   * **Synthetic Data Generator:** Run the local generator script `scripts/generate_mock_data.py` to create a 224-band HDF5 data cube (`data/mock_farm_datacube.h5`).

---

# 🛠️ SECTION 4: Software Stack & Environment Setup

### 1. Python Environment (Backend & Data Science)
Ensure Python 3.10+ or 3.11+ is installed. Install required packages:
```bash
pip install rasterio h5py scikit-learn fastapi uvicorn torch torchvision
```

### 2. Node.js Environment (Frontend GIS Interface)
Ensure Node.js 18+ is installed. Install frontend dependencies:
```bash
cd frontend
npm install react react-dom @deck.gl/core @deck.gl/layers @deck.gl/react mapbox-gl react-map-gl lucide-react
```

---

# 👥 SECTION 5: Week-1 Task Allocation Matrix (For the 4 Team Members)

### 🧑‍💻 Member 1: Systems & API Architecture Lead
* **What to Research:** FastAPI async route handlers, Pydantic v2 schemas, CORS middleware, REST endpoint design.
* **Week 1 Deliverables:**
  * Set up `backend/main.py` with FastAPI server.
  * Implement `/health` and `/api/v1/pca/reduce` REST API routes.
  * Test API using Swagger docs (`http://localhost:8000/docs`).

### 🧑‍💻 Member 2: Geospatial & Data Engineer
* **What to Research:** `Rasterio` datasets, `h5py` file indexing, PCA dimensionality reduction using `sklearn.decomposition.PCA`.
* **Week 1 Deliverables:**
  * Run `scripts/generate_mock_data.py` to generate `mock_farm_datacube.h5`.
  * Build `backend/app/services/data_pipeline.py` to ingest HDF5 & GeoTIFF files.
  * Build `backend/app/services/pca_reducer.py` to perform 224 $\rightarrow$ 32 component PCA reduction.

### 🧑‍💻 Member 3: Deep Learning & PyTorch Specialist
* **What to Research:** PyTorch 3D Convolutional layers (`nn.Conv3d`), input tensor dimension requirements `(Batch, Channels, Depth, Height, Width)`.
* **Week 1 Deliverables:**
  * Study 3D-CNN kernel mechanics for spatial-spectral feature extraction.
  * Draft baseline PyTorch model class `Hybrid3DCNNViT`.
  * Measure PyTorch memory requirements for 32-component PCA tensors.

### 🧑‍💻 Member 4: Frontend GIS & React UI Developer
* **What to Research:** React 18, Vite, Deck.gl v8+ layers (`GeoJsonLayer`, `BitmapLayer`), Mapbox GL JS satellite map styles.
* **Week 1 Deliverables:**
  * Obtain Mapbox public access token.
  * Set up React + Vite + TypeScript frontend in `frontend/`.
  * Build `MapContainer.tsx` rendering Mapbox satellite basemap + Deck.gl Iowa Farm Zone Alpha boundary layer.

---

# 🧪 SECTION 6: How to Test & Verify Everything

1. **Test Synthetic Data Generation:**
   ```bash
   python3 scripts/generate_mock_data.py
   ```
   *Verify:* Creates `data/mock_farm_datacube.h5` (~198 MB) and `data/mock_farm_preview.tif`.

2. **Test Data Pipeline & PCA Reduction:**
   ```bash
   python3 -c "
   import sys; sys.path.append('backend')
   from app.services.data_pipeline import HyperspectralDataLoader
   from app.services.pca_reducer import SpectralPCAReducer
   cube, w, meta = HyperspectralDataLoader.load_hdf5_cube('data/mock_farm_datacube.h5')
   reducer = SpectralPCAReducer(n_components=32)
   red_cube, stats = reducer.fit_transform_cube(cube)
   print('Success! Shape:', red_cube.shape)
   "
   ```

3. **Test Frontend Development Server:**
   ```bash
   cd frontend
   npm run dev
   ```
   *Verify:* Open `http://localhost:5173` to see the interactive Mapbox satellite map with the Iowa Farm Zone Alpha layer.
