import { useCallback } from 'react'
import DeckGL from '@deck.gl/react'
import { Map } from 'react-map-gl/mapbox'
import type { PickingInfo } from '@deck.gl/core'
import { useAppStore } from './store/useAppStore'
import { createFarmBoundaryLayer, createBlightHeatmapLayer } from './layers/farmBoundaryLayer'
import { SpectralDrawer } from './components/SpectralDrawer'
import { LayerControl } from './components/LayerControl'
import { TimelineSlider } from './components/TimelineSlider'
import { Activity, ShieldAlert, Cpu } from 'lucide-react'

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN as string

function App() {
  const {
    viewState,
    setViewState,
    layers,
    heatmapOpacity,
    activeWeekIndex,
    setSelectedPixel,
  } = useAppStore()

  // Camera viewport handler with TypeScript safety
  const onViewStateChange = useCallback(
    ({ viewState: next }: { viewState: any }) => {
      setViewState(next)
    },
    [setViewState]
  )

  // Map Click Handler for Hyperspectral Pixel Extraction
  const onClick = useCallback(
    (info: PickingInfo) => {
      if (info.object && info.coordinate) {
        const props = info.object.properties as any
        const fieldId = props.fieldId || 'field-a'

        // Determine health status based on field ID for realistic simulation
        let healthStatus: 'healthy' | 'moderate' | 'blighted' = 'healthy'
        if (fieldId === 'field-b') healthStatus = 'moderate'
        if (fieldId === 'field-c') healthStatus = 'blighted'

        setSelectedPixel({
          x: info.x,
          y: info.y,
          lat: info.coordinate[1],
          lng: info.coordinate[0],
          fieldId: props.fieldId || 'unknown',
          fieldName: props.name || 'Selected Sector',
          healthStatus,
        })
      }
    },
    [setSelectedPixel]
  )

  // Instantiate Deck.gl Layers
  const boundaryLayer = createFarmBoundaryLayer(layers.boundaries)
  const heatmapLayer = createBlightHeatmapLayer(
    layers.heatmap,
    heatmapOpacity,
    activeWeekIndex
  )

  if (!MAPBOX_TOKEN) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-neutral-950 p-6 text-neutral-100 font-sans">
        <div className="max-w-md rounded-2xl border border-rose-500/30 bg-neutral-900/80 p-6 text-center shadow-2xl backdrop-blur-xl">
          <ShieldAlert className="mx-auto h-12 w-12 text-rose-500" />
          <h2 className="mt-3 text-lg font-bold text-neutral-100">Mapbox Token Missing</h2>
          <p className="mt-2 text-xs text-neutral-400 leading-relaxed">
            Please add <code className="rounded bg-neutral-800 px-1.5 py-0.5 text-rose-400">VITE_MAPBOX_TOKEN</code> to your{' '}
            <code className="rounded bg-neutral-800 px-1.5 py-0.5 text-neutral-300">frontend/.env</code> file to enable WebGL satellite tiles.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="relative h-screen w-screen overflow-hidden bg-neutral-950 font-sans antialiased select-none">
      {/* WebGL Deck.gl Map Canvas */}
      <DeckGL
        viewState={viewState}
        onViewStateChange={onViewStateChange}
        controller={true}
        layers={[boundaryLayer, heatmapLayer]}
        onClick={onClick}
        getCursor={({ isHovering }) => (isHovering ? 'pointer' : 'default')}
        style={{ position: 'absolute', top: '0px', bottom: '0px', left: '0px', right: '0px' }}
      >
        <Map
          reuseMaps
          mapStyle="mapbox://styles/mapbox/satellite-streets-v12"
          mapboxAccessToken={MAPBOX_TOKEN}
        />
      </DeckGL>

      {/* Top Left Branding Header */}
      <div className="pointer-events-none absolute top-4 left-4 z-40 flex items-center gap-3">
        <div className="pointer-events-auto flex items-center gap-3 rounded-2xl border border-white/10 bg-neutral-950/80 px-4 py-3 shadow-2xl backdrop-blur-xl">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-500/20 border border-emerald-500/30 text-emerald-400">
            <Activity className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold tracking-wide text-neutral-100">TerraSpectra</span>
              <span className="inline-flex items-center gap-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium text-emerald-400">
                <Cpu className="h-3 w-3" /> WebGL GIS
              </span>
            </div>
            <div className="text-[11px] text-neutral-400">
              Hyperspectral Crop Disease Forecasting Dashboard
            </div>
          </div>
        </div>
      </div>

      {/* Floating Layer Control Panel (Top Right) */}
      <LayerControl />

      {/* Slide-Over Hyperspectral Plotly Drawer (Right) */}
      <SpectralDrawer />

      {/* Bottom Timeline Date Slider */}
      <TimelineSlider />

      {/* Bottom Right Telemetry HUD */}
      <div className="pointer-events-none absolute bottom-4 right-4 z-30 rounded-xl border border-white/10 bg-neutral-950/80 px-3.5 py-2 font-mono text-[11px] text-neutral-300 shadow-xl backdrop-blur-md">
        lat {(viewState.latitude ?? 0).toFixed(4)}° · lng {(viewState.longitude ?? 0).toFixed(4)}° · zoom{' '}
        {(viewState.zoom ?? 0).toFixed(2)} · pitch {(viewState.pitch ?? 0).toFixed(0)}° · bearing{' '}
        {(viewState.bearing ?? 0).toFixed(0)}°
      </div>
    </div>
  )
}

export default App