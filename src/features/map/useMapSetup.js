import { useEffect, useRef, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import { SITE_COLORS } from '../../lib/siteColors'

const INDIA_CENTER = [80.5, 22.0]
const INDIA_ZOOM   = 4.5
const INDIA_BOUNDS = [[68.0, 6.5], [97.5, 35.5]]

function addSitesLayers(map, onSiteClickRef) {
  if (map.getSource('sites')) return

  map.addSource('sites', {
    type: 'geojson',
    data: { type: 'FeatureCollection', features: [] },
  })

  map.addLayer({
    id: 'sites-fill',
    type: 'fill',
    source: 'sites',
    paint: {
      'fill-color': [
        'match', ['get', 'projectType'],
        'carbon',       SITE_COLORS.carbon.fill,
        'biodiversity', SITE_COLORS.biodiversity.fill,
        '#888888',
      ],
      'fill-opacity': 0.32,
    },
  })

  map.addLayer({
    id: 'sites-outline',
    type: 'line',
    source: 'sites',
    paint: {
      'line-color': [
        'match', ['get', 'projectType'],
        'carbon',       SITE_COLORS.carbon.outline,
        'biodiversity', SITE_COLORS.biodiversity.outline,
        '#555555',
      ],
      'line-width': 1.75,
    },
  })

  map.on('mouseenter', 'sites-fill', () => { map.getCanvas().style.cursor = 'pointer' })
  map.on('mouseleave', 'sites-fill', () => { map.getCanvas().style.cursor = '' })

  map.on('click', 'sites-fill', (e) => {
    const siteId = e.features?.[0]?.properties?.id
    if (siteId) onSiteClickRef.current?.(siteId)
  })
}

export function useMapSetup(
  containerRef,
  siteFeatures,
  activeProjectIds,
  onSiteClick,
  mapStyle = 'mapbox://styles/mapbox/satellite-v9'
) {
  const [map, setMap] = useState(null)
  const currentStyleRef = useRef(mapStyle)

  const onSiteClickRef = useRef(onSiteClick)
  useEffect(() => { onSiteClickRef.current = onSiteClick })

  useEffect(() => {
    const token = import.meta.env.VITE_MAPBOX_TOKEN
    if (!token) return

    mapboxgl.accessToken = token

    const m = new mapboxgl.Map({
      container: containerRef.current,
      style: mapStyle,
      center: INDIA_CENTER,
      zoom: INDIA_ZOOM,
      minZoom: 4,
      maxBounds: INDIA_BOUNDS,
    })

    m.addControl(new mapboxgl.NavigationControl({ showCompass: false }), 'bottom-right')

    const resizeObserver = new ResizeObserver(() => {
      m.resize()
    })
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current)
    }

    m.on('load', () => {
      m.resize()
      addSitesLayers(m, onSiteClickRef)
      setMap(m)
    })

    return () => {
      resizeObserver.disconnect()
      m.remove()
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  // Handle dynamic style changes (e.g. switching between satellite-v9 & satellite-streets-v12)
  useEffect(() => {
    if (!map || !mapStyle) return
    if (currentStyleRef.current === mapStyle) return

    currentStyleRef.current = mapStyle
    map.setStyle(mapStyle)

    const handleStyleLoad = () => {
      addSitesLayers(map, onSiteClickRef)

      map.getSource('sites')?.setData({
        type: 'FeatureCollection',
        features: siteFeatures || [],
      })

      if (!activeProjectIds || activeProjectIds.size === 0) {
        const noneFilter = ['==', ['get', 'projectId'], '']
        map.setFilter('sites-fill', noneFilter)
        map.setFilter('sites-outline', noneFilter)
      } else {
        const idsList = Array.from(activeProjectIds).flatMap((id) => [id, String(id)])
        const visibleFilter = ['in', ['get', 'projectId'], ['literal', idsList]]
        map.setFilter('sites-fill', visibleFilter)
        map.setFilter('sites-outline', visibleFilter)
      }
    }

    map.once('style.load', handleStyleLoad)
  }, [map, mapStyle, siteFeatures, activeProjectIds])

  // Keep source data in sync whenever siteFeatures change
  useEffect(() => {
    if (!map) return
    map.getSource('sites')?.setData({
      type: 'FeatureCollection',
      features: siteFeatures,
    })
  }, [map, siteFeatures])

  // Update the per-project visibility filter
  useEffect(() => {
    if (!map) return

    if (!activeProjectIds || activeProjectIds.size === 0) {
      const noneFilter = ['==', ['get', 'projectId'], '']
      map.setFilter('sites-fill',    noneFilter)
      map.setFilter('sites-outline', noneFilter)
      return
    }

    const idsList = Array.from(activeProjectIds).flatMap((id) => [id, String(id)])
    const visibleFilter = ['in', ['get', 'projectId'], ['literal', idsList]]
    map.setFilter('sites-fill',    visibleFilter)
    map.setFilter('sites-outline', visibleFilter)
  }, [map, activeProjectIds])

  return map
}
