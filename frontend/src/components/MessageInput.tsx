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
    if (!value.trim()) return;

    await onSend(value);
    setValue("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        display: "flex",
        gap: "10px",
        marginTop: "10px",
      }}
    >
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Напишіть повідомлення..."
        style={{
          flex: 1,
          padding: "12px",
          borderRadius: "12px",
          border: "1px solid #ddd",
          fontSize: "14px",
        }}
      />

    <button
        type="submit"
        disabled={disabled}
        style={{
            padding: "12px 16px",
            borderRadius: "12px",
            border: "none",
            background: "#6d28d9",
            color: "#fff",
            cursor: "pointer",
        }}
    >
        →
    </button>
    </form>
  );
}