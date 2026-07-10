import cv2
import time
import logging
from collections import deque
import config
from predictor import SignLanguagePredictor
import utils

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# =====================================================================
# GLOBAL LOGGING INFRASTRUCTURE SETUP
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("MainApplication")

def initialize_mediapipe():
    """Initializes the MediaPipe Tasks API HandLandmarker[cite: 3]."""
    try:
        base_options = python.BaseOptions(model_asset_path=config.MP_TASK_MODEL_PATH)
        
        # Configure the landmarker to operate in real-time video stream mode
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=config.MEDIAPIPE_MAX_NUM_HANDS,
            min_hand_detection_confidence=config.MEDIAPIPE_MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MEDIAPIPE_MIN_TRACKING_CONFIDENCE
        )
        detector = vision.HandLandmarker.create_from_options(options)
        return detector
    except Exception as e:
        logger.critical(f"Failed to initialize MediaPipe Tasks API. Ensure '{config.MP_TASK_MODEL_PATH}' exists. Error: {str(e)}")
        raise e

def main():
    logger.info("Booting Sign Language Core Execution Loop Engine...")
    
    try:
        predictor = SignLanguagePredictor()
        detector = initialize_mediapipe()
    except Exception as e:
        logger.critical("Aborting initialization due to missing dependencies.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.critical("Webcam interface connection could not be established.")
        return

    cv2.namedWindow("Sign Language Recognition System", cv2.WINDOW_AUTOSIZE)

    history_queue = deque(maxlen=config.PREDICTION_HISTORY_SIZE)
    stable_gesture = "None"
    stable_confidence = 0.0
    prev_time = time.time()

    logger.info("Application loop entering real-time Tasks API tracking cycle.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            logger.warning("Blank video feed array package frame dropped.")
            continue

        frame = cv2.flip(frame, 1)
        
        # 1. Prepare image for Tasks API (Requires MediaPipe Image object)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Create a unique timestamp in milliseconds for VIDEO mode prediction
        timestamp_ms = int(time.time() * 1000)
        
        # 2. Execute Detection
        results = detector.detect_for_video(mp_image, timestamp_ms)
        
        bbox_coords = None

        # 3. Process Detection Results
        if results.hand_landmarks:
            # The Tasks API returns a list of landmarks per hand. Extract the first hand.
            hand_landmarks = results.hand_landmarks[0]
            
            # Draw our manual UI connections since mp.solutions is unavailable
            utils.draw_hand_landmarks(frame, hand_landmarks)
            
            # Extract Region of Interest
            roi, bbox_coords = utils.extract_hand_roi(frame, hand_landmarks)
            
            if roi.size > 0 and roi.shape[0] > 0 and roi.shape[1] > 0:
                features = predictor.extract_hog_features(roi)
                
                if features is not None:
                    raw_gesture, raw_confidence = predictor.predict(features)
                    
                    stable_gesture, stable_confidence = utils.prediction_smoothing(
                        history_queue, raw_gesture, raw_confidence
                    )
        else:
            if len(history_queue) > 0:
                history_queue.clear()
            stable_gesture = "None"
            stable_confidence = 0.0
            bbox_coords = None

        fps, prev_time = utils.calculate_fps(prev_time)
        frame = utils.draw_ui(frame, stable_gesture, stable_confidence, fps, bbox_coords)

        cv2.imshow("Sign Language Recognition System", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            logger.info("System cycle interrupt triggered.")
            break

    cap.release()
    cv2.destroyAllWindows()
    logger.info("Operational frameworks safely terminated.")

if __name__ == "__main__":
    main()