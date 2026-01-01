import { StatsSummary } from '../types';

interface StationStatusProps {
  summaries: StatsSummary[];
}

function statusFromSummary(summary: StatsSummary) {
  if (summary.alert_count >= 3) return 'critical';
  if (summary.alert_count >= 1) return 'warning';
  return 'ok';
}

export function StationStatus({ summaries }: StationStatusProps) {
  return (
    <div className="card fade-in">
      <h3>Station Status</h3>
      <div className="grid two">
        {summaries.map((summary) => {
          const status = statusFromSummary(summary);
          return (
            <div key={summary.station_id}>
              <h4>{summary.station_id}</h4>
              <p>
                <span className={`badge ${status}`}>{status.toUpperCase()}</span>
              </p>
              <p>{summary.count} signals</p>
              <p>Avg SNR {summary.avg_snr.toFixed(1)}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
