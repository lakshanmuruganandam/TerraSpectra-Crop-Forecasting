import { create } from 'zustand'
import type { MapViewState } from '@deck.gl/core'

export interface SelectedPixelInfo {
  x: number
  y: number
  lat: number
  lng: number
  fieldId: string
  fieldName: string
  healthStatus: 'healthy' | 'moderate' | 'blighted'
}

export interface LayerVisibility {
  satellite: boolean
  boundaries: boolean
  heatmap: boolean
  terrain: boolean
}

export interface AppState {
  // Map Viewport
  viewState: MapViewState
  setViewState: (viewState: MapViewState) => void

  // Layer Toggles & Opacity
  layers: LayerVisibility
  toggleLayer: (layerKey: keyof LayerVisibility) => void
  heatmapOpacity: number
  setHeatmapOpacity: (opacity: number) => void

  // Selected Field & Spectral Inspector Drawer
  selectedPixel: SelectedPixelInfo | null
  setSelectedPixel: (pixel: SelectedPixelInfo | null) => void
  isDrawerOpen: boolean
  setIsDrawerOpen: (open: boolean) => void

  // Time Series Slider
  activeWeekIndex: number
  setActiveWeekIndex: (index: number) => void
  isPlayingTimeline: boolean
  setIsPlayingTimeline: (playing: boolean) => void

  // Location Presets
  jumpToLocation: (preset: 'ahmedabad' | 'salinas' | 'indian_pines' | 'whu_hi') => void
}

const INITIAL_VIEW_STATE: MapViewState = {
  longitude: 72.565,
  latitude: 23.025,
  zoom: 13.5,
  pitch: 35,
  bearing: 0,
}

export const useAppStore = create<AppState>((set) => ({
  viewState: INITIAL_VIEW_STATE,
  setViewState: (viewState) => set({ viewState }),

  layers: {
    satellite: true,
    boundaries: true,
    heatmap: true,
    terrain: false,
  },
  toggleLayer: (layerKey) =>
    set((state) => ({
      layers: {
        ...state.layers,
        [layerKey]: !state.layers[layerKey],
      },
    })),

  heatmapOpacity: 0.75,
  setHeatmapOpacity: (opacity) => set({ heatmapOpacity: opacity }),

  selectedPixel: null,
  setSelectedPixel: (pixel) => set({ selectedPixel: pixel, isDrawerOpen: !!pixel }),
  isDrawerOpen: false,
  setIsDrawerOpen: (open) => set({ isDrawerOpen: open }),

  activeWeekIndex: 0,
  setActiveWeekIndex: (index) => set({ activeWeekIndex: index }),
  isPlayingTimeline: false,
  setIsPlayingTimeline: (playing) => set({ isPlayingTimeline: playing }),

  jumpToLocation: (preset) => {
    switch (preset) {
      case 'salinas':
        set({
          viewState: {
            longitude: -121.655,
            latitude: 36.677,
            zoom: 13,
            pitch: 45,
            bearing: 15,
          },
        })
        break
      case 'indian_pines':
        set({
          viewState: {
            longitude: -87.0,
            latitude: 40.47,
            zoom: 13.5,
            pitch: 30,
            bearing: 0,
          },
        })
        break
      case 'whu_hi':
        set({
          viewState: {
            longitude: 113.68,
            latitude: 30.52,
            zoom: 14,
            pitch: 40,
            bearing: 20,
          },
        })
        break
      case 'ahmedabad':
      default:
        set({ viewState: INITIAL_VIEW_STATE })
        break
    }
  },
}))
