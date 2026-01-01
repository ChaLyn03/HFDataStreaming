import { Signal } from '../types';

interface SnrChartProps {
  signals: Signal[];
}

function buildPath(values: number[], width: number, height: number) {
  if (values.length === 0) return '';
  const max = Math.max(...values);
  const min = Math.min(...values);
  const range = Math.max(max - min, 1);
  return values
    .map((value, index) => {
      const x = (index / Math.max(values.length - 1, 1)) * width;
      const y = height - ((value - min) / range) * height;
      return `${index === 0 ? 'M' : 'L'}${x.toFixed(1)} ${y.toFixed(1)}`;
    })
    .join(' ');
}

export function SnrChart({ signals }: SnrChartProps) {
  const width = 420;
  const height = 160;
  const values = signals.map((signal) => signal.snr_db).reverse();
  const path = buildPath(values, width, height);

  return (
    <div className="card fade-in">
      <h3>SNR Trend</h3>
      <svg width="100%" viewBox={`0 0 ${width} ${height}`}>
        <rect width={width} height={height} fill="#fff5e9" rx={12} />
        <path d={path} stroke="#e35a1b" strokeWidth="3" fill="none" />
      </svg>
      {signals.length === 0 ? <p>No signal data yet.</p> : null}
    </div>
  );
}
