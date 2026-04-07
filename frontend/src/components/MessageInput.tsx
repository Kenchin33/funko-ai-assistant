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
    if (!value.trim() || disabled) return;

    await onSend(value);
    setValue("");
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", gap: 10 }}>
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Напишіть повідомлення..."
        disabled={disabled}
        style={{ flex: 1, padding: 10 }}
      />
      <button type="submit" disabled={disabled}>
        Send
      </button>
    </form>
  );
}