import { useEffect, useState } from "react";
import axios from "axios";

export default function CveModal({ open, cveId, onClose }) {
  const [cve, setCve] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!open || !cveId) return;

    setLoading(true);
    setError(null);
    setCve(null);

    axios
      .get(`http://localhost:8000/cve/${cveId}`)
      .then(res => {
        setCve(res.data.data);
      })
      .catch(() => {
        setError("Failed to load CVE details");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [open, cveId]);

  if (!open) return null;

  return (
    <div className="modal active" onClick={onClose}>
      <div
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-close" onClick={onClose}>
          ×
        </div>

        {loading && (
          <div className="modal-loading">
            Loading CVE details...
          </div>
        )}

        {error && (
          <div className="modal-error">
            {error}
          </div>
        )}

        {cve && (
          <>
            <h2 className="modal-title">{cve.id}</h2>

            <div className="modal-grid">

              <div>
                <strong>Published:</strong>{" "}
                {cve.published}
              </div>

              <div>
                <strong>Last Modified:</strong>{" "}
                {cve.last_modified}
              </div>

              <div>
                <strong>Description:</strong>
                <p style={{ marginTop: "6px" }}>
                  {
                    cve.cve_raw?.descriptions?.[0]
                      ?.value
                  }
                </p>
              </div>

            </div>
          </>
        )}
      </div>
    </div>
  );
}
