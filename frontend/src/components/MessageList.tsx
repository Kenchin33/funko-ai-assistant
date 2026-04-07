import { useEffect, useRef } from "react";
import type { ChatMessage } from "../types/chat";

export default function MessageList({ messages }: { messages: ChatMessage[] }) {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="message-list">
      {messages.map((m) => (
        <div
          key={m.id}
          className={`message-row ${m.role === "user" ? "user" : "assistant"}`}
        >
          <div className={`message-bubble ${m.role === "user" ? "user" : "assistant"}`}>
            {m.message_text}
          </div>
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
}