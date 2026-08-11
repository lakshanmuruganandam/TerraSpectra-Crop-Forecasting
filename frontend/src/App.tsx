import { useState, useCallback } from 'react'
import DeckGL from '@deck.gl/react'
import { Map } from 'react-map-gl/mapbox'
import type { MapViewState, PickingInfo } from '@deck.gl/core'
import { createFarmBoundaryLayer } from './layers/farmBoundaryLayer'

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN as string

const INITIAL_VIEW_STATE: MapViewState = {
  longitude: 72.565,
  latitude: 23.025,
  zoom: 13,
  pitch: 0,
  bearing: 0,
}

interface FieldProperties {
  fieldId: string
  name: string
}

interface HoverInfo {
  x: number
  y: number
  fieldId: string
  name: string
}

function App() {
  const [viewState, setViewState] = useState<MapViewState>(INITIAL_VIEW_STATE)
  const [hoverInfo, setHoverInfo] = useState<HoverInfo | null>(null)

  const onViewStateChange = useCallback(
    ({ viewState: next }: { viewState: MapViewState }) => {
      setViewState(next)
    },
    []
  )

  const onHover = useCallback((info: PickingInfo) => {
    if (info.object) {
      const props = info.object.properties as FieldProperties
      setHoverInfo({
        x: info.x,
        y: info.y,
        fieldId: props.fieldId,
        name: props.name,
      })
    } else {
      setHoverInfo(null)
    }
  }, [])

  const farmBoundaryLayer = createFarmBoundaryLayer()

  if (!MAPBOX_TOKEN) {
    return (
      <div className="dark h-screen w-screen flex items-center justify-center bg-neutral-950 text-red-400 font-mono">
        Missing VITE_MAPBOX_TOKEN — check frontend/.env
      </div>
    )
  }

  return (
    <div className="dark relative h-screen w-screen overflow-hidden bg-neutral-950">
      <DeckGL
        viewState={viewState}
        onViewStateChange={onViewStateChange}
        controller={true}
        layers={[farmBoundaryLayer]}
        onHover={onHover}
        style={{ position: 'absolute', inset: 0 }}
      >
        <Map
          reuseMaps
          mapStyle="mapbox://styles/mapbox/satellite-streets-v12"
          mapboxAccessToken={MAPBOX_TOKEN}
        />
      </DeckGL>

      {/* Title / branding */}
      <div className="pointer-events-none absolute top-4 left-4 rounded-lg border border-neutral-700/50 bg-neutral-900/85 px-4 py-2.5 shadow-lg backdrop-blur-sm">
        <div className="text-sm font-semibold tracking-wide text-neutral-100">
          TerraSpectra
        </div>
        <div className="text-xs text-neutral-400">
          Map Scaffolding — Week 1
        </div>
      </div>

      {/* Hover tooltip on field polygons */}
      {hoverInfo && (
        <div
          className="pointer-events-none absolute z-10 rounded-md border border-emerald-500/40 bg-neutral-900/95 px-3 py-2 text-xs text-neutral-100 shadow-lg"
          style={{ left: hoverInfo.x + 12, top: hoverInfo.y + 12 }}
        >
          <div className="font-semibold text-emerald-400">{hoverInfo.name}</div>
          <div className="text-neutral-400">ID: {hoverInfo.fieldId}</div>
        </div>
      )}

      {/* Live coordinate / zoom readout */}
      <div className="pointer-events-none absolute bottom-4 right-4 rounded-md border border-neutral-700/50 bg-neutral-900/85 px-3 py-2 font-mono text-xs text-neutral-300 shadow-lg backdrop-blur-sm">
        lat {viewState.latitude.toFixed(4)} · lng {viewState.longitude.toFixed(4)} · zoom{' '}
        {viewState.zoom.toFixed(2)} · pitch {viewState.pitch.toFixed(0)}° · bearing{' '}
        {viewState.bearing.toFixed(0)}°
      </div>
    </div>
  )
}

export default App