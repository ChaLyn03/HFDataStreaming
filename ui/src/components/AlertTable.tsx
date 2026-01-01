import { Alert } from '../types';

interface AlertTableProps {
  alerts: Alert[];
}

export function AlertTable({ alerts }: AlertTableProps) {
  return (
    <div className="card fade-in">
      <h3>Latest Alerts</h3>
      <table className="table">
        <thead>
          <tr>
            <th>Station</th>
            <th>Type</th>
            <th>Severity</th>
            <th>Message</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((alert) => (
            <tr key={alert.id}>
              <td>{alert.station_id}</td>
              <td>{alert.alert_type}</td>
              <td>
                <span className={`badge ${alert.severity}`}>
                  {alert.severity.toUpperCase()}
                </span>
              </td>
              <td>{alert.message}</td>
              <td>{new Date(alert.created_at).toLocaleTimeString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {alerts.length === 0 ? <p>No alerts yet.</p> : null}
    </div>
  );
}
