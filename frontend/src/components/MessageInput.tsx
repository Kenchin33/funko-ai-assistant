import { useState } from "react";

export default function MessageInput({
  onSend,
  disabled,
}: {
  onSend: (text: string) => Promise<void>;
  disabled?: boolean;
}) {
  const [value, setValue] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const trimmed = value.trim();
    if (!trimmed || disabled) return;

    await onSend(trimmed);
    setValue("");
  }

  return (
    <form onSubmit={handleSubmit} className="message-input-form">
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Напишіть повідомлення..."
        className="message-input"
        disabled={disabled}
      />

      <button
        type="submit"
        disabled={disabled}
        className="send-btn"
      >
        →
      </button>
    </form>
  );
}