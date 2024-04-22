import React, { useEffect, useState } from "react";
import styles from "../AskThePDF/askThePDF.module.css";
import axios from "axios";

const AskThePDF = () => {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [docs, setDocs] = useState("");

  const handleChange = (event) => {
    setQuery(event.target.value);
  };

  const handleAsk = async () => {
    console.log("Asking Your PDF:", query);
    const apiUrl = "http://127.0.0.1:8000/querythepdf";

    try {
      const response = await axios.post(
        apiUrl,
        { query },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      console.log("Answer:", response.data);
      setAnswer(response.data.answer);
      setDocs(response.data.supporting_docs);

    } catch (error) {
      console.error("Error:", error);
    }
  };

  console.log((docs.length > 0 ? JSON.stringify(docs[0].metadata) : ""));



  const handleSuggestionOne = () => {
    setQuery(
      "What is a certificate of Insurance?"
    );
  };

  const handleSuggestionTwo = () => {
    setQuery(
      "For adverse weather related claims, what is the average loss amount?"
    );
  };



  return (
    <div className={styles.content}>
      <div className={styles.chat}>
        <h2>Chat with your Documents</h2>
        <div className={styles.question}>
          <input
            className={styles.input}
            type="text"
            value={query}
            onChange={handleChange}
            placeholder="Type your question here..."
          />
          <button className={styles.askBtn} onClick={handleAsk}>
            Ask
          </button>
          <div className={styles.suggestedQuestions}>
            <p>Suggested Questions:</p>

            <button className={styles.suggestion} onClick={handleSuggestionOne}>
                What is a certificate of Insurance?
            </button>
            <button className={styles.suggestion} onClick={handleSuggestionTwo}>
              For adverse weather related claims, what is the average loss amount?
            </button>
          </div>
        </div>
        <div >{answer && <p className={styles.answer}>{answer}</p>}</div>
      </div>
      <div className={styles.references}>
        <h2>Supporting Documentation</h2>

        {docs.length > 0 && (
          <div>
            {docs.map((doc, index) => (
              <div className={styles.referenceCards} key={index}>

                <div className={styles.imgSection}>

                  {/* <img src={doc.image} alt="Supporting image"/> */}
                  <img src={`data:image/png;base64,${doc.image}`} alt="Image" />

                </div>


              </div>
            ))}


          </div>
        )}
      </div>
    </div>
  );
};

export default AskThePDF;
