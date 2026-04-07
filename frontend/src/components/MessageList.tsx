import { useEffect, useRef } from "react";
import type { ChatMessage } from "../types/chat";

function BotIcon() {
  return (
    <div className="avatar avatar-bot" aria-hidden="true">
      🤖
    </div>
  );
}

function UserIcon() {
  return (
    <div className="avatar avatar-user" aria-hidden="true">
      👤
    </div>
  );
}

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
          {m.role === "assistant" && <BotIcon />}

          <div className={`message-bubble ${m.role === "user" ? "user" : "assistant"}`}>
            {m.message_text}
          </div>

          {m.role === "user" && <UserIcon />}
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
}