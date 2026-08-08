# TerraSpectra — Project Contribution Log

This document records every file, script, and research document created for the TerraSpectra hyperspectral crop disease forecasting project, along with a description of what each file does.

---

## Project Lead — Lakshan Muruganandam

All research, data collection, architecture design, and repository organization for Phase 1 of TerraSpectra.

---

### Research Documents (`research_info/`)

| File | Description |
|------|-------------|
| [`research_info/spectral_physics_and_pca.md`](research_info/spectral_physics_and_pca.md) | Deep research on spectral physics — wavelength ranges (VIS 400–700nm, Red Edge 680–750nm, NIR 750–1300nm, SWIR 1300–2500nm), plant disease biomarkers, cellular collapse mechanics, atmospheric calibration (6S & FLAASH), continuum removal via convex hull normalization, full PCA math including covariance matrix, eigendecomposition, and cumulative explained variance. Vegetation indices: PRI, WBI, SIPI. |
| [`research_info/3d_dl_architecture.md`](research_info/3d_dl_architecture.md) | Complete architectural research for the 3D-CNN + Vision Transformer hybrid model. Covers 3D spatial-spectral convolutional kernels on H×W×B cubes, ViT multi-head self-attention for spectral band correlation, PyTorch hybrid architecture outline, CUDA GPU memory tiling strategy, Integrated Gradients XAI for spectral attribution, and seasonal concept drift MLOps monitoring. |
| [`research_info/data_assets.md`](research_info/data_assets.md) | Acquisition guide for all Phase 2 data assets: NASA AVIRIS-NG airborne cubes, EO-1 Hyperion / PRISMA / EnMAP spaceborne cubes, Sentinel-2 multispectral calibration imagery, EcoSIS spectroradiometer leaf spectra, DEM terrain tiles, farm boundary GeoJSON, and Mapbox tile API access. Portal names, API methods, file formats, and EPSG codes for each. |
| [`research_info/frontend_gis_webgl.md`](research_info/frontend_gis_webgl.md) | Technical research for the WebGL GIS frontend. Covers Deck.gl v8 layer architecture (GeoJsonLayer, BitmapLayer, TileLayer), Mapbox GL JS integration in React 18 + Vite, viewport camera synchronization, interactive pixel picking to extract 224-band spectral reflectance, Plotly.js spectral line chart rendering, and WebGL context memory management. |
| [`research_info/packages_and_modules.md`](research_info/packages_and_modules.md) | Complete reference for every Python and Node.js package in the project stack. Backend: rasterio, h5py, netCDF4, GDAL, spectral, pyproj, xarray, numpy, scipy, scikit-learn, PyTorch, timm, einops, captum, shap, FastAPI, uvicorn, pydantic, geopandas, mlflow, wandb, evidently, pytest. Frontend: React 18, TypeScript, Vite, deck.gl, mapbox-gl, react-map-gl, plotly.js, tailwindcss, zustand, vitest. Version numbers, install commands, and key APIs for each. |
| [`research_info/geospatial_file_standards.md`](research_info/geospatial_file_standards.md) | Deep reference for every geospatial file format used in the pipeline. HDF5 (group/dataset/attribute structure, chunking strategy, AVIRIS and PRISMA layouts, h5py API), GeoTIFF (TIFF tags, rasterio API, Cloud Optimized GeoTIFF, band interleaving modes), NetCDF4 (CF conventions, xarray API), ENVI format (.hdr header fields, SPy library), EPSG:4326 / EPSG:3857 / UTM coordinate systems, GeoJSON RFC 7946, Mapbox Terrain-RGB DEM encoding and decoding formula. |
| [`research_info/api_backend_scaffold.md`](research_info/api_backend_scaffold.md) | Full FastAPI backend architecture research. ASGI + uvicorn setup, lifespan context for GPU model loading, CORS middleware configuration, Pydantic v2 request/response DTOs for PCA and prediction endpoints, design of all four API routes (GET /health, POST /api/v1/pca/reduce, GET /api/v1/spectra, POST /api/v1/predict), sliding-window spatial tiling for GPU batch inference, automatic Swagger/OpenAPI documentation, async pytest + httpx testing patterns, and security headers middleware. |
| [`research_info/security_and_privacy.md`](research_info/security_and_privacy.md) | Farm spatial data privacy and API security research. Legal framework (GDPR Article 5, USDA CIPSEA), spatial anonymization techniques (coordinate precision reduction, bounding box fuzzification, k-anonymity), JWT auth with HS256/RS256, RBAC for farmer/analyst/admin roles, token rotation, CORS strict origin allowlisting, full security header table (CSP, HSTS, X-Frame-Options, etc.), CUDA GPU memory isolation between users, AES-256 encryption for HDF5 at rest, TLS 1.3 in transit, slowapi token bucket rate limiting for the inference endpoint, and structured JSON audit logging. |
| [`research_info/mlops_and_testing.md`](research_info/mlops_and_testing.md) | MLOps, testing, and CI/CD research. pytest fixtures and parametrize patterns, httpx AsyncClient for FastAPI testing, vitest + @testing-library/react with Deck.gl mocks, MLflow experiment tracking and model registry, wandb real-time GPU dashboards and hyperparameter sweeps, Evidently AI DataDriftPreset for spectral feature drift, seasonal illumination drift root cause (solar zenith angle), Empirical Line Correction (ELC), MMD-based automated retraining trigger, GitHub Actions CI/CD workflow with coverage gates, and full benchmark metric definitions (OA, AA, Kappa, per-class F1). |
| [`research_info/training_datasets_reference.md`](research_info/training_datasets_reference.md) | Master reference document for all 13 training datasets. For each dataset: sensor name and specs, spatial dimensions, spectral band count and wavelength range, ground sampling distance, full class label table with pixel counts, Python loading code using scipy.io.loadmat, rationale for inclusion in the training pipeline, and a complete post-download directory structure map. Also includes a GitHub file size limit table and guidance on Git LFS for large .mat files. |
| [`research_info/ABSTRACT_AND_TRACKING.md`](research_info/ABSTRACT_AND_TRACKING.md) | Project abstract covering the core problem statement (early-stage crop disease detection using hyperspectral reflectance), technical approach (3D-CNN + ViT + WebGL GIS frontend), and phase-by-phase progress tracking log. |
| [`research_info/ULTIMATE_DATASET_TRACKER.md`](research_info/ULTIMATE_DATASET_TRACKER.md) | Tracker listing every hyperspectral and geographic dataset collected for the project: sensor type, pixel dimensions, spectral band count, and geographic focus for each dataset including Indian Pines, Salinas, Pavia, Botswana, KSC, WHU-Hi (LongKou/HanChuan/HongHu), Houston, Chikusei, Muufl, Trento, Augsburg, Mars CRISM, and the geospatial mock files. |

