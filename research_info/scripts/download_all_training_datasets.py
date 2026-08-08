"""
download_all_training_datasets.py
===================================
TerraSpectra — Master Training Dataset Download Script

PURPOSE
-------
This script downloads all hyperspectral benchmark datasets needed to train
the TerraSpectra crop disease forecasting model. It does NOT run automatically.
Run it manually when you are ready to set up your local training environment.

All files go to research_info/raw/ which is git-ignored.
Nothing here is downloaded unless you explicitly run this script.

USAGE
-----
    cd research_info/scripts
    python3 download_all_training_datasets.py

DATASETS COVERED
----------------
    1.  Indian Pines          — AVIRIS, 145×145,   200 bands, 16 crop classes
    2.  Salinas Valley        — AVIRIS, 512×217,   204 bands, 16 veg classes
    3.  Pavia University      — ROSIS,  610×340,   103 bands, 9 classes
    4.  Botswana              — Hyperion, 1476×256, 145 bands, 14 wetland classes
    5.  Kennedy Space Center  — AVIRIS, 512×614,   176 bands, 13 classes
    6.  WHU-Hi (LongKou / HanChuan / HongHu) — UAV, 270 bands, 9-22 crop classes
    7.  Full HSI Collection   — Houston, Trento, Chikusei, Muufl, Augsburg, CRISM
    8.  USGS Spectral Library — CSV leaf/vegetation spectra (350–2500nm)
    9.  Natural Earth GeoJSON — World country boundaries
    10. Iowa State Boundary   — GeoJSON for spatial clipping

REQUIREMENTS
------------
    pip install huggingface_hub requests

NOTES
-----
    - WHU-Hi and HSI Collection are large (multi-GB). Budget time accordingly.
    - Files >100MB cannot be pushed to GitHub; raw/ is git-ignored by design.
    - If a file already exists it is skipped (safe to re-run after interruptions).
    - Set HF_TOKEN env var for higher HuggingFace rate limits:
        export HF_TOKEN=your_token_here
"""

import os
import sys
import ssl
import time
import json
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


def download_file(url: str, dest_dir: str, filename: str = None) -> str:
    """Download a single file. Skips if already exists."""
    os.makedirs(dest_dir, exist_ok=True)
    filename = filename or os.path.basename(url.split("?")[0])
    filepath = os.path.join(dest_dir, filename)

    if os.path.exists(filepath):
        size_mb = os.path.getsize(filepath) / 1e6
        print(f"  [SKIP] {filename}  ({size_mb:.1f} MB already on disk)")
        return filepath

    print(f"  [DL]   {filename}")
    print(f"         {url}")

    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "TerraSpectra/1.0"})

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=120) as resp, \
             open(filepath, "wb") as f:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded / total * 100
                    print(f"\r         {pct:5.1f}%  {downloaded/1e6:.1f}/{total/1e6:.1f} MB",
                          end="", flush=True)
            print()
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        print(f"  [ERR]  {filename}: {e}")
        return None

    size_mb = os.path.getsize(filepath) / 1e6
    print(f"         Saved {size_mb:.1f} MB → {filepath}")
    return filepath


def download_hf_repo(repo_id: str, dest_dir: str, repo_type: str = "dataset"):
    """Download an entire Hugging Face repo snapshot."""
    install("huggingface_hub")
    from huggingface_hub import snapshot_download
    os.makedirs(dest_dir, exist_ok=True)
    print(f"  [HF]   Downloading {repo_id}")
    print(f"         Destination: {dest_dir}")
    token = os.environ.get("HF_TOKEN", None)
    if not token:
        print("         Tip: set HF_TOKEN env var for faster downloads")
    try:
        snapshot_download(
            repo_id=repo_id,
            repo_type=repo_type,
            local_dir=dest_dir,
            token=token,
            max_workers=4,
        )
        print(f"         Done.")
    except Exception as e:
        print(f"  [ERR]  {repo_id}: {e}")


def section(title: str, notes: str = ""):
    print(f"\n{'─'*60}")
    print(f"  {title}")
    if notes:
        print(f"  {notes}")
    print(f"{'─'*60}")


# ══════════════════════════════════════════════════════════════════════════════
#  DATASET DEFINITIONS
#  Each entry defines WHERE to get the data and WHERE to save it locally.
#  Nothing is downloaded until main() is called.
# ══════════════════════════════════════════════════════════════════════════════

