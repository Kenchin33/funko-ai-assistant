import { useEffect, useRef } from "react";
import type { ChatMessage, ChatReplyAction } from "../types/chat";

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

function MessageActions({ actions }: { actions: ChatReplyAction[] }) {
  if (!actions.length) return null;

  function handleActionClick(action: ChatReplyAction) {
  
    if (action.url.startsWith("/")) {
      console.log("ASSISTANT ACTION URL:", action.url);
      window.parent.postMessage(
        {
          type: "FUNKO_ASSISTANT_NAVIGATE",
          url: action.url,
        },
        "*"
      );
      return;
    }
  
    window.open(action.url, "_blank", "noopener,noreferrer");
  }

  return (
    <div className="message-actions">
      {actions.map((action, index) => (
        <button
          key={`${action.label}-${index}`}
          type="button"
          onClick={() => handleActionClick(action)}
          className="message-action-link"
        >
          {action.label}
        </button>
      ))}
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
      {messages.map((m) => {
        const actions =
          m.role === "assistant" && Array.isArray(m.metadata_json?.actions)
            ? (m.metadata_json?.actions as ChatReplyAction[])
            : [];

        return (
          <div
            key={m.id}
            className={`message-row ${m.role === "user" ? "user" : "assistant"}`}
          >
            {m.role === "assistant" && <BotIcon />}

            <div className="message-content">
              <div className={`message-bubble ${m.role === "user" ? "user" : "assistant"}`}>
                {m.message_text}
              </div>

              {m.role === "assistant" && <MessageActions actions={actions} />}
            </div>

            {m.role === "user" && <UserIcon />}
          </div>
        );
      })}
      <div ref={bottomRef} />
    </div>
  );
}