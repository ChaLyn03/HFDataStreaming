import { render, screen } from '@testing-library/react';
import { LoginPage } from '../pages/LoginPage';

it('renders login messaging', () => {
  render(<LoginPage onLogin={async () => {}} />);
  expect(screen.getByText('HF Signal Monitoring')).toBeInTheDocument();
  expect(screen.getByText('Operator Login')).toBeInTheDocument();
});
