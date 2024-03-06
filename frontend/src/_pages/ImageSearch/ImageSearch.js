import React, { useState, useEffect } from 'react';
import axios from "axios";

const ImageSearch = () => {
  const [droppedImage, setDroppedImage] = useState(null);
  const [similarImages, setSimilarImages] = useState([]);  // similarImages is an array of objects [{image: "image1", metadata: "metadata1"}, {image: "image2", metadata: "metadata2"}]

  useEffect(() => {  }, [similarImages]);

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
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <h1>Image Search</h1>
      <div
        style={{ width: '300px', height: '300px', border: '2px dashed #aaa' }}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        {droppedImage ? (
          <img src={droppedImage} alt="Dropped" style={{ width: '100%', height: '100%' }} />
        ) : (
          <p>Drag & Drop your image here</p>
        )}
      </div>
      <button onClick={handleUpload}>Upload photo</button>
      <SimilarImagesList similarImages={similarImages} />
    </div>
  );
};

const SimilarImagesList = ({ similarImages }) => {
  

  return (
    <div>
      <h2>Similar Images</h2>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
        {similarImages.map((imagePath, index) => (
          <div key={index} style={{ width: '150px', textAlign: 'center' }}>
            {/* Extract the file name from the path */}
            <img src={`/car_damage/${imagePath.split('/').pop()}`} alt={`Image ${index + 1}`} style={{ width: '100%', height: 'auto' }} />
            <p>{imagePath.split('/').pop()}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ImageSearch;
