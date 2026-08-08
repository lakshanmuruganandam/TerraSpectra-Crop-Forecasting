# 🌾 TerraSpectra — Hyperspectral Crop Disease Forecasting

**Domain:** Precision Agriculture & Advanced Computer Vision  
**Status:** Active Development (Week 1 / Phase 5)

---

## ⚠️ Problem Statement
Traditional satellite crop monitoring relies on standard 3-channel RGB or simple 4-channel Multispectral imagery (NDVI). These models suffer from a fatal flaw: **they only detect crop diseases after leaves turn yellow or brown (foliar chlorosis and necrosis)**. By the time visual symptoms appear to human eyes or standard 2D-CNNs, internal cellular structures have already collapsed, making yield loss unrecoverable. 

Furthermore, standard 2D-CNNs treat image input as flat spatial matrices and are fundamentally incapable of processing the massive 3D spatial-spectral depth of Hyperspectral Data Cubes.

## 💡 The TerraSpectra Solution
**TerraSpectra** ingests **Hyperspectral Satellite Data Cubes** capturing **200+ contiguous spectral bands of light** across the electromagnetic spectrum (400 nm to 2500 nm), analyzing subtle chemical changes in plant chlorophyll absorption, anthocyanin accumulation, and cellular water retention.

Using a **Hybrid 3D-CNN + Vision Transformer (ViT)** AI model, TerraSpectra highlights specific infection zones in glowing red on a 3D WebGL dashboard, predicting a **fungal blight outbreak three weeks before any visible symptoms appear**. This allows farm managers to execute localized preventative treatment, saving 95% of pesticide costs and preserving crop yield.

## 🛠️ Core System Architecture
1. **Geospatial Data Pipeline (Python):** Ingests and normalizes multi-gigabyte hyperspectral datacubes (HDF5 / GeoTIFF), using Scikit-learn PCA to compress 200+ bands down to 32 principal components.
2. **Hybrid 3D-CNN & ViT AI Model (PyTorch):** Deep learning architecture utilizing 3D spatial-spectral convolutions alongside a Transformer self-attention engine.
3. **High-Throughput Inference API (FastAPI):** GPU-accelerated REST API handling spatial chunking and real-time prediction raster generation.
4. **Interactive GIS Dashboard (React 18 + Deck.gl):** Professional 3D map interface rendering disease heatmaps over satellite topography, equipped with interactive pixel-picking for 224-band spectral reflectance charting.

## 📂 Project Structure (Full-Stack Monorepo)
```text
TerraSpectra-Crop-Forecasting/
├── backend/                  # Python AI Pipeline & API Code
│   ├── api/                  # FastAPI routes and DTOs
│   └── ml_pipeline/          # PCA scripts, 3D-CNN, and tensor slicing
├── frontend/                 # WebGL GIS Dashboard
│   ├── public/               
│   └── src/                  # React 18, Deck.gl, Mapbox, TailwindCSS
├── data/                     # Raw & Processed Datacubes (Git-Ignored)
├── docs/                     # Executive Planning Documents
│   ├── WEEK1_MAIN_MASTER.md  
│   └── WEEK1_MAIN_MASTER.pdf 
└── research_info/            # R&D Documentation & References
```

## 🚀 Quick Start
*See `docs/WEEK1_MAIN_MASTER.pdf` for the complete Phase 1 to Phase 5 execution roadmap.*
