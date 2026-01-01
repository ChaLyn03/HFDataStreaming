import { LoginForm } from '../components/LoginForm';

interface LoginPageProps {
  onLogin: (username: string, password: string) => Promise<void>;
  error?: string | null;
}

export function LoginPage({ onLogin, error }: LoginPageProps) {
  return (
    <div className="grid two">
      <div className="card fade-in">
        <h2>HF Signal Monitoring</h2>
        <p>
          Demo console for simulated HF signal processing. Authenticate with the demo credentials
          to view live alerts and station health.
        </p>
        <p>
          <strong>Default credentials:</strong> demo / demo
        </p>
      </div>
      <LoginForm onLogin={onLogin} error={error} />
    </div>
  );
}
