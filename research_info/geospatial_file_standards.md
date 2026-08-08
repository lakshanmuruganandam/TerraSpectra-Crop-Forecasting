# Geospatial File Standards and Coordinate Reference Systems

Research notes covering every file format used in the TerraSpectra hyperspectral data pipeline.

---

## 1. HDF5 Format

HDF5 (Hierarchical Data Format version 5) is the primary container format for large-scale multidimensional scientific datasets. NASA Hyperion, PRISMA (ESA/ASI), and AVIRIS-NG all deliver data in HDF5 or HDF5-based formats.

### Internal Structure
HDF5 is organized like a filesystem inside a single binary file:
- **Groups**: Analogous to directories. Nest datasets hierarchically (e.g., `/HDFEOS/GRIDS/Grid1/Data Fields/EO1H_reflectance`)
- **Datasets**: N-dimensional arrays stored with a defined dtype (float32, int16, etc.)
- **Attributes**: Key-value metadata attached to groups or datasets (sensor name, wavelength array, acquisition date, EPSG code)

### Chunking Strategy for 3D Hyperspectral Cubes
A cube of shape (512, 512, 224) with float32 = 238 MB uncompressed. Chunking divides this into smaller tiles for efficient partial I/O:
- Recommended chunk shape for spatial queries: `(64, 64, 224)` — reads full spectral depth for a spatial tile
- Recommended chunk shape for spectral queries: `(512, 512, 8)` — reads a few bands across the full scene
- Always enable `compression='gzip'` with `compression_opts=4` for ~3-5x size reduction

### NASA AVIRIS HDF5 Layout
AVIRIS-NG delivers Level 2 reflectance as HDF5 with the following structure:
```
/reflectance          shape=(lines, samples, bands), dtype=float32
/wavelength           shape=(bands,), units=nanometers
/fwhm                 shape=(bands,), full-width-half-maximum per band
/glt_x, /glt_y       geographic lookup tables for orthorectification
```

### PRISMA HDF5 Layout (HE5-EOS)
PRISMA uses HE5 (an HDF5 extension for Earth Observation):
```
/HDFEOS/SWATHS/PRS_L2D_HCO/Data Fields/VNIR_Cube   shape=(1000, 1000, 66)
/HDFEOS/SWATHS/PRS_L2D_HCO/Data Fields/SWIR_Cube   shape=(1000, 1000, 173)
/HDFEOS/SWATHS/PRS_L2D_HCO/Geolocation Fields/Latitude
/HDFEOS/SWATHS/PRS_L2D_HCO/Geolocation Fields/Longitude
```

### Reading with h5py
```python
import h5py
with h5py.File('aviris_data.h5', 'r') as f:
    cube = f['reflectance'][:]          # full read
    wavelengths = f['wavelength'][:]
    band_50 = f['reflectance'][:, :, 50]  # single band (chunk-efficient if chunked spatially)
```

---

## 2. GeoTIFF Format

GeoTIFF embeds georeferencing metadata (CRS, affine transform, bounding box) directly inside a standard TIFF image. It is the most widely used raster format in GIS.

### Key TIFF Tags and GeoKey Directory
- **GeoKeyDirectoryTag (34736)**: Contains the GeoKey entries defining the CRS
- **ModelPixelScaleTag (33550)**: X/Y pixel resolution in CRS units
- **ModelTiepointTag (33922)**: Maps a pixel coordinate to a ground coordinate
- **GDALMetadata**: Additional metadata as XML inside the TIFF

### Rasterio Read/Write API
```python
import rasterio
from rasterio.transform import from_bounds

# Reading
with rasterio.open('scene.tif') as src:
    data = src.read()           # shape: (bands, height, width)
    crs = src.crs               # e.g. CRS.from_epsg(4326)
    transform = src.transform   # affine transform object
    bounds = src.bounds         # BoundingBox(left, bottom, right, top)

# Writing
with rasterio.open('output.tif', 'w', driver='GTiff',
                   height=512, width=512, count=3,
                   dtype='uint8', crs='EPSG:4326',
                   transform=from_bounds(-93.62, 41.58, -93.60, 41.60, 512, 512)) as dst:
    dst.write(rgb_array)
```

### Cloud Optimized GeoTIFF (COG)
COG is a GeoTIFF with internal tiling and overview levels (image pyramids) that allow HTTP range requests — meaning a web server can serve partial tiles without downloading the full file. Used by the TileLayer in Deck.gl.
- Internal tile size: 512x512 pixels
- Overview levels: each halved from the full resolution (e.g., 1:1, 1:2, 1:4, 1:8)
- Created with: `gdal_translate input.tif output_cog.tif -of COG -co COMPRESS=DEFLATE`

### Band Interleaving
- **BSQ (Band Sequential)**: All rows/cols for Band 1, then Band 2. Best for full-band reads.
- **BIL (Band Interleaved by Line)**: Row 1 of all bands, then Row 2. Balanced for mixed access.
- **BIP (Band Interleaved by Pixel)**: All bands for Pixel(0,0), then Pixel(0,1). Best for spectral queries.

---

## 3. NetCDF4 Format

