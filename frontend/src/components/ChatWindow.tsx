import { useEffect, useMemo, useRef, useState } from "react";
import { createChatSession, getChatMessages, sendMessage } from "../api/chatApi";
import { getFaqItems } from "../api/faqApi";
import type { ChatMessage } from "../types/chat";
import type { FAQItem } from "../types/faq";
import ComplaintForm from "./ComplaintForm";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";

const CHAT_SESSION_KEY = "funko_ai_session_id";
const CHAT_ENDED_KEY = "funko_ai_chat_ended";

export default function ChatWindow() {
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [initializing, setInitializing] = useState(true);
  const [error, setError] = useState("");

  const [faqItems, setFaqItems] = useState<FAQItem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const [menuOpen, setMenuOpen] = useState(false);
  const [chatEnded, setChatEnded] = useState(false);
  const [complaintFormOpen, setComplaintFormOpen] = useState(false);

  const menuRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    async function init() {
      try {
        const faqs = await getFaqItems();
        setFaqItems(faqs);

        const ended = localStorage.getItem(CHAT_ENDED_KEY) === "true";
        setChatEnded(ended);

        const savedSessionId = localStorage.getItem(CHAT_SESSION_KEY);

        if (savedSessionId) {
          const numericSessionId = Number(savedSessionId);

          if (!Number.isNaN(numericSessionId)) {
            setSessionId(numericSessionId);

            const history = await getChatMessages(numericSessionId);
            setMessages(history);

            setInitializing(false);
            return;
          }
        }

        const session = await createChatSession();
        setSessionId(session.id);
        localStorage.setItem(CHAT_SESSION_KEY, String(session.id));
      } catch (err) {
        console.error("Init error:", err);
        setError("Не вдалося ініціалізувати чат.");
      } finally {
        setInitializing(false);
      }
    }

    init();
  }, []);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
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
    return Object.entries(groupedFaq).map(([category, items]) => ({
      category,
      label: items[0]?.category_label || category,
    }));
  }, [groupedFaq]);

  async function handleSend(text: string) {
    if (!sessionId || loading || chatEnded) return;

    setLoading(true);
    setError("");

    try {
      const res = await sendMessage(sessionId, text);

      setMessages((prev) => [
        ...prev,
        res.user_message,
        res.assistant_message,
      ]);

      setSelectedCategory(null);
      setComplaintFormOpen(false);
    } catch (err) {
      console.error("Send message error:", err);
      setError("Не вдалося отримати відповідь від сервера.");
    } finally {
      setLoading(false);
    }
  }

  function resetChatSession() {
    localStorage.removeItem(CHAT_SESSION_KEY);
    localStorage.removeItem(CHAT_ENDED_KEY);
    window.location.reload();
  }

  function endConversation() {
    if (chatEnded) {
      setMenuOpen(false);
      return;
    }

    const farewellMessage: ChatMessage = {
      id: Date.now(),
      session_id: sessionId ?? 0,
      role: "assistant",
      message_text:
        "Дякую за звернення! Якщо знадобиться допомога знову — звертайтесь. Гарного дня 💜",
      detected_intent: "conversation_end",
      metadata_json: null,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, farewellMessage]);
    setChatEnded(true);
    setSelectedCategory(null);
    setComplaintFormOpen(false);
    setMenuOpen(false);
    localStorage.setItem(CHAT_ENDED_KEY, "true");
  }

  function openComplaintForm() {
    const userMessage: ChatMessage = {
      id: Date.now(),
      session_id: sessionId ?? 0,
      role: "user",
      message_text: "Хочу надіслати скаргу",
      detected_intent: "complaint_request",
      metadata_json: null,
      created_at: new Date().toISOString(),
    };
  
    const assistantMessage: ChatMessage = {
      id: Date.now() + 1,
      session_id: sessionId ?? 0,
      role: "assistant",
      message_text:
        "Звісно. Заповніть, будь ласка, форму скарги нижче, і ми передамо її в підтримку.",
      detected_intent: "complaint_form_open",
      metadata_json: null,
      created_at: new Date().toISOString(),
    };
  
    setMessages((prev) => [...prev, userMessage, assistantMessage]);
    setComplaintFormOpen(true);
    setSelectedCategory(null);
  }

  function handleComplaintSuccess() {
    const assistantMessage: ChatMessage = {
      id: Date.now(),
      session_id: sessionId ?? 0,
      role: "assistant",
      message_text:
        "Вашу скаргу отримано. Ми вже працюємо над її розглядом. Чи можу я ще чимось допомогти?",
      detected_intent: "complaint_submitted",
      metadata_json: null,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, assistantMessage]);
    setComplaintFormOpen(false);
    setSelectedCategory(null);
  }

  function renderMenu() {
    if (chatEnded) return null;

    if (selectedCategory) {
      const items = groupedFaq[selectedCategory] || [];

      return (
        <div className="submenu-wrap">
          <div className="submenu-topbar">
            <button
              onClick={() => setSelectedCategory(null)}
              className="quick-action-btn back-btn"
              disabled={loading}
            >
              ← Назад
            </button>
          </div>

          <div className="question-cards">
            {items.map((item) => (
              <button
                key={item.id}
                onClick={() => handleSend(item.question)}
                className="question-card"
                disabled={loading || !sessionId}
              >
                <span className="question-card-icon">✦</span>
                <span className="question-card-text">{item.question}</span>
              </button>
            ))}
          </div>
        </div>
      );
    }

    return (
      <div className="quick-actions">
        {categories.map((item) => (
          <button
            key={item.category}
            onClick={() => setSelectedCategory(item.category)}
            className="quick-action-btn"
            disabled={loading || initializing || complaintFormOpen}
          >
            {item.label}
          </button>
        ))}

        <button
          onClick={openComplaintForm}
          className="quick-action-btn complaint-btn"
          disabled={loading || initializing || complaintFormOpen}
        >
          Скарга
        </button>
      </div>
    );
  }

  return (
    <div className="chat-shell">
      <div className="chat-header">
        <div className="chat-header-title">Funko AI Assistant</div>

        {!chatEnded && (
          <div className="chat-header-menu" ref={menuRef}>
            <button
              className="menu-trigger"
              onClick={() => setMenuOpen((prev) => !prev)}
              aria-label="Відкрити меню"
            >
              ⋮
            </button>

            {menuOpen && (
              <div className="header-dropdown">
                <button className="dropdown-item" onClick={resetChatSession}>
                  Новий чат
                </button>

                <button
                  className="dropdown-item danger"
                  onClick={endConversation}
                >
                  Завершити розмову
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {renderMenu()}

      <div className="chat-body">
        {initializing ? (
          <div className="chat-placeholder">Завантаження історії чату...</div>
        ) : (
          <>
            {messages.length === 0 ? (
              <div className="chat-placeholder">
                Оберіть категорію вище або напишіть своє запитання.
              </div>
            ) : (
              <MessageList messages={messages} />
            )}

            {complaintFormOpen && !chatEnded && (
              <div className="complaint-inline-wrap">
                <ComplaintForm
                  onSuccess={handleComplaintSuccess}
                  onCancel={() => setComplaintFormOpen(false)}
                />
              </div>
            )}
          </>
        )}
      </div>

      {!chatEnded && (
        <div className="chat-footer">
          <MessageInput
            onSend={handleSend}
            disabled={loading || !sessionId || initializing || complaintFormOpen}
          />
          {loading && <p className="chat-status">Асистент думає...</p>}
          {error && <p className="chat-error">{error}</p>}
        </div>
      )}

      {chatEnded && (
        <div className="chat-ended-footer">
          <button className="new-chat-after-end-btn" onClick={resetChatSession}>
            Новий чат
          </button>
        </div>
      )}
    </div>
  );
}