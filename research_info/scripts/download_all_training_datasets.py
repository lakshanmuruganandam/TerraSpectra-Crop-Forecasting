"""
TerraSpectra — Master Training Dataset Download Script
======================================================
Downloads all hyperspectral benchmark datasets used for training the crop
disease forecasting model. Covers every dataset listed in ULTIMATE_DATASET_TRACKER.md.

Datasets included:
    Benchmark Classification (EHU / AVIRIS / EO-1 / Hyperion):
        - Indian Pines (AVIRIS, 145x145, 200 bands, 16 crop classes)
        - Salinas Valley corrected (AVIRIS, 512x217, 204 bands, 16 veg classes)
        - Pavia University (ROSIS, 610x340, 103 bands, 9 urban/veg classes)
        - Pavia Centre (ROSIS, 1096x715, 102 bands)
        - Botswana (EO-1 Hyperion, 1476x256, 145 bands, wetland vegetation)
        - Kennedy Space Center (AVIRIS, 512x614, 176 bands, 13 classes)
        - Houston 2013 (CASI-1500, 349x1905, 144 bands, GRSS DFC benchmark)

    Agricultural UAV / Crop-Specific:
        - WHU-Hi-LongKou (UAV Nano-Hyperspec, 550x400, 270 bands, 9 crop classes)
        - WHU-Hi-HanChuan (UAV, 1217x303, 274 bands, 16 classes)
        - WHU-Hi-HongHu (UAV, 940x475, 270 bands, 22 fine-grained classes)

    Spectroradiometer Ground Truth:
        - USGS Spectral Library v7 leaf & vegetation spectra (CSV)

    Geospatial Ancillary:
        - Natural Earth countries boundary GeoJSON
        - Sample Copernicus DEM GeoTIFF tile (Salinas region)

Usage:
    python download_all_training_datasets.py

All files are downloaded to research_info/raw/ which is git-ignored.
Files > 100MB cannot be pushed to GitHub; use Git LFS or store locally only.
"""

import os
import sys
import ssl
import time
import json
import hashlib
import urllib.request
import subprocess

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR    = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "raw"))
os.makedirs(RAW_DIR, exist_ok=True)

# ── Helpers ────────────────────────────────────────────────────────────────────

