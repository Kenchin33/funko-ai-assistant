import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  getAdminComplaintById,
  updateAdminComplaintStatus,
  type ComplaintItem,
  type ComplaintStatus,
} from "../api/adminApi";

const ADMIN_UNLOCK_KEY = "funko_admin_unlocked";

const statusLabels: Record<ComplaintStatus, string> = {
  new: "Нова",
  in_progress: "В роботі",
  resolved: "Вирішена",
  rejected: "Відхилена",
};

const allowedTransitions: Record<ComplaintStatus, ComplaintStatus[]> = {
  new: ["in_progress"],
  in_progress: ["resolved", "rejected"],
  resolved: [],
  rejected: [],
};

export default function AdminComplaintDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [complaint, setComplaint] = useState<ComplaintItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [statusLoading, setStatusLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const isUnlocked = localStorage.getItem(ADMIN_UNLOCK_KEY) === "true";

    if (!isUnlocked) {
      navigate("/admin");
      return;
    }

    async function loadComplaint() {
      try {
        if (!id) return;
        const data = await getAdminComplaintById(Number(id));
        setComplaint(data);
      } catch (err) {
        console.error("Failed to load complaint:", err);
        setError("Не вдалося завантажити скаргу.");
      } finally {
        setLoading(false);
      }
    }

    loadComplaint();
  }, [id, navigate]);

  const nextStatuses = useMemo(() => {
    if (!complaint) return [];
    return allowedTransitions[complaint.status];
  }, [complaint]);

  async function handleStatusChange(newStatus: ComplaintStatus) {
    if (!complaint) return;

    setStatusLoading(true);
    setError("");

    try {
      const updated = await updateAdminComplaintStatus(complaint.id, newStatus);
      setComplaint(updated);
    } catch (err) {
      console.error("Failed to update status:", err);
      setError("Не вдалося оновити статус скарги.");
    } finally {
      setStatusLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="admin-page">
        <div className="admin-info-box">Завантаження скарги...</div>
      </div>
    );
  }

  if (error || !complaint) {
    return (
      <div className="admin-page">
        <button className="admin-back-btn" onClick={() => navigate("/admin/complaints")}>
          ← Назад
        </button>
        <div className="admin-error-box">{error || "Скаргу не знайдено."}</div>
      </div>
    );
  }

  return (
    <div className="admin-page">
      <button className="admin-back-btn" onClick={() => navigate("/admin/complaints")}>
        ← Назад до списку
      </button>

      <div className="admin-details-card">
        <div className="admin-details-header">
          <div>
            <h1>Скарга #{complaint.id}</h1>
            <p>Детальна інформація про звернення клієнта</p>
          </div>

          <span className={`status-badge status-${complaint.status}`}>
            {statusLabels[complaint.status]}
          </span>
        </div>

        <div className="admin-details-grid">
          <div>
            <strong>Клієнт:</strong>
            <p>{complaint.full_name}</p>
          </div>

          <div>
            <strong>Email:</strong>
            <p>{complaint.email}</p>
          </div>

          <div>
            <strong>Номер замовлення:</strong>
            <p>{complaint.order_number || "не вказано"}</p>
          </div>

          <div>
            <strong>Створено:</strong>
            <p>{new Date(complaint.created_at).toLocaleString()}</p>
          </div>
        </div>

        <div className="admin-details-section">
          <strong>Текст скарги:</strong>
          <p>{complaint.message}</p>
        </div>

        <div className="admin-details-section">
          <strong>Статус:</strong>
          <div className="admin-status-row">
            {nextStatuses.length > 0 ? (
              <>
                <select
                  defaultValue=""
                  onChange={(e) => {
                    const value = e.target.value as ComplaintStatus;
                    if (value) {
                      handleStatusChange(value);
                    }
                  }}
                  className="admin-status-select"
                  disabled={statusLoading}
                >
                  <option value="" disabled>
                    Оберіть новий статус
                  </option>
                  {nextStatuses.map((status) => (
                    <option key={status} value={status}>
                      {statusLabels[status]}
                    </option>
                  ))}
                </select>

                {statusLoading && <span className="admin-status-saving">Збереження...</span>}
              </>
            ) : (
              <p className="admin-final-status-note">
                Цей статус є фінальним і більше не може бути змінений.
              </p>
            )}
          </div>
        </div>

        <div className="admin-details-section">
          <strong>Вкладення:</strong>

          {complaint.attachments.length === 0 ? (
            <p>Вкладень немає.</p>
          ) : (
            <div className="admin-attachments-list">
              {complaint.attachments.map((attachment) => (
                <a
                  key={attachment.id}
                  href={`http://127.0.0.1:8000/api/complaints/attachments/${attachment.id}`}
                  target="_blank"
                  rel="noreferrer"
                  className="admin-attachment-link"
                >
                  {attachment.file_name}
                </a>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}