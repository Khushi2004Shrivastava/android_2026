import ThemeToggle from "./ThemeToggle";

export default function Navbar({ stats }) {
  return (
    <header className="header">
      <div className="header-content">

        <div className="logo-section">
          <h1>Android CVE Intelligence Dashboard</h1>
        </div>

        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <ThemeToggle />
        </div>

        <div className="header-stats">
          <div className="stat">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Total CVEs</div>
          </div>

          <div className="stat">
            <div className="stat-value">{stats.critical}</div>
            <div className="stat-label">Critical</div>
          </div>

          <div className="stat">
            <div className="stat-value">{stats.exploited}</div>
            <div className="stat-label">Exploited</div>
          </div>
        </div>

      </div>
    </header>
  );
}
