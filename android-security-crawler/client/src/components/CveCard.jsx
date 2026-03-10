import React from "react";

function CveCard({ cve }) {
  const getSeverityColor = (score) => {
    if (score >= 9.0) return "bg-red-600";
    if (score >= 7.0) return "bg-orange-500";
    if (score >= 4.0) return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition border-l-4 border-indigo-500">
      <div className="flex justify-between items-start">

        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="text-xl font-bold text-indigo-900">
              {cve.id}
            </h3>

            <span
              className={`${getSeverityColor(
                cve.score
              )} text-white text-xs font-bold px-2 py-1 rounded`}
            >
              {cve.score} {cve.severity}
            </span>
          </div>

          <p className="text-gray-600 text-sm mb-4">
            {cve.description}
          </p>

          <div className="flex gap-4 text-xs text-gray-400 font-mono">
            <span>📅 Pub: {cve.published}</span>
            <span>🔄 Mod: {cve.lastModified}</span>
          </div>
        </div>

        {/* Markdown Report */}
        <a
          href={`http://localhost:8000/api/cve/report/${cve.id}.md`}
          target="_blank"
          rel="noopener noreferrer"
          className="ml-4 flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-indigo-600 hover:text-white transition font-medium text-sm"
        >
          View Report
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
            />
          </svg>
        </a>
      </div>
    </div>
  );
}

export default CveCard;