DATASETS = [

    # ── 1. Indian Pines ───────────────────────────────────────────────────────
    {
        "name": "Indian Pines (AVIRIS)",
        "notes": "145×145 px · 200 bands · 16 crop classes (corn, soy, wheat, hay…)",
        "subdir": "indian_pines",
        "hf": "danaroth/indian_pines",
        "files": [],
    },

    # ── 2. Salinas Valley ─────────────────────────────────────────────────────
    {
        "name": "Salinas Valley (AVIRIS)",
        "notes": "512×217 px · 204 bands · 16 classes (lettuce growth stages, grapes)",
        "subdir": "salinas",
        "hf": "danaroth/salinas",
        "files": [],
    },

    # ── 3. Pavia University ───────────────────────────────────────────────────
    {
        "name": "Pavia University (ROSIS)",
        "notes": "610×340 px · 103 bands · 9 classes (meadows, trees, bare soil…)",
        "subdir": "pavia",
        "hf": "danaroth/pavia_university",
        "files": [],
    },

    # ── 4. Botswana ───────────────────────────────────────────────────────────
    {
        "name": "Botswana (EO-1 Hyperion)",
        "notes": "1476×256 px · 145 bands · 14 wetland/vegetation classes",
        "subdir": "botswana",
        "hf": "danaroth/botswana",
        "files": [],
    },

    # ── 5. Kennedy Space Center ───────────────────────────────────────────────
    {
        "name": "Kennedy Space Center (AVIRIS)",
        "notes": "512×614 px · 176 bands · 13 coastal vegetation classes",
        "subdir": "kennedy_space_center",
        "hf": "danaroth/kennedy_space_center",
        "files": [],
    },

    # ── 6. WHU-Hi (UAV Crop Dataset) ─────────────────────────────────────────
    # LongKou 550×400×270, HanChuan 1217×303×274, HongHu 940×475×270
    # Most directly relevant — sub-metre UAV data with fine-grained crop classes
    {
        "name": "WHU-Hi (LongKou + HanChuan + HongHu)",
        "notes": "UAV · 270 bands · 9–22 crop classes · LARGE (several GB)",
        "subdir": "whu_hi",
        "hf": "danaroth/whu_hi",
        "files": [],
    },

    # ── 7. Full HSI Benchmark Collection ─────────────────────────────────────
    # Houston 2013, Trento, Chikusei, Muufl, Augsburg, Mars CRISM
    {
        "name": "Full HSI Benchmark Collection",
        "notes": "Houston / Trento / Chikusei / Muufl / Augsburg / Mars CRISM · LARGE",
        "subdir": "hsi_collection",
        "hf": "Tanishq165/HSI_Datasets",
        "files": [],
    },

    # ── 8. USGS Spectral Library (CSV) ────────────────────────────────────────
    {
        "name": "USGS Spectral Library — Vegetation",
        "notes": "Leaf/canopy reflectance spectra 350–2500nm · ground truth validation",
        "subdir": "spectral_library",
        "hf": None,
        "files": [
            (
                "https://raw.githubusercontent.com/enricoros/spectral-library-samples/master/data/vegetation_spectra.csv",
                "vegetation_spectra.csv",
            ),
        ],
    },

    # ── 9. Natural Earth Country Boundaries (GeoJSON) ─────────────────────────
    {
        "name": "Natural Earth Country Boundaries",
        "notes": "1:110m GeoJSON · base layer for Deck.gl GeoJsonLayer",
        "subdir": "geospatial",
        "hf": None,
        "files": [
            (
                "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson",
                "countries.geojson",
            ),
        ],
    },

    # ── 10. Iowa State Boundary (GeoJSON) ─────────────────────────────────────
    {
        "name": "Iowa State Boundary",
        "notes": "GeoJSON polygon · spatial clipping for Midwest farm datasets",
        "subdir": "geospatial",
        "hf": None,
        "files": [
            (
                "https://raw.githubusercontent.com/unitedstates/districts/gh-pages/states/IA/shape.geojson",
                "iowa_state_boundary.geojson",
            ),
        ],
    },

]


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "═" * 60)
    print("  TerraSpectra — Training Dataset Downloader")
    print("  Run this script to fetch all datasets locally.")
    print(f"  Output: {RAW_DIR}")
    print("═" * 60)

    success = []
    failed  = []

    for ds in DATASETS:
        section(ds["name"], ds["notes"])
        dest = os.path.join(RAW_DIR, ds["subdir"])

        # Direct HTTP file downloads
        for entry in ds.get("files", []):
            url, fname = entry[0], entry[1]
            result = download_file(url, dest, fname)
            (success if result else failed).append(fname)

        # HuggingFace snapshot download
        if ds.get("hf"):
            download_hf_repo(ds["hf"], dest)

    # ── Summary ───────────────────────────────────────────────────────────────
    section("DOWNLOAD COMPLETE")
    print(f"  Direct files OK : {len(success)}")
    if failed:
        print(f"  Failed          : {len(failed)}")
        for f in failed:
            print(f"    ✗  {f}")

    # Write manifest
    manifest = {
        "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "raw_dir": RAW_DIR,
        "datasets": [{"name": d["name"], "notes": d["notes"]} for d in DATASETS],
        "failed": failed,
    }
    manifest_path = os.path.join(RAW_DIR, "download_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\n  Manifest saved → {manifest_path}")
    print("  Note: raw/ is git-ignored. These files stay local only.")


if __name__ == "__main__":
    main()
