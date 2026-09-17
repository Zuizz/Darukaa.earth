import { Doughnut } from 'react-chartjs-2'
import Card from '../../../components/Card'
import { CHART_THEME } from '../chartConfig'

export default function HealthScoreGauge({ score, target, type, supportingMetric }) {
  const isCarbon = type === 'carbon'
  const fillTone = isCarbon ? CHART_THEME.forest : CHART_THEME.teal

  const data = {
    datasets: [
      {
        data: [score, Math.max(0, 100 - score)],
        backgroundColor: [fillTone, CHART_THEME.gaugeBackground],
        borderWidth: 0,
        circumference: 180,
        rotation: -90,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '78%',
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false },
    },
  }

  return (
    <Card className="flex flex-col justify-between">
      <div className="border-b border-border pb-3">
        <h3 className="text-sm font-semibold text-ink">Site Integrity Score</h3>
        <p className="text-xs text-ink-muted mt-0.5">Composite ecosystem health rating</p>
      </div>

      <div className="relative flex flex-col items-center justify-center my-2">
        <div className="h-36 w-full max-w-[220px]">
          <Doughnut data={data} options={options} />
        </div>
        {/* Center score readout positioned in the arch of the semi-doughnut */}
        <div className="absolute bottom-2 flex flex-col items-center text-center">
          <span className="text-3xl font-bold text-ink leading-none">{score}</span>
          <span className="text-[11px] text-ink-muted mt-1">out of 100</span>
        </div>
      </div>

      <div className="pt-3 border-t border-border flex items-center justify-between text-xs">
        <div>
          <span className="text-ink-muted">Target: </span>
          <span className="font-semibold text-ink">{target}/100</span>
        </div>
        {supportingMetric && (
          <div className="text-right">
            <span className="text-ink-muted">{supportingMetric.label}: </span>
            <span className="font-semibold text-ink">{supportingMetric.value}</span>
            <span className="block text-[10px] text-forest font-medium">{supportingMetric.change}</span>
          </div>
        )}
      </div>
    </Card>
  )
}
