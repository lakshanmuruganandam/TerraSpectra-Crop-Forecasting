"""
generate_synthetic_hsi.py
--------------------------
Generates a synthetic Hyperspectral Data Cube in HDF5 format.
Mimics AVIRIS sensor structure with 224 spectral bands (400–2500nm).
Embeds a realistic vegetation spectral signature with chlorophyll
absorption dip (Red band ~670nm) and high NIR plateau (750–1300nm).

Output is saved to research_info/mock/ (git-ignored).
Run from any directory — paths resolve relative to this script.
"""

import os
import numpy as np
import h5py

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_DIR   = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "mock"))


def generate_synthetic_hsi(width=200, height=200, bands=224):
    os.makedirs(MOCK_DIR, exist_ok=True)
    output_path = os.path.join(MOCK_DIR, "synthetic_aviris_cube.h5")

    print(f"Generating Synthetic HSI Cube: {height}x{width}x{bands} ...")

    # Base cube: random reflectance noise, float32
    rng = np.random.default_rng(seed=42)
    cube = rng.random((height, width, bands), dtype=np.float32)

    # Chlorophyll absorption at Red band (~670nm = band index 27 at 10nm spacing)
    cube[:, :, 25:35] *= 0.25

    # High NIR plateau (750–1300nm = bands 35–90)
    cube[:, :, 35:90] = np.clip(cube[:, :, 35:90] + 0.45, 0.0, 1.0)

    # SWIR water absorption (1350–1450nm and 1820–1960nm — reduced reflectance)
    cube[:, :, 95:100]  *= 0.15
    cube[:, :, 142:156] *= 0.10

    # Embed a blight zone (top-left 40x40 patch — spectral collapse)
    cube[:40, :40, 25:35] *= 0.05   # chlorophyll crash
    cube[:40, :40, 35:90] *= 0.40   # NIR plateau collapse

    cube = np.clip(cube, 0.0, 1.0)

    wavelengths = np.linspace(400, 2500, bands, dtype=np.float32)

    with h5py.File(output_path, "w") as f:
        ds = f.create_dataset(
            "reflectance", data=cube,
            compression="gzip", compression_opts=4,
            chunks=(64, 64, bands)
        )
        ds.attrs["description"]         = "Synthetic AVIRIS-like hyperspectral cube"
        ds.attrs["sensor"]              = "Synthetic (AVIRIS-inspired)"
        ds.attrs["height_px"]           = height
        ds.attrs["width_px"]            = width
        ds.attrs["bands"]               = bands
        ds.attrs["wavelength_start_nm"] = 400
        ds.attrs["wavelength_end_nm"]   = 2500
        ds.attrs["crs"]                 = "EPSG:4326"

        f.create_dataset("wavelength", data=wavelengths)
        f.create_dataset(
            "blight_mask",
            data=(cube[:, :, 30] < 0.05).astype(np.uint8)
        )

    size_mb = os.path.getsize(output_path) / 1e6
    print(f"Saved → {output_path}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    generate_synthetic_hsi()
