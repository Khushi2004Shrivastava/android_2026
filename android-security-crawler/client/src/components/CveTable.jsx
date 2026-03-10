export default function CveTable({ cves, loading, onSelect }) {
  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
        Loading CVEs...
      </div>
    );
  }

  return (
    <div className="cve-table-container">
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>CVE ID</th>
              <th>Severity</th>
              <th>CVSS</th>
              <th>Published</th>
              <th>Last Modified</th>
              <th>Report</th>
            </tr>
          </thead>

          <tbody>
            {cves.map((cve) => (
              <tr
                key={cve.id}
                className="cve-row"
                style={{ cursor: "pointer" }}
                onClick={() => onSelect(cve)}
              >
                <td className="cve-id">{cve.id}</td>
                <td>{cve.severity}</td>
                <td>{cve.score}</td>
                <td>{cve.published || "-"}</td>
                <td>{cve.lastModified || "-"}</td>
                <td
                  onClick={(e) => e.stopPropagation()}
                >
                  <button
                    className="view-report-btn"
                    onClick={() =>
                      window.open(
                        `http://localhost:8000/api/cve/report/${cve.id}.md`,
                        "_blank"
                      )
                    }
                  >
                    View Report
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
