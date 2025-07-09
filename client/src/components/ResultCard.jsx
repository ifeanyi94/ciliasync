import React from "react";
import PlaceholderChart from "./PlaceholderChart";

const ResultCard = ({ imageSrc, resultData }) => {
    return (
      <div className="bg-white shadow-xl rounded-xl p-4 w-full max-w-md mx-auto mt-6">
        <img src={imageSrc} alt="Uploaded preview" className="w-full rounded-md mb-4" />
  
        <div>
          <p className="font-semibold text-sm text-gray-600">Image Name:</p>
          <p className="mb-2">{resultData.imageName}</p>
  
          <p className="font-semibold text-sm text-gray-600">Cilia Count:</p>
          <p className="mb-2">{resultData.ciliaCount}</p>
  
          <p className="font-semibold text-sm text-gray-600">Colocalization Score:</p>
          <p>{resultData.colocScore}</p>
        </div>
      </div>
    );
  };
  
  // Example usage:
  <ResultCard
    imageSrc="/uploads/sample-image.png"
    resultData={{
      imageName: "sample-image.png",
      ciliaCount: 45,
      colocScore: 0.82,
    }}
  />
  
  
  export default ResultCard;