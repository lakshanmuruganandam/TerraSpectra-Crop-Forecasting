import React, { useMemo } from 'react'
import Plot from 'react-plotly.js'
import { X, Activity, AlertTriangle, CheckCircle, ShieldAlert, Sparkles } from 'lucide-react'
import { useAppStore } from '../store/useAppStore'
import { generateSpectralCurve } from '../data/mockFarmFields'

export const SpectralDrawer: React.FC = () => {
  const { selectedPixel, isDrawerOpen, setIsDrawerOpen } = useAppStore()

  const spectralData = useMemo(() => {
    if (!selectedPixel) return null
    return generateSpectralCurve(selectedPixel.healthStatus)
  }, [selectedPixel])

  if (!isDrawerOpen || !selectedPixel || !spectralData) return null

  const getHealthBadge = (status: 'healthy' | 'moderate' | 'blighted') => {
    switch (status) {
      case 'healthy':
        return (
          <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-400">
            <CheckCircle className="h-3.5 w-3.5" /> Healthy Crop (High Reflectance)
          </span>
        )
      case 'moderate':
        return (
          <span className="inline-flex items-center gap-1.5 rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1 text-xs font-medium text-amber-400">
            <AlertTriangle className="h-3.5 w-3.5" /> Early Stress Warning
          </span>
        )
      case 'blighted':
        return (
          <span className="inline-flex items-center gap-1.5 rounded-full border border-rose-500/30 bg-rose-500/10 px-3 py-1 text-xs font-medium text-rose-400">
            <ShieldAlert className="h-3.5 w-3.5" /> Severe Blight / Collapse
          </span>
        )
    }
  }

  return (
    <div className="fixed inset-y-0 right-0 z-50 flex w-full max-w-xl flex-col border-l border-white/10 bg-neutral-950/85 p-6 shadow-2xl backdrop-blur-xl transition-all duration-300 sm:rounded-l-2xl">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-neutral-800/60 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Activity className="h-5 w-5 text-emerald-400" />
            <h2 className="text-lg font-bold tracking-tight text-neutral-100">
              Hyperspectral Inspector
            </h2>
          </div>
          <p className="mt-1 text-xs text-neutral-400">
            Field: <span className="font-semibold text-neutral-200">{selectedPixel.fieldName}</span>{' '}
            ({selectedPixel.fieldId})
          </p>
        </div>
        <button
          onClick={() => setIsDrawerOpen(false)}
          className="rounded-lg p-2 text-neutral-400 transition-colors hover:bg-neutral-800/60 hover:text-white"
        >
          <X className="h-5 w-5" />
        </button>
      </div>

      {/* Details Bar */}
      <div className="mt-4 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-neutral-800/80 bg-neutral-900/60 p-3.5 text-xs text-neutral-300">
        <div>
          <span className="text-neutral-400">Coordinates:</span>{' '}
          <span className="font-mono text-emerald-300">
            {selectedPixel.lat.toFixed(5)}°, {selectedPixel.lng.toFixed(5)}°
          </span>
        </div>
        <div>{getHealthBadge(selectedPixel.healthStatus)}</div>
      </div>

      {/* Plotly Chart Container */}
      <div className="mt-4 flex-1 rounded-xl border border-neutral-800/80 bg-neutral-900/40 p-2 shadow-inner">
        <Plot
          data={[
            {
              x: spectralData.wavelengths,
              y: spectralData.reflectance,
              type: 'scatter',
              mode: 'lines',
              name: 'Reflectance Signature',
              line: {
                color:
                  selectedPixel.healthStatus === 'healthy'
                    ? '#10b981'
                    : selectedPixel.healthStatus === 'moderate'
                    ? '#f59e0b'
                    : '#ef4444',
                width: 2.5,
                shape: 'spline',
              },
            },
          ]}
          layout={{
            autosize: true,
            title: {
              text: '224-Band Reflectance Curve (400nm - 2500nm)',
              font: { color: '#e5e5e5', size: 13, family: 'Inter, sans-serif' },
            },
            paper_bgcolor: 'transparent',
            plot_bgcolor: 'transparent',
            margin: { l: 45, r: 25, t: 40, b: 45 },
            xaxis: {
              title: { text: 'Wavelength (nm)', font: { color: '#a3a3a3', size: 11 } },
              tickfont: { color: '#737373', size: 10 },
              gridcolor: '#262626',
              zerolinecolor: '#404040',
            },
            yaxis: {
              title: { text: 'Reflectance Factor (0 - 1)', font: { color: '#a3a3a3', size: 11 } },
              tickfont: { color: '#737373', size: 10 },
              gridcolor: '#262626',
              zerolinecolor: '#404040',
              range: [0, 0.7],
            },
            annotations: [
              {
                x: 670,
                y: 0.05,
                text: 'Chlorophyll Dip',
                showarrow: true,
                arrowhead: 2,
                arrowcolor: '#10b981',
                font: { color: '#a7f3d0', size: 9 },
              },
              {
                x: 720,
                y: 0.3,
                text: 'Red Edge Slope',
                showarrow: true,
                arrowhead: 2,
                arrowcolor: '#f59e0b',
                font: { color: '#fde68a', size: 9 },
              },
              {
                x: 950,
                y: 0.52,
                text: 'NIR Scattering Plateau',
                showarrow: false,
                font: { color: '#a3a3a3', size: 9 },
              },
            ],
          }}
          useResizeHandler={true}
          style={{ width: '100%', height: '100%', minHeight: '280px' }}
          config={{ displayModeBar: false, responsive: true }}
        />
      </div>

      {/* AI Diagnostic Explanation */}
      <div className="mt-4 rounded-xl border border-emerald-500/20 bg-emerald-950/20 p-4 backdrop-blur-sm">
        <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400">
          <Sparkles className="h-4 w-4" /> AI Spectral Biomarker Analysis
        </div>
        <p className="mt-1.5 text-xs text-neutral-300 leading-relaxed">
          {selectedPixel.healthStatus === 'healthy' &&
            'Normal Red Edge steepness and high NIR plateau (~50% reflectance) indicate robust cell structure and high chlorophyll density.'}
          {selectedPixel.healthStatus === 'moderate' &&
            'Early Red Edge blue-shift detected around 705nm. Chlorophyll breakdown is occurring prior to visible symptomatic yellowing.'}
          {selectedPixel.healthStatus === 'blighted' &&
            'Severe Red Edge slope collapse and depressed NIR reflectance (<25%). High risk of Phytophthora blight outbreak detected.'}
        </p>
      </div>
    </div>
  )
}
