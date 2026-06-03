import { useState } from "react";

export default function FeedbackPanel({ disabled, saved, onSubmit }) {
  const [correctedFood, setCorrectedFood] = useState("");
  const [correctedCalories, setCorrectedCalories] = useState("");

  async function submitCorrect() {
    await onSubmit({ is_correct: true });
  }

  async function submitCorrection(event) {
    event.preventDefault();
    await onSubmit({
      is_correct: false,
      corrected_food: correctedFood || null,
      corrected_calories: correctedCalories ? Number(correctedCalories) : null,
    });
  }

  return (
    <section className="feedback-panel">
      <div className="section-header">
        <h2>Feedback</h2>
        {saved ? <span className="saved-indicator">Saved</span> : null}
      </div>

      <div className="feedback-actions">
        <button type="button" disabled={disabled} onClick={submitCorrect}>
          Correct
        </button>
      </div>

      <form className="correction-form" onSubmit={submitCorrection}>
        <input
          value={correctedFood}
          disabled={disabled}
          onChange={(event) => setCorrectedFood(event.target.value)}
          placeholder="Correct food"
        />
        <input
          value={correctedCalories}
          disabled={disabled}
          onChange={(event) => setCorrectedCalories(event.target.value)}
          placeholder="Correct calories"
          type="number"
          min="0"
        />
        <button type="submit" disabled={disabled}>
          Mark wrong
        </button>
      </form>
    </section>
  );
}
