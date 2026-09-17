/**
 * Shared utility functions.
 *
 * Keep this file small — if a group of helpers grows beyond 3–4 related functions,
 * split into a focused module (e.g. lib/formatters.js, lib/geoUtils.js).
 */

/** Format a number as hectares with one decimal place. */
export function formatHa(value) {
  return `${Number(value).toLocaleString('en-US', { maximumFractionDigits: 1 })} ha`
}

/** Format a tonne-CO₂ value as a short human-readable string. */
export function formatCO2(tonnes) {
  if (tonnes >= 1_000_000) return `${(tonnes / 1_000_000).toFixed(1)}M tCO₂`
  if (tonnes >= 1_000)     return `${(tonnes / 1_000).toFixed(1)}k tCO₂`
  return `${tonnes} tCO₂`
}
