import os

"""
Module Name: config
Purpose: Centralizes all hyperparameter constants, operational thresholds, 
         and file system path variables.
"""

# =====================================================================
# FILE PATH MANAGEMENT
# =====================================================================
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "sign_language_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")

# MediaPipe Tasks API requires the exported Task model
MP_TASK_MODEL_PATH = os.path.join(MODEL_DIR, "hand_landmarker.task")

# =====================================================================
# MACHINE LEARNING PIPELINE PARAMETERS (Unchanged)
# =====================================================================
ROI_SIZE = (50, 50)  
PADDING = 25         

# HOG Parameters
HOG_ORIENTATIONS = 9
HOG_PIXELS_PER_CELL = (8, 8)
HOG_CELLS_PER_BLOCK = (2, 2)
HOG_BLOCK_NORM = 'L2-Hys'

# =====================================================================
# INFERENCE & SIGNAL STABILITY TUNING
# =====================================================================
CONFIDENCE_THRESHOLD = 0.10    
PREDICTION_HISTORY_SIZE = 5   

# =====================================================================
# MEDIAPIPE CORE COMPONENT TUNING
# =====================================================================
MEDIAPIPE_MIN_DETECTION_CONFIDENCE = 0.7
MEDIAPIPE_MIN_TRACKING_CONFIDENCE = 0.5
MEDIAPIPE_MAX_NUM_HANDS = 1   

# =====================================================================
# METADATA LABELS FOR UI PANEL DISPLAY
# =====================================================================
MODEL_NAME = "Random Forest"
FEATURE_METHOD = "HOG"