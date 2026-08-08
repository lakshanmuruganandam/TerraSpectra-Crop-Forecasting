# Dataset Collection Status

Here is the list of hyperspectral and geographic datasets collected for the project. These files have been stored in the research_info folder to keep the main data folder clean until we finalize the pipeline structure.

## Datasets Overview

*   **Pavia University (PaviaU.mat / PaviaU_gt.mat)**
    *   Sensor: ROSIS
    *   Details: 610x340 pixels, 103 spectral bands. Covers urban land use and vegetation.
*   **Salinas Valley (Salinas_corrected.mat / Salinas_gt.mat)**
    *   Sensor: NASA AVIRIS
    *   Details: 512x217 pixels, 204 spectral bands. Focuses on agricultural field crops.
*   **Indian Pines (Indian_pines_corrected.mat / Indian_pines_gt.mat)**
    *   Sensor: NASA AVIRIS
    *   Details: 145x145 pixels, 220 spectral bands. Agricultural crop benchmark.
*   **Cuprite (Cuprite.mat)**
    *   Sensor: AVIRIS
    *   Details: Mining/geology scene, useful for testing high spectral depth.
*   **Botswana (Botswana_data.mat / Botswana_gt.mat)**
    *   Sensor: NASA EO-1 Hyperion
    *   Details: 1476x256 pixels, 145 spectral bands. Wetland and natural vegetation.
*   **Augsburg & Berlin**
    *   Sensors: DAS Specim / HyMap
    *   Details: Detailed urban and forestry scenes with associated train/test splits.
*   **Dioni & Loukia**
    *   Sensor: AVIRIS-NG
    *   Details: 176 bands, mixed forestry and coastal vegetation.
*   **Houston 2013 & 2018**
    *   Sensors: CASI-1500 / AVIRIS-NG
    *   Details: Dense urban and vegetation profiles.
*   **Chikusei**
    *   Sensor: Headwall Photonics
    *   Details: Large agricultural scene in Japan.
*   **Muufl**
    *   Sensor: CASI-1500
    *   Details: Mississippi vegetation and canopy cover.
*   **Trento**
    *   Sensor: AISA Eagle
    *   Details: 63 bands, rural scene (primarily orchards/vineyards).
*   **Mars CRISM (NiliFossae / Utopia / Holden)**
    *   Sensor: MRO CRISM
    *   Details: Mineral and soil spectra.
*   **WHU-Hi (LongKou / HongHu / HanChuan)**
    *   Sensor: Headwall Nano-Hyperspec (UAV)
    *   Details: Fine-grained crop field datasets (cabbage, strawberry, wheat, corn, rice, etc.).

## Geographic & Mock Files
*   **countries_boundary.geojson:** Global administrative boundary vector file.
*   **farm_boundaries.geojson:** Custom farm boundaries polygon coordinates.
*   **mock_farm_datacube.h5:** 224-band simulated agricultural field datacube with a blight outbreak simulation zone.
*   **mock_farm_preview.tif:** GeoTIFF RGB proxy preview of the mock datacube.
