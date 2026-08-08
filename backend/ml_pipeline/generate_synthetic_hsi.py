import numpy as np
import h5py
import os

def generate_synthetic_hsi(filename, width=100, height=100, bands=224):
    """
    Generates a synthetic Hyperspectral Data Cube (HDF5 format).
    Mimics AVIRIS structure with 224 spectral bands.
    """
    print(f"Generating Synthetic Hyperspectral Cube: {width}x{height}x{bands}...")
    
    # Create base cube with random noise (reflectance 0.0 to 1.0)
    # Using float32 to represent reflectance values
    cube = np.random.rand(height, width, bands).astype(np.float32)
    
    # Simulate a "Vegetation" spectral signature pattern
    # Chlorophyll absorption around band 30 (~670nm) -> lower reflectance
    cube[:, :, 25:35] *= 0.3 
    # Red edge and high NIR scattering around bands 40-100 (750nm-1300nm) -> high reflectance
    cube[:, :, 40:100] += 0.5 
    # Clip to keep it between 0 and 1
    cube = np.clip(cube, 0.0, 1.0)
    
    # Create the data/raw directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save as HDF5
    with h5py.File(filename, 'w') as f:
        # Create dataset
        dataset = f.create_dataset('HSI_Data', data=cube, compression="gzip", compression_opts=4)
        # Add spatial/spectral metadata
        dataset.attrs['description'] = 'Synthetic Hyperspectral Data (AVIRIS-like)'
        dataset.attrs['bands'] = bands
        dataset.attrs['wavelength_start_nm'] = 400
        dataset.attrs['wavelength_end_nm'] = 2500
        
    print(f"Successfully saved synthetic HSI cube to {filename} (Size: {cube.nbytes / 1024 / 1024:.2f} MB)")

if __name__ == "__main__":
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/raw/synthetic_aviris_cube.h5'))
    generate_synthetic_hsi(output_path)
