// Color constants for site polygon layers.
// Mapbox layers don't consume Tailwind — these need to be real hex values.
// Reused in ProjectFilterPanel's type indicator dots via inline style.
export const SITE_COLORS = {
  carbon: {
    fill: '#2A5444',    // forest-light — consistent with the nav brand
    outline: '#1B3B2F',
  },
  biodiversity: {
    fill: '#1A7A6E',    // teal — distinct from the green family, reads clearly at polygon opacity
    outline: '#145F55',
  },
}
