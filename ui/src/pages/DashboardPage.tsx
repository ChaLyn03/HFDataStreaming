import { useEffect, useMemo, useState } from 'react';
import { apiRequest } from '../api/client';
import { AlertTable } from '../components/AlertTable';
import { SnrChart } from '../components/SnrChart';
import { StationStatus } from '../components/StationStatus';
import { Alert, Signal, StatsSummary } from '../types';

interface DashboardPageProps {
  token: string;
  onLogout: () => void;
}

export function DashboardPage({ token, onLogout }: DashboardPageProps) {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [summaries, setSummaries] = useState<StatsSummary[]>([]);
  const [stationFilter, setStationFilter] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');
  const [loading, setLoading] = useState(false);

  const filteredAlerts = useMemo(() => {
    return alerts.filter((alert) => {
      if (stationFilter && alert.station_id !== stationFilter) return false;
      if (severityFilter && alert.severity !== severityFilter) return false;
      return true;
    });
  }, [alerts, stationFilter, severityFilter]);

  const refresh = async () => {
    setLoading(true);
    try {
      const [alertsResp, signalsResp, statsResp] = await Promise.all([
        apiRequest<Alert[]>('/alerts?limit=20', token),
        apiRequest<Signal[]>('/signals?limit=40', token),
        apiRequest<StatsSummary[]>('/stats/summary', token)
      ]);
      setAlerts(alertsResp);
      setSignals(signalsResp);
      setSummaries(statsResp);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, 15000);
    return () => clearInterval(interval);
  }, []);

  const stations = Array.from(new Set(alerts.map((alert) => alert.station_id)));

  return (
    <div className="grid">
      <div className="header">
        <div>
          <span>HF SIGNAL MONITOR</span>
          <h1>Operational Dashboard</h1>
        </div>
        <div>
          <button className="button secondary" onClick={refresh} disabled={loading}>
            {loading ? 'Refreshing...' : 'Refresh'}
          </button>
          <button className="button" onClick={onLogout} style={{ marginLeft: 10 }}>
            Logout
          </button>
        </div>
      </div>

      <div className="card fade-in">
        <h3>Filters</h3>
        <div className="grid two">
          <label>
            Station
            <select className="input" value={stationFilter} onChange={(e) => setStationFilter(e.target.value)}>
              <option value="">All</option>
              {stations.map((station) => (
                <option key={station} value={station}>
                  {station}
                </option>
              ))}
            </select>
          </label>
          <label>
            Severity
            <select className="input" value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)}>
              <option value="">All</option>
              <option value="warning">Warning</option>
              <option value="critical">Critical</option>
            </select>
          </label>
        </div>
      </div>

      <div className="grid two">
        <AlertTable alerts={filteredAlerts} />
        <SnrChart signals={signals} />
      </div>

      <StationStatus summaries={summaries} />
    </div>
  );
}
