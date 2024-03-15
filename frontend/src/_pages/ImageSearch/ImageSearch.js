import React, { useState, useEffect } from 'react';
import axios from "axios";
import styles from "./imageSearch.module.css";

const ImageSearch = () => {
  const [droppedImage, setDroppedImage] = useState(null);
  const [similarImages, setSimilarImages] = useState([]);  // similarImages is an array of objects [{image: "image1", metadata: "metadata1"}, {image: "image2", metadata: "metadata2"}]
  const [showLossAmount, setShowLossAmount] = useState(false); // State to track whether to show lossAmountTbd
  const [similarDocs, setSimilarDocs] = useState("");

  useEffect(() => { }, [similarImages]);

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    const reader = new FileReader();

    reader.onload = (event) => {
      setDroppedImage(event.target.result);
    };

    reader.readAsDataURL(file);
  };

  const handleUpload = async () => {
    const apiUrl = "http://127.0.0.1:8000/imageSearch";
    setShowLossAmount(true); // Show lossAmountTbd when the button is clicked


    try {
      const response = await axios.post(
        apiUrl,
        { droppedImage },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      setSimilarImages(response.data.similar_photos);
      setSimilarDocs(response.data.similar_docs);
    
    } catch (error) {
      console.error("Error:", error);
    }
  };
  
  console.log((similarDocs.length > 0 ? JSON.stringify(similarDocs[0].customerID) : ""));

  const getCurrentDate = () => {
    const currentDate = new Date();
    const day = currentDate.getDate().toString().padStart(2, '0');
    const month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
    const year = currentDate.getFullYear();

    return `${year}-${month}-${day}`;
  };


  return (
    <div className={styles.content}>
      <div className={styles.imageSearchSection}>
        <h2>Image Search</h2>
        <div
          className={styles.dragBox}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          {droppedImage ? (
            <img className={styles.droppedImage} src={droppedImage} alt="Dropped" />
          ) : (
            <p className={styles.dragText}>Drag &amp; Drop your image here</p>
          )}
        </div>
        <button className={styles.uploadBtn} onClick={handleUpload}>Upload photo</button>

        <hr className={styles.hr}></hr>

        {showLossAmount && ( // Conditionally render lossAmountTbd based on showLossAmount state

          <div className={styles.uploadedImgInfo}>

            <div className={styles.info}>
              <p className={styles.fieldTitle}>CustomerID:</p>
              <p className={styles.fieldContent}>C1234</p>
            </div>

            <div className={styles.info}>
              <p className={styles.fieldTitle}>Claim Date:</p>
              <p className={styles.fieldContent}>{getCurrentDate()}</p>
            </div>

            <div className={styles.info}>
              <p className={styles.fieldTitle}>Claim Status:</p>
              <p className={styles.statusTag}>Active</p>
            </div>

            <div className={styles.info}>
              <p className={styles.fieldTitle}>Loss Amount:</p>
              <p className={styles.lossTbd}>TBD</p>
            </div>
          </div>

        )}
      </div>

      <div className={styles.similarImageSection}>

        <SimilarImagesList similarImages={similarImages} similarDocs={similarDocs}/>

      </div>
    </div>
  );
};

const SimilarImagesList = ({ similarImages, similarDocs }) => {
  return (
    <div>
      <h2>Similar Claims</h2>

      {similarImages.map((imagePath, index) => (
        
        
        <div key={index} >

          <div className={styles.referenceCards}>

            <div className={styles.imgSection}>
              {/* Extract the file name from the path */}
              {/* <img src={`/photos/${imagePath.split('/').pop()}`} alt={`Image ${index + 1}`} /> */}
              {/* <img src={`/${imagePath}`} alt={`Image ${index + 1}`} /> */}
              <img src={`/${imagePath}`} alt={`Image ${index + 1}`} />
            </div>


            <div className={styles.contentSection}>
              {/*<p>{imagePath.split('/').pop()}</p>*/}

              <div className={styles.upperSection}>
                <div className={styles.fieldWrapper}>
                  <p className={styles.fieldTitle}>Customer ID:</p>
                  {/* <p className={styles.fieldContent}>{JSON.stringify(similarDocs[0].customerID)}</p> */}
                  <p className={styles.fieldContent}>placeholder</p>
                </div>

                <div className={styles.fieldWrapper}>
                  <p className={styles.fieldTitle}>Claim Date:</p>
                  <p className={styles.fieldContent}>20/07/1998</p>
                </div>

                <div className={styles.fieldWrapper}>
                  <p className={styles.fieldTitle}>Loss Amount:</p>
                  <p className={styles.lossAmount}>$9999</p>
                </div>
              </div>

              <div className={styles.lowerSection}>
                <p className={styles.fieldTitle}>Damage Description:</p>
                <p className={styles.fieldContent}>Damage Description placeholder</p>
              </div>
            </div>

          </div>
        </div>
      ))}

    </div>
  );
};

export default ImageSearch;
