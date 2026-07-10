import cv2
import time
from collections import Counter
import config

# Manually defined connections for the 21 MediaPipe Hand Landmarks
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # Pinky
]

def draw_hand_landmarks(frame, hand_landmarks):
    """
    Purpose: Manually draws the connections and nodes for hand tracking without mp.solutions.
    Inputs:  frame -> Image to draw on.
             hand_landmarks -> List of landmark objects from the Tasks API.
    """
    h, w, _ = frame.shape
    
    # Draw connections
    for connection in HAND_CONNECTIONS:
        idx1, idx2 = connection
        lm1, lm2 = hand_landmarks[idx1], hand_landmarks[idx2]
        cx1, cy1 = int(lm1.x * w), int(lm1.y * h)
        cx2, cy2 = int(lm2.x * w), int(lm2.y * h)
        cv2.line(frame, (cx1, cy1), (cx2, cy2), (220, 220, 220), 2)
        
    # Draw landmarks (circles)
    for lm in hand_landmarks:
        cx, cy = int(lm.x * w), int(lm.y * h)
        cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

def extract_hand_roi(frame, hand_landmarks):
    """
    Purpose: Generates bounding box from raw tasks API landmarks and extracts ROI.
    """
    h, w, _ = frame.shape
    
    # Map normalized landmark values into absolute camera frame pixels
    x_coords = [int(lm.x * w) for lm in hand_landmarks]
    y_coords = [int(lm.y * h) for lm in hand_landmarks]
    
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    
    x_min = max(0, x_min - config.PADDING)
    y_min = max(0, y_min - config.PADDING)
    x_max = min(w, x_max + config.PADDING)
    y_max = min(h, y_max + config.PADDING)
    
    roi = frame[y_min:y_max, x_min:x_max]
    bbox = (x_min, y_min, x_max, y_max)
    
    return roi, bbox

def prediction_smoothing(history_queue, raw_gesture, raw_confidence):
    """Dampens jittery predictions using a sliding history queue."""
    history_queue.append((raw_gesture, raw_confidence))
    gestures_only = [item[0] for item in history_queue]
    
    stable_gesture = Counter(gestures_only).most_common(1)[0][0]
    matching_confs = [item[1] for item in history_queue if item[0] == stable_gesture]
    stable_confidence = sum(matching_confs) / len(matching_confs) if matching_confs else 0.0
    
    return stable_gesture, stable_confidence

def calculate_fps(prev_time):
    """Calculates system FPS."""
    current_time = time.time()
    delta = current_time - prev_time
    fps = int(1 / delta) if delta > 0 else 0
    return fps, current_time

def draw_premium_panel(img, pt1, pt2, color, thickness, radius=15):
    """Core drawing helper for rounded UI panels."""
    x1, y1 = pt1
    x2, y2 = pt2
    w, h = x2 - x1, y2 - y1
    radius = min(radius, abs(w) // 2, abs(h) // 2)
    
    if thickness < 0:
        cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, -1)
        cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, -1)
        cv2.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, -1)
        cv2.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, -1)
        cv2.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, -1)
        cv2.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, -1)
    else:
        cv2.line(img, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
        cv2.line(img, (x1 + radius, y2), (x2 - radius, y2), color, thickness)
        cv2.line(img, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
        cv2.line(img, (x2, y1 + radius), (x2, y2 - radius), color, thickness)
        cv2.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)
        cv2.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)

def draw_ui(frame, gesture, confidence, fps, bbox):
    """Clean Professional UI"""

    is_invalid = (gesture in ["Unknown Gesture", "None"])
    gesture_color = (0, 69, 255) if is_invalid else (0, 255, 120)

    # Small Top-Left Card
    overlay = frame.copy()

    cv2.rectangle(overlay, (15, 15), (270, 135), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.45, frame, 0.55, 0, frame)

    cv2.rectangle(frame, (15, 15), (270, 135), (90, 90, 90), 1)

    cv2.putText(
        frame,
        "SIGN LANGUAGE AI",
        (25, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 215, 255),
        2,
        cv2.LINE_AA
    )

    cv2.putText(
        frame,
        f"Gesture : {gesture}",
        (25, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        gesture_color,
        2,
        cv2.LINE_AA
    )

    cv2.putText(
        frame,
        f"Confidence : {confidence * 100:.1f}%",
        (25, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    cv2.putText(
        frame,
        f"FPS : {fps}",
        (25, 123),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    # Tracking Box
    if bbox:
        x_min, y_min, x_max, y_max = bbox

        box_color = (0, 255, 120) if not is_invalid else (0, 165, 255)

        cv2.rectangle(
            frame,
            (x_min, y_min),
            (x_max, y_max),
            box_color,
            2
        )

    return frame