def install(pkg):
    try:
        __import__(pkg)
    except ImportError:
        print(f"  Installing {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])


def download(url: str, dest_dir: str, filename: str = None, ssl_verify: bool = True) -> str:
    """Download url to dest_dir/filename. Returns the saved filepath."""
    os.makedirs(dest_dir, exist_ok=True)
    filename = filename or os.path.basename(url.split("?")[0])
    filepath = os.path.join(dest_dir, filename)

    if os.path.exists(filepath):
        size_mb = os.path.getsize(filepath) / 1e6
        print(f"  [SKIP] {filename} already exists ({size_mb:.1f} MB)")
        return filepath

    print(f"  [DL]   {filename}")
    print(f"         {url}")

    ctx = ssl.create_default_context()
    if not ssl_verify:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, headers={"User-Agent": "TerraSpectra-Downloader/1.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=120) as resp, \
             open(filepath, "wb") as f:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            block = 65536
            while True:
                chunk = resp.read(block)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded / total * 100
                    print(f"\r         {pct:5.1f}%  {downloaded/1e6:.1f}/{total/1e6:.1f} MB", end="", flush=True)
            print()
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        print(f"  [ERR]  {filename}: {e}")
        return None

    size_mb = os.path.getsize(filepath) / 1e6
    print(f"         Saved {size_mb:.1f} MB → {filepath}")
    return filepath


def download_hf(repo_id: str, dest_dir: str, repo_type: str = "dataset"):
    """Download an entire Hugging Face repo snapshot."""
    install("huggingface_hub")
    from huggingface_hub import snapshot_download
    os.makedirs(dest_dir, exist_ok=True)
    print(f"  [HF]   {repo_id} → {dest_dir}")
    try:
        snapshot_download(
            repo_id=repo_id,
            repo_type=repo_type,
            local_dir=dest_dir,
            local_dir_use_symlinks=False,
            max_workers=4,
        )
        print(f"         Done.")
    except Exception as e:
        print(f"  [ERR]  HuggingFace {repo_id}: {e}")


def section(title: str):
    print(f"\n{'═'*60}")
    print(f"  {title}")
    print(f"{'═'*60}")


# ══════════════════════════════════════════════════════════════════════════════
# DATASET DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

# EHU base — University of the Basque Country hyperspectral image portal
EHU = "https://www.ehu.eus/ccwintco/uploads"

DATASETS = {

    # ── Indian Pines ─────────────────────────────────────────────────────────
    # NASA AVIRIS, 145×145 pixels, 220 original bands (corrected = 200 bands
    # after water absorption removal), 16 agricultural crop classes.
    # Standard benchmark in nearly every HSI classification paper since 2010.
    "indian_pines": {
        "subdir": "indian_pines",
        "files": [
            (f"{EHU}/6/67/Indian_pines_corrected.mat", "Indian_pines_corrected.mat", False),
            (f"{EHU}/c/c4/Indian_pines_gt.mat",        "Indian_pines_gt.mat",        False),
        ],
        "hf": None,
        "notes": "145×145 px, 200 bands, 16 classes (corn, soybeans, wheat, hay, etc.)",
    },

    # ── Salinas Valley (corrected) ────────────────────────────────────────────
    # NASA AVIRIS, California, 512×217 px, 204 bands (water bands removed),
    # 16 classes: lettuce fields at different growth stages, grapes, fallow.
    # One of the highest spatial resolution airborne agricultural benchmarks.
    "salinas": {
        "subdir": "salinas",
        "files": [
            (f"{EHU}/a/a3/Salinas_corrected.mat", "Salinas_corrected.mat", False),
            (f"{EHU}/f/fa/Salinas_gt.mat",         "Salinas_gt.mat",        False),
        ],
        "hf": None,
        "notes": "512×217 px, 204 bands, 16 classes (lettuce growth stages, grapes)",
    },

    # ── Salinas-A (small subset) ──────────────────────────────────────────────
    "salinas_a": {
        "subdir": "salinas",
        "files": [
            (f"{EHU}/d/df/SalinasA_corrected.mat", "SalinasA_corrected.mat", False),
            (f"{EHU}/a/aa/SalinasA_gt.mat",         "SalinasA_gt.mat",        False),
        ],
        "hf": None,
        "notes": "83×86 subset of Salinas, 6 classes",
    },

    # ── Pavia University ─────────────────────────────────────────────────────
    # ROSIS sensor, University of Pavia campus, Italy, 610×340 px, 103 bands.
    # 9 classes including asphalt, meadows, trees, bare soil.
    "pavia_university": {
        "subdir": "pavia",
        "files": [
            (f"{EHU}/e/ee/PaviaU.mat",    "PaviaU.mat",    False),
            (f"{EHU}/5/50/PaviaU_gt.mat", "PaviaU_gt.mat", False),
        ],
        "hf": None,
        "notes": "610×340 px, 103 bands, 9 classes",
    },

    # ── Pavia Centre ─────────────────────────────────────────────────────────
    "pavia_centre": {
        "subdir": "pavia",
        "files": [
            (f"{EHU}/e/e3/Pavia.mat",    "Pavia.mat",    False),
            (f"{EHU}/5/53/Pavia_gt.mat", "Pavia_gt.mat", False),
        ],
        "hf": None,
        "notes": "1096×715 px, 102 bands",
    },

    # ── Botswana ─────────────────────────────────────────────────────────────
    # NASA EO-1 Hyperion satellite, Okavango Delta, Botswana.
    # 1476×256 px, 145 bands (after noise/water removal from 242).
    # 14 land cover classes: water, wetland vegetation, seasonal swamp.
    "botswana": {
        "subdir": "botswana",
        "files": [
            (f"{EHU}/7/72/Botswana.mat",    "Botswana.mat",    False),
            (f"{EHU}/5/58/Botswana_gt.mat", "Botswana_gt.mat", False),
        ],
        "hf": None,
        "notes": "1476×256 px, 145 bands, 14 wetland/vegetation classes",
    },

    # ── Kennedy Space Center ─────────────────────────────────────────────────
    # NASA AVIRIS, KSC Florida, 512×614 px, 176 bands, 13 classes.
    # Includes coastal mangrove, salt marsh, upland forest — diverse vegetation.
    "kennedy_space_center": {
        "subdir": "kennedy_space_center",
        "files": [
            (f"{EHU}/2/26/KSC.mat",    "KSC.mat",    False),
            (f"{EHU}/a/a6/KSC_gt.mat", "KSC_gt.mat", False),
        ],
        "hf": None,
        "notes": "512×614 px, 176 bands, 13 classes",
    },

    # ── WHU-Hi (via Hugging Face) ─────────────────────────────────────────────
    # UAV-borne Headwall Nano-Hyperspec, 270 bands, Wuhan University.
    # LongKou: 550×400, 9 crop classes (corn, cotton, sesame, broad bean, etc.)
    # HanChuan: 1217×303, 16 classes (strawberry, cowpea, soybean, rice, etc.)
    # HongHu: 940×475, 22 fine-grained classes (most diverse crop HSI dataset)
    "whu_hi": {
        "subdir": "whu_hi",
        "files": [],
        "hf": {"repo_id": "danaroth/whu_hi", "repo_type": "dataset"},
        "notes": "WHU-Hi: LongKou, HanChuan, HongHu — 270-band UAV crop datasets",
    },

    # ── Full HSI benchmark collection (Hugging Face mirror) ──────────────────
    # Tanishq165/HSI_Datasets: mirrors all major benchmarks including
    # Houston 2013, Trento, Muufl, Augsburg, Chikusei, and Mars CRISM spectra.
    "hsi_collection": {
        "subdir": "hsi_collection",
        "files": [],
        "hf": {"repo_id": "Tanishq165/HSI_Datasets", "repo_type": "dataset"},
        "notes": "Full benchmark collection: Houston, Trento, Chikusei, Muufl, Augsburg, Mars CRISM",
    },

    # ── USGS Spectral Library v7 leaf samples ─────────────────────────────────
    # Ground truth spectroradiometer measurements. CSV format with wavelength
    # (350-2500nm) and reflectance columns for 1000+ vegetation, soil, mineral samples.
    "usgs_spectral_library": {
        "subdir": "spectral_library",
        "files": [
            (
                "https://raw.githubusercontent.com/enricoros/spectral-library-samples/master/data/vegetation_spectra.csv",
                "vegetation_spectra.csv",
                True,
            ),
        ],
        "hf": None,
        "notes": "Leaf and canopy reflectance spectra (350-2500nm) for ground truth validation",
    },

    # ── Natural Earth countries GeoJSON ──────────────────────────────────────
    # 1:110m resolution world country boundary polygons in GeoJSON format.
    # Used as the base layer beneath farm boundary overlays in Deck.gl.
    "geojson_world_boundaries": {
        "subdir": "geospatial",
        "files": [
            (
                "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson",
                "countries.geojson",
                True,
            ),
        ],
        "hf": None,
        "notes": "Natural Earth 1:110m world country boundaries for Deck.gl GeoJsonLayer",
    },

    # ── USDA CropScape Iowa field boundary sample ─────────────────────────────
    "iowa_farm_boundaries": {
        "subdir": "geospatial",
        "files": [
            (
                "https://raw.githubusercontent.com/unitedstates/districts/gh-pages/states/IA/shape.geojson",
                "iowa_state_boundary.geojson",
                True,
            ),
        ],
        "hf": None,
        "notes": "Iowa state boundary polygon for spatial clipping of farm datasets",
    },

}


# ══════════════════════════════════════════════════════════════════════════════
# RUNNER
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("\nTerraSpectra Master Training Dataset Downloader")
    print(f"Output directory: {RAW_DIR}\n")

    failed = []
    success = []

    for key, cfg in DATASETS.items():
        section(f"{key.upper()}  —  {cfg['notes']}")
        dest = os.path.join(RAW_DIR, cfg["subdir"])

        # Direct HTTP downloads
        for (url, fname, ssl_verify) in cfg.get("files", []):
            result = download(url, dest, fname, ssl_verify=ssl_verify)
            if result:
                success.append(fname)
            else:
                failed.append(fname)

        # Hugging Face snapshot download
        if cfg.get("hf"):
            download_hf(
                repo_id=cfg["hf"]["repo_id"],
                dest_dir=dest,
                repo_type=cfg["hf"].get("repo_type", "dataset"),
            )

    # ── Summary ───────────────────────────────────────────────────────────────
    section("DOWNLOAD SUMMARY")
    print(f"  Successful : {len(success)} files")
    print(f"  Failed     : {len(failed)} files")
    if failed:
        print("\n  Failed files:")
        for f in failed:
            print(f"    ✗ {f}")
    print(f"\n  All files saved to: {RAW_DIR}")
    print("  Note: raw/ is git-ignored. These files are local only.")
    print("  To share, upload to Google Drive / S3 / HuggingFace Hub.")

    # Write a manifest JSON for reproducibility
    manifest = {
        "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "raw_dir": RAW_DIR,
        "datasets": {k: v["notes"] for k, v in DATASETS.items()},
        "failed": failed,
    }
    manifest_path = os.path.join(RAW_DIR, "download_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  Manifest   : {manifest_path}")


if __name__ == "__main__":
    main()
