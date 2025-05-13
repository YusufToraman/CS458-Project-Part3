import React, { useState } from "react";
import "../styles.css";

const TOOLS = ["ChatGPT", "Bard", "Claude", "Copilot"];

const initialForm = {
  email: "",
  name: "",
  birthdate: "",
  education: "",
  city: "",
  gender: "",
  ai_models: [],
  cons: {},
  use_case: "",
};

const SurveyPage = () => {
  const [formData, setFormData] = useState(initialForm);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const updateField = (e) => {
    const { name, value } = e.target;
    setFormData((d) => ({ ...d, [name]: value }));
  };

  const toggleTool = (e) => {
    const { value, checked } = e.target;
    setFormData((d) => {
      const ai_models = checked
        ? [...d.ai_models, value]
        : d.ai_models.filter((t) => t !== value);

      const cons = { ...d.cons };
      if (!checked) delete cons[value];

      return { ...d, ai_models, cons };
    });
  };

  const updateCons = (tool, text) =>
    setFormData((d) => ({ ...d, cons: { ...d.cons, [tool]: text } }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const res = await fetch(
        `${process.env.REACT_APP_API_URL}/auth/submit-survey/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
        }
      );

      const data = await res.json();
      if (res.ok) {
        setSuccess("Survey submitted successfully!");
        setFormData(initialForm);
      } else setError(data.error || "Survey submission failed.");
    } catch (_err) {
      setError("Something went wrong.");
    }
  };

  return (
    <div className="survey-container">
      <button
        className="back-button"
        onClick={() => (window.location.href = "/dashboard")}
      >
        ⬅ Back to Dashboard
      </button>
      <h1 className="page-title">Survey Page</h1>
      <h2 className="survey-title">AI Survey</h2>

      <form onSubmit={handleSubmit} noValidate>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={updateField}
          required
        />
        <input
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={updateField}
          required
        />
        <input
          name="birthdate"
          placeholder="Birthdate (dd/mm/yyyy)"
          value={formData.birthdate}
          onChange={updateField}
          required
        />
        <input
          name="education"
          placeholder="Education Level"
          value={formData.education}
          onChange={updateField}
          required
        />
        <input
          name="city"
          placeholder="City"
          value={formData.city}
          onChange={updateField}
          required
        />

        <select
          name="gender"
          value={formData.gender}
          onChange={updateField}
          required
            className="field-gap"
        >
          <option value="">Select Gender</option>
          <option>Male</option>
          <option>Female</option>
        </select>
        <div className="ai-tools field-gap">
          <span className="section-label">AI Tools Used</span>

          {TOOLS.map((tool) => (
            <div className="tool-item" key={tool}>
              <input
                type="checkbox"
                value={tool}
                checked={formData.ai_models.includes(tool)}
                onChange={toggleTool}
                id={`tool-${tool}`}
              />
              <label htmlFor={`tool-${tool}`} className="tool-label">
                {tool}
              </label>

              {formData.ai_models.includes(tool) && (
                <textarea
                  className="cons-input"
                  placeholder={`Cons of ${tool} (optional)`}
                  value={formData.cons[tool] || ""}
                  onChange={(e) => updateCons(tool, e.target.value)}
                />
              )}
            </div>
          ))}
        </div>

        <textarea
          name="use_case"
          placeholder="Describe your use case..."
          value={formData.use_case}
          onChange={updateField}
          rows={3}
          required
        />

        {(error || success) && (
        <div
            className={`message-box ${error ? "error-message" : "success-message"}`}
        >
            {error ? (
            <>
                <span className="icon">❌</span> {error}
            </>
            ) : (
            <>
                <span className="icon">✅</span> {success}
            </>
            )}
        </div>
        )}
        <button type="submit" className="submit-btn">
        Send
        </button>

      </form>
      {!!success && <p className="success-message">{success}</p>}
    </div>
  );
};

export default SurveyPage;
