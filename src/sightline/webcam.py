
from pathlib import Path
import time

import cv2
import torch
from ultralytics import YOLO


# ============================================================
# SIGHTLINE CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "best.pt"

CAMERA_INDEX = 0

CAMERA_WIDTH = 480
CAMERA_HEIGHT = 360

# Smaller inference images reduce CPU workload.
IMAGE_SIZE = 320

# Minimum confidence passed to YOLO/ByteTrack.
TRACK_CONFIDENCE = 0.15

# Run inference approximately four times per second.
INFERENCE_INTERVAL = 0.25

# Display thresholds by class.
# Lower phone threshold temporarily helps us investigate
# why phones are not being detected.
CLASS_THRESHOLDS = {
    "person": 0.60,
    "phone": 0.15,
}

DEFAULT_DISPLAY_CONFIDENCE = 0.30


def get_display_threshold(class_name):
    return CLASS_THRESHOLDS.get(
        class_name,
        DEFAULT_DISPLAY_CONFIDENCE,
    )


def main():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"\nSightline model not found:\n{MODEL_PATH}\n\n"
            "Place your trained best.pt file inside models/."
        )

    # Limit CPU threads for this older dual-core laptop.
    torch.set_num_threads(2)
    cv2.setNumThreads(1)

    print("=" * 48)
    print("SIGHTLINE - CPU OPTIMIZED WEBCAM TRACKER")
    print("=" * 48)
    print(f"Model: {MODEL_PATH}")
    print(f"Inference size: {IMAGE_SIZE}")
    print(f"Inference interval: {INFERENCE_INTERVAL}s")
    print("Loading model...")

    model = YOLO(str(MODEL_PATH))

    print("Model loaded successfully.")
    print("Classes:", model.names)

    # Open webcam using Windows DirectShow first.
    camera = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

    if not camera.isOpened():
        camera.release()
        camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        raise RuntimeError(
            "Cannot open webcam. Close other camera applications "
            "and check Windows camera permissions."
        )

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    last_inference_time = 0.0
    last_annotated = None

    displayed_fps = 0.0
    previous_display_time = time.perf_counter()

    print("\nSightline is running.")
    print("Show objects to your webcam.")
    print("Press Q in the video window to quit.\n")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Unable to read webcam frame.")
                break

            now = time.perf_counter()

            # Run the expensive model only at the chosen interval.
            if (
                last_annotated is None
                or now - last_inference_time >= INFERENCE_INTERVAL
            ):
                results = model.track(
                    source=frame,
                    persist=True,
                    tracker="bytetrack.yaml",
                    conf=TRACK_CONFIDENCE,
                    imgsz=IMAGE_SIZE,
                    verbose=False,
                )

                result = results[0]

                # Filter displayed boxes by class-specific confidence.
                # The trained model itself is not modified.
                if result.boxes is not None and len(result.boxes) > 0:
                    class_ids = result.boxes.cls.int().tolist()
                    confidences = result.boxes.conf.tolist()

                    keep = [
                        i
                        for i, (class_id, confidence) in enumerate(
                            zip(class_ids, confidences)
                        )
                        if confidence >= get_display_threshold(
                            model.names[class_id]
                        )
                    ]

                    result.boxes = result.boxes[keep]

                last_annotated = result.plot()
                last_inference_time = time.perf_counter()

            # Calculate approximate displayed loop FPS.
            display_now = time.perf_counter()
            elapsed = display_now - previous_display_time
            previous_display_time = display_now

            if elapsed > 0:
                instant_fps = 1.0 / elapsed
                displayed_fps = (
                    instant_fps
                    if displayed_fps == 0
                    else 0.8 * displayed_fps + 0.2 * instant_fps
                )

            # Show FPS and inference size.
            cv2.putText(
                last_annotated,
                f"Sightline | Loop: {displayed_fps:.1f} FPS",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

            cv2.putText(
                last_annotated,
                f"Input: {IMAGE_SIZE} | Phone conf: "
                f"{CLASS_THRESHOLDS['phone']:.2f}",
                (10, 49),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 255),
                1,
                cv2.LINE_AA,
            )

            cv2.imshow(
                "Sightline | Detection + Tracking",
                last_annotated,
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\nStopping Sightline...")

    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("Sightline stopped.")


if __name__ == "__main__":
    main()