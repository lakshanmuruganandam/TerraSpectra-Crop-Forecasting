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
    // ── Indian Pines, Indiana (AVIRIS Test Site ~ -87.00, 40.47) ──────
    {
      type: 'Feature',
      properties: {
        fieldId: 'ip-corn-1',
        name: 'Indian Pines - Corn Sector A',
        cropType: 'Corn-no till',
        areaHectares: 34.2,
        healthScore: 88,
        blightRisk: 'Low',
        lastScanned: '2026-08-25',
        ndviMean: 0.79,
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [-87.015, 40.462],
            [-86.995, 40.462],
            [-86.995, 40.478],
            [-87.015, 40.478],
            [-87.015, 40.462],
          ],
        ],
      },
    },
    {
      type: 'Feature',
      properties: {
        fieldId: 'ip-soybean-2',
        name: 'Indian Pines - Soybean Sector B (Foliar Blight)',
        cropType: 'Soybeans-min till',
        areaHectares: 26.5,
        healthScore: 41,
        blightRisk: 'Severe',
        lastScanned: '2026-08-28',
        ndviMean: 0.44,
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [-86.992, 40.465],
            [-86.978, 40.465],
            [-86.978, 40.479],
            [-86.992, 40.479],
            [-86.992, 40.465],
          ],
        ],
      },
    },
    {
      type: 'Feature',
      properties: {
        fieldId: 'ip-wheat-3',
        name: 'Indian Pines - Wheat Plot C',
        cropType: 'Winter Wheat',
        areaHectares: 19.8,
        healthScore: 68,
        blightRisk: 'Moderate',
        lastScanned: '2026-08-27',
        ndviMean: 0.63,
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [-87.012, 40.450],
            [-86.988, 40.450],
            [-86.988, 40.460],
            [-87.012, 40.460],
            [-87.012, 40.450],
          ],
        ],
      },
    },

    // ── Salinas Valley, California (AVIRIS Test Site ~ -121.65, 36.67) ──
    {
      type: 'Feature',
      properties: {
        fieldId: 'salinas-lettuce-1',
        name: 'Salinas Valley - Romaine Lettuce Plot 14',
        cropType: 'Romaine Lettuce',
        areaHectares: 22.0,
        healthScore: 84,
        blightRisk: 'Low',
        lastScanned: '2026-08-26',
        ndviMean: 0.77,
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [-121.668, 36.670],
            [-121.648, 36.670],
            [-121.648, 36.685],
            [-121.668, 36.685],
            [-121.668, 36.670],
          ],
        ],
      },
    },
    {
      type: 'Feature',
      properties: {
        fieldId: 'salinas-vineyard-2',
        name: 'Salinas Valley - Pinot Noir Vineyard',
        cropType: 'Grapes / Vineyard',
        areaHectares: 31.4,
        healthScore: 49,
        blightRisk: 'Moderate',
        lastScanned: '2026-08-28',
        ndviMean: 0.52,
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [-121.645, 36.665],
            [-121.630, 36.665],
            [-121.630, 36.680],
            [-121.645, 36.680],
            [-121.645, 36.665],
          ],
        ],
      },
    },

    // ── Ahmedabad Agro Benchmark Site (~ 72.56, 23.03) ───────────────
    {
      type: 'Feature',
      properties: {
        fieldId: 'field-a',
        name: 'Ahmedabad - Field Alpha (Lettuce Plot 1)',
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
        name: 'Ahmedabad - Field Beta (Vineyard Zone 4)',
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
        name: 'Ahmedabad - Field Gamma (Corn Sector 12)',
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

    // ── WHU-Hi Agricultural UAV Benchmark Site (~ 113.68, 30.52) ─────
    {
      type: 'Feature',
      properties: {
        fieldId: 'whu-cabbage-1',
        name: 'WHU-Hi LongKou - Brassica Cabbage Site',
        cropType: 'Chinese Cabbage',
        areaHectares: 15.6,
        healthScore: 89,
        blightRisk: 'Low',
        lastScanned: '2026-08-20',
        ndviMean: 0.81,
      },
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [113.670, 30.512],
            [113.688, 30.512],
            [113.688, 30.525],
            [113.670, 30.525],
            [113.670, 30.512],
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