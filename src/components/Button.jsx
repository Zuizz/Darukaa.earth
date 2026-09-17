/**
 * Button variants:
 *   primary  — amber fill, main CTAs
 *   secondary — forest outline, secondary actions
 *   ghost    — no border, low-emphasis actions
 *
 * Sizes: sm | md (default) | lg
 */
const variantClasses = {
  primary: "bg-amber text-white hover:bg-amber-dark active:bg-amber-dark",
  secondary:
    "border border-forest text-forest hover:bg-forest hover:text-cream",
  ghost: "text-ink-muted hover:text-ink hover:bg-cream-dark",
};

const sizeClasses = {
  sm: "px-3 py-1.5 text-xs",
  md: "px-4 py-2 text-sm",
  lg: "px-5 py-2.5 text-base",
};

export default function Button({
  variant = "primary",
  size = "md",
  disabled = false,
  className = "",
  children,
  ...rest
}) {
  return (
    <button
      disabled={disabled}
      className={`
        inline-flex items-center justify-center gap-2 rounded-md font-medium
        transition-colors focus-visible:outline-none focus-visible:ring-2
        focus-visible:ring-amber focus-visible:ring-offset-2
        disabled:opacity-40 disabled:cursor-not-allowed
        ${variantClasses[variant]}
        ${sizeClasses[size]}
        ${className}
      `}
      {...rest}
    >
      {children}
    </button>
  );
}
