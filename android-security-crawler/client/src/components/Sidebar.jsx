import React from "react";

export default function Sidebar({
  filters,
  setFilters,
  onReset,
  onSearch,
  loading
}) {
  const toggleTag = (type, value) => {
    const current = filters[type] || [];

    if (current.includes(value)) {
      setFilters({
        ...filters,
        [type]: current.filter(v => v !== value)
      });
    } else {
      setFilters({
        ...filters,
        [type]: [...current, value]
      });
    }
  };

  const isActive = (type, value) =>
    filters[type]?.includes(value);

  return (
    <div className="filter-panel">

      {/* HEADER */}
      <div className="filter-header">
        <div className="filter-title">
          🔍 Advanced Filters
        </div>

        <div className="filter-actions">
          <button
            className="btn btn-secondary"
            onClick={onReset}
          >
            Reset All
          </button>
        </div>
      </div>

      {/* FILTERS */}
      <div className="filter-grid">

        {/* Date From */}
        <div className="filter-group">
          <label className="filter-label">Published From</label>
          <input
            type="date"
            className="filter-input"
            value={filters.startDate || ""}
            onChange={(e) =>
              setFilters({
                ...filters,
                startDate: e.target.value
              })
            }
          />
        </div>

        {/* Date To */}
        <div className="filter-group">
          <label className="filter-label">Published To</label>
          <input
            type="date"
            className="filter-input"
            value={filters.endDate || ""}
            onChange={(e) =>
              setFilters({
                ...filters,
                endDate: e.target.value
              })
            }
          />
        </div>

        {/* Search */}
        <div className="filter-group">
          <label className="filter-label">
            CVE ID / Android ID
          </label>
          <input
            className="filter-input"
            placeholder="CVE-2024-XXXX"
            value={filters.keyword || ""}
            onChange={(e) =>
              setFilters({
                ...filters,
                keyword: e.target.value
              })
            }
          />
        </div>

        {/* Severity */}
        <div className="filter-group">
          <label className="filter-label">Severity</label>
          <div className="multi-select">
            {["CRITICAL", "HIGH", "MEDIUM", "LOW"].map(sev => (
              <div
                key={sev}
                className={`tag ${
                  isActive("severity", sev)
                    ? "active"
                    : ""
                }`}
                onClick={() =>
                  toggleTag("severity", sev)
                }
              >
                {sev}
              </div>
            ))}
          </div>
        </div>

        {/* Patch Status */}
        <div className="filter-group">
          <label className="filter-label">Patch Status</label>
          <div className="multi-select">
            {["patched", "pending", "unpatched"].map(status => (
              <div
                key={status}
                className={`tag ${
                  isActive("patchStatus", status)
                    ? "active"
                    : ""
                }`}
                onClick={() =>
                  toggleTag("patchStatus", status)
                }
              >
                {status}
              </div>
            ))}
          </div>
        </div>

        {/* Vendor */}
        <div className="filter-group">
          <label className="filter-label">Vendor</label>
          <div className="multi-select">
            {[
              "Samsung",
              "Xiaomi",
              "Qualcomm",
              "MediaTek",
              "Google"
            ].map(v => (
              <div
                key={v}
                className={`tag ${
                  isActive("vendor", v)
                    ? "active"
                    : ""
                }`}
                onClick={() =>
                  toggleTag("vendor", v)
                }
              >
                {v}
              </div>
            ))}
          </div>
        </div>

        {/* CVSS MIN */}
        <div className="filter-group">
          <label className="filter-label">CVSS Min</label>
          <input
            type="number"
            className="filter-input"
            min="0"
            max="10"
            step="0.1"
            value={filters.minScore || ""}
            onChange={(e) =>
              setFilters({
                ...filters,
                minScore: e.target.value
              })
            }
          />
        </div>

        {/* CVSS MAX */}
        <div className="filter-group">
          <label className="filter-label">CVSS Max</label>
          <input
            type="number"
            className="filter-input"
            min="0"
            max="10"
            step="0.1"
            value={filters.maxScore || ""}
            onChange={(e) =>
              setFilters({
                ...filters,
                maxScore: e.target.value
              })
            }
          />
        </div>
      </div>

      <div className="filter-actions mt-6 flex justify-end gap-3">

        <button
          className="btn btn-primary"
          onClick={onSearch}
          disabled={loading}
        >
          {loading ? "Searching..." : "Search CVEs"}
        </button>
      </div>

    </div>
  );
}
