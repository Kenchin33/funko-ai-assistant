import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import ChatWindow from "./components/ChatWindow";
import AdminComplaintDetailsPage from "./pages/AdminComplaintDetailsPage";
import AdminComplaintsPage from "./pages/AdminComplaintsPage";
import AdminLoginPage from "./pages/AdminLoginPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ChatWindow />} />
        <Route path="/admin" element={<AdminLoginPage />} />
        <Route path="/admin/complaints" element={<AdminComplaintsPage />} />
        <Route path="/admin/complaints/:id" element={<AdminComplaintDetailsPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}