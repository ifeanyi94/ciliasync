import { useState, useEffect } from "react";
import { Upload } from "lucide-react";
import CountVsColoc from "./CountVsColoc";
import ResultCard from "./ResultCard";
import PlaceholderChart from "./PlaceholderChart";
import { Link } from "react-router-dom";

export default function ImageUpload() {
  const [mode, setMode] = useState("cilia"); // "cilia" or "coloc"
  const [redImage, setRedImage] = useState(null);
  const [greenImage, setGreenImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [resultData, setResultData] = useState(null);

  // Auto trigger for coloc when both images selected
  useEffect(() => {
    if (mode === "coloc" && redImage && greenImage) {
      handleUpload();
    }
  }, [redImage, greenImage, mode]);

  const handleUpload = async (fileOverride = null) => {
    const redFile = fileOverride || redImage;

    if (!redFile || (mode === "coloc" && !greenImage)) {
      alert("Please upload the required image(s).");
      return;
    }

    const formData = new FormData();
    formData.append("red_image", redFile);
    if (mode === "coloc") formData.append("green_image", greenImage);

    setPreview(URL.createObjectURL(redFile));

    try {
      // 🔴 1. Send to FastAPI
      const fastapiEndpoint =
        mode === "coloc"
          ? "http://127.0.0.1:8001/predict/coloc"
          : "http://127.0.0.1:8001/predict/cilia";

      const fastapiRes = await fetch(fastapiEndpoint, {
        method: "POST",
        body: formData,
      });

      if (!fastapiRes.ok) throw new Error("FastAPI processing failed");
      const fastapiResult = await fastapiRes.json();
      console.log("FastAPI returned:", fastapiResult);

      const overlayUrl = fastapiResult.overlay_url
        ? `http://127.0.0.1:8001${fastapiResult.overlay_url}`
        : null;

      // 🟢 2. Send to Django backend
      const djangoForm = new FormData();
      djangoForm.append("image", redFile);
      djangoForm.append("cilia_count", fastapiResult.cilia_count ?? 0);
      djangoForm.append(
        "coloc_score",
        mode === "coloc" ? fastapiResult.coloc_score ?? 0.0 : 0.0
      );

      const djangoRes = await fetch("http://127.0.0.1:8000/api/results/", {
        method: "POST",
        body: djangoForm,
      });

      if (!djangoRes.ok) {
        const errText = await djangoRes.text();
        console.error("Django error response:", errText);
        throw new Error("Failed to store result in Django");
      }

      const djangoData = await djangoRes.json();
      console.log("Django stored:", djangoData);

      setResultData({
        imageName: redFile.name,
        ciliaCount: djangoData.cilia_count,
        colocScore: djangoData.coloc_score,
        overlayUrl,
      });

      alert("Image processed and result saved!");
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Something went wrong.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-10 px-4 w-full max-w-4xl mx-auto">
      <nav className="mb-6 w-full flex justify-center gap-6 text-indigo-600 font-semibold">
        <Link to="/" className="hover:underline">Upload</Link>
        <Link to="/dashboard" className="hover:underline">Dashboard</Link>
      </nav>

      <h1 className="text-2xl font-semibold text-center text-gray-800 mb-4">
        CiliaSync Analyzer
      </h1>

      {/* MODE SELECTION */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setMode("cilia")}
          className={`px-4 py-2 rounded-lg ${
            mode === "cilia"
              ? "bg-gradient-to-r from-sky-500 via-blue-500 to-indigo-500 text-white"
              : "bg-white border border-gray-300 text-gray-400"
          }`}
        >
          Count Cilia
        </button>
        <button
          onClick={() => setMode("coloc")}
          className={`px-4 py-2 rounded-lg ${
            mode === "coloc"
              ? "bg-gradient-to-r from-sky-500 via-blue-500 to-indigo-500 text-white"
              : "bg-white border border-gray-300 text-gray-400"
          }`}
        >
          Colocalization
        </button>
      </div>

      {/* IMAGE INPUTS */}
      <div className="w-full grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <label className="flex flex-col items-center justify-center border-2 border-dashed border-red-400 rounded-xl p-6 cursor-pointer hover:border-red-500 transition w-full">
          <Upload className="w-8 h-8 text-red-500 mb-2" />
          <span className="text-red-500 mb-2">Upload Red Channel</span>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => {
              const file = e.target.files[0];
              setRedImage(file);
              if (mode === "cilia" && file) handleUpload(file);
            }}
            className="hidden"
          />
        </label>

        {mode === "coloc" && (
          <label className="flex flex-col items-center justify-center border-2 border-dashed border-green-400 rounded-xl p-6 cursor-pointer hover:border-green-500 transition w-full">
            <Upload className="w-8 h-8 text-green-500 mb-2" />
            <span className="text-green-500 mb-2">Upload Green Channel</span>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => {
                const file = e.target.files[0];
                setGreenImage(file);
              }}
              className="hidden"
            />
          </label>
        )}
      </div>

      {/* Optional fallback button for colocalization */}
      {mode === "coloc" && (
        <button
          onClick={() => handleUpload()}
          className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition mb-6"
        >
          Analyze
        </button>
      )}

      <CountVsColoc />

      {resultData && (
        <div className="mt-6 w-full">
          <ResultCard
            imageSrc={resultData.overlayUrl || preview}
            resultData={{
              imageName: resultData.imageName,
              ciliaCount: resultData.ciliaCount,
              colocScore: resultData.colocScore,
            }}
          />
          <PlaceholderChart />
        </div>
      )}
    </div>
  );
}
