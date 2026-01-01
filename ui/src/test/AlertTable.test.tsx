import { render, screen } from '@testing-library/react';
import { AlertTable } from '../components/AlertTable';

const alerts = [
  {
    id: '1',
    signal_id: 's1',
    station_id: 'STATION-001',
    severity: 'warning',
    alert_type: 'LOW_SNR',
    message: 'SNR low',
    created_at: new Date().toISOString()
  }
];

it('renders alert rows', () => {
  render(<AlertTable alerts={alerts} />);
  expect(screen.getByText('STATION-001')).toBeInTheDocument();
  expect(screen.getByText('LOW_SNR')).toBeInTheDocument();
});
