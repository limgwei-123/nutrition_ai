function formatPercent(value) {
  return `${Math.round(value * 100)}%`;
}

export default function MetricsPanel({ metrics }) {
  const items = [
    ["Total", metrics?.total_predictions ?? 0],
    ["Successful", metrics?.successful_predictions ?? 0],
    ["Failed", metrics?.failed_predictions ?? 0],
    ["Avg latency", `${metrics?.average_latency_ms ?? 0} ms`],
    ["Avg confidence", formatPercent(metrics?.average_confidence ?? 0)],
    ["Feedback", metrics?.feedback_count ?? 0],
    ["Positive feedback", formatPercent(metrics?.positive_feedback_rate ?? 0)],
    ["Avg calorie error", metrics?.average_calorie_error ?? "-"],
  ];

  return (
    <aside className="panel metrics-panel">
      <div className="section-header">
        <h2>Metrics</h2>
      </div>
      <div className="metrics-grid">
        {items.map(([label, value]) => (
          <div className="metric-item" key={label}>
            <span className="label">{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
    </aside>
  );
}
