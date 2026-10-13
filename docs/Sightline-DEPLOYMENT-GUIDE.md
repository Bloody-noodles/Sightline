# Sightline — Deployment Guide

This guide describes the current local prototype and outlines safe next steps if you later decide to host Sightline. The current hosted Hugging Face Space is a static frontend; it does not run the Python inference API.

## 1. Current architecture

### Local development

- Browser dashboard: `http://127.0.0.1:5500`
- FastAPI service: `http://127.0.0.1:8000`
- Model checkpoint: `models/best.pt`
- API module: `src/sightline/api.py`

The browser sends webcam frames to the local API, which runs the model and returns detections. ByteTrack is used by the API for tracking.

### Hosted static frontend

Current Space:

`https://huggingface.co/spaces/rigidmayor7/Sightline`

A static Space can serve HTML, CSS, and JavaScript, but it does not automatically run the local Python API. The hosted HTTPS page also cannot use `127.0.0.1` to reach the developer's computer: in a browser, `127.0.0.1` refers to the device running that browser.

Do not point the public frontend at `http://127.0.0.1:8000` and expect it to work for other visitors.

## 2. Run locally

Open a terminal at the project root:

```powershell
cd C:\Users\PC\Desktop\Sightline
.\.venv\Scripts\Activate.ps1
python -m uvicorn sightline.api:app --app-dir src --reload
```

In a second terminal:

```powershell
python -m http.server 5500 --directory app
```

Open:

- Dashboard: `http://127.0.0.1:5500`
- API docs: `http://127.0.0.1:8000/docs`

Keep both terminals running while testing. Stop each server with `Ctrl+C`.

## 3. Hosting choices for future work

Choose a deployment option only when you need remote inference. Check current free-tier limits, sleep behaviour, storage, hardware availability, and terms before committing to a provider; these can change.

### Option A — Keep it local

**Best for:** learning, demos on your own laptop, and keeping inference local.

Advantages:
- No separate hosting service required.
- Webcam frames can be processed by the local API.
- Easier to debug.

Limitations:
- The API is available only on the machine unless deliberately networked.
- CPU inference is slow on older hardware.
- Other people cannot use your local API from the public website.

### Option B — Host the frontend only

**Best for:** presenting the design and explaining the project.

Advantages:
- Lightweight static hosting.
- Can share a public project page.

Limitations:
- No Python inference is provided by static hosting alone.
- Live detection requires a reachable inference backend or a separate client-side model implementation.

### Option C — Host the API separately

**Best for:** a shareable live demo where a remote server performs inference.

Before selecting a provider, confirm:
- Python process and model weights are supported.
- Available RAM/CPU/GPU are adequate.
- The service can accept image uploads and handle request timeouts.
- Persistent storage or model-download setup is understood.
- Free-tier quotas and sleep behaviour are acceptable.
- HTTPS, authentication, CORS, upload limits, and privacy controls can be configured.

A hosted backend must have its own reachable HTTPS URL. The frontend should call that configured backend URL, not `localhost`.

**Budget note:** A free option may be possible, but it is not guaranteed to be fast, always awake, or available indefinitely. Check current provider terms before choosing one.

## 4. Safe deployment sequence

Do not expose the current development API publicly as-is. A safer sequence is:

1. Finish local testing and record known limitations.
2. Separate development settings from deployment settings.
3. Add upload size limits and robust image validation.
4. Add authentication or another appropriate access control if the API should not be open to everyone.
5. Configure HTTPS and restrict CORS to the exact frontend origin.
6. Avoid logging image contents or secrets.
7. Verify how webcam frames are processed, transmitted, and retained.
8. Test invalid uploads, slow requests, server restarts, and resource limits.
9. Deploy the API to a suitable host.
10. Update the frontend to use the deployed HTTPS API URL.
11. Test from a different device/network without exposing your personal laptop.
12. Publish clear setup, privacy, and limitations notes.

## 5. Configuration reminder

Do not hard-code a public backend URL until the backend actually exists and has been tested. For local development, the dashboard currently calls:

`http://127.0.0.1:8000/predict`

When a backend is deployed, update the frontend API base URL and the backend CORS configuration together. Never use a wildcard CORS policy as a substitute for authentication.

## 6. Release checklist

- [ ] Local API and dashboard tests pass.
- [ ] Model file and dataset rights have been reviewed.
- [ ] Deployment host and current plan limits have been checked.
- [ ] API upload limits and error handling are implemented.
- [ ] HTTPS is enabled for remote access.
- [ ] CORS allows only the intended frontend origin(s).
- [ ] Authentication/access control is appropriate for the demo.
- [ ] No private footage, credentials, or model weights are accidentally published.
- [ ] Webcam start/stop and data-retention behaviour have been tested.
- [ ] Public page explains the prototype's limitations.
- [ ] Tested from a second device or network.

## 7. Change history

| Date | Change |
|---|---|
| TODO | Initial deployment guide created for the local prototype and static frontend |
