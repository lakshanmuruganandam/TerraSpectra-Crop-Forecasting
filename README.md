# TerraSpectra - Hyperspectral Crop Disease Forecasting

This project is focused on precision agriculture and computer vision to identify crop diseases before visible symptoms appear.

## The Problem
Traditional satellite monitoring uses RGB or multispectral images (NDVI). These only detect crop diseases after the leaves yellow or turn brown, meaning the crop's cell structure has already collapsed and yield loss is unavoidable. Standard 2D-CNN models also cannot handle the deep spectral dimensions of hyperspectral data.

## The Solution
TerraSpectra uses 3D spatial-spectral data cubes containing over 200 contiguous bands from 400nm to 2500nm. The backend uses a hybrid 3D-CNN and Vision Transformer model to spot cellular changes, water loss, and chlorophyll breakdown. This allows the system to predict disease hotspots up to three weeks before visible symptoms show, giving time for targeted treatments.

## System Architecture
*   **Geospatial Data Pipeline:** Python scripts using Rasterio and h5py to load datasets and Scikit-learn PCA to reduce spectral depth down to 32 components.
*   **Hybrid Model:** A PyTorch model combining 3D convolutions for spatial-spectral features and a Vision Transformer for inter-band correlations.
*   **Inference API:** FastAPI routes for handling real-time prediction overlays and spatial tiling.
*   **GIS Dashboard:** React 18 frontend with Deck.gl and Mapbox to overlay heatmaps on satellite basemaps with custom Plotly charts.

## Folder Structure
*   `docs/` - Project specifications and master specs (`WEEK1_MAIN_MASTER.md`, `WEEK1_MAIN_MASTER.pdf`).
*   `research_info/` - Central directory containing all research documentation, specs, datasets, scripts, backend, and frontend:
    *   `research_info/backend/` - FastAPI backend architecture and ML pipeline generators.
    *   `research_info/frontend/` - React 18 + Deck.gl + Mapbox GIS dashboard UI application.
    *   `research_info/scripts/` - Dataset downloader scripts (`download_all_training_datasets.py`, `download_datasets.py`) and synthetic mock data generator (`generate_mock_data.py`).
    *   `research_info/raw/` & `research_info/processed/` - Folders for downloading raw satellite data and saving preprocessed outputs.
    *   `research_info/mock/` - Contains generated mock HDF5 cubes and GeoTIFF previews for testing without real satellite downloads.
*   `secret/` - Additional reference blueprints and initial project planning documents.

