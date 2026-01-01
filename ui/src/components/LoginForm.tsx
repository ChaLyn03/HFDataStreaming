import { useState } from 'react';

interface LoginFormProps {
  onLogin: (username: string, password: string) => Promise<void>;
  error?: string | null;
}

export function LoginForm({ onLogin, error }: LoginFormProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    try {
      await onLogin(username, password);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="card fade-in" onSubmit={handleSubmit}>
      <h2>Operator Login</h2>
      <label>
        Username
        <input
          className="input"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          placeholder="demo"
        />
      </label>
      <label>
        Password
        <input
          className="input"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="demo"
        />
      </label>
      {error ? <p style={{ color: '#b42318' }}>{error}</p> : null}
      <button className="button" type="submit" disabled={loading}>
        {loading ? 'Signing in...' : 'Login'}
      </button>
    </form>
  );
}
