import React from 'react'
import { Layers, Eye, EyeOff, MapPin, Sliders } from 'lucide-react'
import { useAppStore } from '../store/useAppStore'

export const LayerControl: React.FC = () => {
  const { layers, toggleLayer, heatmapOpacity, setHeatmapOpacity, jumpToLocation } = useAppStore()

  return (
    <div className="absolute top-4 right-4 z-40 w-72 rounded-2xl border border-white/10 bg-neutral-950/80 p-4 shadow-2xl backdrop-blur-xl transition-all">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-neutral-800/80 pb-3">
        <div className="flex items-center gap-2 text-sm font-semibold text-neutral-100">
          <Layers className="h-4 w-4 text-emerald-400" />
          <span>Layer Control</span>
        </div>
        <span className="rounded-full bg-emerald-500/10 px-2 py-0.5 font-mono text-[10px] text-emerald-400 border border-emerald-500/20">
          WebGL Live
        </span>
      </div>

      {/* Layer Toggles */}
      <div className="mt-3.5 space-y-2.5">
        {/* Farm Boundaries */}
        <div className="flex items-center justify-between rounded-xl bg-neutral-900/50 p-2.5 transition-colors hover:bg-neutral-900/80">
          <div className="flex items-center gap-2.5 text-xs text-neutral-200">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400/50" />
            <span>Farm Boundaries</span>
          </div>
          <button
            onClick={() => toggleLayer('boundaries')}
            className="text-neutral-400 transition-colors hover:text-white"
          >
            {layers.boundaries ? (
              <Eye className="h-4 w-4 text-emerald-400" />
            ) : (
              <EyeOff className="h-4 w-4 text-neutral-600" />
            )}
          </button>
        </div>

        {/* AI Blight Heatmap */}
        <div className="flex flex-col gap-2 rounded-xl bg-neutral-900/50 p-2.5 transition-colors hover:bg-neutral-900/80">
          <div className="flex items-center justify-between text-xs text-neutral-200">
            <div className="flex items-center gap-2.5">
              <span className="h-2.5 w-2.5 rounded-full bg-rose-500 shadow-sm shadow-rose-500/50" />
              <span>Blight Risk Heatmap</span>
            </div>
            <button
              onClick={() => toggleLayer('heatmap')}
              className="text-neutral-400 transition-colors hover:text-white"
            >
              {layers.heatmap ? (
                <Eye className="h-4 w-4 text-rose-400" />
              ) : (
                <EyeOff className="h-4 w-4 text-neutral-600" />
              )}
            </button>
          </div>

          {/* Opacity Slider */}
          {layers.heatmap && (
            <div className="mt-1 flex items-center gap-2 border-t border-neutral-800/60 pt-2 text-[11px] text-neutral-400">
              <Sliders className="h-3 w-3 text-neutral-500" />
              <span>Opacity:</span>
              <input
                type="range"
                min="0.1"
                max="1.0"
                step="0.05"
                value={heatmapOpacity}
                onChange={(e) => setHeatmapOpacity(parseFloat(e.target.value))}
                className="h-1.5 flex-1 cursor-pointer accent-emerald-500 bg-neutral-800 rounded-lg"
              />
              <span className="font-mono text-neutral-300 w-7 text-right">
                {Math.round(heatmapOpacity * 100)}%
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Location Presets */}
      <div className="mt-4 border-t border-neutral-800/80 pt-3">
        <div className="flex items-center gap-1.5 text-xs font-semibold text-neutral-400 mb-2">
          <MapPin className="h-3.5 w-3.5 text-emerald-400" />
          <span>Location Presets</span>
        </div>
        <div className="grid grid-cols-2 gap-1.5 text-[11px]">
          <button
            onClick={() => jumpToLocation('ahmedabad')}
            className="rounded-lg border border-neutral-800 bg-neutral-900/60 py-1.5 px-2 text-neutral-300 transition-colors hover:border-emerald-500/50 hover:bg-emerald-950/30 hover:text-white"
          >
            Ahmedabad
          </button>
          <button
            onClick={() => jumpToLocation('salinas')}
            className="rounded-lg border border-neutral-800 bg-neutral-900/60 py-1.5 px-2 text-neutral-300 transition-colors hover:border-emerald-500/50 hover:bg-emerald-950/30 hover:text-white"
          >
            Salinas, CA
          </button>
          <button
            onClick={() => jumpToLocation('indian_pines')}
            className="rounded-lg border border-neutral-800 bg-neutral-900/60 py-1.5 px-2 text-neutral-300 transition-colors hover:border-emerald-500/50 hover:bg-emerald-950/30 hover:text-white"
          >
            Indian Pines
          </button>
          <button
            onClick={() => jumpToLocation('whu_hi')}
            className="rounded-lg border border-neutral-800 bg-neutral-900/60 py-1.5 px-2 text-neutral-300 transition-colors hover:border-emerald-500/50 hover:bg-emerald-950/30 hover:text-white"
          >
            WHU-Hi China
          </button>
        </div>
      </div>
    </div>
  )
}
