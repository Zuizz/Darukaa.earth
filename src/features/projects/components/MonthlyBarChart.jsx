import { Bar } from 'react-chartjs-2'
import Card from '../../../components/Card'
import { CHART_THEME, baseTooltipOptions, baseScalesOptions } from '../chartConfig'

const DEFAULT_MONTHS = ['Dec 23', 'Jan 24', 'Feb 24', 'Mar 24', 'Apr 24', 'May 24', 'Jun 24', 'Jul 24', 'Aug 24', 'Sep 24', 'Oct 24', 'Nov 24']

export default function MonthlyBarChart({ metric, type, months = [] }) {
  const isCarbon = type === 'carbon'
  const barColor = isCarbon ? CHART_THEME.amber : CHART_THEME.amberDark
  const labels = months.length > 0 ? months : (metric.months || DEFAULT_MONTHS)

  const chartData = {
    labels,
    datasets: [
      {
        label: metric.label,
        data: metric.trend,
        backgroundColor: barColor,
        hoverBackgroundColor: isCarbon ? CHART_THEME.amberDark : CHART_THEME.forest,
        borderRadius: 4,
        borderSkipped: false,
        maxBarThickness: 28,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        ...baseTooltipOptions,
        callbacks: {
          label: (context) => ` ${context.parsed.y} ${metric.unit}`,
        },
      },
    },
    scales: {
      ...baseScalesOptions,
    },
  }

  return (
    <Card className="flex flex-col gap-3">
      <div className="flex items-baseline justify-between border-b border-border pb-3">
        <div>
          <h3 className="text-sm font-semibold text-ink">{metric.label}</h3>
          <p className="text-xs text-ink-muted mt-0.5">{metric.description}</p>
        </div>
        <div className="text-right">
          <span className="text-lg font-bold text-ink">{metric.totalAnnual}</span>
          <span className="block text-[11px] text-ink-muted">12-mo total</span>
        </div>
      </div>

      <div className="h-56 w-full">
        <Bar data={chartData} options={options} />
      </div>
    </Card>
  )
}
