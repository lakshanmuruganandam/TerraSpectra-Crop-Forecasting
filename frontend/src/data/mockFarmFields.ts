import type { FeatureCollection, Polygon } from 'geojson'

export interface FarmFieldProperties {
  fieldId: string
  name: string
  cropType: string
  areaHectares: number
  healthScore: number // 0 - 100
  blightRisk: 'Low' | 'Moderate' | 'Severe' | 'Critical'
  lastScanned: string
  ndviMean: number
}

export const mockFarmFields: FeatureCollection<Polygon, FarmFieldProperties> = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      properties: {
        fieldId: 'field-a',
        name: 'Field Alpha (Lettuce Plot 1)',
        cropType: 'Romaine Lettuce',
        areaHectares: 18.4,
        healthScore: 92,
        blightRisk: 'Low',
        lastScanned: '2026-08-10',
        ndviMean: 0.82,
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [72.55, 23.03],
            [72.565, 23.03],
            [72.565, 23.04],
            [72.55, 23.04],
            [72.55, 23.03],
          ],
        ],
      },
    },
    {
      type: 'Feature',
      properties: {
        fieldId: 'field-b',
        name: 'Field Beta (Vineyard Zone 4)',
        cropType: 'Thompson Seedless Grapes',
        areaHectares: 24.1,
        healthScore: 64,
        blightRisk: 'Moderate',
        lastScanned: '2026-08-08',
        ndviMean: 0.61,
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [72.57, 23.02],
            [72.585, 23.02],
            [72.585, 23.032],
            [72.57, 23.032],
            [72.57, 23.02],
          ],
        ],
      },
    },
    {
      type: 'Feature',
      properties: {
        fieldId: 'field-c',
        name: 'Field Gamma (Corn Sector 12)',
        cropType: 'Field Corn',
        areaHectares: 12.8,
        healthScore: 38,
        blightRisk: 'Severe',
        lastScanned: '2026-08-11',
        ndviMean: 0.39,
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [72.545, 23.015],
            [72.558, 23.015],
            [72.558, 23.024],
            [72.545, 23.024],
            [72.545, 23.015],
          ],
        ],
      },
    },
  ],
}

// Generate realistic 224-band Hyperspectral reflectance curves (400nm - 2500nm)
export function generateSpectralCurve(healthStatus: 'healthy' | 'moderate' | 'blighted'): {
  wavelengths: number[]
  reflectance: number[]
  bands: number
} {
  const bands = 224
  const wavelengths: number[] = []
  const reflectance: number[] = []

  const startWl = 400
  const endWl = 2500
  const step = (endWl - startWl) / (bands - 1)

  for (let i = 0; i < bands; i++) {
    const wl = startWl + i * step
    wavelengths.push(Math.round(wl))

    let val = 0.1

    if (wl >= 400 && wl <= 680) {
      // Visible light (Chlorophyll absorption dip around 670nm)
      val = 0.05 + 0.05 * Math.sin(((wl - 400) / 280) * Math.PI)
      if (wl >= 650 && wl <= 680) val *= 0.6 // Deep absorption
    } else if (wl > 680 && wl <= 750) {
      // Red Edge transition slope
      const progress = (wl - 680) / 70
      if (healthStatus === 'healthy') {
        val = 0.05 + progress * 0.45 // Steep healthy Red Edge rise
      } else if (healthStatus === 'moderate') {
        val = 0.07 + progress * 0.32
      } else {
        val = 0.12 + progress * 0.18 // Blighted blue-shift & collapsed slope
      }
    } else if (wl > 750 && wl <= 1300) {
      // NIR Plateau (Leaf cellular structure scattering)
      if (healthStatus === 'healthy') {
        val = 0.5 + Math.random() * 0.04
      } else if (healthStatus === 'moderate') {
        val = 0.35 + Math.random() * 0.04
      } else {
        val = 0.22 + Math.random() * 0.05 // Severe cellular collapse
      }
    } else if (wl > 1300 && wl <= 2500) {
      // SWIR region with atmospheric water absorption dips at ~1450nm and ~1950nm
      const baseSwir = healthStatus === 'healthy' ? 0.3 : 0.2
      val = baseSwir + Math.random() * 0.03
      if (wl >= 1400 && wl <= 1500) val *= 0.25 // Water absorption dip 1
      if (wl >= 1900 && wl <= 2000) val *= 0.15 // Water absorption dip 2
    }

    reflectance.push(parseFloat(Math.max(0, Math.min(1, val)).toFixed(4)))
  }

  return { wavelengths, reflectance, bands }
}