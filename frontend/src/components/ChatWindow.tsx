import { useEffect, useState } from "react";
import { createChatSession, sendMessage } from "../api/chatApi";
import type { ChatMessage, ChatReplyAction } from "../types/chat";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";

const quickActions = [
  { label: "Доставка", question: "Які у вас умови доставки?" },
  { label: "Оплата", question: "Які у вас варіанти оплати?" },
  { label: "Повернення", question: "У яких випадках можливе повернення замовлення?" },
  { label: "Оригінальність", question: "Ви продаєте оригінальну продукцію?" },
  { label: "Передзамовлення", question: "Які умови передзамовлення?" },
  { label: "Контакти", question: "Як я можу зв'язатись з вами?" },
];

export default function ChatWindow() {
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [actions, setActions] = useState<ChatReplyAction[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function init() {
      const session = await createChatSession();
      setSessionId(session.id);
    }
    init();
  }, []);

  async function handleSend(text: string) {
    if (!sessionId) return;

    setLoading(true);

    const res = await sendMessage(sessionId, text);

    setMessages((prev) => [
      ...prev,
      res.user_message,
      res.assistant_message,
    ]);

    setActions(res.actions || []);
    setLoading(false);
  }

  return (
    <div
      style={{
        maxWidth: 600,
        margin: "40px auto",
        borderRadius: "20px",
        overflow: "hidden",
        boxShadow: "0 20px 60px rgba(0,0,0,0.1)",
        background: "#ffffff",
      }}
    >
      {/* HEADER */}
      <div
        style={{
          padding: "16px",
          background: "#6d28d9", // фіолетовий
          color: "#fff",
          fontWeight: "bold",
        }}
      >
        Funko AI Assistant
      </div>

      {/* QUICK ACTIONS */}
      <div
        style={{
          padding: "10px",
          display: "flex",
          gap: "10px",
          flexWrap: "wrap",
          borderBottom: "1px solid #eee",
        }}
      >
        {quickActions.map((action, i) => (
          <button
            key={i}
            onClick={() => handleSend(action.question)}
            style={{
              padding: "8px 12px",
              borderRadius: "10px",
              border: "none",
              background: "#ede9fe",
              color: "#5b21b6",
              cursor: "pointer",
              fontSize: "13px",
            }}
          >
            {action.label}
          </button>
        ))}
      </div>

      {/* CHAT */}
      <div
        style={{
          height: 400,
          overflowY: "auto",
          background: "#fafafa",
        }}
      >
        <MessageList messages={messages} />
      </div>

      {/* ACTION BUTTONS (з бекенду) */}
      {actions.length > 0 && (
        <div style={{ padding: "10px", display: "flex", gap: "10px", flexWrap: "wrap" }}>
          {actions.map((a, i) => (
            <a
              key={i}
              href={a.url}
              target="_blank"
              style={{
                padding: "8px 12px",
                borderRadius: "10px",
                background: "#ddd6fe",
                color: "#4c1d95",
                textDecoration: "none",
              }}
            >
              {a.label}
            </a>
          ))}
        </div>
      )}

      {/* INPUT */}
      <div style={{ padding: "10px" }}>
        <MessageInput onSend={handleSend} disabled={loading} />
        {loading && (
          <p style={{ fontSize: "12px", color: "#6b7280" }}>
            Асистент думає...
          </p>
        )}
      </div>
    </div>
  );
}