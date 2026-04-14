import axios from "axios";

export type ComplaintStatus = "new" | "in_progress" | "resolved" | "rejected";

export interface ComplaintAttachment {
  id: number;
  file_name: string;
  mime_type: string;
  file_size: number;
  uploaded_at: string;
}

export interface ComplaintItem {
  id: number;
  full_name: string;
  email: string;
  order_number: string | null;
  message: string;
  status: ComplaintStatus;
  created_at: string;
  attachments: ComplaintAttachment[];
}

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export async function getAdminComplaints(): Promise<ComplaintItem[]> {
  const response = await api.get<ComplaintItem[]>("/admin/complaints");
  return response.data;
}

export async function getAdminComplaintById(id: number): Promise<ComplaintItem> {
  const response = await api.get<ComplaintItem>(`/admin/complaints/${id}`);
  return response.data;
}

export async function updateAdminComplaintStatus(
  id: number,
  status: ComplaintStatus
): Promise<ComplaintItem> {
  const response = await api.patch<ComplaintItem>(`/admin/complaints/${id}/status`, {
    status,
  });
  return response.data;
}