

import React, { useState } from 'react';
import UserProfile from '../../_components/userProfile/UserProfile';
import styles from './askLeafy.module.css';


const AskLeafy = () => {
  const [question, setQuestion] = useState('');

  const handleChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleAsk = () => {
    // Handle asking Leafy
    console.log('Asking Leafy:', question);
  };

  const handleLoremIpsum = () => {
    setQuestion('Find accidents caused by adverse weather. Tell me the average repair time for this claim based on similar claims.');
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
          
          <button className={styles.askBtn} onClick={handleAsk}>Ask</button>

          <div className={styles.suggestedQuestions}>
            <button className={styles.suggestion} onClick={handleLoremIpsum}>Find accidents caused by adverse weather.
              Tell me the average repair time for this claim based on similar claims.
             </button>
          </div>
        </div>

        <div className={styles.answer}>


        </div>
      </div>


      <div className={styles.references}>
        <h2>References</h2>
      </div>
    </div>
  );
};

export default AskLeafy;
