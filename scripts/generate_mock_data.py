import os
import h5py
import numpy as np
import rasterio
from rasterio.transform import from_bounds

def generate_synthetic_hyperspectral_cube(
    output_h5_path: str,
    output_tif_path: str,
    height: int = 512,
    width: int = 512,
    num_bands: int = 224
):
    """
    Generates a synthetic 224-band Hyperspectral Data Cube simulating an agricultural farm
    with healthy crops, soil, water bodies, and an early-stage fungal blight outbreak.
    """
    os.makedirs(os.path.dirname(output_h5_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_tif_path), exist_ok=True)
    print(f"Generating synthetic hyperspectral data cube ({height}x{width}x{num_bands})...")
    
    # 1. Generate Wavelengths (400nm to 2500nm)
    wavelengths = np.linspace(400, 2500, num_bands)
    
    # 2. Base Reflectance Curves
    veg_curve = np.zeros(num_bands)
    for i, w in enumerate(wavelengths):
        if w < 500:
            veg_curve[i] = 0.05 + 0.02 * np.random.randn() # Blue absorption
        elif 500 <= w < 600:
            veg_curve[i] = 0.15 + 0.03 * np.exp(-((w - 550)**2)/800) # Green reflection peak
        elif 600 <= w < 680:
            veg_curve[i] = 0.04 + 0.01 * np.random.randn() # Red absorption
        elif 680 <= w < 750:
            veg_curve[i] = 0.05 + 0.45 * (w - 680) / 70 # Red Edge steep incline
        elif 750 <= w < 1300:
            veg_curve[i] = 0.50 + 0.03 * np.random.randn() # NIR plateau
        elif 1300 <= w < 1500:
            veg_curve[i] = 0.25 - 0.15 * np.exp(-((w - 1450)**2)/1000) # Water absorption
        else:
            veg_curve[i] = 0.20 + 0.05 * np.random.randn() # SWIR region

    infected_curve = veg_curve.copy()
    for i, w in enumerate(wavelengths):
        if 680 <= w < 750:
            infected_curve[i] *= 0.6  # Chlorophyll breakdown
        elif 750 <= w < 1300:
            infected_curve[i] *= 0.55 # Cell structure breakdown
        elif 1300 <= w < 1500:
            infected_curve[i] += 0.12 # Foliar water loss

    # 3. Create Spatial Grid
    cube = np.zeros((height, width, num_bands), dtype=np.float32)
    labels = np.zeros((height, width), dtype=np.int32) # 0: Healthy, 1: Infected Blight Zone
    
    for b in range(num_bands):
        cube[:, :, b] = veg_curve[b] + np.random.normal(0, 0.02, (height, width))
    
    cy, cx, radius = 250, 300, 60
    y_grid, x_grid = np.ogrid[:height, :width]
    dist_from_center = np.sqrt((x_grid - cx)**2 + (y_grid - cy)**2)
    infection_mask = dist_from_center <= radius
    
    for b in range(num_bands):
        cube[:, :, b][infection_mask] = infected_curve[b] + np.random.normal(0, 0.02, np.sum(infection_mask))
    labels[infection_mask] = 1

    cube = np.clip(cube, 0.0, 1.0)
    
    # 4. Save to HDF5 Format
    with h5py.File(output_h5_path, 'w') as h5f:
        h5f.create_dataset('hyperspectral_cube', data=cube, compression='gzip', chunks=(64, 64, num_bands))
        h5f.create_dataset('ground_truth_labels', data=labels, compression='gzip')
        h5f.create_dataset('wavelengths', data=wavelengths)
        h5f.attrs['location'] = 'Iowa Farm Zone Alpha'
        h5f.attrs['sensor'] = 'Synthetic Hyperion AVIRIS-NG'
        h5f.attrs['epsg'] = 4326
        h5f.attrs['bbox'] = [-93.62, 41.58, -93.60, 41.60]
    
    print(f"✅ HDF5 Hyperspectral Data Cube saved to: {output_h5_path}")

    # 5. Save RGB Synthetic Proxy GeoTIFF using Rasterio
    r_idx = np.argmin(np.abs(wavelengths - 650))
    g_idx = np.argmin(np.abs(wavelengths - 550))
    b_idx = np.argmin(np.abs(wavelengths - 470))
    
    rgb_raster = np.stack([cube[:, :, r_idx], cube[:, :, g_idx], cube[:, :, b_idx]], axis=0)
    rgb_uint8 = (rgb_raster * 255).astype(np.uint8)

    transform = from_bounds(-93.62, 41.58, -93.60, 41.60, width, height)
    
    with rasterio.open(
        output_tif_path,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=3,
        dtype=np.uint8,
        crs='EPSG:4326',
        transform=transform,
    ) as dst:
        dst.write(rgb_uint8)
        
    print(f"✅ GeoTIFF RGB preview saved to: {output_tif_path}")

if __name__ == "__main__":
    generate_synthetic_hyperspectral_cube(
        output_h5_path="/Users/lakshanmuruganandam/Desktop/INFOTACT/PROJECT-1/data/mock_farm_datacube.h5",
        output_tif_path="/Users/lakshanmuruganandam/Desktop/INFOTACT/PROJECT-1/data/mock_farm_preview.tif"
    )
