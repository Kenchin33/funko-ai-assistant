import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export interface ComplaintPayload {
  fullName: string;
  email: string;
  orderNumber?: string;
  message: string;
  file?: File | null;
}

export async function createComplaint(payload: ComplaintPayload) {
  const formData = new FormData();

  formData.append("full_name", payload.fullName);
  formData.append("email", payload.email);
  formData.append("message", payload.message);

  if (payload.orderNumber) {
    formData.append("order_number", payload.orderNumber);
  }

  if (payload.file) {
    formData.append("file", payload.file);
  }

  const response = await api.post("/complaints", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}