NetCDF4 (Network Common Data Form) is used for multidimensional climate and satellite time-series data. ESA Sentinel-2 L1C products and many atmospheric model outputs use NetCDF.

### CF Conventions
The Climate and Forecast (CF) conventions define standard variable naming, units, and coordinate systems. Key conventions:
- Dimensions must include `time`, `lat`, `lon` or `x`, `y`
- Variables must have `units` attribute (e.g., `'nm'` for wavelengths, `'W m-2 sr-1 um-1'` for radiance)
- Coordinate variables must match their dimension name

### Reading with xarray
```python
import xarray as xr
ds = xr.open_dataset('sentinel2_reflectance.nc')
# Access a specific band by wavelength
b8a = ds['reflectance'].sel(wavelength=865, method='nearest')
# Slice a spatial region
region = ds['reflectance'].isel(x=slice(100, 200), y=slice(100, 200))
```

---

## 4. ENVI Format

ENVI (Environment for Visualizing Images) is the native format of AVIRIS airborne sensors and many HyMap/CASI deliveries. It consists of two files: a raw binary data file and a plaintext `.hdr` header.

### Header File Structure (.hdr)
```
ENVI
description = { AVIRIS-NG Reflectance }
samples = 598
lines = 512
bands = 425
header offset = 0
file type = ENVI Standard
data type = 4           ; 4 = float32
interleave = bil
sensor type = AVIRIS-NG
wavelength units = nanometers
wavelength = {
  380.000, 390.000, 400.000, ..., 2500.000
}
fwhm = {
  6.00, 6.00, ..., 6.00
}
```

### Reading with spectral Python (SPy)
```python
import spectral
img = spectral.open_image('aviris_scene.hdr')
cube = img.load()                        # shape: (lines, samples, bands)
wavelengths = img.bands.centers          # array of wavelength center values
single_band = img.read_band(50)          # reads band index 50
```

---

## 5. Coordinate Reference Systems

### EPSG:4326 — WGS 84 Geographic
- Coordinates: latitude (degrees N/S) and longitude (degrees E/W)
- Used for: raw GPS coordinates, GeoJSON farm boundaries, satellite metadata lat/lon bounding boxes, ground truth GPS measurements
- Datum: World Geodetic System 1984 ellipsoid

### EPSG:3857 — Web Mercator
- Coordinates: X and Y in meters from the origin (0°N, 0°E)
- Used for: Mapbox satellite basemap tiles, Deck.gl BitmapLayer bounds, XYZ tile endpoints
- The projection distorts area at high latitudes but is standard for all web mapping applications
- Conversion at equator: 1 degree longitude ≈ 111,320 meters

### UTM Zones (EPSG:326XX / 327XX)
- Used for: orthorectified satellite imagery (Sentinel-2, PRISMA L2A)
- Zone calculation: zone = floor((longitude + 180) / 6) + 1
- Example: Iowa farmland (~93°W) falls in UTM Zone 15N = EPSG:32615

### Reprojection with pyproj and rasterio
```python
from pyproj import Transformer
transformer = Transformer.from_crs('EPSG:4326', 'EPSG:3857', always_xy=True)
x_web_mercator, y_web_mercator = transformer.transform(lon, lat)

# Reprojecting a full raster with rasterio
from rasterio.warp import reproject, Resampling, calculate_default_transform
transform_new, width, height = calculate_default_transform(
    src.crs, 'EPSG:3857', src.width, src.height, *src.bounds)
```

---

## 6. GeoJSON Format

GeoJSON (RFC 7946) is the standard for encoding geographic features as JSON. Farm boundaries and disease cluster polygons are stored as GeoJSON FeatureCollections.

### Structure
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
          [-93.621, 41.582],
          [-93.619, 41.582],
          [-93.619, 41.580],
          [-93.621, 41.580],
          [-93.621, 41.582]
        ]]
      },
      "properties": {
        "farm_id": "iowa-alpha-001",
        "crop_type": "corn",
        "area_acres": 1000
      }
    }
  ]
}
```

GeoJSON always uses EPSG:4326 (WGS 84) by specification. Deck.gl's GeoJsonLayer reads this directly without reprojection.

---

## 7. Mapbox Terrain-RGB DEM

Terrain-RGB is Mapbox's scheme for encoding elevation data into PNG raster tiles. Each pixel's RGB values encode an elevation value.

### Decoding Formula
```
height = -10000 + ((R * 256 * 256 + G * 256 + B) * 0.1)
```
- Range: -10,000m to +6,553.5m
- Resolution: 0.1 meter vertical
- Tile URL format: `https://api.mapbox.com/v4/mapbox.terrain-rgb/{z}/{x}/{y}.pngraw?access_token={TOKEN}`

### Usage in Deck.gl
The `TerrainLayer` in Deck.gl ingests Terrain-RGB tiles directly and extrudes them into a 3D mesh surface, allowing the disease heatmap overlay to drape over actual farm topography.
- Mapbox style string for satellite + terrain: `mapbox://styles/mapbox/satellite-v9`
- 3D terrain toggle requires `mapbox-gl` v2.9+ with the `terrain` property in the map style JSON
