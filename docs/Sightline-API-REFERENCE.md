# Sightline — API Reference

This document describes the local FastAPI service as currently implemented and tested. If the code changes, update this reference to match the actual implementation.

## 1. Overview

Sightline uses a local FastAPI service to load the custom YOLO11n checkpoint and return detections for an uploaded image. The service also calls Ultralytics tracking with ByteTrack. The browser dashboard sends webcam frames to this API.

- **Base URL:** `http://127.0.0.1:8000`
- **Interactive API documentation:** `http://127.0.0.1:8000/docs`
- **Model file:** `models/best.pt`
- **Main module:** `src/sightline/api.py`

This is a local prototype. It is not a public production API.

## 2. Start the API

Open a terminal in the project root:

```powershell
cd C:\Users\PC\Desktop\Sightline
.\.venv\Scripts\Activate.ps1
python -m uvicorn sightline.api:app --app-dir src --reload
```

Keep this terminal open while using the dashboard. To stop the service, press `Ctrl+C`.

If PowerShell activation is blocked by the machine's execution policy, use Command Prompt activation instead:

```bat
.venv\Scripts\activate.bat
```

Then run the Uvicorn command shown above.

## 3. Endpoints

### `GET /`

Returns a short service status message.

Example response:

```json
{
  "app": "Sightline",
  "status": "running",
  "docs": "/docs"
}
```

### `GET /health`

Returns basic health and model-file information. Example:

```json
{
  "status": "healthy",
  "model_file_exists": true,
  "model_loaded": false
}
```

`model_loaded: false` after a restart is expected when the model is loaded lazily. It does not necessarily mean the service is broken. Send a prediction request, then check the endpoint again if needed.

### `POST /predict`

Accepts one uploaded image and returns detection information in JSON.

The request uses `multipart/form-data` with the image file field expected by the API implementation. The easiest way to test the exact field name and upload a file is through `/docs`:

1. Open `http://127.0.0.1:8000/docs`.
2. Expand `POST /predict`.
3. Select **Try it out**.
4. Choose an image file.
5. Select **Execute**.
6. Inspect the JSON response.

The response includes fields such as image dimensions, detection count, a tracking-enabled flag, and a list of detections. Each detection can include class ID, class name, confidence, tracking ID, and bounding-box coordinates. Exact fields depend on the current `api.py` implementation.

## 4. Model and tracking behaviour

The API loads the model from `models/best.pt` and runs inference using Ultralytics. The current prototype calls the tracking interface with ByteTrack (`bytetrack.yaml`).

Recorded implementation details:
- Inference image size has been set to `320`.
- A confidence threshold of `0.15` was recorded previously; verify the current value in `src/sightline/api.py` before relying on it.
- The service selects CUDA when PyTorch reports a CUDA GPU available; otherwise it uses CPU.
- The model is loaded lazily, so the first prediction may take longer than subsequent predictions.

**Tracking note:** A single uploaded image can return a tracking-related field or ID, but reliable temporal tracking must be assessed over sequential frames. The browser webcam test previously showed IDs remaining stable while an object moved.

## 5. Connect the local dashboard

Start a second terminal in the project root and run:

```powershell
python -m http.server 5500 --directory app
```

Open the dashboard at:

`http://127.0.0.1:5500`

The API and dashboard use different local ports:
- Dashboard: `http://127.0.0.1:5500`
- API: `http://127.0.0.1:8000`

The API's current CORS configuration permits the local dashboard origin `http://127.0.0.1:5500`. Use that same origin rather than changing the configuration unnecessarily.

## 6. Troubleshooting

### API does not start

- Confirm the terminal is in the `Sightline` project root.
- Activate `.venv`.
- Check that dependencies are installed from `requirements.txt`.
- Read the first error shown in the terminal before trying changes.

### Model file is missing

Confirm this file exists:

`Sightline\models\best.pt`

The `.pt` file is intentionally excluded from Git by `.gitignore`; keep model weights private unless you deliberately choose an appropriate hosting method.

### `/health` says `model_loaded: false`

This can be normal after restarting because the model is lazy-loaded. Try a prediction through `/docs`. If prediction fails, inspect the terminal error.

### Dashboard cannot reach the API

- Start the API on port `8000`.
- Start the static server on port `5500`.
- Open the dashboard using `http://127.0.0.1:5500`, not by double-clicking `index.html`.
- Check the browser developer console and API terminal for the actual error.
- Avoid changing CORS to `*` as a shortcut.

### Prediction is slow

The current laptop has older CPU hardware and webcam performance has been observed around 4–6 FPS in this prototype. First-frame model loading can also add delay. Treat this as an approximate observation, not a benchmark.

### A class is missed or confused

This is a known limitation of the current custom model. Phone recall was recorded at approximately 39.3%, and occasional shoe/motorcycle confusion was observed. Better lighting and a clear view may help during testing, but they do not guarantee a correct detection.

## 7. Security and privacy

- Keep the service bound to localhost for local development.
- Do not expose port `8000` to the public internet, use a public tunnel, or configure router port-forwarding for this prototype.
- Use images and webcam footage you have permission to process.
- The webcam dashboard is intended for deliberate, user-controlled testing. Stop the camera when finished.
- Do not upload `models/best.pt`, private footage, or secrets to a public repository.
- Before deployment, add appropriate authentication, rate limiting, request limits, error handling, and a reviewed privacy/security design.

## 8. Change history

| Date | Change |
|---|---|
| TODO | Initial API reference drafted from the current local prototype notes; verify against `src/sightline/api.py` after code changes |
