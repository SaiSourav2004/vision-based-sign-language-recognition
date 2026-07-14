<div align="center">

# 🤟 Vision-Based Sign Language Recognition System

**Real-Time Gesture Translation using Machine Learning, HOG Features, and MediaPipe**

[![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Tasks_API-00BFA5?style=for-the-badge&logo=google&logoColor=white)](https://developers.google.com/mediapipe)
[![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

*Bridging the communication gap with high-speed, edge-optimized Computer Vision.*

---

<!-- 💡 PRO TIP: Record a 10-second GIF of your working Streamlit app and replace the link below -->
<!-- <img src="https://via.placeholder.com/800x400/1A202C/4A90E2?text=Insert+Demo+GIF+Here" alt="Project Demo" width="800"/> -->
<img width="1639" height="960" alt="ChatGPT Image Jul 14, 2026, 07_35_01 PM" src="https://github.com/user-attachments/assets/bd34ff68-6337-472a-8eb8-ca63b3c939a4" />


</div>

## 📖 Project Overview

The **Vision-Based Sign Language Recognition System** is a real-time, end-to-end machine learning application designed to translate static sign language gestures into text. By leveraging Google's MediaPipe Tasks API for precise spatial tracking and extracting Histogram of Oriented Gradients (HOG), this system achieves exceptional classification accuracy using a highly optimized Random Forest engine. 

Deployed as a modern web application via Streamlit and WebRTC, the project processes live webcam feeds entirely in the browser with zero deep-learning overhead.

## ✨ Key Features

*   ⚡ **Low-Latency Real-Time Inference:** Processes live video streams at 30+ FPS on standard CPU hardware.
*   ✋ **Precision Hand Tracking:** Utilizes the modern MediaPipe `vision.HandLandmarker` Tasks API.
*   📐 **Geometric Distortion Prevention:** Implements dynamic 1:1 aspect ratio square bounding boxes to preserve HOG spatial integrity.
*   🧠 **Advanced Feature Engineering:** Extracts robust HOG shape/edge descriptors, normalized via `StandardScaler`.
*   🛡️ **Temporal Smoothing:** Employs historical majority-voting queues to eliminate UI flickering and stabilize predictions.
*   🌐 **Cloud-Ready Web Interface:** Interactive, glassmorphism-styled Streamlit frontend with WebRTC live-streaming.

## 🧠 System Architecture & Workflow

> **Webcam Feed** ➔ **MediaPipe HandLandmarker** ➔ **Square ROI Crop** ➔ **Grayscale Conversion** ➔ **HOG Extraction** ➔ **StandardScaler** ➔ **Random Forest** ➔ **Temporal Smoothing** ➔ **UI Output**

## 📊 Dataset & Model Performance

The inference engine was trained on a custom curated dataset, evaluating multiple ML algorithms to find the perfect balance between speed and precision.

### Dataset Specifications
| Metric | Detail |
| :--- | :--- |
| **Total Images** | 55,500 |
| **Total Classes** | 37 (Digits `0-9`, Alphabets `A-Z`, Special `_`) |
| **Class Distribution** | ~1,500 images per class |
| **Input Dimensions** | 50 x 50 x 3 (RGB) |

### Algorithm Evaluation
| Algorithm | Validation Accuracy | Deployment Status |
| :--- | :--- | :--- |
| 🏆 **Random Forest** | **99.98%** | **Deployed (Production)** |
| 🥈 K-Nearest Neighbors (KNN) | 99.36% | Evaluated |
| 🥉 Decision Tree | 97.14% | Evaluated |
| ❌ Gaussian Naive Bayes | 87.78% | Evaluated |

## 🛠️ Technology Stack

<details>
<summary>Click to expand full technology stack</summary>

*   **Core Language:** Python 3.14
*   **Computer Vision:** OpenCV (`opencv-python-headless`), Scikit-Image
*   **Spatial Tracking:** MediaPipe (Tasks API / `hand_landmarker.task`)
*   **Machine Learning:** Scikit-Learn, NumPy, Joblib
*   **Web Framework:** Streamlit, Streamlit-WebRTC
</details>

## 📂 Repository Structure

```text
vision-sign-language/
│
├── models/
│   ├── sign_language_model.pkl    # Trained Random Forest classifier weights
│   ├── scaler.pkl                 # StandardScaler normalization matrix
│   ├── label_encoder.pkl          # Target label alphanumeric decoder
│   └── hand_landmarker.task       # MediaPipe Tasks API binary
│
├── app.py                         # Premium Streamlit WebRTC application
├── detect_app.py                  # OpenCV local desktop testing application
├── predictor.py                   # Isolated Machine Learning inference engine
├── utils.py                       # Core utilities (ROI, Smoothing, Bounding Boxes)
├── config.py                      # Centralized hyperparameters and system thresholds
├── requirements.txt               # Deployment dependencies
└── README.md                      # Project documentation
🚀 Installation & Setup
Follow these steps to deploy the project locally.

1. Clone the repository

Bash
git clone [https://github.com/yourusername/vision-sign-language.git](https://github.com/yourusername/vision-sign-language.git)
cd vision-sign-language
2. Initialize Virtual Environment

Bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
3. Install Dependencies

Bash
pip install -r requirements.txt
4. Model Placement
Ensure that sign_language_model.pkl, scaler.pkl, label_encoder.pkl, and hand_landmarker.task are downloaded and placed securely inside the /models directory.

💻 Usage
Launch the Professional Streamlit Web Application:

Bash
streamlit run app.py
The application will automatically launch in your default web browser. Grant webcam permissions when prompted.

Launch the Local OpenCV Desktop Version:

Bash
python detect_app.py
Press ESC to gracefully terminate the OpenCV hardware loop.

🔮 Future Scope
Sequence Modeling: Integrate LSTMs or Transformers to translate continuous, moving sign language sequences.

Mobile Edge Deployment: Convert the Random Forest inference engine to TensorFlow Lite or ONNX for native Android/iOS integration.

Expanded Vocabulary: Scale the dataset to include two-handed signs and contextual ASL phrasing.

Developed for the Capstone Project / Final Year Presentation

Computer Vision • Machine Learning • UI/UX Architecture
