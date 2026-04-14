import { useState } from "react";
import { useNavigate } from "react-router-dom";

const ADMIN_UNLOCK_KEY = "funko_admin_unlocked";
const DEMO_ADMIN_PASSWORD = "admin123";

export default function AdminLoginPage() {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  function handleLogin(e: React.FormEvent) {
    e.preventDefault();

    if (password === DEMO_ADMIN_PASSWORD) {
      localStorage.setItem(ADMIN_UNLOCK_KEY, "true");
      navigate("/admin/complaints");
      return;
    }

    setError("Невірний пароль адміністратора.");
  }

  return (
    <div className="admin-login-page">
      <div className="admin-login-card">
        <h1>Адмінка Funko</h1>
        <p>Тимчасовий вхід для адміністратора</p>

        <form onSubmit={handleLogin} className="admin-login-form">
          <input
            type="password"
            placeholder="Введіть пароль адміністратора"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="admin-login-input"
          />

          {error && <p className="admin-login-error">{error}</p>}

          <button type="submit" className="admin-login-btn">
            Увійти
          </button>
        </form>
      </div>
    </div>
  );
}