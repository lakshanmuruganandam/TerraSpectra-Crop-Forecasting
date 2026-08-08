# Training Datasets — Complete Reference

All hyperspectral and geospatial datasets used for training the TerraSpectra crop disease forecasting model. Every dataset listed here has a corresponding entry in `scripts/download_all_training_datasets.py`.

Raw binary files are stored in `research_info/raw/` which is git-ignored (files can be 100MB–2GB+). Run the download script to acquire them locally.

---

## How to Download Everything

```bash
cd research_info/scripts
python3 download_all_training_datasets.py
```

Files are saved to `research_info/raw/` organized by subdirectory.

---

## Dataset 1 — Indian Pines (AVIRIS)

**Sensor:** NASA AVIRIS (Airborne Visible/Infrared Imaging Spectrometer)  
**Location:** Northwestern Indiana, USA (mixed agricultural and forested area)  
**Spatial size:** 145 × 145 pixels  
**Spectral bands:** 200 (corrected from 220; bands 104–108, 150–163, 220 removed for water absorption)  
**Wavelength range:** 400 – 2500 nm  
**Ground sampling distance:** 20 meters  
**Number of classes:** 16  
**Total labeled pixels:** 10,249

### Class Labels
| ID | Class | Pixels |
|----|-------|--------|
| 1 | Alfalfa | 54 |
| 2 | Corn-notill | 1434 |
| 3 | Corn-mintill | 834 |
| 4 | Corn | 234 |
| 5 | Grass-pasture | 497 |
| 6 | Grass-trees | 747 |
| 7 | Grass-pasture-mowed | 26 |
| 8 | Hay-windrowed | 489 |
| 9 | Oats | 20 |
| 10 | Soybean-notill | 968 |
| 11 | Soybean-mintill | 2468 |
| 12 | Soybean-clean | 614 |
| 13 | Wheat | 212 |
| 14 | Woods | 1294 |
| 15 | Buildings-Grass-Trees-Drives | 380 |
| 16 | Stone-Steel-Towers | 95 |

### Loading
```python
import scipy.io
import numpy as np

data = scipy.io.loadmat('raw/indian_pines/Indian_pines_corrected.mat')
gt   = scipy.io.loadmat('raw/indian_pines/Indian_pines_gt.mat')

cube   = data['indian_pines_corrected'].astype(np.float32)  # (145, 145, 200)
labels = gt['indian_pines_gt']                               # (145, 145)
```

### Why this dataset
Indian Pines is the single most-cited HSI benchmark in the literature. It is the "MNIST of hyperspectral remote sensing." Training on this establishes baseline OA/AA/κ numbers to compare against published results.

---

## Dataset 2 — Salinas Valley (AVIRIS, corrected)

**Sensor:** NASA AVIRIS  
**Location:** Salinas Valley, California, USA  
**Spatial size:** 512 × 217 pixels  
**Spectral bands:** 204 (corrected from 224; water absorption bands removed)  
**Wavelength range:** 400 – 2500 nm  
**Ground sampling distance:** 3.7 meters (highest spatial resolution airborne agricultural dataset)  
**Number of classes:** 16  
**Total labeled pixels:** 54,129

### Class Labels
| ID | Class | Pixels |
|----|-------|--------|
| 1 | Brocoli_green_weeds_1 | 2009 |
| 2 | Brocoli_green_weeds_2 | 3726 |
| 3 | Fallow | 1976 |
| 4 | Fallow_rough_plow | 1394 |
| 5 | Fallow_smooth | 2678 |
| 6 | Stubble | 3959 |
| 7 | Celery | 3579 |
| 8 | Grapes_untrained | 11271 |
| 9 | Soil_vinyard_develop | 6203 |
| 10 | Corn_senesced_green_weeds | 3278 |
| 11 | Lettuce_romaine_4wk | 1068 |
| 12 | Lettuce_romaine_5wk | 1927 |
| 13 | Lettuce_romaine_6wk | 916 |
| 14 | Lettuce_romaine_7wk | 1070 |
| 15 | Vinyard_untrained | 7268 |
| 16 | Vinyard_vertical_trellis | 1807 |

### Loading
```python
data = scipy.io.loadmat('raw/salinas/Salinas_corrected.mat')
gt   = scipy.io.loadmat('raw/salinas/Salinas_gt.mat')
cube   = data['salinas_corrected'].astype(np.float32)  # (512, 217, 204)
labels = gt['salinas_gt']                               # (512, 217)
```

### Why this dataset
Salinas is the primary agricultural crop benchmark with fine-grained lettuce growth stage classes. The lettuce 4wk → 5wk → 6wk → 7wk classes directly model what we want for disease progression detection — identifying subtle spectral shifts between temporally close crop states.

---

## Dataset 3 — Salinas-A (Subset)

