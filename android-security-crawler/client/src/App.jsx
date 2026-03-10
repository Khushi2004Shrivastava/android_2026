import { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import CveTable from "./components/CveTable";
import CveModal from "./components/CveModal";
import { fetchCves } from "./api/cveApi";

export default function App() {
  const [filters, setFilters] = useState({
    keyword: "",
    startDate: "",
    endDate: "",
    minScore: "",
    maxScore: "",
    severity: [],
    vendor: [],
    patchStatus: []
  });

  const [cves, setCves] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedCveId, setSelectedCveId] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  useEffect(() => {
    loadCves();
  }, []);

  const loadCves = async () => {
    try {
      setLoading(true);
      setHasSearched(true);

      const res = await fetchCves(filters);
      setCves(res.data);
    } catch (err) {
      console.error("Failed to fetch CVEs:", err);
    } finally {
      setLoading(false);
    }
  };

  const resetFilters = () => {
    setFilters({
      keyword: "",
      startDate: "",
      endDate: "",
      minScore: "",
      maxScore: "",
      severity: [],
      vendor: [],
      patchStatus: []
    });
  };

  const stats = {
    total: cves.length,
    critical: cves.filter(c => c.severity === "CRITICAL").length,
    exploited: cves.filter(c => c.exploited).length
  };

  return (
    <>
      <Navbar stats={stats} />

      <div className="container">

        <Sidebar
          filters={filters}
          setFilters={setFilters}
          onReset={resetFilters}
          onSearch={loadCves}
          loading={loading}
        />

        <div className="dashboard-grid">

          {!hasSearched && (
            <div className="empty-state">
              Apply filters and click <b>Search CVEs</b>
            </div>
          )}

          <CveTable
            loading={loading}
            cves={cves}
            onSelect={(cve) => setSelectedCveId(cve.id)}
          />
        </div>

        <CveModal
          open={!!selectedCveId}
          cveId={selectedCveId}
          onClose={() => setSelectedCveId(null)}
        />

      </div>
    </>
  );
}
