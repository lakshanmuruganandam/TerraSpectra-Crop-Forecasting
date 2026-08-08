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
*   `backend/` - FastAPI backend and ML training scripts.
*   `frontend/` - React application with Deck.gl and Mapbox integration.
*   `data/` - Holds processed and raw datasets (should be kept clean).
*   `docs/` - Project specifications and timeline blueprints.
*   `research_info/` - Contains all gathered HSI datasets, GeoJSON boundaries, mock data, and theoretical research notes.
