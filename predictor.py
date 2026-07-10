import os
import logging
import numpy as np
import joblib
import cv2
from skimage.feature import hog
from skimage.color import rgb2gray
import config

logger = logging.getLogger(__name__)

class SignLanguagePredictor:
    """
    Purpose:
        Encapsulates the full machine learning inference sequence—from inputting a 
        raw image crop, extracting HOG features, running transformations, 
        up to predicting class tags via the Random Forest model.
    """
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.load_models()

    def load_models(self):
        """Loads serialized Scikit-Learn pipelines from disk to memory."""
        try:
            logger.info("Starting model loading operations...")
            
            for path in [config.MODEL_PATH, config.SCALER_PATH, config.LABEL_ENCODER_PATH]:
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Required model file missing: {path}")

            self.model = joblib.load(config.MODEL_PATH)
            self.scaler = joblib.load(config.SCALER_PATH)
            self.label_encoder = joblib.load(config.LABEL_ENCODER_PATH)
            
            logger.info("All pipeline serialized layers mapped into RAM effectively.")
        except Exception as e:
            logger.error(f"Inference Engine crashed during startup: {str(e)}")
            raise e

    def extract_hog_features(self, roi):
        """Formats image matrices to compute Histogram of Oriented Gradients features."""
        try:
            # 1. Resize 
            roi_resized = cv2.resize(roi, config.ROI_SIZE, interpolation=cv2.INTER_AREA)
            
            # 2. Convert to RGB
            roi_rgb = cv2.cvtColor(roi_resized, cv2.COLOR_BGR2RGB)
            
            # 3. Convert to Grayscale
            gray = rgb2gray(roi_rgb)
            
            # 4. Extract HOG
            features = hog(
                gray,
                orientations=config.HOG_ORIENTATIONS,
                pixels_per_cell=config.HOG_PIXELS_PER_CELL,
                cells_per_block=config.HOG_CELLS_PER_BLOCK,
                block_norm=config.HOG_BLOCK_NORM
            )
            return features
        except Exception as e:
            logger.warning(f"Feature vector extraction failed: {str(e)}")
            return None

    def predict(self, features):
        """Maps HOG vectors into target predicted classes."""
        try:
            # Format to 2D array
            features_reshaped = features.reshape(1, -1)
            
            # Scale
            features_scaled = self.scaler.transform(features_reshaped)
            
            # Predict
            probabilities = self.model.predict_proba(features_scaled)[0]
            pred_idx = np.argmax(probabilities)
            confidence = probabilities[pred_idx]
            
            if confidence >= config.CONFIDENCE_THRESHOLD:
                decoded_label = self.decode_prediction(pred_idx)
            else:
                decoded_label = "Unknown Gesture"
            print("Prediction:", decoded_label)
            print("Confidence:", confidence)


            return decoded_label, float(confidence)
        except Exception as e:
            logger.error(f"Prediction processing error: {str(e)}")
            return "Unknown Gesture", 0.0

    def decode_prediction(self, class_index):
        """Decodes integer predictions back to labels (0-9, A-Z, _)."""
        return str(self.label_encoder.inverse_transform([class_index])[0])
    
    

