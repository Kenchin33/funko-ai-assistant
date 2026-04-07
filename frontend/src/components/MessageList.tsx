import type { ChatMessage } from "../types/chat";

export default function MessageList({ messages }: { messages: ChatMessage[] }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      {messages.map((m) => (
        <div
          key={m.id}
          style={{
            alignSelf: m.role === "user" ? "flex-end" : "flex-start",
            background: m.role === "user" ? "#2563eb" : "#e5e7eb",
            color: m.role === "user" ? "#fff" : "#000",
            padding: "10px",
            borderRadius: "10px",
            maxWidth: "70%",
          }}
        >
          {m.message_text}
        </div>
      ))}
    </div>
  );
}