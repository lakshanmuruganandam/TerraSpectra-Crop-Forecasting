import os
import sys
import subprocess

def install_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Ensure h5py, numpy, and rasterio are installed
install_package("h5py")
install_package("numpy")
install_package("rasterio")

import numpy as np
import h5py
import rasterio
from rasterio.transform import from_bounds

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK_H5_PATH = os.path.join(PROJECT_ROOT, "research_info", "mock", "mock_farm_datacube.h5")
MOCK_TIF_PATH = os.path.join(PROJECT_ROOT, "research_info", "mock", "mock_farm_preview.tif")

def generate_mock_datasets(height=512, width=512, num_bands=224):
    print("Generating mock agricultural HDF5 and GeoTIFF datasets...")
    try:
        # Generate Wavelengths (400nm to 2500nm)
        wavelengths = np.linspace(400, 2500, num_bands)
        
        # Base Reflectance Curves
        veg_curve = np.zeros(num_bands)
        for i, w in enumerate(wavelengths):
            if w < 500:
                veg_curve[i] = 0.05 + 0.02 * np.random.randn()
            elif 500 <= w < 600:
                veg_curve[i] = 0.15 + 0.03 * np.exp(-((w - 550)**2)/800)
            elif 600 <= w < 680:
                veg_curve[i] = 0.04 + 0.01 * np.random.randn()
            elif 680 <= w < 750:
                veg_curve[i] = 0.05 + 0.45 * (w - 680) / 70
            elif 750 <= w < 1300:
                veg_curve[i] = 0.50 + 0.03 * np.random.randn()
            elif 1300 <= w < 1500:
                veg_curve[i] = 0.25 - 0.15 * np.exp(-((w - 1450)**2)/1000)
            else:
                veg_curve[i] = 0.20 + 0.05 * np.random.randn()

        infected_curve = veg_curve.copy()
        for i, w in enumerate(wavelengths):
            if 680 <= w < 750:
                infected_curve[i] *= 0.6
            elif 750 <= w < 1300:
                infected_curve[i] *= 0.55
            elif 1300 <= w < 1500:
                infected_curve[i] += 0.12

        # Create Spatial Grid
        cube = np.zeros((height, width, num_bands), dtype=np.float32)
        labels = np.zeros((height, width), dtype=np.int32)
        
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
        
        # Save HDF5
        with h5py.File(MOCK_H5_PATH, 'w') as h5f:
            h5f.create_dataset('hyperspectral_cube', data=cube, compression='gzip', chunks=(64, 64, num_bands))
            h5f.create_dataset('ground_truth_labels', data=labels, compression='gzip')
            h5f.create_dataset('wavelengths', data=wavelengths)
            h5f.attrs['location'] = 'Iowa Farm Zone Alpha'
            h5f.attrs['sensor'] = 'Synthetic Hyperion AVIRIS-NG'
            h5f.attrs['epsg'] = 4326
            h5f.attrs['bbox'] = [-93.62, 41.58, -93.60, 41.60]
        print(f"Saved mock farm HDF5 datacube to: {MOCK_H5_PATH}")

        # Save RGB Proxy GeoTIFF
        r_idx = np.argmin(np.abs(wavelengths - 650))
        g_idx = np.argmin(np.abs(wavelengths - 550))
        b_idx = np.argmin(np.abs(wavelengths - 470))
        rgb_raster = np.stack([cube[:, :, r_idx], cube[:, :, g_idx], cube[:, :, b_idx]], axis=0)
        rgb_uint8 = (rgb_raster * 255).astype(np.uint8)
        
        transform = from_bounds(-93.62, 41.58, -93.60, 41.60, width, height)
        with rasterio.open(
            MOCK_TIF_PATH,
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
        print(f"Saved mock farm GeoTIFF preview to: {MOCK_TIF_PATH}")
        print("Mock dataset generation completed successfully.")
    except Exception as e:
        print(f"Error generating mock datasets: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_mock_datasets()
