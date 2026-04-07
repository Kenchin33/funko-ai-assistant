import axios from "axios";
import type { ChatReplyResponse } from "../types/chat";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export async function createChatSession() {
  const res = await api.post("/chat/sessions", {
    user_name: null,
    user_email: null,
    source: "web_app",
  });

  return res.data;
}

export async function sendMessage(
  sessionId: number,
  messageText: string
): Promise<ChatReplyResponse> {
  const res = await api.post(
    `/chat/sessions/${sessionId}/reply`,
    {
      message_text: messageText,
    }
  );

  return res.data;
}