import { useEffect, useState } from "react";

import { createFeedback, createPrediction, getMetrics } from "./api.js";
import FeedbackPanel from "./components/FeedbackPanel.jsx";
import MetricsPanel from "./components/MetricsPanel.jsx";
import PredictionForm from "./components/PredictionForm.jsx";
import PredictionResult from "./components/PredictionResult.jsx";

export default function App() {
  const [prediction, setPrediction] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [feedbackSaved, setFeedbackSaved] = useState(false);
  const [error, setError] = useState("");

  async function refreshMetrics() {
    const nextMetrics = await getMetrics();
    setMetrics(nextMetrics);
  }

  useEffect(() => {
    refreshMetrics().catch(() => {
      setMetrics(null);
    });
  }, []);

  async function handlePredict(text) {
    setLoading(true);
    setError("");
    setFeedbackSaved(false);

    try {
      const result = await createPrediction(text);
      setPrediction(result);
      await refreshMetrics();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleFeedback(payload) {
    if (!prediction) return;

    setError("");
    await createFeedback(prediction.id, payload);
    setFeedbackSaved(true);
    await refreshMetrics();
  }

  return (
    <main className="app-shell">
      <section className="workspace">
        <div className="panel primary-panel">
          <div className="title-row">
            <div>
              <p className="eyebrow">Nutrition AI</p>
              <h1>Estimate meal calories</h1>
            </div>
            <span className="status-pill">Mock provider</span>
          </div>

          <PredictionForm onSubmit={handlePredict} loading={loading} />
          {error ? <p className="error-message">{error}</p> : null}
          <PredictionResult prediction={prediction} />
          <FeedbackPanel
            disabled={!prediction || prediction.status !== "success"}
            saved={feedbackSaved}
            onSubmit={handleFeedback}
          />
        </div>

        <MetricsPanel metrics={metrics} />
      </section>
    </main>
  );
}
