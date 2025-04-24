# 🧪 CiliaSync

**CiliaSync** is a full-stack, modular bioinformatics image analysis tool designed for **automated quantification of primary cilia** and **protein co-localization detection** in antibody-stained microscopy images. It combines **deep learning**, **classical image processing**, and **C# high-performance segmentation** to support biological image analytics at scale.

---

## 🚀 Live Demo *(Coming Soon)*

- **Frontend**: `https://ciliasync-frontend.netlify.app/`
- **Backend**: `https://ciliasync-backend.onrender.com/`

---

## 🧠 Core Features

- 📤 Upload `.png` / `.jpeg` microscopy images (dual-channel supported)
- 🧮 **Automatically count primary cilia** via image morphology
- 🔬 **Quantify protein co-localization**:
  - Segment membrane vs cytoplasm
  - Measure signal overlap (Pearson, Jaccard, % overlap)
- 🧠 **ML-powered pattern detection** using PyTorch
- ⚙️ **C# CLI module** for fast membrane segmentation
- 📊 Visual dashboard with filtering, graphing & CSV export
- 🔁 Easily retrain ML models using new user-provided datasets

---

## 🧰 Tech Stack

| Layer           | Technology                                      |
|------------------|-------------------------------------------------|
| **Frontend**     | React, TailwindCSS                              |
| **Backend**      | Django REST + FastAPI (ASGI)                    |
| **Image Analysis**| OpenCV, scikit-image                           |
| **Machine Learning**| PyTorch (CNN/UNet model)                   |
| **Perf. Module** | C# CLI (.NET Core)                              |
| **Database**     | PostgreSQL (via Django ORM)                     |
| **Deployment**   | Netlify (frontend), Render (backend & DB)       |

---

## 📁 Project Structure

ciliasync/ 
├── client/ # React + Tailwind frontend 
├── backend/ 
│ ├── django_core/ # Django + REST Framework 
│ ├── fastapi_core/ # ML endpoints (inference, training) 
│ ├── ml_model/ # PyTorch model, trainer, dataset loader 
│ └── asgi.py # Combines Django + FastAPI under ASGI 
├── image-core/ # C# CLI for segmentation 
├── data/ # Sample training/testing images 
├── notebooks/ # Jupyter notebooks (EDA, experiments) 
├── README.md # This file!

---

## 🧪 Core Analysis Modules

### 1️⃣ Primary Cilium Detection
- Converts to grayscale
- Uses thresholding + morphological ops
- Detects blobs, outputs:
  - `cilia_count`
  - Highlighted image with bounding overlays

### 2️⃣ Co-localization Analysis
- Accepts dual-channel image (e.g. green + red)
- Separates image into:
  - **Membrane** (1–2px from boundary)
  - **Cytoplasm**
- Calculates:
  - % Overlap (Pearson Correlation, Jaccard Index)
  - Signal heatmaps per region
- Returns results and annotated overlays

### 3️⃣ PyTorch ML Module (Core)
- CNN (or UNet) trained to detect co-localization patterns
- CLI for training on custom data
- REST API for inference via FastAPI
- Retrainable with user-labeled image sets

### 4️⃣ C# CLI Integration
- Membrane segmentation
- JSON output of ROI statistics
- Integrated via `subprocess.run()` from Python

---

## 📦 Installation & Dev Setup

### 1. Clone the Repo
bash
git clone https://github.com/your-username/ciliasync.git
cd ciliasync 


2. Frontend Setup

bash
cd client
npm install
npm run dev

3. Backend Setup
bash
cd ../backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run backend (ASGI app combining Django + FastAPI)
uvicorn asgi:app --reload

4. C# CLI Module (Optional but recommended)
bash
cd ../image-core
dotnet build
./cilia-segmenter input.png output.json

5. ML Model Training
bash
cd backend/ml_model/
python train.py --data-dir ../../data/train

6. ML Inference API
bash
curl -X POST http://localhost:8000/api/predict \
     -F "image=@path/to/image.png"

Returns:
json

{
  "membrane_colocalization": 0.89,
  "cytoplasmic_colocalization": 0.44,
  "heatmap_url": "/media/heatmap.png"
}

📊 Data & Visual Dashboard
View uploaded images + overlays
Filter by tag, condition, date
Export session summaries to .csv

Charts:
Cilia count histograms
Colocalization scatterplots
Per-condition analysis

🗃️ Database Schema (PostgreSQL)
sql
CREATE TABLE analysis (
  id SERIAL PRIMARY KEY,
  image_url TEXT,
  cilia_count INT,
  coloc_membrane FLOAT,
  coloc_cytoplasm FLOAT,
  heatmap_url TEXT,
  created_at TIMESTAMP,
  tags TEXT[],
  method_used TEXT
);

🔮 Future Enhancements
Per-cell nucleus segmentation
3D Z-stack image support
Auth system for multi-user tracking
Browser-based manual annotation tools
AutoML pipeline for transfer learning

📜 License
MIT License © 2025
Created for educational, academic, and research purposes in bioimage informatics.

🤝 Contributing
Pull requests and feedback are welcome!
We encourage collaboration from:

Image analysis researchers
ML practitioners
Full-stack developers
Lab techs and microscopists

