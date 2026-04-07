export type ChatRole = "user" | "assistant";

export interface ChatReplyAction {
  type: string;
  label: string;
  url: string;
}

export interface ChatMessageMetadata {
  actions?: ChatReplyAction[];
  [key: string]: unknown;
}

export interface ChatMessage {
  id: number;
  session_id: number;
  role: ChatRole;
  message_text: string;
  detected_intent: string | null;
  metadata_json: ChatMessageMetadata | null;
  created_at: string;
}

export interface ChatReplyResponse {
  session_id: number;
  user_message: ChatMessage;
  assistant_message: ChatMessage;
  matched_faq_id: number | null;
  matched_intent: string;
  actions: ChatReplyAction[];
}