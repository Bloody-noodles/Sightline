# Project decisions

- Name: Sightline
- Identity: research / engineering project
- Scope: broad computer-vision experimentation
- First milestone: webcam multi-object detection and tracking
- Initial detector: YOLO11n
- Initial tracker: ByteTrack
- Dataset workflow: Roboflow -> Google Drive -> Google Colab
- Initial image size: 640, subject to validation

Principles: establish a reproducible baseline before comparing architectures; evaluate on a held-out test set; document data sources/licences; do not equate augmented images with independent photographs.
