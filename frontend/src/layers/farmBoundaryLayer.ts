import { GeoJsonLayer } from '@deck.gl/layers'
import { mockFarmFields } from '../data/mockFarmFields'

export function createFarmBoundaryLayer() {
  return new GeoJsonLayer({
    id: 'farm-boundaries',
    data: mockFarmFields,
    pickable: true,
    stroked: true,
    filled: true,
    getFillColor: [26, 188, 156, 40],
    getLineColor: [46, 204, 113, 255],
    getLineWidth: 2,
    lineWidthMinPixels: 2,
  })
}