import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAdminComplaints, type ComplaintItem, type ComplaintStatus } from "../api/adminApi";

const ADMIN_UNLOCK_KEY = "funko_admin_unlocked";

const statusTabs: { status: ComplaintStatus; title: string }[] = [
  { status: "new", title: "Нові" },
  { status: "in_progress", title: "В роботі" },
  { status: "resolved", title: "Вирішені" },
  { status: "rejected", title: "Відхилені" },
];

const statusLabels: Record<ComplaintStatus, string> = {
  new: "Нова",
  in_progress: "В роботі",
  resolved: "Вирішена",
  rejected: "Відхилена",
};

export default function AdminComplaintsPage() {
  const [complaints, setComplaints] = useState<ComplaintItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeStatus, setActiveStatus] = useState<ComplaintStatus>("new");

  const navigate = useNavigate();

  useEffect(() => {
    const isUnlocked = localStorage.getItem(ADMIN_UNLOCK_KEY) === "true";

    if (!isUnlocked) {
      navigate("/admin");
      return;
    }

    async function loadComplaints() {
      try {
        const data = await getAdminComplaints();
        setComplaints(data);
      } catch (err) {
        console.error("Failed to load complaints:", err);
        setError("Не вдалося завантажити список скарг.");
      } finally {
        setLoading(false);
      }
    }

    loadComplaints();
  }, [navigate]);

  function handleLogout() {
    localStorage.removeItem(ADMIN_UNLOCK_KEY);
    navigate("/admin");
  }

  const filteredComplaints = useMemo(() => {
    return complaints.filter((complaint) => complaint.status === activeStatus);
  }, [complaints, activeStatus]);

  const counts = useMemo(() => {
    return {
      new: complaints.filter((c) => c.status === "new").length,
      in_progress: complaints.filter((c) => c.status === "in_progress").length,
      resolved: complaints.filter((c) => c.status === "resolved").length,
      rejected: complaints.filter((c) => c.status === "rejected").length,
    };
  }, [complaints]);

  return (
    <div className="admin-page">
      <div className="admin-page-header">
        <div>
          <h1>Скарги клієнтів</h1>
          <p>Тимчасова адмін-панель</p>
        </div>

        <button onClick={handleLogout} className="admin-logout-btn">
          Вийти
        </button>
      </div>

      {loading ? (
        <div className="admin-info-box">Завантаження скарг...</div>
      ) : error ? (
        <div className="admin-error-box">{error}</div>
      ) : complaints.length === 0 ? (
        <div className="admin-info-box">Скарг поки немає.</div>
      ) : (
        <>
          <div className="admin-status-tabs">
            {statusTabs.map((tab) => (
              <button
                key={tab.status}
                className={`admin-status-tab ${
                  activeStatus === tab.status ? "active" : ""
                }`}
                onClick={() => setActiveStatus(tab.status)}
              >
                <span>{tab.title}</span>
                <span className={`status-counter status-${tab.status}`}>
                  {counts[tab.status]}
                </span>
              </button>
            ))}
          </div>

          {filteredComplaints.length === 0 ? (
            <div className="admin-empty-section">
              У категорії “{statusTabs.find((t) => t.status === activeStatus)?.title}” скарг поки немає.
            </div>
          ) : (
            <div className="admin-complaints-list">
              {filteredComplaints.map((complaint) => (
                <button
                  key={complaint.id}
                  className="admin-complaint-card admin-complaint-card-button"
                  onClick={() => navigate(`/admin/complaints/${complaint.id}`)}
                >
                  <div className="admin-complaint-top">
                    <div>
                      <h3>Скарга #{complaint.id}</h3>
                      <p>
                        <strong>Клієнт:</strong> {complaint.full_name}
                      </p>
                      <p>
                        <strong>Email:</strong> {complaint.email}
                      </p>
                      <p>
                        <strong>Замовлення:</strong>{" "}
                        {complaint.order_number || "не вказано"}
                      </p>
                    </div>

                    <span className={`status-badge status-${complaint.status}`}>
                      {statusLabels[complaint.status]}
                    </span>
                  </div>

                  <div className="admin-complaint-body">
                    <p>
                      <strong>Текст скарги:</strong>
                    </p>
                    <p>{complaint.message}</p>
                  </div>

                  <div className="admin-complaint-footer">
                    <p>
                      <strong>Вкладення:</strong> {complaint.attachments.length}
                    </p>
                    <p>
                      <strong>Створено:</strong>{" "}
                      {new Date(complaint.created_at).toLocaleString()}
                    </p>
                  </div>
                </button>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}