# Sightline — Project Roadmap

This roadmap records sensible next steps for the current Sightline prototype. It is intentionally staged so that improvements build on the working version instead of creating unnecessary rework.

## Current baseline

Sightline currently has:
- A custom YOLO11n model with 11 object classes.
- A local FastAPI inference API.
- ByteTrack tracking integrated into the API.
- A browser dashboard with webcam controls, bounding boxes, tracking IDs, and session statistics.
- Supporting documentation for the dataset, experiments, API, testing, privacy/security, and deployment.

Recorded model metrics:
- Precision: 71.9%
- Recall: 54.3%
- mAP@0.50: 60.2%
- mAP@0.50:0.95: 50.9%
- Phone recall: approximately 39.3%

These metrics are the recorded baseline; confirm the original evaluation settings before treating them as a reproducible benchmark.

## Phase 1 — Preserve the working project

**Priority: high**

- [ ] Confirm all documentation files are saved in `docs/`.
- [ ] Keep a backup of the working dashboard and API before substantial edits.
- [ ] Confirm `models/*.pt` remains excluded from Git.
- [ ] Run the manual smoke tests in `docs/TESTING_GUIDE.md`.
- [ ] Record any failed checks and exact error messages.

**Completion condition:** the current local version still starts, detects objects, tracks them, and displays session statistics.

## Phase 2 — Make the project reproducible

**Priority: high**

- [ ] Fill confirmed dataset version, export date, and image counts in `docs/DATASET.md`.
- [ ] Recover actual training settings from the original Colab notebook.
- [ ] Add confirmed training details to `docs/EXPERIMENT_LOG.md`.
- [ ] Record the Python and key library versions used locally.
- [ ] Add a small, permitted sample image for repeatable API testing if licensing allows.

**Completion condition:** another developer can understand how the model was trained and how to start the local prototype without guessing key settings.

## Phase 3 — Improve reliability without retraining yet

**Priority: medium**

- [ ] Test the app in good daylight and ordinary indoor lighting.
- [ ] Try multiple distances and object orientations.
- [ ] Record missed detections and class confusion rather than changing many settings at once.
- [ ] Verify that the camera can be stopped and API errors do not permanently break the dashboard.
- [ ] Keep the current model as a baseline before any experiment.

**Known issue:** phone recall was recorded at approximately 39.3%, and occasional shoe/motorcycle confusion was observed. These issues should be documented, not hidden.

**Completion condition:** a small, repeatable manual test record describes where the current model works and where it fails.

## Phase 4 — Add automated checks

**Priority: medium**

Potential tests under `tests/`:
- API root and health endpoint tests.
- Upload validation tests.
- Prediction response-schema tests.
- A lightweight test using a small permitted image.
- Frontend error-state checks where practical.

Start with tests that run quickly and do not require a webcam or a large model download for every test run.

**Completion condition:** basic regressions can be caught before manually opening the dashboard.

## Phase 5 — Decide whether to improve the model

**Priority: optional; use evidence first**

Do not retrain only because one webcam test failed. First gather examples of the failures and determine whether the cause is lighting, distance, class imbalance, annotation quality, or model capacity.

If evidence supports a new training run:
- [ ] Preserve the current checkpoint and baseline metrics.
- [ ] Choose one clear hypothesis.
- [ ] Make a documented dataset or training change.
- [ ] Record exact settings and dataset version.
- [ ] Evaluate on a defined held-out split.
- [ ] Compare against the baseline before replacing `best.pt`.

**Completion condition:** any new model is kept only if its measured performance or practical behaviour justifies the change.

## Phase 6 — Prepare a shareable demo

**Priority: only when needed**

- [ ] Decide whether the goal is a portfolio presentation or live remote inference.
- [ ] For a presentation, the static frontend can show the interface and explain the architecture.
- [ ] For remote live inference, choose and verify a suitable backend host first.
- [ ] Add upload limits, suitable access controls, HTTPS, restricted CORS, and clear error handling.
- [ ] Update the frontend API URL only after the backend is live and tested.
- [ ] Revisit privacy, model/dataset licensing, and deployment costs.

**Important:** the existing hosted static frontend does not run the Python model. Do not expose the local laptop API publicly as a shortcut.

## Phase 7 — Portfolio polish

**Priority: medium**

- [ ] Keep `README.md` accurate about what works today.
- [ ] Add screenshots or a short demo clip only if they can be shared safely.
- [ ] Include model metrics and known limitations.
- [ ] Explain the technical choices: YOLO11n, FastAPI, ByteTrack, and browser webcam integration.
- [ ] Include clear local setup instructions.
- [ ] Link to the hosted frontend as a UI presentation, not as a claim of hosted inference.

**Completion condition:** a reviewer can understand the problem, architecture, implementation, measured results, limitations, and how to run the project.

## Suggested order

1. Preserve and smoke-test the current working version.
2. Complete confirmed dataset and experiment details.
3. Run a small set of repeatable lighting/object tests.
4. Add basic automated API tests.
5. Decide whether a model change is justified.
6. Prepare a public live demo only if there is a concrete need.

## Decision log

| Date | Decision | Reason |
|---|---|---|
| TODO | Keep the current trained model as the baseline | Preserve a working version and avoid unmeasured changes |
| TODO | Defer remote inference deployment | Current goal can proceed locally without exposing the development API |

## Change history

| Date | Change |
|---|---|
| TODO | Initial project roadmap created from the current prototype status |
