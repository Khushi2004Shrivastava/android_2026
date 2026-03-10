import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 20000
});

export const fetchCves = (filters) => {
  console.log("Fetching CVEs with filters:", filters);
  return api.get("/api/cve/", {
    params: {
      keyword: filters.keyword || undefined,
      startDate: filters.startDate || undefined,
      endDate: filters.endDate || undefined,
      minScore: filters.minScore || undefined,
      maxScore: filters.maxScore || undefined,
      vendors: filters.vendor || [],
      severity: filters.severity || []
    }
  });
};
