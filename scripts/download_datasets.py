import os
import sys
import subprocess

def install_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Ensure huggingface_hub is installed
install_package("huggingface_hub")

from huggingface_hub import snapshot_download

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT_ROOT, "research_info", "raw")

def download_huggingface_datasets():
    print(f"Starting snapshot download of HSI Datasets from Hugging Face to {RAW_DIR}...")
    try:
        snapshot_download(
            repo_id="Tanishq165/HSI_Datasets",
            repo_type="dataset",
            local_dir=RAW_DIR,
            local_dir_use_symlinks=False,
            max_workers=4
        )
        print("Hugging Face dataset download completed successfully.")
    except Exception as e:
        print(f"Error downloading from Hugging Face: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_huggingface_datasets()
