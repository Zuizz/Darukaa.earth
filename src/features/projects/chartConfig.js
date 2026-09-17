import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";

// Register all required Chart.js components once
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
);

export const CHART_THEME = {
  forest: "#009E4D",
  forestLight: "#10B981",
  forestFill: "rgba(0, 158, 77, 0.15)",
  amber: "#C99A3C",
  amberDark: "#A67C28",
  amberFill: "rgba(201, 154, 60, 0.18)",
  teal: "#1A7A6E",
  tealDark: "#145F55",
  tealFill: "rgba(26, 122, 110, 0.15)",
  ink: "#1C1C1A",
  inkMuted: "#5C5C58",
  border: "#D8D4C8",
  creamDark: "#EDE9DE",
  gaugeBackground: "#E8E4D8",
};

export const baseTooltipOptions = {
  backgroundColor: CHART_THEME.forest,
  titleColor: "#F7F5EF",
  bodyColor: "#F7F5EF",
  borderColor: CHART_THEME.amber,
  borderWidth: 1,
  padding: 10,
  cornerRadius: 6,
  displayColors: false,
  titleFont: {
    family: "'Inter', sans-serif",
    size: 11,
    weight: "600",
  },
  bodyFont: {
    family: "'Inter', sans-serif",
    size: 12,
    weight: "500",
  },
};

export const baseScalesOptions = {
  x: {
    grid: {
      display: false,
    },
    ticks: {
      color: CHART_THEME.inkMuted,
      font: {
        family: "'Inter', sans-serif",
        size: 11,
      },
    },
    border: {
      color: CHART_THEME.border,
    },
  },
  y: {
    grid: {
      color: "rgba(216, 212, 200, 0.45)",
      tickBorderDash: [3, 3],
    },
    ticks: {
      color: CHART_THEME.inkMuted,
      font: {
        family: "'Inter', sans-serif",
        size: 11,
      },
    },
    border: {
      display: false,
    },
  },
};
