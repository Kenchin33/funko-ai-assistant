import { useEffect, useRef, useState } from "react";
import { createComplaint } from "../api/complaintApi";

interface ComplaintFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}

interface PreviewFile {
  file: File;
  previewUrl: string;
}

const MAX_FILES = 3;

export default function ComplaintForm({
  onSuccess,
  onCancel,
}: ComplaintFormProps) {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [orderNumber, setOrderNumber] = useState("");
  const [message, setMessage] = useState("");
  const [files, setFiles] = useState<PreviewFile[]>([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    return () => {
      files.forEach((item) => URL.revokeObjectURL(item.previewUrl));
    };
  }, [files]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!fullName.trim() || !email.trim() || !message.trim()) {
      setError("Будь ласка, заповніть обов’язкові поля.");
      return;
    }

    if (files.length > MAX_FILES) {
      setError("Можна додати максимум 3 фото.");
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
        files: files.map((item) => item.file),
      });
    
      setError("");
      files.forEach((item) => URL.revokeObjectURL(item.previewUrl));
      setFiles([]);
      setFullName("");
      setEmail("");
      setOrderNumber("");
      setMessage("");
    
      onSuccess();
    } catch (err) {
      console.error("Complaint submit error:", err);
      setError("Не вдалося відправити скаргу. Спробуйте ще раз.");
    } finally {
      setLoading(false);
    }
  }

  function handlePickFile() {
    fileInputRef.current?.click();
  }

  function handleFilesChange(e: React.ChangeEvent<HTMLInputElement>) {
    const selectedFiles = Array.from(e.target.files ?? []);

    if (!selectedFiles.length) return;

    const nextItems = selectedFiles.map((file) => ({
      file,
      previewUrl: URL.createObjectURL(file),
    }));

    const combined = [...files, ...nextItems];

    if (combined.length > MAX_FILES) {
      nextItems.forEach((item) => URL.revokeObjectURL(item.previewUrl));
      setError("Можна додати максимум 3 фото.");
      e.target.value = "";
      return;
    }

    setFiles(combined);
    setError("");
    e.target.value = "";
  }

  function removeFile(index: number) {
    setFiles((prev) => {
      const target = prev[index];
      if (target) {
        URL.revokeObjectURL(target.previewUrl);
      }
      return prev.filter((_, i) => i !== index);
    });
  }

  return (
    <div className="complaint-inline-card">
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

        <div className="complaint-file-row">
          <input
            ref={fileInputRef}
            type="file"
            accept=".jpg,.jpeg,.png,image/jpeg,image/png"
            multiple
            onChange={handleFilesChange}
            className="complaint-file-input-hidden"
          />

          <button
            type="button"
            onClick={handlePickFile}
            className="complaint-pick-file-btn"
          >
            Додати фото
          </button>

          <span className="complaint-file-name">
            {files.length > 0
              ? `Вибрано файлів: ${files.length}/3`
              : "Фото не вибрано"}
          </span>
        </div>

        {files.length > 0 && (
          <div className="complaint-preview-grid">
            {files.map((item, index) => (
              <div key={`${item.file.name}-${index}`} className="complaint-preview-card">
                <img
                  src={item.previewUrl}
                  alt={item.file.name}
                  className="complaint-preview-image"
                />

                <div className="complaint-preview-info">
                  <span className="complaint-preview-name">{item.file.name}</span>
                  <button
                    type="button"
                    className="complaint-file-remove-btn"
                    onClick={() => removeFile(index)}
                  >
                    Видалити
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

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