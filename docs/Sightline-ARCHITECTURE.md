# Sightline — Architecture Overview

## 1. Purpose

Sightline is a browser-based object detection and tracking prototype built around a custom YOLO11n model. The current workflow captures webcam frames in the browser, sends them to a local API, and displays detections and tracking information.

This document describes the current prototype, not a production deployment.

## 2. High-level architecture

```text
User
 |
 v
Browser dashboard
(app/index.html + app/style.css)
 |
 | webcam frame upload (HTTP)
 v
Local FastAPI service
(src/sightline/api.py)
 |
 | image preprocessing / inference
 v
Custom YOLO11n checkpoint
(models/best.pt)
 |
 | detection + tracking results
 v
FastAPI JSON response
 |
 v
Browser draws boxes, labels, IDs,
counts, and session statistics
```

The browser uses the webcam through the browser's permission system. The frontend sends frames to the API; the model inference currently happens in Python, not in the static HTML page.

## 3. Main components

| Component | Location | Responsibility |
|---|---|---|
| Dashboard HTML | `app/index.html` | Main interface, camera controls, display structure |
| Dashboard CSS | `app/style.css` | Layout and visual styling |
| FastAPI app | `src/sightline/api.py` | HTTP routes, image handling, model inference and response |
| Model weights | `models/best.pt` | Trained custom YOLO11n checkpoint |
| Dataset notes | `docs/DATASET.md` | Dataset sources, labels, and reproducibility notes |
| Experiment log | `docs/EXPERIMENT_LOG.md` | Model metrics and experiment records |
| API reference | `docs/API_REFERENCE.md` | Local endpoints and startup instructions |
| Testing guide | `docs/TESTING_GUIDE.md` | Manual verification checklist |
| Privacy/security notes | `docs/PRIVACY_SECURITY.md` | Local privacy and security assumptions |
| Deployment guide | `docs/DEPLOYMENT_GUIDE.md` | Current setup and future hosting considerations |
| Roadmap | `docs/ROADMAP.md` | Priorities and future work |

## 4. Runtime flow

1. The user opens the dashboard through the local static server.
2. The user grants camera permission and starts the webcam.
3. The frontend captures and downsizes frames before sending them to the local API.
4. The API receives an image and loads the model if it has not already been loaded.
5. YOLO performs inference; the API calls the tracking interface configured with ByteTrack.
6. The API serializes detection details into a JSON response.
7. The frontend draws the returned boxes and labels, and updates counts and session statistics.
8. The process repeats while the camera session is active.

The frontend has been recorded as sending frames up to a maximum width of 640 pixels, at JPEG quality 0.75, about every 1500 ms, while preventing overlapping requests. Verify these values in the current frontend code if they are changed.

## 5. Model summary

The custom model has 11 classes:

`backpack`, `book`, `bottle`, `car`, `cup`, `handbag`, `motorcycle`, `person`, `phone`, `shoe`, `sunglasses`

Recorded evaluation metrics:
- Precision: 71.9%
- Recall: 54.3%
- mAP@0.50: 60.2%
- mAP@0.50:0.95: 50.9%
- Phone recall: approximately 39.3%

The exact evaluation split and settings should be recovered from the training notebook before these metrics are used as a formal reproducible benchmark.

## 6. Local development ports

| Service | URL |
|---|---|
| Dashboard | `http://127.0.0.1:5500` |
| API | `http://127.0.0.1:8000` |
| API documentation | `http://127.0.0.1:8000/docs` |
| API health | `http://127.0.0.1:8000/health` |

The dashboard and API are separate local services and both need to be running for live detection.

## 7. Hosted frontend boundary

The current Hugging Face Space is:

`https://huggingface.co/spaces/rigidmayor7/Sightline`

It serves a static frontend. Static hosting does not itself execute the Python model. A hosted browser page cannot use `127.0.0.1` to reach the developer's laptop; that address refers to the device running the browser.

For remote live inference, Sightline would need a separately hosted API and an updated frontend API URL, along with appropriate HTTPS, CORS, upload validation, access control, and privacy protections.

## 8. Design boundaries and limitations

- Detection quality varies with lighting, distance, object appearance, and occlusion.
- Phone recall is a known weakness in the recorded baseline.
- Occasional shoe/motorcycle confusion was observed.
- Tracking IDs are temporary tracker identifiers, not guaranteed permanent identities.
- CPU webcam performance was observed at approximately 4–6 FPS on the available older laptop; this is an informal observation.
- The current system is a prototype and should not be treated as a high-stakes identity or surveillance system.

## 9. Change history

| Date | Change |
|---|---|
| TODO | Initial architecture overview drafted from the current prototype notes |
