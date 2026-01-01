import { useState } from 'react';
import { apiRequest } from './api/client';
import { DashboardPage } from './pages/DashboardPage';
import { LoginPage } from './pages/LoginPage';
import './styles/main.css';

interface TokenResponse {
  access_token: string;
}

export function App() {
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (username: string, password: string) => {
    setError(null);
    try {
      const response = await apiRequest<TokenResponse>('/auth/login', undefined, {
        method: 'POST',
        body: JSON.stringify({ username, password })
      });
      setToken(response.access_token);
    } catch (err) {
      setError('Invalid credentials.');
    }
  };

  const handleLogout = () => setToken(null);

  return (
    <main>
      <div className="app-shell">
        {token ? (
          <DashboardPage token={token} onLogout={handleLogout} />
        ) : (
          <LoginPage onLogin={handleLogin} error={error} />
        )}
      </div>
    </main>
  );
}
