import { useEffect, useState } from "react";
import { createChatSession, sendMessage } from "../api/chatApi";
import type { ChatMessage, ChatReplyAction } from "../types/chat";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";

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
    <div style={{ maxWidth: 600, margin: "40px auto" }}>
      <h2>Funko AI Assistant</h2>

      <div style={{ minHeight: 300, marginBottom: 20 }}>
        <MessageList messages={messages} />
      </div>

      {actions.length > 0 && (
        <div style={{ marginBottom: 10 }}>
          {actions.map((a, i) => (
            <a key={i} href={a.url} target="_blank">
              {a.label}
            </a>
          ))}
        </div>
      )}

      <MessageInput onSend={handleSend} disabled={loading} />
    </div>
  );
}