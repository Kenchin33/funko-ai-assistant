import { useEffect, useRef } from "react";
import type { ChatMessage } from "../types/chat";

export default function MessageList({ messages }: { messages: ChatMessage[] }) {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "12px",
        padding: "10px",
      }}
    >
      {messages.map((m) => (
        <div
          key={m.id}
          style={{
            display: "flex",
            justifyContent: m.role === "user" ? "flex-end" : "flex-start",
          }}
        >
          <div
            style={{
              background: m.role === "user" ? "#2563eb" : "#ffffff",
              color: m.role === "user" ? "#ffffff" : "#111827",
              padding: "12px 16px",
              borderRadius: "16px",
              maxWidth: "70%",
              boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
              whiteSpace: "pre-wrap",
            }}
          >
            {m.message_text}
          </div>
        </div>
      ))}

      <div ref={bottomRef} />
    </div>
  );
}