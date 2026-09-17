/**
 * Card — a basic surface container.
 *
 * Props:
 *   className (string?) — extra classes merged onto the card div
 *   children  (node)
 *   padding   (bool, default true) — set false when the card content manages its own padding
 */
export default function Card({
  className = "",
  padding = true,
  children,
  ...props
}) {
  return (
    <div
      className={`bg-white rounded-lg border border-border ${padding ? "p-5" : ""} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
