import React, { useEffect, useState } from "react";
import styles from "./askLeafy.module.css";
import axios from "axios";

const AskLeafy = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [docs, setDocs] = useState("");

  const handleChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleAsk = async () => {
    console.log("Asking Leafy:", question);
    const API_BASE_IP = process.env.REACT_APP_BASE_URL;
    const PORT = process.env.REACT_APP_PORT_URL;
    const apiUrl = `http://${API_BASE_IP}:${PORT}/askTheLlm`;

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
      setDocs(response.data.similar_docs);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  console.log(docs.length > 0 ? JSON.stringify(docs[0].metadata) : "");

  const handleSuggestionOne = () => {
    setQuestion(
      "Show me claims related to tire damage and summarise the coverages"
    );
  };

  const handleSuggestionTwo = () => {
    setQuestion(
      "For adverse weather related claims, what is the average loss amount?"
    );
  };

  return (
    <div className={styles.content}>
      <div className={styles.chat}>
        <h2>Ask Leafy a Question</h2>
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
            <p>Suggested Questions:</p>

            <button className={styles.suggestion} onClick={handleSuggestionOne}>
              Show me claims related to tire damage and summarise the coverages
            </button>
            <button className={styles.suggestion} onClick={handleSuggestionTwo}>
              For adverse weather related claims, what is the average loss
              amount?
            </button>
          </div>
        </div>
        <div>{answer && <p className={styles.answer}>{answer}</p>}</div>
      </div>
      <div className={styles.references}>
        <h2>References</h2>

        {docs.length > 0 && (
          <div>
            {docs.map((doc, index) => (
              <div className={styles.referenceCards} key={index}>
                <div className={styles.imgSection}>
                  <img
                    src={`/photos/${doc.metadata.photo}`}
                    alt="Claim photo"
                  />
                </div>

                <div className={styles.contentSection}>
                  <div className={styles.upperSection}>
                    <div className={styles.fieldWrapper}>
                      <p className={styles.fieldTitle}>Customer ID:</p>
                      <p className={styles.fieldContent}>
                        {doc.metadata.customerID}
                      </p>
                    </div>

                    <div className={styles.fieldWrapper}>
                      <p className={styles.fieldTitle}>Claim Date:</p>
                      <p className={styles.fieldContent}>
                        {doc.metadata.claimFNOLDate}
                      </p>
                    </div>

                    <div className={styles.fieldWrapper}>
                      <p className={styles.fieldTitle}>Loss Amount:</p>
                      <p className={styles.lossAmount}>
                        ${doc.metadata.totalLossAmount}
                      </p>
                    </div>
                  </div>

                  <div className={styles.lowerSection}>
                    <p className={styles.fieldTitle}>Claim Description:</p>
                    <p className={styles.fieldContent}>{doc.page_content}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AskLeafy;
