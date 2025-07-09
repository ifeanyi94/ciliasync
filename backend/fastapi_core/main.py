import sys 
import os

# Add the root directory to Python path BEFORE any project imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from pathlib import Path
from tempfile import NamedTemporaryFile
import math
import torch
import numpy as np
from PIL import Image
import torchvision.transforms as T
import cv2
import traceback  # << Added here

from fastapi import UploadFile, File
import shutil
import uuid
from backend.cilia_cli_runner import run_csharp_analysis


try:
    from image_core.cilia_detection.detector import detect_cilia
    from image_core.colocalization.membrane_coloc import calculate_membrane_cytoplasm_colocalization
    from image_core.model import SimpleUNet
    from image_core.utils import dice_score, iou_score
except Exception as e:
    print(">>> ERROR DURING IMPORT <<<")
    traceback.print_exc()

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static/media directories
STATIC_DIR = Path(__file__).resolve().parent / "static"
MEDIA_DIR = STATIC_DIR / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

def sanitize_result(data: dict) -> dict:
    return {
        k: (None if isinstance(v, float) and math.isnan(v) else v)
        for k, v in data.items()
    }

@app.post("/predict/cilia")
async def predict_cilia(
    red_image: UploadFile = File(...)
):
    try:
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp_red:
            tmp_red.write(await red_image.read())
            red_path = tmp_red.name

        filename = f"{Path(red_image.filename).stem}_{uuid4().hex[:6]}.png"
        save_path = MEDIA_DIR / filename

        result = detect_cilia(red_path, str(save_path))
        cilia_count = result["cilia_count"]

        return {
            "cilia_count": cilia_count,
            "overlay_url": f"/media/{filename}"
        }

    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return JSONResponse(status_code=500, content={"error": traceback_str})

@app.post("/predict/coloc")
async def predict_colocalization(
    red_image: UploadFile = File(...),
    green_image: UploadFile = File(...)
):
    try:
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp_red:
            tmp_red.write(await red_image.read())
            red_path = tmp_red.name

        with NamedTemporaryFile(delete=False, suffix=".png") as tmp_green:
            tmp_green.write(await green_image.read())
            green_path = tmp_green.name

        coloc_metrics = calculate_membrane_cytoplasm_colocalization(red_path, green_path)

        return sanitize_result(coloc_metrics)

    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return JSONResponse(status_code=500, content={"error": traceback_str})

@app.post("/predict/mask")
async def predict_mask(
    image: UploadFile = File(...),
    mask: UploadFile = File(None)  # Optional ground-truth for metrics
):
    try:
        # Save uploaded input image
        with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(await image.read())
            input_path = tmp.name

        # Load and preprocess input image
        img = Image.open(input_path).convert("RGB")
        transform = T.Compose([
            T.Resize((256, 256)),
            T.ToTensor()
        ])
        img_tensor = transform(img).unsqueeze(0)  # [1, 3, 256, 256]

        # Use absolute path to load model
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        checkpoint_path = BASE_DIR / "image_core" / "checkpoints" / "unet_cilia.pt"

        print(f"\n>>> Looking for model at: {checkpoint_path}\n")  # Debug print

        model = SimpleUNet()
        model.load_state_dict(torch.load(checkpoint_path, map_location="cpu"))
        model.eval()

        with torch.no_grad():
            pred = model(img_tensor)[0, 0].numpy()
            pred_bin = (pred > 0.5).astype(np.uint8) * 255

        # Save predicted mask
        filename = f"pred_{uuid4().hex[:6]}.png"
        mask_path = MEDIA_DIR / filename
        Image.fromarray(pred_bin).save(mask_path)

        response = {
            "overlay_url": f"/media/{filename}"
        }

        # Optional: compute metrics
        if mask:
            with NamedTemporaryFile(delete=False, suffix=".png") as tmp_mask:
                tmp_mask.write(await mask.read())
                gt_mask = Image.open(tmp_mask.name).convert("L")
                gt_mask = gt_mask.resize((256, 256))
                gt_arr = np.array(gt_mask)
                gt_bin = (gt_arr > 128).astype(np.uint8)

                dice = dice_score(pred_bin // 255, gt_bin)
                iou = iou_score(pred_bin // 255, gt_bin)

                response["metrics"] = {
                    "dice": round(dice, 4),
                    "iou": round(iou, 4)
                }

        return response

    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return JSONResponse(status_code=500, content={"error": traceback_str})

@app.post("/analyze-csharp")
async def analyze_csharp(file: UploadFile = File(...)):
    try:
        # Use tempfile for safe, OS-independent temp file creation
        with NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            temp_input_path = tmp_file.name

        result = run_csharp_analysis(temp_input_path)
        return result

    except Exception as e:
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return JSONResponse(status_code=500, content={"error": traceback_str})

    finally:
        try:
            if os.path.exists(temp_input_path):
                os.remove(temp_input_path)
        except Exception as cleanup_err:
            print(f"Cleanup error: {cleanup_err}")
