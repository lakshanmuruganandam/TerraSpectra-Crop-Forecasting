# Frontend GIS & WebGL Research Report: Hyperspectral Crop Disease Forecasting

## 1. WebGL GIS Map Rendering Engines and Deck.gl Layer Architecture & Compositing

Deck.gl is a highly scalable WebGL2-powered framework designed specifically for visualizing large datasets. It operates on a **reactive programming model** similar to React, where layers are instantiated every render cycle with new props, and the core engine diffs these props to update the underlying WebGL state minimally.

### Architecture & Compositing:
- **luma.gl Backbone**: Deck.gl is built on luma.gl, exposing WebGL2 capabilities through a clean API.
- **Layer Compositing**: Deck.gl composites multiple layers off-screen before rendering to the canvas. It handles depth testing automatically, allowing 3D geometries and 2D overlays to seamlessly integrate.
- **Data Updates**: Instead of mutating layers, you pass new layer instances. Performance is preserved using `updateTriggers` which tell the engine exactly when to re-calculate WebGL buffers.

## 2. Integrating Deck.gl with Mapbox GL JS (React 18 + Vite)

In a React 18 + Vite environment, integrating Deck.gl with Mapbox is best achieved using `react-map-gl`. Mapbox acts as the basemap engine, while Deck.gl acts as a transparent WebGL canvas overlaid exactly on top, synchronizing camera states.

**Vite Specifics**: Vite uses ES modules. Mapbox GL JS v2/v3 might require specific worker transpilation configurations, but `react-map-gl` abstracts most of this away. 

### Architectural Pattern (Overlaid vs. Interleaved):
- **Overlaid**: Deck.gl renders on a separate `<canvas>` positioned over Mapbox. Easiest to implement, perfect for most 2D overlays.
- **Interleaved**: Deck.gl renders *inside* Mapbox's WebGL context via `MapboxLayer`. Necessary if hyperspectral data needs to be occluded by Mapbox 3D buildings or terrain.

## 3. Specific Layer Configurations

### A. GeoJsonLayer (Polygons)
Used to render farm boundaries, crop zones, or disease clusters.
- **Configuration**: Use binary data attributes if the GeoJSON is massive to prevent main-thread serialization bottlenecks. Use `filled: true`, `stroked: true`, and data-driven styling for fill colors.

### B. BitmapLayer (Heatmaps/Rasters)
Ideal for rendering static hyperspectral index images (e.g., NDVI, disease stress indices) over specific farm coordinates.
- **Configuration**: Requires bounding box coordinates `[left, bottom, right, top]` to stretch the image correctly over the projection.

### C. TileLayer (Pyramid Zooming)
Crucial for hyperspectral imagery which is too massive to load at once. The `TileLayer` fetches standard XYZ map tiles or Cloud Optimized GeoTIFFs (using `geotiff.js`) depending on the zoom level.
- **Configuration**: Combine with `BitmapLayer` inside the `renderSubLayers` prop to render each individual tile once fetched.

## 4. Viewport Camera Synchronization Mechanics

In React, the camera state (latitude, longitude, zoom, pitch, bearing) is treated as a controlled component state. `react-map-gl`'s `<Map>` and `deck.gl`'s `<DeckGL>` components share this state. 

- **State Hook**: `const [viewState, setViewState] = useState(initialViewState);`
- **Syncing**: Pass `viewState` and an `onViewStateChange` callback to DeckGL to ensure pan, zoom, tilt, and rotation are completely synchronized with the basemap.

## 5. Interactive Canvas Pixel Picking & Plotly.js Integration

To analyze a specific pixel's 224-band spectrum:
1. **Picking**: Deck.gl has a built-in picking engine. Enable it by setting `pickable: true` on the `BitmapLayer` or `TileLayer`.
2. **onClick Handler**: When clicked, Deck.gl provides `info.coordinate` (the lng/lat). If using `BitmapLayer`, it also provides `info.bitmap.pixel` (the x/y pixel of the source image).
3. **Data Retrieval**: Send the coordinates to the backend to fetch the continuous 224-band spectral array.
4. **Rendering with Plotly.js**: Pass the spectral array (wavelengths on X-axis, reflectance on Y-axis) to a `<Plot>` component (`react-plotly.js`).

