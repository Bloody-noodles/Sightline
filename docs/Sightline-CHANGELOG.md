# Sightline — Changelog

This file records user-visible changes to Sightline. Add an entry whenever a meaningful feature, behaviour, model, dependency, or documentation change is made.

Use dates in `YYYY-MM-DD` format where known. If the exact date is unknown, leave it as `TODO` rather than guessing.

## Unreleased

### Added
- Supporting project documentation for dataset, experiments, API usage, testing, privacy/security, deployment, roadmap, and architecture.

### Notes
- Confirm the current contents of each document and the actual code before publishing a release.

## Prototype history

### TODO — Custom model and local inference
- Added a custom YOLO11n checkpoint at `models/best.pt`.
- Integrated model inference into a local FastAPI service.
- Added `/`, `/health`, and `/predict` API routes.

### TODO — Browser webcam dashboard
- Added a browser dashboard in `app/index.html` and `app/style.css`.
- Connected the dashboard to the local API.
- Added bounding-box overlays and detection labels.

### TODO — Object tracking
- Enabled tracking through Ultralytics with ByteTrack.
- Displayed tracking IDs in the dashboard.
- Observed stable IDs while objects remained continuously visible during manual testing.

### TODO — Session statistics
- Added session-level tracking-ID statistics and detection counts.
- Added a reset control for session statistics.

### TODO — Static frontend hosting
- Published a static frontend Space at:
  `https://huggingface.co/spaces/rigidmayor7/Sightline`
- The hosted Space is a frontend presentation layer; the Python inference API remains a separate service.

## Changelog entry template

Copy this template for future changes:

### YYYY-MM-DD — Short title

#### Added
- 

#### Changed
- 

#### Fixed
- 

#### Known limitations
- 

#### Verification
- Tests run:
- Result:
- Model/dataset version (if relevant):

## Versioning guidance

For an early prototype, informal labels such as `prototype-0.1` can be useful, but do not assign a version number until you decide what the release represents.

When you start tagging releases:
- Record the code commit or tag.
- Record the matching model checkpoint and dataset version.
- Record any changes to API request/response formats.
- Note breaking changes and known limitations.
- Do not include private model weights or sensitive test footage in a public release by accident.

## Change history

| Date | Change |
|---|---|
| TODO | Initial changelog drafted from recorded prototype history |
