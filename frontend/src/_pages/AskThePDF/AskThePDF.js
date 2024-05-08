import React, { useEffect, useState } from "react";
import styles from "../AskThePDF/askThePDF.module.css";
import axios from "axios";

const AskThePDF = () => {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [docs, setDocs] = useState([]);
  const [customerSelected, setCustomerSelected] = useState(false); // Track if a customer is selected
  const [selectedCustomer, setSelectedCustomer] = useState(null); // Track selected customer object


  // Customer objects for Maria and Peter -> to be modified when we have the collection
  const maria = {
    photo: "/jane.png",
    name: "Maria Ramirez",
    customerId: "123456",
    location: "Barcelona, Spain",
    documents: "cataluna_policy.pdf",
  };

  const peter = {
    photo: "/rob.png",
    name: "Peter Green",
    customerId: "789012",
    location: "New York, USA",
    documents: "nyc_guidelines.pdf",
  };

  //Change these two functions once we have the backend //
  const handleMariaClick = () => {
    console.log("Maria");
    setCustomerSelected(true);
    setSelectedCustomer(maria);

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
    console.log("Asking Your PDF:", query);
    const API_BASE_IP = "localhost";
    const PORT = "8000";
    const apiUrl = `http://${API_BASE_IP}:${PORT}/querythepdf`;

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
            <button className={styles.customerBtn} onClick={handleMariaClick}>
              <div className={styles.customerContent}>
                <img src="/jane.png" alt="Maria" className={styles.customerImage} />
                <div>
                  <strong>Maria Ramirez</strong>
                  <br />
                  Barcelona, Spain
                </div>
              </div>
            </button>

            <button className={styles.customerBtn} onClick={handlePeterClick}>
              <div className={styles.customerContent}>
                <img src="/rob.png" alt="Peter" className={styles.customerImage} />
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

                <button className={styles.suggestion} onClick={handleSuggestionOne}>
                  What is a certificate of Insurance?
                </button>
                <button className={styles.suggestion} onClick={handleSuggestionTwo}>
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
        <h2>References</h2>

        {customerSelected && ( // Render customerInfo only if a customer is selected
          <div className={styles.customerInfo}>

            <div className={styles.customerPhoto}>
              <img src={selectedCustomer.photo} alt="Customer Photo" className={styles.customerPhoto} />
            </div>

            <div className={styles.upperSection}>
              <div className={styles.fieldWrapper}>
                <p className={styles.fieldTitle}>Name:</p>
                <p className={styles.fieldContent}>{selectedCustomer.name}</p>
              </div>
              <div className={styles.fieldWrapper}>
                <p className={styles.fieldTitle}>Customer ID:</p>
                <p className={styles.fieldContent}>{selectedCustomer.customerId}</p>
              </div>
              <div className={styles.fieldWrapper}>
                <p className={styles.fieldTitle}>Location:</p>
                <p className={styles.fieldContent}>{selectedCustomer.location}</p>
              </div>
              <div className={styles.fieldWrapper}>
                <p className={styles.fieldTitle}>Documents:</p>
                <p className={styles.fieldContent}>{selectedCustomer.documents}</p>
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
