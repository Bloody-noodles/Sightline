# Sightline

**Sightline is a computer-vision research project for detecting and tracking people and selected everyday objects through a browser webcam.** It uses a custom-trained YOLO11n model, a FastAPI inference backend, and ByteTrack for frame-to-frame object tracking.

The project explores the complete workflow: preparing a custom dataset, training and evaluating an object detector, serving predictions through an API, and displaying detections in a browser dashboard.

> **Project status:** Working local prototype. Detection accuracy varies by object and scene conditions. Tracking IDs support frame-to-frame association and should not be treated as guaranteed long-term identity recognition.

## Features

- Custom-trained YOLO11n object detector.
- FastAPI endpoint for image inference.
- ByteTrack tracking IDs for detections across sequential frames.
- Browser dashboard using a webcam, with bounding boxes, class labels, confidence scores, and tracking IDs.
- Session statistics for observed tracking IDs, with a reset control.
- Local-first inference workflow designed to run on a personal computer.

## Object classes

The model was trained for these 11 classes:

`backpack`, `book`, `bottle`, `car`, `cup`, `handbag`, `motorcycle`, `person`, `phone`, `shoe`, `sunglasses`

The model may misclassify or miss objects, particularly under poor lighting, glare, unusual viewpoints, or when an object is difficult to distinguish visually.

## Technology stack

- **Detection:** Ultralytics YOLO11n
- **Tracking:** ByteTrack
- **API:** FastAPI
- **Server:** Uvicorn
- **Frontend:** HTML, CSS, JavaScript, browser MediaDevices API
- **Dataset annotation/versioning:** Roboflow
- **Training:** Google Colab
- **Model framework:** PyTorch / Ultralytics

## Training baseline

The custom model was trained using a dataset assembled for Sightline.

| Metric | Recorded result |
|---|---:|
| Precision | 71.9% |
| Recall | 54.3% |
| mAP@50 | 60.2% |
| mAP@50–95 | 50.9% |

These figures describe the recorded evaluation baseline, not a guarantee of real-world webcam performance. Phone detection was a weaker class in the evaluation, with recall around 39.3%. Results can vary with lighting, distance, camera quality, object scale, and background.

## How it works

1. The browser requests webcam permission.
2. The dashboard captures frames and sends them to the local API.
3. FastAPI passes each frame to the custom YOLO11n model.
4. ByteTrack associates detections across sequential frames and assigns tracking IDs.
5. The API returns class names, confidence scores, bounding boxes, and tracking IDs.
6. The dashboard draws the results and updates session statistics.

Tracking is not the same as re-identification: an object that disappears for a while may return with a different ID. Session unique-ID statistics count IDs observed, not guaranteed distinct physical objects.

## Project structure

```text
Sightline/
├── app/
│   ├── index.html
│   └── style.css
├── dataset/
├── docs/
├── models/
│   └── best.pt              # local model weights; not committed
├── notebooks/
├── src/
│   └── sightline/
│       ├── __init__.py
│       └── api.py
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

- `app/`: browser dashboard.
- `dataset/`: dataset records and local-only data locations.
- `docs/`: design notes, dataset details, and experiment records.
- `models/`: local model weights and artifact notes.
- `notebooks/`: training and evaluation notebooks.
- `src/sightline/`: API and reusable Python code.
- `tests/`: automated tests.

## Run locally

### 1. Requirements

- Python 3.10 recommended.
- A webcam for live dashboard testing.
- Model weights at `models/best.pt`.
- The packages listed in `requirements.txt`.

### 2. Install dependencies

From the project root, create and activate a virtual environment if you have not already done so.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell activation is blocked, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### 3. Start the API

Run this from the project root with the virtual environment activated:

```bash
python -m uvicorn sightline.api:app --app-dir src --reload
```

The API is available at `http://127.0.0.1:8000`.

- Health check: `http://127.0.0.1:8000/health`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

### 4. Start the dashboard

Open a second terminal in the project root and activate the same virtual environment if needed. Then run:

```bash
python -m http.server 5500 --directory app
```

Open `http://127.0.0.1:5500` in your browser and allow webcam access.

Keep both servers running while using the local application. If the model file is missing, the API cannot perform inference.

## Dataset and reproducibility

The dataset was assembled from custom-collected and sourced images and annotated/versioned in Roboflow. Before redistributing any dataset or images, verify each source's licence and permitted machine-learning use.

For reproducibility, record the following in `docs/DATASET.md` and `docs/EXPERIMENT_LOG.md`:

- Roboflow project and dataset version.
- Class order and image counts per split.
- Dataset export format and preprocessing.
- Training/validation/test split details.
- Model checkpoint, image size, epochs, batch size, and random seed where applicable.
- Python, PyTorch, and Ultralytics versions.
- Evaluation metrics and per-class results.

## Limitations and next steps

Known limitations include:

- Uneven accuracy between object classes; some phones may not be detected.
- Confusion between visually similar classes in challenging scenes.
- Reduced reliability in low light, glare, and unusual object poses.
- Inference speed depends on the computer and camera frame rate.
- Tracking IDs may change after an object is lost or reacquired.
- The hosted static frontend is a presentation layer; local Python inference requires the local API.

Potential next steps:

- Test detection in consistent daylight and indoor lighting.
- Compare confidence thresholds and inference image sizes without sacrificing responsiveness.
- Add automated tests for API responses and error handling.
- Capture a short demo and document known limitations.
- Improve the README and experiment logs as the project evolves.

## Privacy and security

- The intended local workflow sends webcam frames to the API on the same computer.
- Do not expose the local API publicly or configure broad CORS permissions without a clear security design.
- Do not commit API keys, credentials, private datasets, or model weights unless you deliberately intend to publish them and have checked the applicable permissions.
- Confirm image licences and usage terms before redistributing data.

## Author and project

Sightline is a personal computer-vision project focused on practical experimentation with object detection, tracking, API development, and browser-based visualization.
