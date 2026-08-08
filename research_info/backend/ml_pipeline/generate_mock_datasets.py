"""
generate_mock_datasets.py
--------------------------
Mass-generates synthetic .mat-format fallback datasets that exactly match
the shape and variable naming conventions of the real HSI benchmark datasets.

This is used when the real datasets cannot be downloaded (e.g., EHU server
403 blocks, gated portals). The synthetic .mat files have the correct
variable names so all training code loads them without modification.

Datasets generated:
    - Indian Pines (145x145x200, 16 classes)
    - Salinas corrected (512x217x204, 16 classes)
    - Salinas A (83x86x204, 6 classes)
    - Pavia University (610x340x103, 9 classes)
    - Pavia Centre (1096x715x102, 9 classes)
    - Botswana (1476x256x145, 14 classes)
    - Kennedy Space Center (512x614x176, 13 classes)
    - Houston 2013 (349x1905x144, 15 classes)
    - Trento (600x166x63, 6 classes)
    - WHU-Hi LongKou (550x400x270, 9 classes)

Output saved to research_info/mock/ (git-ignored).
Run from any directory — paths resolve relative to this script.
"""

import os
import numpy as np
import scipy.io as sio

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_DIR   = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "mock", "mat_datasets"))

# ── Dataset specifications ─────────────────────────────────────────────────────
# (height, width, bands, n_classes, data_var_name, gt_var_name)
DATASETS = {
    "Indian_pines_corrected": {
        "shape": (145, 145, 200), "classes": 16,
        "data_var": "indian_pines_corrected", "gt_var": "indian_pines_gt",
        "gt_file": "Indian_pines_gt"
    },
    "Salinas_corrected": {
        "shape": (512, 217, 204), "classes": 16,
        "data_var": "salinas_corrected", "gt_var": "salinas_gt",
        "gt_file": "Salinas_gt"
    },
    "SalinasA_corrected": {
        "shape": (83, 86, 204), "classes": 6,
        "data_var": "salinasA_corrected", "gt_var": "salinasA_gt",
        "gt_file": "SalinasA_gt"
    },
    "PaviaU": {
        "shape": (610, 340, 103), "classes": 9,
        "data_var": "paviaU", "gt_var": "paviaU_gt",
        "gt_file": "PaviaU_gt"
    },
    "Pavia": {
        "shape": (1096, 715, 102), "classes": 9,
        "data_var": "pavia", "gt_var": "pavia_gt",
        "gt_file": "Pavia_gt"
    },
    "Botswana": {
        "shape": (1476, 256, 145), "classes": 14,
        "data_var": "Botswana", "gt_var": "Botswana_gt",
        "gt_file": "Botswana_gt"
    },
    "KSC": {
        "shape": (512, 614, 176), "classes": 13,
        "data_var": "KSC", "gt_var": "KSC_gt",
        "gt_file": "KSC_gt"
    },
    "Houston": {
        "shape": (349, 1905, 144), "classes": 15,
        "data_var": "Houston", "gt_var": "Houston_gt",
        "gt_file": "Houston_gt"
    },
    "Trento": {
        "shape": (600, 166, 63), "classes": 6,
        "data_var": "Trento", "gt_var": "Trento_gt",
        "gt_file": "Trento_gt"
    },
    "WHU_Hi_LongKou": {
        "shape": (550, 400, 270), "classes": 9,
        "data_var": "WHU_Hi_LongKou", "gt_var": "WHU_Hi_LongKou_gt",
        "gt_file": "WHU_Hi_LongKou_gt"
    },
}


def generate_mock_dataset(name: str, spec: dict, rng: np.random.Generator):
    h, w, b = spec["shape"]
    n_cls   = spec["classes"]

    # Synthetic spectral cube: realistic vegetation-like pattern
    cube = rng.random((h, w, b)).astype(np.float32)
    # Chlorophyll absorption dip
    band_red  = min(27, b - 1)
    band_nir  = min(45, b - 1)
    cube[:, :, max(0, band_red-5):band_red+5] *= 0.25
    cube[:, :, band_nir:min(band_nir+40, b)]  = np.clip(
        cube[:, :, band_nir:min(band_nir+40, b)] + 0.4, 0, 1
    )

    # Ground truth: integer labels 0 (background) to n_cls
    gt = rng.integers(0, n_cls + 1, size=(h, w), dtype=np.uint8)

    # Save data .mat
    data_path = os.path.join(MOCK_DIR, f"{name}.mat")
    sio.savemat(data_path, {spec["data_var"]: cube})

    # Save ground truth .mat
    gt_path = os.path.join(MOCK_DIR, f"{spec['gt_file']}.mat")
    sio.savemat(gt_path, {spec["gt_var"]: gt})

    size_mb = os.path.getsize(data_path) / 1e6
    print(f"  {name:40s} {h}x{w}x{b}  →  {size_mb:.1f} MB")


def main():
    os.makedirs(MOCK_DIR, exist_ok=True)
    rng = np.random.default_rng(seed=42)

    print(f"\nGenerating {len(DATASETS)} synthetic .mat datasets → {MOCK_DIR}\n")
    print(f"  {'Dataset':<40} {'Shape':<18} Size")
    print(f"  {'-'*65}")

    for name, spec in DATASETS.items():
        generate_mock_dataset(name, spec, rng)

    print(f"\nAll {len(DATASETS)} datasets generated successfully.")
    print("These are SYNTHETIC fallbacks — replace with real data for production training.")


if __name__ == "__main__":
    main()
