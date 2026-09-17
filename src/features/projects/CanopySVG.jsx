// Inline SVG canopy motif for the empty state.
// Kept as a component so it inherits Tailwind color utilities via className.
export default function CanopySVG({ className = '' }) {
  return (
    <svg
      className={className}
      viewBox="0 0 120 80"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      {/* Ground line */}
      <line x1="10" y1="72" x2="110" y2="72" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.3" />

      {/* Left tree — tall, narrow */}
      <line x1="32" y1="72" x2="32" y2="42" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.5" />
      <ellipse cx="32" cy="36" rx="10" ry="13" fill="currentColor" opacity="0.15" />
      <ellipse cx="32" cy="34" rx="7" ry="9" fill="currentColor" opacity="0.25" />

      {/* Centre tree — largest */}
      <line x1="60" y1="72" x2="60" y2="36" stroke="currentColor" strokeWidth="2" strokeLinecap="round" opacity="0.5" />
      <ellipse cx="60" cy="27" rx="16" ry="18" fill="currentColor" opacity="0.13" />
      <ellipse cx="60" cy="25" rx="11" ry="13" fill="currentColor" opacity="0.22" />
      <ellipse cx="60" cy="22" rx="7" ry="8" fill="currentColor" opacity="0.3" />

      {/* Right tree — shorter, offset */}
      <line x1="88" y1="72" x2="88" y2="50" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.5" />
      <ellipse cx="88" cy="43" rx="11" ry="12" fill="currentColor" opacity="0.15" />
      <ellipse cx="88" cy="41" rx="7.5" ry="8" fill="currentColor" opacity="0.22" />

      {/* Small foreground shrub */}
      <ellipse cx="48" cy="70" rx="8" ry="5" fill="currentColor" opacity="0.12" />
      <ellipse cx="74" cy="70" rx="6" ry="4" fill="currentColor" opacity="0.1" />
    </svg>
  )
}
