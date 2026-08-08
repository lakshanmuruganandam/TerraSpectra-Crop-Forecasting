# Phase 2 Data Assets: Hyperspectral Crop Disease Forecasting

## 1. Airborne Hyperspectral Datacubes (e.g., NASA AVIRIS-NG)
*   **Portal Names:** NASA JPL AVIRIS Data Portal, NASA Earthdata Search.
*   **API Access Methods:** Earthdata CMR (Common Metadata Repository) API, standard `earthaccess` Python library.
*   **Formatting:** ENVI format (binary file with a `.hdr` header), NetCDF4.
*   **CRS Details:** WGS 84 (EPSG:4326) or projected UTM zones (e.g., EPSG:326XX).

## 2. Spaceborne Satellite Datacubes (e.g., EO-1 Hyperion, PRISMA, EnMAP)
*   **Portal Names:** USGS EarthExplorer (Hyperion), ASI PRISMA Portal (Italian Space Agency), DLR EOWEB GeoPortal (EnMAP).
*   **API Access Methods:** USGS M2M (Machine-to-Machine) API, ASI PRISMA REST API, DLR EOWEB API.
*   **Formatting:** 
    *   Hyperion: HDF4, GeoTIFF
    *   PRISMA: HDF5 (specifically HE5-EOS)
    *   EnMAP: GeoTIFF, ENVI
*   **CRS Details:** Geolocated raw data in EPSG:4326; Ortho-rectified L2A products typically in WGS 84 / UTM zones (EPSG:326XX / EPSG:327XX).

## 3. Multispectral Satellite Calibration Imagery (e.g., Sentinel-2/6)
*   *Note: Sentinel-2 is primarily used for multispectral optical imagery, whereas Sentinel-6 focuses on radar altimetry.*
*   **Portal Names:** Copernicus Data Space Ecosystem (CDSE, replaced SciHub).
*   **API Access Methods:** OData API, STAC (SpatioTemporal Asset Catalog) API, Sentinel Hub Process API.
*   **Formatting:** SAFE format containing JPEG2000 (`.jp2`) and Cloud Optimized GeoTIFFs (COG).
*   **CRS Details:** WGS 84 / UTM zones (EPSG:326XX / EPSG:327XX).

## 4. Spectroradiometer Ground Truth Leaf Measurement Datasets
*   **Portal Names:** EcoSIS Spectral Library, NASA ORNL DAAC (for ABoVE datasets).
*   **API Access Methods:** EcoSIS REST API (`https://ecosis.org/api`), ORNL DAAC Spatial Data Access API.
*   **Formatting:** CSV, JSON, NetCDF.
*   **CRS Details:** Ground point measurements are consistently standard WGS 84 (EPSG:4326).

## 5. 3D Digital Elevation Models (DEM) & Farm Boundary Vector Polygons
*   **Portal Names:** Mapbox Studio, AWS Registry of Open Data (Copernicus 30m DEM), USDA FSA/CropScape (for US boundaries).
*   **API Access Methods:** Mapbox Raster Tiles API, AWS S3 STAC access, OGC WFS/WMS for boundaries.
*   **Formatting:** 
    *   DEM: Terrain-RGB (PNG), Cloud Optimized GeoTIFF (COG).
    *   Boundaries: GeoJSON, ESRI Shapefile.
*   **CRS Details:** DEM Terrain-RGB is usually EPSG:3857 (Web Mercator); Farm Boundaries are typically EPSG:4326 or local state plane projections.

## 6. Web GIS Tile Provider Access Tokens (Mapbox, etc.)
*   **Portal Names:** Mapbox Developer Portal, Sentinel Hub, Google Earth Engine.
*   **API Access Methods:** Mapbox Static Tiles API, Mapbox GL JS access token provisioning, RESTful XYZ tile endpoints.
*   **Formatting:** XYZ Tiles (PNG/JPG for raster tiles, Mapbox Vector Tiles/MVT for vector data).
*   **CRS Details:** Almost exclusively EPSG:3857 (Web Mercator) for compatibility with web-based maps.

## 7. Synthetic Datacube Generator Scripts/Methodologies
*   **Methodologies:** PROSAIL (Radiative Transfer Model for simulating leaf/canopy reflectance), DIRSIG, SCOPE (Soil Canopy Observation, Photochemistry and Energy fluxes).
*   **Portal Names / Access:** Open-source GitHub repositories (e.g., `prosail` Python package).
*   **API Access Methods:** Standard programmatic interfaces via Python or R libraries (import packages to define geometry, leaf biophysics, and output synthetics).
*   **Formatting:** Outputs are generated as N-dimensional NumPy arrays, typically serialized into HDF5 or NetCDF4 formats.
*   **CRS Details:** Inherently user-defined based on synthetic scenarios, but generally modeled onto standard grids mapping to EPSG:4326 or EPSG:3857.
