import { useState } from "react";
import { createComplaint } from "../api/complaintApi";

interface ComplaintFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}

export default function ComplaintForm({
  onSuccess,
  onCancel,
}: ComplaintFormProps) {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [orderNumber, setOrderNumber] = useState("");
  const [message, setMessage] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!fullName.trim() || !email.trim() || !message.trim()) {
      setError("Будь ласка, заповніть обов’язкові поля.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      await createComplaint({
        fullName,
        email,
        orderNumber,
        message,
        file,
      });

      onSuccess();
    } catch (err) {
      console.error("Complaint submit error:", err);
      setError("Не вдалося відправити скаргу. Спробуйте ще раз.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="complaint-form-wrap">
      <div className="complaint-form-header">
        <h3>Подати скаргу</h3>
        <p>Заповніть форму нижче, і ми розглянемо ваше звернення.</p>
      </div>

      <form onSubmit={handleSubmit} className="complaint-form">
        <input
          type="text"
          placeholder="Прізвище та ім’я *"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          className="complaint-input"
        />

        <input
          type="email"
          placeholder="Email *"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="complaint-input"
        />

        <input
          type="text"
          placeholder="Номер замовлення"
          value={orderNumber}
          onChange={(e) => setOrderNumber(e.target.value)}
          className="complaint-input"
        />

        <textarea
          placeholder="Опишіть вашу скаргу *"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="complaint-textarea"
          rows={5}
        />

        <input
          type="file"
          accept=".jpg,.jpeg,.png,image/jpeg,image/png"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          className="complaint-file-input"
        />

        {error && <p className="chat-error">{error}</p>}

        <div className="complaint-form-actions">
          <button
            type="button"
            onClick={onCancel}
            className="complaint-cancel-btn"
            disabled={loading}
          >
            Скасувати
          </button>

          <button
            type="submit"
            className="complaint-submit-btn"
            disabled={loading}
          >
            {loading ? "Відправка..." : "Надіслати скаргу"}
          </button>
        </div>
      </form>
    </div>
  );
}