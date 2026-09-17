import { useEffect, useRef, useState } from 'react'
import MapboxDraw from '@mapbox/mapbox-gl-draw'

/**
 * Attaches MapboxDraw to the map when it becomes available.
 * Returns the drawn feature that's pending a name/project assignment,
 * plus callbacks the form uses to confirm or cancel.
 */
export function useMapDraw(map) {
  const drawRef = useRef(null)
  const [pendingFeature, setPendingFeature] = useState(null)

  useEffect(() => {
    if (!map) return

    const draw = new MapboxDraw({
      displayControlsDefault: false,
      controls: { polygon: true, trash: true },
      defaultMode: 'simple_select',
    })

    map.addControl(draw, 'top-left')
    drawRef.current = draw

    function handleDrawCreate(e) {
      // Leave the drawn polygon visible while the form is open so the user
      // can see what they just drew. handleDrawComplete removes it on submit.
      setPendingFeature(e.features[0])
    }

    map.on('draw.create', handleDrawCreate)

    return () => {
      map.off('draw.create', handleDrawCreate)
      // map.remove() tears down the map including its controls, so removeControl
      // can throw if cleanup order puts it after the map is gone. Swallow that case.
      try {
        map.removeControl(draw)
      } catch { /* map already removed */ }
      drawRef.current = null
    }
  }, [map])

  function handleDrawComplete() {
    drawRef.current?.deleteAll()
    setPendingFeature(null)
  }

  function handleDrawCancel() {
    drawRef.current?.deleteAll()
    setPendingFeature(null)
  }

  return { pendingFeature, handleDrawComplete, handleDrawCancel }
}
