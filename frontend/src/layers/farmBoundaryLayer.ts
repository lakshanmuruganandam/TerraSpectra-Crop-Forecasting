import { GeoJsonLayer } from '@deck.gl/layers'
import { BitmapLayer } from '@deck.gl/layers'
import { mockFarmFields } from '../data/mockFarmFields'

export function createFarmBoundaryLayer(visible: boolean = true) {
  return new GeoJsonLayer({
    id: 'farm-boundaries',
    data: mockFarmFields,
    visible,
    pickable: true,
    stroked: true,
    filled: true,
    getFillColor: [26, 188, 156, 30],
    getLineColor: [46, 204, 113, 240],
    getLineWidth: 2.5,
    lineWidthMinPixels: 2,
  })
}

// Generate a synthetic Canvas Heatmap representing 3D-CNN Blight Risk Predictions
export function createBlightRiskHeatmapCanvas(weekIndex: number = 0): string {
  const canvas = document.createElement('canvas')
  canvas.width = 256
  canvas.height = 256
  const ctx = canvas.getContext('2d')
  if (!ctx) return ''

  // Clear canvas
  ctx.clearRect(0, 0, 256, 256)

  // Simulate field disease progression across weeks
  const spreadFactor = Math.min(1.0, 0.2 + weekIndex * 0.25)

  // Gradient 1: Field Alpha (Healthy -> Mild stress)
  const gradA = ctx.createRadialGradient(100, 80, 5, 100, 80, 60 * spreadFactor)
  gradA.addColorStop(0, `rgba(46, 204, 113, ${0.8 * spreadFactor})`)
  gradA.addColorStop(0.7, `rgba(241, 196, 15, ${0.5 * spreadFactor})`)
  gradA.addColorStop(1, 'rgba(0, 0, 0, 0)')

  ctx.fillStyle = gradA
  ctx.fillRect(0, 0, 256, 256)

  // Gradient 2: Field Beta (Moderate Blight Outbreak)
  const gradB = ctx.createRadialGradient(180, 150, 10, 180, 150, 70 * spreadFactor)
  gradB.addColorStop(0, `rgba(231, 76, 60, ${0.85 * spreadFactor})`) // Severe Red
  gradB.addColorStop(0.5, `rgba(230, 126, 34, ${0.65 * spreadFactor})`) // Orange
  gradB.addColorStop(1, 'rgba(0, 0, 0, 0)')

  ctx.fillStyle = gradB
  ctx.fillRect(0, 0, 256, 256)

  // Gradient 3: Field Gamma (Critical Cell Collapse Zone)
  const gradC = ctx.createRadialGradient(70, 200, 5, 70, 200, 55 * spreadFactor)
  gradC.addColorStop(0, `rgba(192, 57, 43, ${0.9 * spreadFactor})`)
  gradC.addColorStop(0.6, `rgba(241, 196, 15, ${0.6 * spreadFactor})`)
  gradC.addColorStop(1, 'rgba(0, 0, 0, 0)')

  ctx.fillStyle = gradC
  ctx.fillRect(0, 0, 256, 256)

  return canvas.toDataURL('image/png')
}

export function createBlightHeatmapLayer(
  visible: boolean = true,
  opacity: number = 0.75,
  weekIndex: number = 0,
  centerLng: number = -87.0
) {
  const image = createBlightRiskHeatmapCanvas(weekIndex)

  // Choose bounding box matching the current viewpoint cluster
  let bounds: [number, number, number, number] = [-87.02, 40.445, -86.97, 40.485] // Indian Pines default
  if (centerLng > 70 && centerLng < 75) {
    bounds = [72.54, 23.01, 72.59, 23.045] // Ahmedabad
  } else if (centerLng < -115) {
    bounds = [-121.675, 36.66, -121.625, 36.69] // Salinas Valley
  } else if (centerLng > 100) {
    bounds = [113.665, 30.505, 113.695, 30.53] // WHU-Hi LongKou
  }

  return new BitmapLayer({
    id: 'blight-risk-heatmap',
    bounds,
    image,
    visible,
    opacity,
    pickable: false,
  })
}