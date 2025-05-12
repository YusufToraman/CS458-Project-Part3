import React, { useState } from "react";
import axios from "axios";
import "../tdd.css";

export default function SurveyBuilder() {
  const [title, setTitle] = useState("");
  const [questions, setQuestions] = useState([]);

  const addQuestion = () => {
    const id = crypto.randomUUID();
    setQuestions([
      ...questions,
      {
        id,
        question_text: "",
        question_type: "text",
        options: [],
        condition_question: null,
        condition_answer: "",
      },
    ]);
  };

  const removeQuestion = (index) => {
    const deletedId = questions[index].id;
    const updated = questions.filter((_, i) => i !== index);

    // Remove any conditionals that reference the deleted question
    const cleaned = updated.map((q) => {
      if (q.condition_question === deletedId) {
        return {
          ...q,
          condition_question: null,
          condition_answer: "",
        };
      }
      return q;
    });

    setQuestions(cleaned);
  };

  const handleQuestionChange = (index, field, value) => {
    const updated = [...questions];
    updated[index][field] = value;
    setQuestions(updated);
  };

  const handleAddOption = (index) => {
    const updated = [...questions];
    updated[index].options.push({ text: "" });
    setQuestions(updated);
  };

  const handleOptionChange = (qIndex, oIndex, value) => {
    const updated = [...questions];
    updated[qIndex].options[oIndex].text = value;
    setQuestions(updated);
  };

  const handleRemoveOption = (qIndex, oIndex) => {
    const updated = [...questions];
    updated[qIndex].options.splice(oIndex, 1);
    setQuestions(updated);
  };

  const handleSubmit = async () => {
    const simplifiedQuestions = questions.map((q) => ({
      number: q.id,
      question_text: q.question_text,
      question_type: q.question_type,
      options: q.options,
      condition_question: q.condition_question,
      condition_answer: q.condition_answer,
    }));

    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/auth/survey-build/`, {
        title,
        questions: simplifiedQuestions,
      });
      alert("Survey created successfully!");
      setTitle("");
      setQuestions([]);
    } catch (error) {
      console.error(error);
      alert("Failed to create survey.");
    }
  };

  return (
    <div className="survey-container">
      <h1 className="page-title">Create a Survey</h1>
      <input
        className="field-gap"
        placeholder="Survey Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      {questions.map((q, idx) => (
        <div key={q.id} className="question-block">
          <div className="tool-item">
            <strong>Q{idx + 1} (ID: {q.id.substring(0, 8)}).</strong>
            <input
              className="field-gap"
              placeholder="Question text"
              value={q.question_text}
              onChange={(e) =>
                handleQuestionChange(idx, "question_text", e.target.value)
              }
            />
            <button onClick={() => removeQuestion(idx)} className="delete-btn">
              ✕
            </button>
          </div>

          <select
            className="field-gap"
            value={q.question_type}
            onChange={(e) =>
              handleQuestionChange(idx, "question_type", e.target.value)
            }
          >
            <option value="text">Text</option>
            <option value="multiple_choice">Multiple Choice</option>
            <option value="dropdown">Dropdown</option>
            <option value="checkbox">Checkbox</option>
            <option value="rating">Rating</option>
          </select>

          {["multiple_choice", "dropdown", "checkbox"].includes(
            q.question_type
          ) && (
            <div className="options-wrapper">
              <strong>Options:</strong>
              {q.options.map((opt, i) => (
                <div key={i} className="tool-item">
                  <input
                    value={opt.text}
                    onChange={(e) =>
                      handleOptionChange(idx, i, e.target.value)
                    }
                    placeholder={`Option ${i + 1}`}
                  />
                  <button
                    onClick={() => handleRemoveOption(idx, i)}
                    className="delete-btn"
                  >
                    ✕
                  </button>
                </div>
              ))}
              <button
                onClick={() => handleAddOption(idx)}
                className="add-option-btn"
              >
                + Add Option
              </button>
            </div>
          )}

          {questions.length > 1 && (
            <div className="field-gap">
              <label>Show only if question:</label>
              <select
                value={q.condition_question || ""}
                onChange={(e) =>
                  handleQuestionChange(
                    idx,
                    "condition_question",
                    e.target.value || null
                  )
                }
              >
                <option value="">None</option>
                {questions
                  .filter((other) => other.id !== q.id)
                  .map((other) => (
                    <option key={other.id} value={other.id}>
                      {`Q${
                        questions.findIndex((qq) => qq.id === other.id) + 1
                      } (ID: ${other.id.substring(0, 8)}): ${
                        other.question_text || "(no text)"
                      }`}
                    </option>
                  ))}
              </select>
              <input
                className="field-gap"
                placeholder="Required answer"
                value={q.condition_answer || ""}
                onChange={(e) =>
                  handleQuestionChange(idx, "condition_answer", e.target.value)
                }
              />
            </div>
          )}
        </div>
      ))}

      <button onClick={addQuestion} className="submit-btn">
        + Add Question
      </button>
      <button onClick={handleSubmit} className="submit-btn">
        Submit Survey
      </button>
    </div>
  );
}
