const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Request failed");
  }

  return response.json();
}

export function createPrediction(text) {
  return request("/predictions", {
    method: "POST",
    body: JSON.stringify({ text }),
  });
}

export function createFeedback(predictionId, payload) {
  return request(`/predictions/${predictionId}/feedback`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getMetrics() {
  return request("/metrics");
}
