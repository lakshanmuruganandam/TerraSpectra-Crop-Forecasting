# Packages and Modules Research

All packages required for the TerraSpectra backend and frontend. This covers Phase 3 of the project specification.

---

## Backend Python Environment

### Geospatial Raster and Datacube I/O

**rasterio** (v1.3+)
- Install: `pip install rasterio`
- Used for reading and writing GeoTIFF files, accessing CRS metadata, applying affine transforms, and reprojecting rasters between EPSG codes.
- Key APIs: `rasterio.open()`, `dataset.read()`, `dataset.crs`, `dataset.transform`, `rasterio.warp.reproject()`

**h5py** (v3.9+)
- Install: `pip install h5py`
- Used for reading and writing HDF5 hyperspectral datacubes. NASA Hyperion and PRISMA data is delivered in HDF5 / HE5 format.
- Key APIs: `h5py.File()`, `f['dataset'][:]`, `f.create_dataset()`, `f.attrs`, chunked storage with `chunks=(64,64,224)`

**netCDF4** (v1.6+)
- Install: `pip install netCDF4`
- Used for reading ESA Sentinel and climate model files in CF-compliant NetCDF4 format.
- Key APIs: `netCDF4.Dataset()`, `dataset.variables['reflectance'][:]`, dimensions and variable metadata

**GDAL / osgeo** (v3.6+)
- Install: `pip install gdal` or via conda `conda install -c conda-forge gdal`
- Low-level geospatial raster engine used internally by rasterio. Also used directly for VRT virtual raster mosaics and warping.
- Key APIs: `gdal.Open()`, `gdal.Warp()`, `gdal.Translate()`, `osr.SpatialReference()`

**spectral (SPy)** (v0.23+)
- Install: `pip install spectral`
- Used specifically for reading ENVI format files (the native delivery format for AVIRIS and HyMap airborne sensors).
- Key APIs: `spectral.open_image('file.hdr')`, `img.read_band()`, `img.read_subimage()`, `img.bands.centers` (wavelength array)

**pyproj** (v3.5+)
- Install: `pip install pyproj`
- Coordinate reference system transformations. Converts between EPSG:4326 (lat/lon) and EPSG:3857 (Web Mercator) for Mapbox tile alignment.
- Key APIs: `pyproj.Transformer.from_crs()`, `transformer.transform(lat, lon)`

**xarray** (v2023+)
- Install: `pip install xarray`
- Labeled N-dimensional arrays. Used for opening NetCDF time-series satellite composites with named dimensions (time, band, x, y).
- Key APIs: `xr.open_dataset()`, `ds.sel(band=670)`, `ds.isel(time=0)`

---

### Machine Learning and Dimensionality Reduction

**numpy** (v1.24+)
- Install: `pip install numpy`
- Foundation for all array math. Used for tensor reshaping, band indexing, reflectance normalization, and covariance matrix construction.
- Key APIs: `np.reshape()`, `np.linalg.eig()`, `np.cumsum()`, `np.clip()`, `np.argmin()`

**scipy** (v1.11+)
- Install: `pip install scipy`
- Signal processing for spectral smoothing (Savitzky-Golay filter), convex hull computation for continuum removal, and statistical tests.
- Key APIs: `scipy.signal.savgol_filter()`, `scipy.spatial.ConvexHull()`, `scipy.stats.ks_2samp()`

**scikit-learn** (v1.3+)
- Install: `pip install scikit-learn`
- Used for PCA dimensionality reduction, train/test splitting, and StandardScaler normalization.
- Key APIs: `sklearn.decomposition.PCA(n_components=32)`, `pca.fit_transform()`, `pca.explained_variance_ratio_`, `sklearn.preprocessing.StandardScaler()`

**pandas** (v2.0+)
- Install: `pip install pandas`
- Used for ground truth label CSV management, spectroradiometer dataset loading, and organizing per-pixel spectral metadata.
- Key APIs: `pd.read_csv()`, `df.groupby()`, `df.merge()`

---

### Deep Learning

