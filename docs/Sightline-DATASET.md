# Sightline Dataset Record

This document records the dataset used to train Sightline's custom YOLO11n object detector. Update the fields marked **TODO** using the actual Roboflow project and export details.

## Dataset overview

- **Project:** Sightline
- **Annotation and versioning:** Roboflow
- **Task:** Object detection
- **Model family:** Ultralytics YOLO11n
- **Number of classes:** 11
- **Dataset version:** TODO — record the exact Roboflow version
- **Export format:** TODO — confirm the format used for training (for example, YOLO format)
- **Export date:** TODO
- **Dataset archive location:** Private/local or Google Drive location; do not publish private paths or credentials

## Classes and class order

Confirm the exact class order in the exported `data.yaml`. The order matters because class IDs in labels must match this list.

1. `backpack`
2. `book`
3. `bottle`
4. `car`
5. `cup`
6. `handbag`
7. `motorcycle`
8. `person`
9. `phone`
10. `shoe`
11. `sunglasses`

**Important:** This is the intended class list. Before reproducing training, compare it with the `names` field in the exact `data.yaml` used for the recorded run.

## Image sources and collection

The dataset was assembled for this project rather than relying on a ready-made pretrained detection dataset. Collection methods included:

- Photos captured using a mobile phone camera.
- Images sourced from Unsplash.
- Images sourced from Pexels.
- Images found through Google Images, with the original source and licence checked where possible.

Record the actual source and usage terms for each image or source batch. A search-engine result is not itself a licence to reuse an image. Before sharing the dataset or its images publicly, check the original source's licence and whether machine-learning training and redistribution are permitted.

## Annotation and dataset versioning

Images were uploaded to Roboflow for annotation and versioning.

Before creating or exporting a dataset version:

- Check that each visible target object is labelled with the correct class.
- Check that bounding boxes fit the visible object and do not include excessive background.
- Keep class definitions consistent (especially visually confusable categories such as `shoe` and `motorcycle`).
- Review small, blurry, occluded, and low-light objects carefully.
- Check for duplicate or near-duplicate images across training, validation, and test splits.
- Confirm the class IDs and names in `data.yaml`.
- Record any preprocessing or augmentation applied by Roboflow.

## Split and image counts

Fill in these values from the exact Roboflow version used for training.

| Split | Image count | Notes |
|---|---:|---|
| Train | TODO | Confirm from exported dataset |
| Validation | TODO | Confirm from exported dataset |
| Test | TODO | Confirm from exported dataset |
| **Total** | **TODO** | Avoid counting the same image more than once |

Also record per-class instance counts if available. Image counts and labelled-object counts are different measurements.

## Training export and integrity checks

The training workflow used Google Colab and a dataset archive stored in Google Drive.

Before training, verify:

1. The ZIP archive corresponds to the recorded Roboflow version.
2. The archive extracts successfully.
3. `data.yaml` points to valid image directories for each split.
4. Class names and class order match the list above.
5. Image and label files exist and correspond to one another.
6. Labels use the expected YOLO bounding-box format.
7. Train, validation, and test splits are present and not accidentally mixed.

Do not include private Drive paths, access tokens, API keys, or other credentials in this document.

## Known model-evaluation observation

The recorded baseline had lower recall for the `phone` class than desired (approximately 39.3% in the evaluation discussed for this project). This is a model-performance observation, not proof of a dataset error. Potential factors include class representation, object size, lighting, viewpoint, and annotation consistency.

The model has also occasionally confused visually similar or difficult examples, such as a shoe being classified as a motorcycle. These failures should be recorded and investigated rather than hidden.

## Reproducibility checklist

- [ ] Record Roboflow project name/ID and exact dataset version.
- [ ] Record export format, export date, and preprocessing settings.
- [ ] Record exact train/validation/test image counts.
- [ ] Verify `data.yaml` class order.
- [ ] Record per-class labelled-object counts where available.
- [ ] Check source licences and permitted ML-training use.
- [ ] Preserve a copy of the exact dataset configuration used for training.
- [ ] Link this record to the corresponding entry in `docs/EXPERIMENT_LOG.md`.

## Change history

| Date | Change |
|---|---|
| TODO | Initial dataset record; replace with the date this file is committed |
