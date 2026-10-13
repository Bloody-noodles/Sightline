from pathlib import Path
from functools import lru_cache
import io

import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image, UnidentifiedImageError

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "best.pt"

app = FastAPI(
    title="Sightline API",
    description="Object detection and tracking API powered by Sightline's trained YOLO11n model.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Load the model only when prediction is requested.
@lru_cache(maxsize=1)
def get_model():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Place best.pt inside the project's models folder."
        )

    torch.set_num_threads(2)
    return YOLO(str(MODEL_PATH))


@app.get("/")
def root():
    return {
        "app": "Sightline",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_file_exists": MODEL_PATH.is_file(),
        "model_loaded": get_model.cache_info().currsize > 0,
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=415,
            detail="Please upload an image file.",
        )

    image_bytes = await file.read(10 * 1024 * 1024 + 1)

    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Image must be 10 MB or smaller.",
        )

    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image.",
        )

    try:
        model = get_model()
        device = 0 if torch.cuda.is_available() else "cpu"

        # Keep tracker state between successive frames from the same camera.
        results = model.track(
            source=image,
            imgsz=320,
            conf=0.10,
            device=device,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        print(f"Sightline tracking error: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Tracking failed. Check the API terminal for details.",
        )

    result = results[0]
    detections = []
    boxes = result.boxes

    if boxes is not None:
        for box in boxes:
            class_id = int(box.cls.item())
            confidence = float(box.conf.item())
            x1, y1, x2, y2 = [
                round(float(value), 2)
                for value in box.xyxy[0].tolist()
            ]

            track_id = int(box.id.item()) if box.id is not None else None

            detections.append({
                "class_id": class_id,
                "class_name": model.names[class_id],
                "confidence": round(confidence, 4),
                "track_id": track_id,
                "box": {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                },
            })

    return {
        "image": {
            "width": image.width,
            "height": image.height,
        },
        "count": len(detections),
        "tracking_enabled": True,
        "detections": detections,
    }
