import type { FeatureCollection, Polygon } from 'geojson'

interface FarmFieldProperties {
    fieldId: string
    name: string
}

export const mockFarmFields: FeatureCollection<Polygon, FarmFieldProperties> = {
    type: 'FeatureCollection',
    features: [
        {
            type: 'Feature',
            properties: { fieldId: 'field-a', name: 'Field A' },
            geometry: {
                type: 'Polygon',
                coordinates: [[[72.55, 23.03], [72.565, 23.03], [72.565, 23.04], [72.55, 23.04], [72.55, 23.03]]],
            },
        },
        {
            type: 'Feature',
            properties: { fieldId: 'field-b', name: 'Field B' },
            geometry: {
                type: 'Polygon',
                coordinates: [[[72.57, 23.02], [72.585, 23.02], [72.585, 23.032], [72.57, 23.032], [72.57, 23.02]]],
            },
        },
        {
            type: 'Feature',
            properties: { fieldId: 'field-c', name: 'Field C' },
            geometry: {
                type: 'Polygon',
                coordinates: [[[72.545, 23.015], [72.558, 23.015], [72.558, 23.024], [72.545, 23.024], [72.545, 23.015]]],
            },
        },
    ],
}