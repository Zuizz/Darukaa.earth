import { Line } from 'react-chartjs-2'
import Card from '../../../components/Card'
import { CHART_THEME, baseTooltipOptions, baseScalesOptions } from '../chartConfig'

const DEFAULT_MONTHS = ['Dec 23', 'Jan 24', 'Feb 24', 'Mar 24', 'Apr 24', 'May 24', 'Jun 24', 'Jul 24', 'Aug 24', 'Sep 24', 'Oct 24', 'Nov 24']

export default function TimeSeriesLineChart({ metric, type, months = [] }) {
  const isCarbon = type === 'carbon'
  const lineColor = isCarbon ? CHART_THEME.forestLight : CHART_THEME.teal
  const fillColor = isCarbon ? CHART_THEME.forestFill : CHART_THEME.tealFill
  const labels = months.length > 0 ? months : (metric.months || DEFAULT_MONTHS)

  const chartData = {
    labels,
    datasets: [
      {
        label: metric.label,
        data: metric.trend,
        borderColor: lineColor,
        backgroundColor: fillColor,
        fill: true,
        tension: 0.35,
        borderWidth: 2,
        pointRadius: 3,
        pointHoverRadius: 6,
        pointBackgroundColor: lineColor,
        pointHoverBackgroundColor: CHART_THEME.amber,
        pointHoverBorderColor: '#ffffff',
        pointHoverBorderWidth: 2,
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
      y: {
        ...baseScalesOptions.y,
        ticks: {
          ...baseScalesOptions.y.ticks,
          callback: (val) => `${val}${metric.unit === '%' ? '%' : ''}`,
        },
      },
    },
  }

  return (
    <Card className="flex flex-col gap-3">
      <div className="flex items-baseline justify-between border-b border-border pb-3">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-semibold text-ink">{metric.label} Trend (12 Months)</h3>
            <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-forest/10 text-forest">
              {metric.annualChange}
            </span>
          </div>
          <p className="text-xs text-ink-muted mt-0.5">{metric.description}</p>
        </div>
        <div className="text-right">
          <span className="text-xl font-bold text-ink">{metric.currentValue}</span>
          <span className="block text-[11px] text-ink-muted">Latest reading</span>
        </div>
      </div>

      <div className="h-64 w-full">
        <Line data={chartData} options={options} />
      </div>
    </Card>
  )
}
