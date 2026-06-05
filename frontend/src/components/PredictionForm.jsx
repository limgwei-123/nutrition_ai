import { useState } from "react";

export default function PredictionForm({ onSubmit, loading }) {
  const [text, setText] = useState("egg");

  function handleSubmit(event) {
    event.preventDefault();
    onSubmit(text);
  }

  return (
    <form className="prediction-form" onSubmit={handleSubmit}>
      <label htmlFor="meal-text">Meal text(Only one)</label>
      <textarea
        id="meal-text"
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="Describe a meal,such as toast(current system only one food is allow)"
        rows={1}
      />
      <button type="submit" disabled={loading || !text.trim()}>
        {loading ? "Estimating..." : "Estimate calories"}
      </button>
    </form>
  );
}
