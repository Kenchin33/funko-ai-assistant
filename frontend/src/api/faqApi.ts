import axios from "axios";
import type { FAQItem } from "../types/faq";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export async function getFaqItems(): Promise<FAQItem[]> {
  const response = await api.get<FAQItem[]>("/faq");
  return response.data;
}