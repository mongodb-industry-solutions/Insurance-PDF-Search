import React, { useState } from "react";
import styles from "./askLeafy.module.css";
import axios from "axios";

const AskLeafy = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleAsk = async () => {
    console.log("Asking Leafy:", question);
    const apiUrl = "http://127.0.0.1:8000/testTheLlm";

    try {
      const response = await axios.post(
        apiUrl,
        { question },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      console.log("Answer:", response.data);
      setAnswer(response.data.result);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleLoremIpsum = () => {
    setQuestion(
      "Find accidents caused by adverse weather. Tell me the average repair time for this claim based on similar claims."
    );
  };

  return (
    <div className={styles.content}>
      <div className={styles.chat}>
        <h2>Ask Leafy a question</h2>
        <div className={styles.question}>
          <input
            className={styles.input}
            type="text"
            value={question}
            onChange={handleChange}
            placeholder="Type your question here..."
          />
          <button className={styles.askBtn} onClick={handleAsk}>
            Ask
          </button>
          <div className={styles.suggestedQuestions}>
            <button className={styles.suggestion} onClick={handleLoremIpsum}>
              Find accidents caused by adverse weather. Tell me the average
              repair time for this claim based on similar claims.
            </button>
          </div>
        </div>
        <div className={styles.answer}>{answer && <p>{answer}</p>}</div>
      </div>
      <div className={styles.references}>
        <h2>References</h2>
      </div>
    </div>
  );
};

export default AskLeafy;
