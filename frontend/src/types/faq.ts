export interface FAQItem {
  id: number;
  category: string;
  category_label: string;
  question: string;
  answer: string;
  keywords: string | null;
  button_label: string | null;
  button_url: string | null;
  priority: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}