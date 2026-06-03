export default function PredictionResult({ prediction }) {
  if (!prediction) {
    return (
      <section className="result-panel empty-state">
        <p>No prediction yet.</p>
      </section>
    );
  }

  return (
    <section className="result-panel">
      <div>
        <span className="label">Food</span>
        <strong>{prediction.predicted_food || "No food identified"}</strong>
      </div>
      <div className="result-grid">
        <div>
          <span className="label">Calories</span>
          <strong>{prediction.estimated_calories ?? "-"}</strong>
        </div>
        <div>
          <span className="label">Confidence</span>
          <strong>
            {prediction.confidence === null
              ? "-"
              : `${Math.round(prediction.confidence * 100)}%`}
          </strong>
        </div>
        <div>
          <span className="label">Latency</span>
          <strong>{prediction.latency_ms} ms</strong>
        </div>
        <div>
          <span className="label">Status</span>
          <strong>{prediction.status}</strong>
        </div>
      </div>
    </section>
  );
}
