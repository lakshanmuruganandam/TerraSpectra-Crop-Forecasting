# CONTRIBUTING.md — TerraSpectra

---

## Lakshan Muruganandam

**Research Documents**

- `research_info/spectral_physics_and_pca.md` — Spectral physics, wavelength ranges (VIS/NIR/SWIR), plant disease biomarkers, atmospheric calibration, continuum removal, full PCA math, vegetation indices (PRI, WBI, SIPI)
- `research_info/3d_dl_architecture.md` — 3D-CNN + Vision Transformer hybrid architecture, CUDA tiling, Integrated Gradients XAI, seasonal drift MLOps
- `research_info/data_assets.md` — Acquisition guide for AVIRIS, Hyperion, PRISMA, EnMAP, Sentinel-2, EcoSIS spectra, DEM tiles, GeoJSON farm boundaries
- `research_info/frontend_gis_webgl.md` — Deck.gl layer architecture, Mapbox GL JS React integration, pixel picking, Plotly spectral chart, WebGL memory management
- `research_info/packages_and_modules.md` — Every Python and Node.js package: rasterio, h5py, PyTorch, timm, FastAPI, deck.gl, mapbox-gl, plotly.js — versions, install commands, key APIs
- `research_info/geospatial_file_standards.md` — HDF5, GeoTIFF, NetCDF4, ENVI format specs, EPSG:4326 / EPSG:3857 / UTM coordinate systems, GeoJSON, Terrain-RGB DEM
- `research_info/api_backend_scaffold.md` — FastAPI architecture, CORS, Pydantic DTOs, all API endpoints design, sliding-window tiling, Swagger docs, async pytest patterns
- `research_info/security_and_privacy.md` — Farm spatial privacy (GDPR/USDA), JWT auth, RBAC, CORS hardening, CUDA memory isolation, AES-256 encryption, rate limiting, audit logging
- `research_info/mlops_and_testing.md` — pytest, vitest, MLflow, wandb sweeps, Evidently drift detection, CI/CD GitHub Actions, OA/AA/Kappa benchmark metrics
- `research_info/training_datasets_reference.md` — Full reference for all 13 training datasets: sensor specs, spatial/band dimensions, all class labels, Python loading code
- `research_info/ABSTRACT_AND_TRACKING.md` — Project abstract, problem statement, phase-by-phase progress tracking
- `research_info/ULTIMATE_DATASET_TRACKER.md` — Master tracker for every dataset: Indian Pines, Salinas, Pavia, Botswana, KSC, WHU-Hi, Houston, Chikusei, Muufl, Trento, Augsburg, Mars CRISM

**Scripts**

- `research_info/scripts/download_all_training_datasets.py` — Master download script for all 13 training datasets via HuggingFace (Indian Pines, Salinas, Pavia, Botswana, KSC, WHU-Hi, full HSI collection, USGS spectra, GeoJSON boundaries). Run manually when needed.
- `research_info/scripts/download_datasets.py` — HuggingFace snapshot downloader for the Tanishq165/HSI_Datasets collection
- `research_info/scripts/generate_mock_data.py` — Synthetic 200×200×224 band HDF5 agricultural datacube generator with embedded blight zone, plus RGB GeoTIFF preview

**Backend**

- `research_info/backend/requirements.txt` — Full Python dependency list (FastAPI, uvicorn, rasterio, h5py, PyTorch, scikit-learn, mlflow, wandb, evidently, pytest and more)
- `research_info/backend/ml_pipeline/generate_synthetic_hsi.py` — Generates a synthetic AVIRIS-like HDF5 hyperspectral cube with realistic vegetation spectral signature
- `research_info/backend/ml_pipeline/generate_mock_datasets.py` — Mass-generates synthetic `.mat` fallback files for all 10 benchmark datasets with correct variable names and spectral signatures

**Frontend Scaffold**

- `research_info/frontend/src/App.tsx` — Root React component, entry point for the GIS dashboard
- `research_info/frontend/src/index.css` — Global styles and Tailwind CSS directives
- `research_info/frontend/src/main.tsx` — React DOM render entry point
- `research_info/frontend/package.json` — Node.js manifest with all frontend dependencies (deck.gl, mapbox-gl, plotly.js, zustand, vitest)
- `research_info/frontend/vite.config.ts` — Vite bundler config
- `research_info/frontend/tailwind.config.js` — Tailwind CSS theme configuration
- `research_info/frontend/index.html` — HTML entry point

---

## Kishansingh Rajeshsingh Chauhan

## Kishansingh Rajeshsingh Chauhan

Set up the frontend — React + Vite + TypeScript app inside `frontend/`.

Got the base map working with Mapbox and Deck.gl (satellite view, full pan/zoom/rotate/tilt). Added a Deck.gl layer on top for farm field boundaries, using mock GeoJSON data for now since real farm data isn't in yet — 3 placeholder fields near Ahmedabad. Also added hover tooltips on the fields and a small live readout showing lat/lng/zoom in the corner.

Files:
- `frontend/src/App.tsx` main map component
- `frontend/src/layers/farmBoundaryLayer.ts` the boundary layer
- `frontend/src/data/mockFarmFields.ts` placeholder field data (has `fieldId` so it's easy to hook up real backend data later)

## Prathamesh Lad

*(Add your files and contributions here)*

---

## Rashmi R K

Added Indian Pines hyperspectral dataset.
Added data/indianpinearray.npy-hyperspectral image data
Added data/IPgt.npy-ground-truth labels for the Indian Pines dataset
