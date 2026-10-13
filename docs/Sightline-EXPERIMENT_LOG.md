# Sightline — Experiment Log

This file records training runs, model evaluation results, and application-level experiments for Sightline. Keep confirmed facts separate from settings that still need to be recovered from the original notebook or training output.

## 1. Project baseline

| Field | Value |
|---|---|
| Project | Sightline |
| Model family | Ultralytics YOLO11n |
| Task | Custom object detection; application prototype also uses ByteTrack tracking |
| Classes | 11 custom classes (listed below) |
| Training environment | Google Colab |
| Model artifact used by local API | `models/best.pt` |
| Original Drive artifact path | `/content/drive/MyDrive/Sightline/results/yolo11n_corrected_labels_v1/weights/best.pt` |
| Dataset version / export | TODO — record exact Roboflow project/version and export details |
| Training date | TODO — recover from notebook or run history |
| Ultralytics version | TODO — recover from notebook/output |
| Training configuration | TODO — recover from notebook; do not infer from inference settings |

### Class list

`backpack`, `book`, `bottle`, `car`, `cup`, `handbag`, `motorcycle`, `person`, `phone`, `shoe`, `sunglasses`

Verify class order against the exact `data.yaml` used for training before relying on numeric class IDs in any report.

## 2. Recorded model evaluation baseline

The following metrics were recorded for the trained model:

| Metric | Recorded value |
|---|---:|
| Precision (P) | 71.9% |
| Recall (R) | 54.3% |
| mAP@0.50 | 60.2% |
| mAP@0.50:0.95 | 50.9% |
| Phone-class recall | Approximately 39.3% |

**Interpretation:** The recorded precision is higher than recall, so the model misses some objects. Phone recall is a known weak point. A shoe was also observed to be temporarily misclassified as a motorcycle during webcam use, then corrected in a later frame.

**Important evaluation note:** The exact evaluation split, sample counts, confidence threshold, image size, and metric-export source have not been recorded here yet. Recover these from the training notebook or evaluation output before presenting the metrics as a fully reproducible benchmark.

## 3. Training run record

Complete this section from the original Google Colab notebook or training logs. Do not fill values by guessing.

| Setting | Value |
|---|---|
| Run name | `yolo11n_corrected_labels_v1` |
| Model / starting weights | TODO |
| Dataset YAML path | TODO |
| Roboflow dataset version | TODO |
| Epochs requested | TODO |
| Epochs completed | TODO |
| Training image size (`imgsz`) | TODO |
| Batch size | TODO |
| Optimizer | TODO |
| Learning rate / schedule | TODO |
| Train / validation / test image counts | TODO |
| Best checkpoint path | `results/yolo11n_corrected_labels_v1/weights/best.pt` |
| Final checkpoint path | TODO |
| Training output / results CSV | TODO |
| Notes | TODO |

### Keep training and inference settings separate

The local FastAPI prototype currently runs inference with `imgsz=320` and a confidence threshold that has been discussed as `0.15` (confirm the actual current value in `src/sightline/api.py`). These are **inference settings**, not confirmed training settings. Do not copy them into the training table unless the notebook verifies that they were also used during training.

## 4. Application inference and tracking baseline

| Field | Current recorded behaviour |
|---|---|
| API | FastAPI served by Uvicorn |
| Prediction endpoint | `POST /predict` |
| Model loading | Lazy-loaded from `models/best.pt` |
| Tracking | Ultralytics tracking with ByteTrack (`bytetrack.yaml`) |
| Inference device | CUDA when available; otherwise CPU |
| Webcam frame width | Downscaled to a maximum width of 640 px in the frontend |
| JPEG quality | 0.75 |
| Request interval | About 1500 ms |
| Observed CPU webcam performance | Approximately 4–6 FPS on the available older laptop; actual speed varies with conditions |
| Tracking IDs | IDs were observed to remain stable as an object moved during the session |
| Session statistics | Dashboard counts unique tracking IDs observed in the session and displays detection counts |

Tracking IDs are tracker-generated identifiers, not guaranteed permanent identities for physical objects. An ID can change or be reused, especially after occlusion, missed detections, or tracker resets.

## 5. Experiment history

Use one entry per meaningful change. Change only one major variable at a time where possible.

### EXP-001 — Custom YOLO11n model baseline

- **Goal:** Establish a working custom detector for the Sightline class set.
- **Change:** Trained a YOLO11n model using the custom dataset in Google Colab.
- **Artifact:** `models/best.pt`
- **Recorded metrics:** P 71.9%; R 54.3%; mAP@0.50 60.2%; mAP@0.50:0.95 50.9%.
- **Known weakness:** Phone recall approximately 39.3%.
- **Unrecorded details:** Exact dataset version, training settings, evaluation split and date.
- **Outcome:** Baseline checkpoint was copied into the local project and used by the API.

### EXP-002 — Local API integration

- **Goal:** Run the trained model through a local HTTP API.
- **Change:** Integrated the model with FastAPI and exposed `POST /predict`.
- **Outcome:** A test image successfully returned structured detections through the API documentation interface.
- **Notes:** Single-image predictions confirm API integration, but do not by themselves establish temporal tracking.

### EXP-003 — Webcam tracking dashboard

- **Goal:** Demonstrate object detection and tracking through a browser webcam.
- **Change:** Connected the local dashboard to the local API and enabled ByteTrack.
- **Outcome:** Tracking IDs were observed to remain stable while an object moved. Dashboard remained responsive during testing.
- **Known behaviour:** Occasional class confusion (shoe/motorcycle) and missed phone detections were observed.
- **Performance note:** Roughly 4–6 FPS was observed on the available CPU-only/older-laptop setup; this is an approximate observation, not a controlled benchmark.

### EXP-004 — Session statistics

- **Goal:** Add lightweight session-level feedback to the dashboard.
- **Change:** Added a counter for unique tracking IDs observed during the session, reset controls, and detection counts.
- **Outcome:** User confirmed the counters worked.
- **Caveat:** Unique IDs are not necessarily equal to the number of distinct physical objects.

## 6. Future experiment template

Copy this section for each new experiment.

### EXP-XXX — Short experiment title

- **Date:**
- **Goal / hypothesis:**
- **Baseline checkpoint:**
- **Dataset / split:**
- **Single variable changed:**
- **Exact change made:**
- **Evaluation method and settings:**
- **Results:**
- **Qualitative observations:**
- **Runtime / hardware:**
- **Decision:** Keep / revert / investigate further
- **Next step:**

## 7. Reproducibility checklist

Before claiming that a run is reproducible, record:

- [ ] Exact dataset version and export format
- [ ] Exact `data.yaml` and class order
- [ ] Training notebook or script
- [ ] Model starting weights
- [ ] Epochs, batch size, image size, optimizer and learning-rate settings
- [ ] Library versions and runtime environment
- [ ] Evaluation split and metric output
- [ ] Best checkpoint and results CSV
- [ ] Any post-training changes or export steps

## 8. Change history

| Date | Change |
|---|---|
| TODO | Initial experiment log created; existing known metrics and application observations documented |
