import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAdminComplaints, type ComplaintItem, type ComplaintStatus } from "../api/adminApi";

const ADMIN_UNLOCK_KEY = "funko_admin_unlocked";

const statusSections: { status: ComplaintStatus; title: string }[] = [
  { status: "new", title: "Нові" },
  { status: "in_progress", title: "В роботі" },
  { status: "resolved", title: "Вирішені" },
  { status: "rejected", title: "Відхилені" },
];

export default function AdminComplaintsPage() {
  const [complaints, setComplaints] = useState<ComplaintItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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

  const groupedComplaints = useMemo(() => {
    return statusSections.map((section) => ({
      ...section,
      items: complaints.filter((complaint) => complaint.status === section.status),
    }));
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
        <div className="admin-status-sections">
          {groupedComplaints.map((section) => (
            <section key={section.status} className="admin-status-section">
              <div className="admin-status-section-header">
                <h2>{section.title}</h2>
                <span className={`status-counter status-${section.status}`}>
                  {section.items.length}
                </span>
              </div>

              {section.items.length === 0 ? (
                <div className="admin-empty-section">
                  У цій категорії скарг поки немає.
                </div>
              ) : (
                <div className="admin-complaints-list">
                  {section.items.map((complaint) => (
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
                          {complaint.status}
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
            </section>
          ))}
        </div>
      )}
    </div>
  );
}