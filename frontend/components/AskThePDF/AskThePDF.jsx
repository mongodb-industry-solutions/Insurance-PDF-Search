"use client";

import { useState } from "react";
import styles from "./askThePDF.module.css";

const AskThePDF = () => {
  const industry = "insurance";
  const demo_name = "pdf_search";
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [docs, setDocs] = useState([]);
  const [customerSelected, setCustomerSelected] = useState(false); // Track if a customer is selected
  const [selectedCustomer, setSelectedCustomer] = useState(null); // Track selected customer object
  const [loading, setLoading] = useState(false);

  // Customer objects for Ryan and Peter -> to be modified when we have the collection
  const ryan = {
    photo: "/eddie.png",
    name: "Ryan Tan",
    Country: "Singapore, SG",
    guidelines: "guidlines_risk_management_singapore.pdf",
  };

  const peter = {
    photo: "/rob.png",
    name: "Peter Green",
    Country: "New York, USA",
    guidelines: "guidlines_insurance_ny.pdf",
  };

  const handleRyanClick = () => {
    console.log("Ryan");
    setCustomerSelected(true);
    setSelectedCustomer(ryan);
  };

  const handlePeterClick = () => {
    console.log("Peter");
    setCustomerSelected(true);
    setSelectedCustomer(peter);
  };

  ////

  const handleChange = (event) => {
    setQuery(event.target.value);
  };

  const handleAsk = async () => {
    if (!selectedCustomer) return;

    setLoading(true); // Start loading
    const guidelines = selectedCustomer.guidelines;

    console.log("Industry:", industry);
    console.log("Demo name:", demo_name);
    console.log("Asking Your PDF:", query);
    console.log("Using the file:", guidelines);
    try {
      const response = await fetch("/api/querythepdf", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ industry, demo_name, query, guidelines }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Answer:", data);
      setAnswer(data.answer);
      setDocs(data.supporting_docs);
    } catch (error) {
      console.error("Error:", error);
      setAnswer("Sorry, there was an error processing your request. Please try again.");
      setDocs([]);
    } finally {
      setLoading(false); // Reset loading state
    }
  };

  const handleSuggestionOne = () => {
    setQuery("What forms are required for a certificate of insurance?");
  };

  const handleSuggestionTwo = () => {
    setQuery(
      "What are risk control measures associated with claim handling and case reserving?"
    );
  };

  return (
    <div className={styles.content}>
      <div className={styles.chat}>
        <div className={styles.selectCustomerSection}>
          <p className={styles.selectText}>Select a Customer</p>
          <div>
            <button className={styles.customerBtn} onClick={handleRyanClick}>
              <div className={styles.customerContent}>
                <img
                  src="/eddie.png"
                  alt="Ryan"
                  className={styles.customerImage}
                />
                <div>
                  <strong>Ryan Tan</strong>
                  <br />
                  Singapore, SG
                </div>
              </div>
            </button>

            <button className={styles.customerBtn} onClick={handlePeterClick}>
              <div className={styles.customerContent}>
                <img
                  src="/rob.png"
                  alt="Peter"
                  className={styles.customerImage}
                />
                <div>
                  <strong>Peter Green</strong>
                  <br />
                  New York, USA
                </div>
              </div>
            </button>
          </div>
        </div>

        {customerSelected && ( // Render askSection only if a customer is selected
          <div className={styles.askSection}>
            <h2>Ask the PDF</h2>
            <div className={styles.question}>
              <input
                className={styles.input}
                type="text"
                value={query}
                onChange={handleChange}
                placeholder="Type your question here..."
              />
              <button
                className={styles.askBtn}
                onClick={handleAsk}
                disabled={loading} // Disable button while loading
              >
                {loading ? <div className={styles.spinner}></div> : "Ask"}
              </button>

              <div className={styles.suggestedQuestions}>
                <p>Suggested Questions:</p>

                <button
                  className={styles.suggestion}
                  onClick={handleSuggestionOne}
                >
                  What forms are required for a certificate of insurance?
                </button>
                <button
                  className={styles.suggestion}
                  onClick={handleSuggestionTwo}
                >
                  What are risk control measures associated with claim handling and case reserving?
                </button>
              </div>
            </div>
            <div>{answer && <p className={styles.answer}>{answer}</p>}</div>
          </div>
        )}
      </div>

      <div className={styles.references}>
        <h2>Reference documents</h2>

        {customerSelected && ( // Render customerInfo only if a customer is selected
          <div className={styles.customerInfo}>
            <div className={styles.customerPhoto}>
              <img
                src={selectedCustomer.photo}
                alt="Customer Photo"
                className={styles.customerPhoto}
              />
            </div>

            <div className={styles.upperSection}>
              <div className={styles.fieldWrapper}>
                <p className={styles.fieldTitle}>Name:</p>
                <p className={styles.fieldContent}>{selectedCustomer.name}</p>
              </div>
              <div className={styles.fieldWrapper}>
                <p className={styles.fieldTitle}>Location:</p>
                <p className={styles.fieldContent}>
                  {selectedCustomer.Country}
                </p>
              </div>
              <div className={styles.fieldWrapper}>
                <p className={styles.fieldTitle}>Documents:</p>
                <p className={styles.fieldContent}>
                  {selectedCustomer.guidelines.slice(0, 20) + "..."}
                </p>
              </div>
            </div>
          </div>
        )}

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
