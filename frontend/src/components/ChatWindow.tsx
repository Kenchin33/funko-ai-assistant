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
  const [error, setError] = useState<string>("");

  useEffect(() => {
    async function init() {
      try {
        const session = await createChatSession();
        setSessionId(session.id);
      } catch (err) {
        console.error("Session init error:", err);
        setError("Не вдалося створити чат-сесію.");
      }
    }

    init();
  }, []);

  async function handleSend(text: string) {
    if (!sessionId || loading) return;

    setLoading(true);
    setError("");

    try {
      const res = await sendMessage(sessionId, text);

      setMessages((prev) => [
        ...prev,
        res.user_message,
        res.assistant_message,
      ]);

      setActions(res.actions || []);
    } catch (err) {
      console.error("Send message error:", err);
      setError("Не вдалося отримати відповідь від сервера.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat-shell">
      <div className="chat-header">Funko AI Assistant</div>

      <div className="quick-actions">
        {quickActions.map((action, i) => (
          <button
            key={i}
            onClick={() => handleSend(action.question)}
            className="quick-action-btn"
            disabled={loading || !sessionId}
          >
            {action.label}
          </button>
        ))}
      </div>

      <div className="chat-body">
        {messages.length === 0 ? (
          <div className="chat-placeholder">
            Поставте запитання або оберіть одну з категорій вище.
          </div>
        ) : (
          <MessageList messages={messages} />
        )}
      </div>

      {actions.length > 0 && (
        <div className="backend-actions">
          {actions.map((a, i) => (
            <a
              key={i}
              href={a.url}
              target="_blank"
              rel="noreferrer"
              className="backend-action-link"
            >
              {a.label}
            </a>
          ))}
        </div>
      )}

      <div className="chat-footer">
        <MessageInput onSend={handleSend} disabled={loading || !sessionId} />
        {loading && <p className="chat-status">Асистент думає...</p>}
        {error && <p className="chat-error">{error}</p>}
      </div>
    </div>
  );
}