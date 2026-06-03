import { useState } from "react";

export default function PredictionForm({ onSubmit, loading }) {
  const [text, setText] = useState("2 eggs and toast");

  function handleSubmit(event) {
    event.preventDefault();
    onSubmit(text);
  }

  return (
    <form className="prediction-form" onSubmit={handleSubmit}>
      <label htmlFor="meal-text">Meal text</label>
      <textarea
        id="meal-text"
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="Describe a meal, such as 2 eggs and toast"
        rows={4}
      />
      <button type="submit" disabled={loading || !text.trim()}>
        {loading ? "Estimating..." : "Estimate calories"}
      </button>
    </form>
  );
}
