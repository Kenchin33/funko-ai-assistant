import { useState } from "react";
import { checkOrder } from "../api/orderCheckApi";

interface Props {
  onSuccess: (message: string) => void;
  onCancel: () => void;
}

export default function OrderCheckForm({ onSuccess, onCancel }: Props) {
  const [orderNumber, setOrderNumber] = useState("");
  const [email, setEmail] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!orderNumber.trim() || !email.trim()) {
      setError("Заповніть всі поля");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const res = await checkOrder({
        orderNumber,
        email,
      });

      onSuccess(res.message);
    } catch (err) {
      console.error(err);
      setError("Помилка перевірки замовлення");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="complaint-inline-card">
      <div className="complaint-form-header">
        <h3>Перевірити замовлення</h3>
        <p>Введіть номер замовлення та email</p>
      </div>

      <form onSubmit={handleSubmit} className="complaint-form">
        <input
          type="text"
          placeholder="Номер замовлення *"
          value={orderNumber}
          onChange={(e) => setOrderNumber(e.target.value)}
          className="complaint-input"
        />

        <input
          type="email"
          placeholder="Email *"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="complaint-input"
        />

        {error && <p className="chat-error">{error}</p>}

        <div className="complaint-form-actions">
          <button type="button" onClick={onCancel} className="complaint-cancel-btn">
            Скасувати
          </button>

          <button type="submit" className="complaint-submit-btn" disabled={loading}>
            {loading ? "Перевірка..." : "Перевірити"}
          </button>
        </div>
      </form>
    </div>
  );
}