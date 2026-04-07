import { useEffect, useMemo, useState } from "react";
import { createChatSession, sendMessage } from "../api/chatApi";
import { getFaqItems } from "../api/faqApi";
import type { ChatMessage, ChatReplyAction } from "../types/chat";
import type { FAQItem } from "../types/faq";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";

const categoryLabels: Record<string, string> = {
  delivery: "Доставка",
  payment: "Оплата",
  returns: "Повернення",
  originality: "Оригінальність",
  stock: "Наявність",
  preorder: "Передзамовлення",
  manager_contact: "Контакти",
};

export default function ChatWindow() {
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [actions, setActions] = useState<ChatReplyAction[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");

  const [faqItems, setFaqItems] = useState<FAQItem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  useEffect(() => {
    async function init() {
      try {
        const [session, faqs] = await Promise.all([
          createChatSession(),
          getFaqItems(),
        ]);

        setSessionId(session.id);
        setFaqItems(faqs);
      } catch (err) {
        console.error("Init error:", err);
        setError("Не вдалося ініціалізувати чат.");
      }
    }

    init();
  }, []);

  const groupedFaq = useMemo(() => {
    const grouped: Record<string, FAQItem[]> = {};

    for (const item of faqItems) {
      if (!grouped[item.category]) {
        grouped[item.category] = [];
      }
      grouped[item.category].push(item);
    }

    return grouped;
  }, [faqItems]);

  const categories = useMemo(() => {
    return Object.keys(groupedFaq);
  }, [groupedFaq]);

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
      setSelectedCategory(null);
    } catch (err) {
      console.error("Send message error:", err);
      setError("Не вдалося отримати відповідь від сервера.");
    } finally {
      setLoading(false);
    }
  }

  function renderMenu() {
    if (selectedCategory) {
      const items = groupedFaq[selectedCategory] || [];

      return (
        <div className="quick-actions">
          <button
            onClick={() => setSelectedCategory(null)}
            className="quick-action-btn back-btn"
            disabled={loading}
          >
            ← Назад
          </button>

          {items.map((item) => (
            <button
              key={item.id}
              onClick={() => handleSend(item.question)}
              className="quick-action-btn question-btn"
              disabled={loading || !sessionId}
            >
              {item.question}
            </button>
          ))}
        </div>
      );
    }

    return (
      <div className="quick-actions">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
            className="quick-action-btn"
            disabled={loading}
          >
            {categoryLabels[category] || category}
          </button>
        ))}
      </div>
    );
  }

  return (
    <div className="chat-shell">
      <div className="chat-header">Funko AI Assistant</div>

      {renderMenu()}

      <div className="chat-body">
        {messages.length === 0 ? (
          <div className="chat-placeholder">
            Оберіть категорію вище або напишіть своє запитання.
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