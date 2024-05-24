import React, { useEffect, useState } from "react";
import styles from "../AskThePDF/askThePDF.module.css";
import axios from "axios";

const AskThePDF = () => {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [docs, setDocs] = useState([]);
  const [customerSelected, setCustomerSelected] = useState(false); // Track if a customer is selected
  const [selectedCustomer, setSelectedCustomer] = useState(null); // Track selected customer object

  // Customer objects for Ryan and Peter -> to be modified when we have the collection
  const ryan = {
    photo: "/eddie.png",
    name: "Ryan Tan",
    Country: "Singapore, SG",
    guidelines: "guidlinesforinsurance.pdf",
  };

  const peter = {
    photo: "/rob.png",
    name: "Peter Green",
    Country: "New York, USA",
    guidelines: "risk_management_guidelines_insurance_core_actitities copy.pdf",
  };

  //Change these two functions once we have the backend //
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
    const guidelines = selectedCustomer.guidelines;

    console.log("Asking Your PDF:", query);
    console.log("Using the file:", guidelines);

    const API_BASE_IP = process.env.REACT_APP_BASE_URL;
    const PORT = process.env.REACT_APP_PORT_URL;
    const apiUrl = `http://${API_BASE_IP}:${PORT}/querythepdf`;

    try {
      const response = await axios.post(
        apiUrl,
        { query, guidelines },
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

  const handleSuggestionOne = () => {
    setQuery("What is a certificate of Insurance?");
  };

  const handleSuggestionTwo = () => {
    setQuery(
      "For adverse weather related claims, what is the average loss amount?"
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
              <button className={styles.askBtn} onClick={handleAsk}>
                Ask
              </button>
              <div className={styles.suggestedQuestions}>
                <p>Suggested Questions:</p>

                <button
                  className={styles.suggestion}
                  onClick={handleSuggestionOne}
                >
                  What is a certificate of Insurance?
                </button>
                <button
                  className={styles.suggestion}
                  onClick={handleSuggestionTwo}
                >
                  For adverse weather related claims, what is the average loss
                  amount?
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
