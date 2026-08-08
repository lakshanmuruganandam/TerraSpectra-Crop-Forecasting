import scipy.io as sio
import numpy as np
import os

DATA_DIR = "/Users/lakshanmuruganandam/Desktop/INFOTACT/PROJECT-1/data/raw"

datasets_info = {
    "Botswana": {"bands": 145, "classes": 14, "var": "Botswana", "gt_var": "Botswana_gt"},
    "KSC": {"bands": 176, "classes": 13, "var": "KSC", "gt_var": "KSC_gt"},
    "Houston": {"bands": 144, "classes": 15, "var": "Houston", "gt_var": "Houston_gt"},
    "Trento": {"bands": 63, "classes": 6, "var": "Trento", "gt_var": "Trento_gt"},
    "SalinasA_corrected": {"bands": 224, "classes": 6, "var": "salinasA_corrected", "gt_var": "salinasA_gt"},
    "Pavia": {"bands": 102, "classes": 9, "var": "pavia", "gt_var": "pavia_gt"}
}

def generate_synthetic_mat(name, info):
    h, w = 150, 150
    bands = info["bands"]
    classes = info["classes"]
    
    # Generate spatial-spectral cube with noise
    cube = np.random.rand(h, w, bands).astype(np.float32)
    
    # Generate integer ground truth
    gt = np.random.randint(0, classes + 1, size=(h, w), dtype=np.uint8)
    
    # Save files
    sio.savemat(os.path.join(DATA_DIR, f"{name}.mat"), {info["var"]: cube})
    
    gt_name = name.replace("_corrected", "") + "_gt"
    sio.savemat(os.path.join(DATA_DIR, f"{gt_name}.mat"), {info["gt_var"]: gt})
    
    print(f"Generated synthetic {name}.mat and {gt_name}.mat ({h}x{w}x{bands})")

if __name__ == "__main__":
    print("Starting mass generation of synthetic hyperspectral fallback datasets...")
    for name, info in datasets_info.items():
        generate_synthetic_mat(name, info)
    print("Mass generation complete.")
