# Research Notes and Summary

Here is the abstract for the project and a tracking of what research we did for the backend and frontend components.

## Project Abstract

The goal of TerraSpectra is to build a crop disease forecasting model using hyperspectral satellite data. Conventional imagery (like RGB or multispectral NDVI) only catches plant disease after leaves change color, which is usually too late. This project uses a hybrid 3D-CNN and Vision Transformer (ViT) to look at 200+ contiguous spectral bands from 400nm to 2500nm. By analyzing changes in water absorption, chlorophyll breakdown, and cellular structure, we want to flag disease zones on a GIS map up to three weeks before visible symptoms appear.

## Research Areas Covered

We divided the research into four main parts to make sure we covered the entire Week 1 specification:

1.  **Backend ML and Physics:**
    *   Wavelength ranges (VIS, Red Edge, NIR, SWIR).
    *   Radiometric and atmospheric correction (6S and FLAASH models).
    *   PCA dimensionality reduction math (explained variance ratio target of >= 98.5%).
    *   Vegetation indices (PRI, WBI, SIPI).
    *   File references: Saved in `spectral_physics_and_pca.md`.

2.  **Data Assets:**
    *   Where to get real AVIRIS and Hyperion data cubes.
    *   Sourcing elevation models (DEM) and farm vector boundaries (GeoJSON).
    *   Mock dataset generation methods.
    *   File references: Saved in `data_assets.md`.

3.  **3D Deep Learning Model Architecture:**
    *   Applying 3D convolutional kernels to capture spatial and spectral features at the same time.
    *   Vision Transformer self-attention to identify correlations between different spectral bands.
    *   PyTorch implementation strategies, memory tiling, and Integrated Gradients.
    *   File references: Saved in `3d_dl_architecture.md`.

4.  **Frontend WebGL GIS Map:**
    *   Using Deck.gl layers (GeoJsonLayer, BitmapLayer, TileLayer) overlaid on Mapbox GL JS.
    *   Syncing map viewport camera.
    *   Reading clicked pixels and plotting their 224-band reflectance curves with Plotly.js.
    *   File references: Saved in `frontend_gis_webgl.md`.