**Spatial size:** 83 × 86 pixels  
**Bands:** 204  
**Classes:** 6 (a sub-region of the full Salinas scene)

Useful for rapid prototyping and debugging the data pipeline before scaling to the full scene.

---

## Dataset 4 — Pavia University (ROSIS)

**Sensor:** Reflective Optics System Imaging Spectrometer (ROSIS-03)  
**Location:** University of Pavia campus, Italy  
**Spatial size:** 610 × 340 pixels  
**Spectral bands:** 103 (corrected from 115)  
**Wavelength range:** 430 – 860 nm (VNIR only — no SWIR)  
**Ground sampling distance:** 1.3 meters (very high spatial resolution)  
**Number of classes:** 9

### Class Labels
| ID | Class |
|----|-------|
| 1 | Asphalt |
| 2 | Meadows |
| 3 | Gravel |
| 4 | Trees |
| 5 | Painted metal sheets |
| 6 | Bare soil |
| 7 | Bitumen |
| 8 | Self-blocking bricks |
| 9 | Shadows |

### Why this dataset
Although urban, Pavia University contains meadows, trees, and bare soil at 1.3m resolution. The fine spatial resolution helps validate that our CNN kernels are learning meaningful spatial-spectral features and not just coarse region boundaries.

---

## Dataset 5 — Pavia Centre (ROSIS)

**Spatial size:** 1096 × 715 pixels  
**Bands:** 102  
**Classes:** 9 (same taxonomy as Pavia University)

Larger scene. Used for testing sliding-window tiling and prediction reassembly.

---

## Dataset 6 — Botswana (EO-1 Hyperion)

**Sensor:** NASA Earth Observing-1 (EO-1) Hyperion spaceborne hyperspectral imager  
**Location:** Okavango Delta wetlands, Botswana  
**Acquisition date:** May 31, 2001  
**Spatial size:** 1476 × 256 pixels  
**Spectral bands:** 145 (from 242; noisy and water-absorption bands removed)  
**Wavelength range:** 400 – 2500 nm  
**Ground sampling distance:** 30 meters  
**Number of classes:** 14

### Class Labels
| ID | Class |
|----|-------|
| 1 | Water |
| 2 | Hippo grass |
| 3 | Floodplain grasses 1 |
| 4 | Floodplain grasses 2 |
| 5 | Reeds |
| 6 | Riparian |
| 7 | Firescar 2 |
| 8 | Island interior |
| 9 | Acacia woodlands |
| 10 | Acacia shrublands |
| 11 | Acacia grasslands |
| 12 | Short mopane |
| 13 | Mixed mopane |
| 14 | Exposed soils |

### Why this dataset
Botswana is the only benchmark from a spaceborne sensor (EO-1 Hyperion), which is the closest analog to real production data that will come from PRISMA / EnMAP satellites. Training on both airborne (3.7m) and spaceborne (30m) data improves robustness to sensor variation.

---

## Dataset 7 — Kennedy Space Center (AVIRIS)

**Sensor:** NASA AVIRIS  
**Location:** Kennedy Space Center, Florida  
**Spatial size:** 512 × 614 pixels  
**Spectral bands:** 176 (noisy bands removed)  
**Wavelength range:** 400 – 2500 nm  
**Ground sampling distance:** 18 meters  
**Number of classes:** 13

Classes cover coastal wetland ecosystems (salt marsh, mangrove) and upland vegetation (scrub oak, slash pine). Useful for testing model generalization to vegetation types not present in Midwest crop benchmarks.

---

## Dataset 8 — WHU-Hi-LongKou (UAV Nano-Hyperspec)

**Sensor:** Headwall Nano-Hyperspec mounted on DJI Matrice 600 Pro UAV  
**Location:** LongKou farm, Wuhan, Hubei, China  
**Spatial size:** 550 × 400 pixels  
**Spectral bands:** 270  
**Wavelength range:** 400 – 1000 nm (VNIR + partial NIR)  
**Ground sampling distance:** 0.463 meters (sub-meter UAV resolution)  
**Number of classes:** 9  
**Total labeled pixels:** 204,542

### Class Labels
| ID | Class | Pixels |
|----|-------|--------|
| 1 | Corn | 13,894 |
| 2 | Cotton | 8,717 |
| 3 | Sesame | 9,526 |
| 4 | Broad-leaf soybean | 13,612 |
| 5 | Narrow-leaf soybean | 14,815 |
| 6 | Rice | 5,765 |
| 7 | Water | 18,185 |
| 8 | Roads and houses | 12,654 |
| 9 | Mixed weed | 108,368 |

### Why this dataset
WHU-Hi is the most directly relevant dataset for TerraSpectra. It is UAV-collected at sub-meter resolution with the same crop types (corn, soybean, rice) that are the primary targets for disease forecasting. The 270-band coverage and the mixed weed class make it ideal for training the disease segmentation head.

