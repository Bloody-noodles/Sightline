# Sightline — Testing Guide

This guide provides a lightweight checklist for manually testing the local Sightline prototype. It is designed for the current development setup, not as a claim that automated tests already exist.

## 1. Test setup

Project root:

`C:\Users\PC\Desktop\Sightline`

Expected local services:
- API: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`
- Dashboard: `http://127.0.0.1:5500`

### Start the API

In a terminal opened at the project root:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn sightline.api:app --app-dir src --reload
```

### Start the dashboard

Open a second terminal at the project root:

```powershell
python -m http.server 5500 --directory app
```

Then open `http://127.0.0.1:5500`.

## 2. Manual smoke tests

Mark each test only after you have actually performed it.

| ID | Test | Steps | Expected result | Status |
|---|---|---|---|---|
| SM-01 | API root | Open `http://127.0.0.1:8000/` | JSON reports the app is running | Not recorded |
| SM-02 | Health endpoint | Open `http://127.0.0.1:8000/health` | Health JSON is returned; model file exists | Not recorded |
| SM-03 | API documentation | Open `http://127.0.0.1:8000/docs` | Interactive API docs load | Not recorded |
| SM-04 | Single-image prediction | Use `POST /predict` in `/docs` and upload a supported image | JSON response includes image/detection information | Previously tested successfully; repeat after relevant changes |
| SM-05 | Missing/invalid image | Try a request without a valid image, if supported by the endpoint form | Clear client error; server remains running | Not recorded |
| SM-06 | Dashboard loads | Open `http://127.0.0.1:5500` | Dashboard interface appears | Previously tested successfully; repeat after relevant changes |
| SM-07 | Camera permission | Start the camera using the dashboard control | Browser asks for or receives camera permission | Previously tested successfully; repeat after relevant changes |
| SM-08 | Live detection | Show a clear object in reasonable lighting | Bounding boxes and detection labels appear when the model detects the object | Previously tested; results vary by class and lighting |
| SM-09 | Tracking stability | Move one visible object slowly through the frame | Tracking ID generally stays stable while continuously detected | Previously observed; not guaranteed |
| SM-10 | Session statistics | Observe the counters, then use the reset control | Statistics update and reset as designed | User previously confirmed counters worked |
| SM-11 | Stop camera | Stop camera from the dashboard | Camera feed stops | Not recorded |
| SM-12 | API unavailable | Stop API while dashboard is open | Dashboard handles failed requests without freezing | Not recorded |

## 3. Regression checklist

Run the relevant checks after changing the API, model, dashboard, or dependencies.

- [ ] API starts without an exception.
- [ ] `/` returns the expected status JSON.
- [ ] `/health` returns a response.
- [ ] `/docs` loads.
- [ ] A valid image receives a prediction response.
- [ ] Dashboard loads from the local static server.
- [ ] Browser camera can be started and stopped.
- [ ] Bounding boxes and labels draw in the correct approximate positions.
- [ ] Detection count updates as the visible scene changes.
- [ ] Tracking IDs appear and are reasonably stable for continuously visible objects.
- [ ] Session statistics update and reset.
- [ ] An API failure does not permanently break the dashboard.
- [ ] Camera is stopped when testing is finished.

## 4. Test conditions and limitations

Detection results depend on the model, lighting, distance, occlusion, object size, and camera quality. A missed detection does not automatically mean the dashboard is broken.

Known model limitations from previous testing:
- Phone recall was recorded at approximately 39.3%.
- Occasional shoe/motorcycle class confusion was observed.
- Webcam performance was approximately 4–6 FPS on the available older laptop; this is an informal observation.

Tracking IDs are temporary tracker identifiers. They should not be interpreted as reliable real-world identities or a guaranteed count of distinct physical objects.

## 5. Evidence log

For a meaningful test, record enough detail to repeat it.

| Field | Record |
|---|---|
| Date / time | TODO |
| Code version or Git commit | TODO |
| Model checkpoint | `models/best.pt` unless changed |
| Test image / scene | TODO; avoid storing private footage unnecessarily |
| Lighting and distance | TODO |
| Expected result | TODO |
| Actual result | TODO |
| Pass / fail / inconclusive | TODO |
| Notes / error message | TODO |

If a test fails, copy the exact error message and note which step produced it. Change one thing at a time, and avoid recording secrets or private footage in the log.

## 6. Future automated tests

The current guide is primarily a manual checklist. Automated tests can later be added under `tests/`, for example:
- API route tests using FastAPI's test client
- validation tests for missing or invalid uploads
- response-schema tests
- a lightweight smoke test using a small, permitted sample image

Do not add a large model download or webcam requirement to routine automated tests unless there is a clear need.

## 7. Change history

| Date | Change |
|---|---|
| TODO | Initial manual testing guide created from the current prototype notes |