**torch (PyTorch)** (v2.1+)
- Install: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`
- Core deep learning framework. Used for defining 3D-CNN layers, Vision Transformer attention blocks, training loops, CUDA tensor operations, and mixed precision (AMP).
- Key APIs: `nn.Conv3d()`, `nn.TransformerEncoderLayer()`, `torch.cuda.amp.autocast()`, `torch.utils.data.DataLoader()`, `nn.Module`

**timm** (v0.9+)
- Install: `pip install timm`
- HuggingFace model hub for Vision Transformer (ViT) pretrained backbone architectures.
- Key APIs: `timm.create_model('vit_base_patch16_224', pretrained=True)`, `model.forward_features()`

**einops** (v0.7+)
- Install: `pip install einops`
- Elegant tensor reshaping for Transformer token preparation from 3D CNN feature maps.
- Key APIs: `einops.rearrange(x, 'b c d h w -> b (h w) (c d)')`, `einops.reduce()`

---

### Explainable AI (XAI)

**captum** (v0.6+)
- Install: `pip install captum`
- PyTorch-native XAI library. Used for Integrated Gradients spectral attribution to identify which wavelengths (bands) drive disease predictions.
- Key APIs: `captum.attr.IntegratedGradients(model)`, `ig.attribute(input_tensor, target=class_idx)`, `captum.attr.LayerGradCam()`

**shap** (v0.43+)
- Install: `pip install shap`
- Shapley value-based feature attribution. Used for global band importance plots across the full training set.
- Key APIs: `shap.DeepExplainer(model, background)`, `shap.summary_plot(shap_values, feature_names=wavelengths)`

---

### REST API

**FastAPI** (v0.104+)
- Install: `pip install fastapi`
- Async REST API framework. Provides automatic OpenAPI / Swagger docs, Pydantic schema validation, and ASGI compatibility.
- Key APIs: `@app.get()`, `@app.post()`, `FastAPI(title=...)`, `APIRouter()`, `BackgroundTasks`

**uvicorn** (v0.24+)
- Install: `pip install uvicorn[standard]`
- ASGI server used to serve the FastAPI application. Supports HTTP/2 and WebSockets.
- Run command: `uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000`

**pydantic** (v2.0+)
- Install: Bundled with FastAPI
- Data validation and serialization library. All request/response JSON schemas are defined as Pydantic BaseModel classes.
- Key APIs: `class PCARequest(BaseModel)`, `model.model_validate()`, `model.model_dump()`

**python-multipart** (v0.0.6+)
- Install: `pip install python-multipart`
- Required for file upload endpoints (for uploading HDF5 hyperspectral datacubes to the API).

**httpx** (v0.25+)
- Install: `pip install httpx`
- Async HTTP client. Used in pytest tests to call FastAPI endpoints via `httpx.AsyncClient(app=app)`.

---

### Vector GIS and Signal Processing

**shapely** (v2.0+)
- Install: `pip install shapely`
- Geometric operations on farm boundary polygons (intersection, union, buffer zones around disease hotspots).
- Key APIs: `shapely.geometry.Polygon()`, `polygon.intersection()`, `polygon.area`

**geopandas** (v0.14+)
- Install: `pip install geopandas`
- GeoDataFrame for loading, filtering, and reprojecting farm boundary GeoJSON files.
- Key APIs: `gpd.read_file('farm_boundaries.geojson')`, `gdf.to_crs('EPSG:3857')`, `gdf.plot()`

---

### MLOps

**mlflow** (v2.8+)
- Install: `pip install mlflow`
- Experiment tracking for PCA variance ratios, model accuracy, and training hyperparameters.
- Key APIs: `mlflow.start_run()`, `mlflow.log_param()`, `mlflow.log_metric()`, `mlflow.pytorch.log_model()`

**wandb** (v0.16+)
- Install: `pip install wandb`
- Real-time training dashboards, GPU utilization monitoring, and model artifact versioning.
- Key APIs: `wandb.init(project='terraspectra')`, `wandb.log({'train_loss': loss})`, `wandb.log_artifact()`

**evidently** (v0.4+)
- Install: `pip install evidently`
- Used for detecting seasonal spectral drift in production data vs training distribution.
- Key APIs: `evidently.report.Report(metrics=[DataDriftPreset()])`, `report.run(reference_data=df_train, current_data=df_prod)`

---

### Testing

**pytest** (v7.4+)
- Install: `pip install pytest pytest-asyncio pytest-cov`
- Python test runner for all backend unit and integration tests.
- Key APIs: `@pytest.fixture`, `@pytest.mark.asyncio`, `pytest.approx()`, `--cov=backend --cov-report=html`

---

## Frontend Node.js Environment

All packages are installed inside `research_info/frontend/` using `npm install`.

**React 18** (`react`, `react-dom`)
- Version: 18.2.0
- The UI component framework. Uses concurrent rendering and Suspense for async data loading.

**TypeScript** (v5.0+)
- Strict type checking across all component props, API response shapes, and Deck.gl layer configurations.

**Vite** (v5.0+)
- Ultra-fast ES module bundler and dev server. HMR (Hot Module Replacement) for instant React updates during development.
- Config file: `vite.config.ts`

**@deck.gl/core, @deck.gl/layers, @deck.gl/react** (v8.9+)
- Install: `npm install @deck.gl/core @deck.gl/layers @deck.gl/react`
- WebGL2 GIS rendering engine. GeoJsonLayer for farm boundaries, BitmapLayer for heatmaps, TileLayer for pyramid tile loading.

**mapbox-gl** (v3.0+)
- Install: `npm install mapbox-gl`
- Satellite basemap renderer. Requires a Mapbox public access token from mapbox.com/account.

**react-map-gl** (v7.1+)
- Install: `npm install react-map-gl`
- React wrapper for Mapbox GL JS. Manages viewport state as a controlled React state.

**plotly.js / react-plotly.js** (v2.26+)
- Install: `npm install plotly.js react-plotly.js`
- Interactive charting library. Used to render the 224-band spectral reflectance line chart when a pixel is clicked on the map.

**tailwindcss** (v3.3+)
- Install: `npm install tailwindcss postcss autoprefixer`
- Utility-first CSS framework for layout, typography, and dark mode theming.

**zustand** (v4.4+)
- Install: `npm install zustand`
- Lightweight global state management. Used for sharing selected pixel coordinates and spectral data between the map and chart components.

**vitest** (v1.0+)
- Install: `npm install vitest @testing-library/react @testing-library/jest-dom`
- Vite-native test runner. Replaces Jest for React component unit testing, hook testing, and Deck.gl layer mocking.