---

### Scripts (`research_info/scripts/`)

| File | Description |
|------|-------------|
| [`research_info/scripts/download_all_training_datasets.py`](research_info/scripts/download_all_training_datasets.py) | Master download script for all 13 training datasets. Downloads Indian Pines, Salinas (full + A subset), Pavia University, Pavia Centre, Botswana, Kennedy Space Center, WHU-Hi (LongKou/HanChuan/HongHu) via Hugging Face, full HSI benchmark collection (Houston 2013, Trento, Chikusei, Muufl, Augsburg, Mars CRISM) via Hugging Face, USGS spectral library CSV, Natural Earth world boundary GeoJSON, and Iowa state boundary GeoJSON. All files saved to `research_info/raw/`. Generates a `download_manifest.json` for reproducibility. |
| [`research_info/scripts/download_datasets.py`](research_info/scripts/download_datasets.py) | Original Hugging Face snapshot downloader for the `Tanishq165/HSI_Datasets` full benchmark collection. Downloads to `research_info/raw/` using the `huggingface_hub` library. |
| [`research_info/scripts/generate_mock_data.py`](research_info/scripts/generate_mock_data.py) | Synthetic agricultural datacube generator. Creates a 200×200×224 band float32 HDF5 datacube simulating a farm field with a blight outbreak zone embedded using spectral curve manipulation. Also generates a 3-band RGB GeoTIFF preview of the mock field with embedded EPSG:4326 CRS and affine geotransform. Saves to `research_info/mock/`. |

---

### Frontend Scaffold (`research_info/frontend/`)

A scaffolded React 18 + TypeScript + Vite + Tailwind CSS application that represents the future GIS dashboard. Stored inside `research_info/` to keep it with the research phase assets. Not yet connected to a backend.

