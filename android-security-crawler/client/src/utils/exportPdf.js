import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export const exportToPdf = (cves) => {
  const doc = new jsPDF("l", "mm", "a4");

  doc.setFontSize(18);
  doc.text("Android CVE Intelligence Report", 14, 18);

  autoTable(doc, {
    startY: 25,
    head: [[
      "CVE ID",
      "Severity",
      "CVSS",
      "Description",
      "Published"
    ]],
    body: cves.map(cve => [
      cve.id,
      cve.severity,
      cve.score,
      cve.description?.slice(0, 80) + "...",
      cve.published
    ])
  });

  doc.save(`android-cve-report-${Date.now()}.pdf`);
};