## 6. WebGL Context, Performance Optimization & Memory Management

- **Binary Data (Zero-Copy)**: Instead of passing arrays of objects to Deck.gl, pass typed arrays (`Float32Array`) directly. This bypasses the CPU formatting step and injects data straight into GPU memory.
- **updateTriggers**: Explicitly declare when attributes should update: `updateTriggers: { getFillColor: [selectedDiseaseState] }`.
- **Context Loss Handling**: Browsers drop WebGL contexts to save memory (especially on mobile). Handle `onWebGLInitialized` to set up resources and `onWebGLContextLost` to gracefully pause rendering or trigger a page reload/recovery.
- **Memory Management**: Use `useEffect` cleanup functions to destroy Mapbox instances and free large TypedArrays when the map unmounts.

---

## React + Deck.gl + Plotly Architectural Blueprint

```tsx
// MapComponent.tsx
import React, { useState, useCallback, useMemo } from 'react';
import DeckGL from '@deck.gl/react/typed';
import { GeoJsonLayer, BitmapLayer } from '@deck.gl/layers/typed';
import { Map } from 'react-map-gl';
import Plot from 'react-plotly.js';

const MAPBOX_ACCESS_TOKEN = 'your_mapbox_token_here';

const INITIAL_VIEW_STATE = {
  longitude: -122.4,
  latitude: 37.74,
  zoom: 11,
  maxZoom: 20,
  pitch: 30,
  bearing: 0
};

export default function HyperspectralMap({ farmBoundaries, hyperspectralImgUrl, imgBounds }) {
  const [viewState, setViewState] = useState(INITIAL_VIEW_STATE);
  const [spectralData, setSpectralData] = useState(null);

  // Layer 1: Farm Boundaries
  const geoLayer = useMemo(() => new GeoJsonLayer({
    id: 'farm-boundaries',
    data: farmBoundaries,
    pickable: true,
    stroked: true,
    filled: true,
    lineWidthMinPixels: 2,
    getFillColor: [160, 160, 180, 100],
    getLineColor: [255, 255, 255]
  }), [farmBoundaries]);

  // Layer 2: Hyperspectral Bitmap Heatmap
  const bitmapLayer = useMemo(() => new BitmapLayer({
    id: 'hyperspectral-bitmap',
    bounds: imgBounds, // [left, bottom, right, top]
    image: hyperspectralImgUrl,
    pickable: true,
    onClick: async (info) => {
      if (info.coordinate) {
        // Fetch 224-band data for clicked coordinate
        const response = await fetch(\`/api/spectra?lat=\${info.coordinate[1]}&lng=\${info.coordinate[0]}\`);
        const data = await response.json();
        setSpectralData(data); // { wavelengths: [], reflectance: [] }
      }
    }
  }), [hyperspectralImgUrl, imgBounds]);

  const onViewStateChange = useCallback(({ viewState }) => {
    setViewState(viewState);
  }, []);

  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh' }}>
      {/* GIS Map Container */}
      <div style={{ flex: 1, position: 'relative' }}>
        <DeckGL
          layers={[bitmapLayer, geoLayer]}
          viewState={viewState}
          onViewStateChange={onViewStateChange}
          controller={true}
          // Context loss handling
          onWebGLContextLost={(e) => console.error("WebGL Context Lost:", e)}
        >
          <Map reuseMaps mapStyle="mapbox://styles/mapbox/satellite-v9" mapboxAccessToken={MAPBOX_ACCESS_TOKEN} />
        </DeckGL>
      </div>

      {/* Spectral Analytics Sidebar */}
      {spectralData && (
        <div style={{ width: '400px', backgroundColor: '#fff', borderLeft: '1px solid #ccc' }}>
          <h3>Pixel Spectral Signature (224 Bands)</h3>
          <Plot
            data={[
              {
                x: spectralData.wavelengths,
                y: spectralData.reflectance,
                type: 'scatter',
                mode: 'lines',
                line: { color: 'green' }
              }
            ]}
            layout={{ 
              width: 380, 
              height: 300, 
              title: 'Reflectance vs Wavelength',
              xaxis: { title: 'Wavelength (nm)' },
              yaxis: { title: 'Reflectance (%)' }
            }}
          />
        </div>
      )}
    </div>
  );
}
```
