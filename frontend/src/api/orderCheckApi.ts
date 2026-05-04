import axios from "axios";
import type { ChatMessage } from "../types/chat";

const api = axios.create({
  baseURL: "http://127.0.0.1:8001/api",
});

export interface OrderCheckPayload {
  sessionId: number;
  orderNumber: string;
  email: string;
}

export interface OrderCheckResponse {
  found: boolean;
  message: string;
  user_message: ChatMessage;
  assistant_message: ChatMessage;
  order?: {
    order_number: string;
    email: string;
    status: string;
    total_amount: string;
    created_at: string;
    tracking_number: string | null;
    order_url: string;
  };
}

export async function checkOrder(
  payload: OrderCheckPayload
): Promise<OrderCheckResponse> {
  const response = await api.post<OrderCheckResponse>("/orders/check", {
    session_id: payload.sessionId,
    order_number: payload.orderNumber,
    email: payload.email,
  });

  return response.data;
}