---

## Dataset 9 — WHU-Hi-HanChuan

**Spatial size:** 1217 × 303 pixels  
**Bands:** 274  
**Classes:** 16 (includes strawberry, cowpea, soybean, sorghum, water spinach, watermelon, rapeseed, garlic, broad bean, tree, grass, red roof, gray roof, plastic, soil, water)

The largest and most diverse crop class set of the WHU-Hi collection.

---

## Dataset 10 — WHU-Hi-HongHu

**Spatial size:** 940 × 475 pixels  
**Bands:** 270  
**Classes:** 22 (most fine-grained crop dataset available)

Includes subspecies-level distinction between short/tall/recumbent rape, weed and sparse weed varieties.

---

## Dataset 11 — Full HSI Benchmark Collection (HuggingFace: Tanishq165/HSI_Datasets)

A pre-packaged mirror of:
- Houston 2013 (CASI-1500, 349×1905, 144 bands, 15 classes — GRSS Data Fusion Contest gold standard)
- Houston 2018 (AVIRIS-NG, 601×2384, 48 bands)
- Trento (AISA Eagle + LiDAR, 600×166, 63 bands, 6 rural orchard/vineyard classes)
- Chikusei (Headwall Photonics, 2517×2335 px, 128 bands, Japanese farmland)
- Muufl (CASI-1500, 325×220, 72 bands, Mississippi vegetation and man-made structures)
- Augsburg (DAS Specim IQ + DSM, 332×485, 180 bands, urban forestry)
- Mars CRISM (MRO, mineral and soil spectra for spectral library diversity)

---

## Dataset 12 — USGS Spectral Library v7 (Ground Truth)

The USGS Spectral Library contains measured reflectance spectra from 350–2500nm for ~1000 vegetation, soil, rock, and manmade material samples. Used as ground truth validation for the spectral signatures extracted from hyperspectral cubes.

CSV columns: `wavelength_nm`, `reflectance`, `sample_name`, `material_type`

---

## Dataset 13 — Natural Earth Country Boundaries (GeoJSON)

1:110m scale world country boundary polygons. Used as the base geographic layer in the Deck.gl GeoJsonLayer for the farm map visualization.

Source: `https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson`

---

## Directory Structure After Download

```
research_info/raw/
├── download_manifest.json          ← auto-generated list of what was downloaded
├── indian_pines/
│   ├── Indian_pines_corrected.mat
│   └── Indian_pines_gt.mat
├── salinas/
│   ├── Salinas_corrected.mat
│   ├── Salinas_gt.mat
│   ├── SalinasA_corrected.mat
│   └── SalinasA_gt.mat
├── pavia/
│   ├── PaviaU.mat
│   ├── PaviaU_gt.mat
│   ├── Pavia.mat
│   └── Pavia_gt.mat
├── botswana/
│   ├── Botswana.mat
│   └── Botswana_gt.mat
├── kennedy_space_center/
│   ├── KSC.mat
│   └── KSC_gt.mat
├── whu_hi/
│   ├── WHU_Hi_LongKou.mat
│   ├── WHU_Hi_LongKou_gt.mat
│   ├── WHU_Hi_HanChuan.mat
│   ├── WHU_Hi_HanChuan_gt.mat
│   ├── WHU_Hi_HongHu.mat
│   └── WHU_Hi_HongHu_gt.mat
├── hsi_collection/
│   ├── Houston2013/
│   ├── Trento/
│   ├── Chikusei/
│   ├── Muufl/
│   └── ...
├── spectral_library/
│   └── vegetation_spectra.csv
└── geospatial/
    ├── countries.geojson
    └── iowa_state_boundary.geojson
```

---

## Notes on File Sizes and GitHub Limits

GitHub enforces a 100MB per-file hard limit and recommends files under 50MB.

| Dataset | File | Size |
|---------|------|------|
| Indian Pines | Indian_pines_corrected.mat | ~13 MB |
| Salinas corrected | Salinas_corrected.mat | ~28 MB |
| Pavia University | PaviaU.mat | ~21 MB |
| Botswana | Botswana.mat | ~56 MB |
| KSC | KSC.mat | ~57 MB |
| WHU-Hi LongKou | WHU_Hi_LongKou.mat | ~150 MB |
| Chikusei | Chikusei.mat | ~2 GB |

Files under 100MB are pushed directly to GitHub.
Files 100MB–2GB require Git LFS (`git lfs track "*.mat"`).
Files above 2GB (Chikusei) must be stored externally (HuggingFace, Google Drive, S3).

All raw binary files are excluded from this repository via `.gitignore`.
Only the download script and this documentation are committed.