| File | Description |
|------|-------------|
| [`research_info/frontend/src/App.tsx`](research_info/frontend/src/App.tsx) | Root React component. Entry point for the hyperspectral GIS dashboard UI. |
| [`research_info/frontend/src/App.css`](research_info/frontend/src/App.css) | Component-scoped styles for App.tsx. |
| [`research_info/frontend/src/index.css`](research_info/frontend/src/index.css) | Global styles, Tailwind CSS directives (@tailwind base/components/utilities). |
| [`research_info/frontend/src/main.tsx`](research_info/frontend/src/main.tsx) | React DOM root render entry point. |
| [`research_info/frontend/vite.config.ts`](research_info/frontend/vite.config.ts) | Vite bundler configuration for React + TypeScript with path aliases. |
| [`research_info/frontend/tailwind.config.js`](research_info/frontend/tailwind.config.js) | Tailwind CSS content paths and theme configuration. |
| [`research_info/frontend/package.json`](research_info/frontend/package.json) | Node.js project manifest listing all frontend dependencies (React, deck.gl, mapbox-gl, plotly.js, etc.) and dev scripts. |
| [`research_info/frontend/tsconfig.json`](research_info/frontend/tsconfig.json) | TypeScript compiler configuration for the full project. |
| [`research_info/frontend/index.html`](research_info/frontend/index.html) | HTML entry point — Vite injects the compiled React bundle here at build time. |
| [`research_info/frontend/README.md`](research_info/frontend/README.md) | Frontend setup and run instructions. |

---

### Backend Scaffold (`backend/`)

Placeholder structure for the future FastAPI inference server. The `backend/ml_pipeline/` scripts are research-phase synthetic data generators and are not the production pipeline.

| File | Description |
|------|-------------|
| [`backend/requirements.txt`](backend/requirements.txt) | Python dependency list for the backend: FastAPI, uvicorn, rasterio, h5py, scikit-learn, numpy, scipy, and all other packages needed for the API server and ML pipeline. |
| [`backend/ml_pipeline/generate_synthetic_hsi.py`](backend/ml_pipeline/generate_synthetic_hsi.py) | Script to generate synthetic hyperspectral image cubes using PROSAIL-inspired radiative transfer simulation parameters. |
| [`backend/ml_pipeline/generate_mega_synthetic_datasets.py`](backend/ml_pipeline/generate_mega_synthetic_datasets.py) | Extended version of the synthetic generator producing larger batch datasets with multi-class disease severity labels for initial model benchmarking. |

---

### Project Documentation (`docs/`, root)

| File | Description |
|------|-------------|
| [`docs/WEEK1_MAIN_MASTER.md`](docs/WEEK1_MAIN_MASTER.md) | The canonical master specification document for Week 1. Defines all four phases: spectral physics + PCA (Phase 1), data acquisition (Phase 2), 3D-CNN + ViT architecture (Phase 3), and WebGL GIS frontend (Phase 4). All research documents in `research_info/` are derived from the requirements in this file. |
| [`docs/WEEK1_MAIN_MASTER.pdf`](docs/WEEK1_MAIN_MASTER.pdf) | PDF export of the master spec for offline reference. |
| [`README.md`](README.md) | Repository overview, project description, tech stack summary, and directory guide for anyone landing on the GitHub page. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | This file. Complete list of all files created, what each does, and contributor attribution. |

---

### Repository Configuration

| File | Description |
|------|-------------|
| [`.gitignore`](.gitignore) | Excludes all binary data from the repository: `research_info/raw/` (downloaded satellite cubes, .mat files), `research_info/mock/` (generated HDF5/GeoTIFF files), `research_info/processed/`, `backend/venv/`, `node_modules/`, `__pycache__/`, `.env`, `.DS_Store`, and the `secret/` planning documents directory. |

---

## How to Get All Training Data

```bash
cd research_info/scripts
python3 download_all_training_datasets.py
```

This downloads all 13 datasets (Indian Pines, Salinas, Pavia, Botswana, KSC, WHU-Hi, Houston, Chikusei, Muufl, Trento, Augsburg, USGS spectra, GeoJSON boundaries) to `research_info/raw/`.

## How to Generate Mock Data

```bash
cd research_info/scripts
python3 generate_mock_data.py
```

Creates a synthetic 200×200×224 band HDF5 datacube and RGB GeoTIFF preview in `research_info/mock/`.

## How to Run the Frontend (Development)

```bash
cd research_info/frontend
npm install
npm run dev
```

Opens at `http://localhost:5173`.

---

## Team Members

- **Lakshan Muruganandam** — Project lead, research architecture, data pipeline design
- **Kishansingh Rajeshsingh Chauhan** — *(update with your contributions)*
- **Prathamesh Lad** — *(update with your contributions)*
- **Rashmi R K** — *(update with your contributions)*
