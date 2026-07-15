import streamlit as st

st.title("Test")

try:
    import cv2
    st.success(f"OpenCV Loaded: {cv2.__version__}")
except Exception as e:
    st.error(str(e))


# import streamlit as st
# import cv2
# import av
# import time
# from collections import deque
# from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# import config
# import utils
# from predictor import SignLanguagePredictor
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision

# # ==========================================
# # PAGE CONFIGURATION & CUSTOM CSS
# # ==========================================
# st.set_page_config(page_title="Sign Language AI", layout="wide", initial_sidebar_state="expanded")

# st.markdown("""
#     <style>
#     /* Global Dark Navy Theme & Typography */
#     .stApp {
#         background-color: #050A15; /* Deep Navy Background */
#         color: #F8FAFC;
#         font-family: 'Inter', sans-serif;
#     }
    
#     /* Hero Title & Subtitle */
#     .hero-title {
#         font-size: 2.8rem;
#         font-weight: 900;
#         color: #4A90E2;
#         text-align: center;
#         margin-bottom: 0px;
#         letter-spacing: -1px;
#     }
#     .hero-subtitle {
#         font-size: 1.1rem;
#         color: #94A3B8;
#         text-align: center;
#         margin-top: 5px;
#         margin-bottom: 3rem;
#         font-weight: 400;
#     }
    
#     /* Premium Stats Cards (Glassmorphism) */
#     .stat-container {
#         display: flex;
#         justify-content: space-between;
#         gap: 20px;
#         margin-bottom: 2rem;
#     }
#     .stat-card {
#         flex: 1;
#         background: rgba(15, 23, 42, 0.6);
#         backdrop-filter: blur(12px);
#         padding: 1.5rem;
#         border-radius: 16px;
#         border: 1px solid rgba(255, 255, 255, 0.05);
#         border-top: 4px solid #4A90E2;
#         text-align: center;
#         box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
#     }
#     .stat-value {
#         font-size: 2.2rem;
#         font-weight: 800;
#         color: #FFFFFF;
#         margin-bottom: 0px;
#     }
#     .stat-label {
#         font-size: 0.9rem;
#         color: #94A3B8;
#         text-transform: uppercase;
#         letter-spacing: 1.5px;
#         margin-top: 5px;
#         font-weight: 500;
#     }
    
#     /* Live Analytics Cards (Smaller Secondary Metrics) */
#     .live-card {
#         background: rgba(15, 23, 42, 0.6);
#         backdrop-filter: blur(12px);
#         padding: 1.2rem;
#         border-radius: 12px;
#         border: 1px solid rgba(255, 255, 255, 0.05);
#         border-left: 4px solid #4A90E2;
#         text-align: center;
#         margin-bottom: 15px;
#         box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
#     }
#     .live-value {
#         font-size: 1.8rem;
#         font-weight: 700;
#         color: #4A90E2;
#         margin: 0;
#     }
#     .live-label {
#         font-size: 0.85rem;
#         color: #94A3B8;
#         text-transform: uppercase;
#         letter-spacing: 1px;
#         margin: 0;
#     }
    
#     /* Prominent Gesture Card (Hero Element) */
#     .gesture-card {
#         background: linear-gradient(145deg, rgba(15, 23, 42, 0.9) 0%, rgba(5, 10, 21, 0.9) 100%);
#         backdrop-filter: blur(15px);
#         padding: 2.5rem 1rem;
#         border-radius: 16px;
#         border: 1px solid rgba(74, 144, 226, 0.3);
#         border-top: 6px solid #4A90E2;
#         text-align: center;
#         margin-bottom: 25px;
#         box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(74, 144, 226, 0.05);
#     }
#     .gesture-title {
#         font-size: 1rem;
#         color: #94A3B8;
#         text-transform: uppercase;
#         letter-spacing: 2px;
#         margin-bottom: 10px;
#         font-weight: 600;
#     }
#     .gesture-value {
#         font-size: 75px;
#         font-weight: 900;
#         color: #FFFFFF;
#         text-shadow: 0 0 15px rgba(74, 144, 226, 0.8), 0 0 30px rgba(74, 144, 226, 0.6), 0 0 45px rgba(74, 144, 226, 0.4);
#         margin: 10px 0;
#         display: block;
#         line-height: 1;
#     }
    
#     /* Subtle Animation on Change */
#     .gesture-changed {
#         animation: gesture-pop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) both;
#     }
    
#     @keyframes gesture-pop {
#         0% { transform: scale(0.9); text-shadow: 0 0 30px rgba(74, 144, 226, 1), 0 0 60px rgba(74, 144, 226, 0.8); }
#         50% { transform: scale(1.05); }
#         100% { transform: scale(1); text-shadow: 0 0 15px rgba(74, 144, 226, 0.8), 0 0 30px rgba(74, 144, 226, 0.6), 0 0 45px rgba(74, 144, 226, 0.4); }
#     }
    
#     /* Webcam Container Styling */
#     .webcam-wrapper {
#         border-radius: 16px;
#         overflow: hidden;
#         border: 2px solid rgba(255, 255, 255, 0.1);
#         box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
#         background: #000000;
#         padding: 0;
#         width: 100%;
#     }
#     /* Force WebRTC video to fill the wrapper */
#     .webcam-wrapper video {
#         width: 100% !important;
#         height: auto !important;
#         border-radius: 14px;
#     }
    
#     /* Divider */
#     hr {
#         border-color: rgba(255, 255, 255, 0.1);
#         margin-top: 3rem;
#         margin-bottom: 3rem;
#     }
    
#     /* Sidebar Styling Override */
#     [data-testid="stSidebar"] {
#         background-color: #030712 !important;
#         border-right: 1px solid rgba(255,255,255,0.05);
#     }
#     </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # SIDEBAR: PROFESSIONAL DASHBOARD
# # ==========================================
# with st.sidebar:
#     st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=60)
#     st.title("System Specs")
#     st.markdown("---")
    
#     st.markdown("### 🧠 Model Info")
#     st.markdown(f"**Architecture:** {config.MODEL_NAME}")
#     st.markdown(f"**Feature Extractor:** {config.FEATURE_METHOD}")
#     st.markdown(f"**Target Classes:** 37 (0-9, A-Z, _)")
    
#     st.markdown("---")
#     st.markdown("### ⚡ Real-Time Status")
#     st.markdown("🟢 **System:** Online")
#     st.markdown("🟢 **WebRTC:** Ready")
#     st.markdown("🟢 **Model:** Loaded")
    
#     st.markdown("---")
#     st.markdown("### 🛠️ Tech Stack")
#     st.markdown("`Python 3.14` `OpenCV` `MediaPipe` `Scikit-Learn` `Streamlit`")

# # ==========================================
# # MAIN CONTENT: HERO & STATS
# # ==========================================
# st.markdown('<p class="hero-title">Vision-Based Sign Language Recognition</p>', unsafe_allow_html=True)
# st.markdown('<p class="hero-subtitle">Real-Time Gesture Recognition using MediaPipe, HOG Features, and Random Forest Classification</p>', unsafe_allow_html=True)

# # Static Statistics Cards
# st.markdown("""
#     <div class="stat-container">
#         <div class="stat-card">
#             <p class="stat-value">55,500</p>
#             <p class="stat-label">Dataset Images</p>
#         </div>
#         <div class="stat-card">
#             <p class="stat-value">37</p>
#             <p class="stat-label">Classes Detected</p>
#         </div>
#         <div class="stat-card">
#             <p class="stat-value">99.98%</p>
#             <p class="stat-label">Model Accuracy</p>
#         </div>
#     </div>
# """, unsafe_allow_html=True)

# # ==========================================
# # RESOURCE CACHING (PREVENTS RELOADING)
# # ==========================================
# @st.cache_resource
# def load_ml_engine():
#     return SignLanguagePredictor()

# @st.cache_resource
# def load_mediapipe_engine():
#     base_options = python.BaseOptions(model_asset_path=config.MP_TASK_MODEL_PATH)
#     options = vision.HandLandmarkerOptions(
#         base_options=base_options,
#         running_mode=vision.RunningMode.VIDEO,
#         num_hands=config.MEDIAPIPE_MAX_NUM_HANDS,
#         min_hand_detection_confidence=config.MEDIAPIPE_MIN_DETECTION_CONFIDENCE,
#         min_tracking_confidence=config.MEDIAPIPE_MIN_TRACKING_CONFIDENCE
#     )
#     return vision.HandLandmarker.create_from_options(options)

# predictor = load_ml_engine()
# detector = load_mediapipe_engine()

# # ==========================================
# # WEBRTC VIDEO PROCESSOR
# # ==========================================
# class VideoProcessor:
#     """
#     Handles real-time frame processing. ML pipeline remains strictly unchanged.
#     Text overlays removed from OpenCV frame to favor the dedicated analytics panel.
#     """
#     def __init__(self):
#         self.history_queue = deque(maxlen=config.PREDICTION_HISTORY_SIZE)
#         self.prev_time = time.time()
#         self.last_timestamp_ms = 0
        
#         # State variables for Streamlit Analytics Panel
#         self.current_gesture = "Waiting..."
#         self.current_confidence = 0.0
#         self.current_fps = 0

#     def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
#         img = frame.to_ndarray(format="bgr24")
#         img = cv2.flip(img, 1)

#         rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

#         current_timestamp_ms = int(time.time() * 1000)
#         if current_timestamp_ms <= self.last_timestamp_ms:
#             current_timestamp_ms = self.last_timestamp_ms + 1
#         self.last_timestamp_ms = current_timestamp_ms

#         results = detector.detect_for_video(mp_image, current_timestamp_ms)

#         stable_gesture = "Waiting..."
#         stable_confidence = 0.0
#         bbox_coords = None

#         if results.hand_landmarks:
#             hand_landmarks = results.hand_landmarks[0]
            
#             roi, bbox_coords = utils.extract_hand_roi(img, hand_landmarks)
            
#             if roi.size > 0 and roi.shape[0] > 0 and roi.shape[1] > 0:
#                 features = predictor.extract_hog_features(roi)
                
#                 if features is not None:
#                     raw_gesture, raw_confidence = predictor.predict(features)
#                     stable_gesture, stable_confidence = utils.prediction_smoothing(
#                         self.history_queue, raw_gesture, raw_confidence
#                     )
#         else:
#             self.history_queue.clear()

#         # Update FPS
#         current_time = time.time()
#         fps = int(1 / (current_time - self.prev_time)) if (current_time - self.prev_time) > 0 else 0
#         self.prev_time = current_time

#         # Save to class state for Streamlit metrics
#         self.current_gesture = stable_gesture
#         self.current_confidence = stable_confidence
#         self.current_fps = fps

#         # -----------------------------------------------------
#         # CLEAN CAMERA OVERLAY (Bounding box only)
#         # -----------------------------------------------------
#         is_invalid = stable_gesture in ["Unknown", "Waiting..."]
#         theme_color = (0, 150, 255) if is_invalid else (0, 255, 120)

#         if bbox_coords:
#             x_min, y_min, x_max, y_max = bbox_coords
#             # Thin, clean bounding box only - NO TEXT OVERLAYS
#             cv2.rectangle(img, (x_min, y_min), (x_max, y_max), theme_color, 2)

#         return av.VideoFrame.from_ndarray(img, format="bgr24")

# # ==========================================
# # WEBRTC STREAMER & LIVE ANALYTICS
# # ==========================================
# RTC_CONFIGURATION = RTCConfiguration(
#     {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
# )

# # Layout for Webcam and Analytics Panel: ~70% / 30% Width Split
# col_cam, col_stats = st.columns([2.2, 1], gap="large")

# with col_cam:
#     st.markdown('<div class="webcam-wrapper">', unsafe_allow_html=True)
#     ctx = webrtc_streamer(
#         key="sign-language-stream",
#         mode=WebRtcMode.SENDRECV,
#         rtc_configuration=RTC_CONFIGURATION,
#         video_processor_factory=VideoProcessor,
#         media_stream_constraints={"video": True, "audio": False},
#         async_processing=True,
#     )
#     st.markdown('</div>', unsafe_allow_html=True)

# with col_stats:
#     st.markdown("<h3 style='text-align: center; color: #F8FAFC; margin-bottom: 20px;'>Live Analytics</h3>", unsafe_allow_html=True)
    
#     # Placeholder for live updates
#     analytics_placeholder = st.empty()

# # ==========================================
# # ADDITIONAL STATIC SECTIONS
# # ==========================================
# st.markdown("<hr>", unsafe_allow_html=True)
# st.markdown("### 📋 Project Overview")
# st.markdown("""
# This application bridges the communication gap by translating static sign language gestures into text in real-time. 
# It captures webcam frames, isolates the user's hand utilizing MediaPipe's spatial landmarks, and extracts structural 
# features through a Histogram of Oriented Gradients (HOG) transformation. These features are classified by a Random 
# Forest algorithm trained on 55,500 samples.
# """)

# st.markdown("### ⚙️ Workflow Diagram")
# st.info("Webcam Feed ➔ MediaPipe HandLandmarker ➔ Square ROI Crop ➔ Grayscale ➔ HOG Extraction ➔ StandardScaler ➔ Random Forest ➔ Temporal Smoothing ➔ Output")

# # ==========================================
# # BACKGROUND THREAD POLLING (Must be at the very bottom)
# # ==========================================
# if ctx.state.playing:
    
#     # Variables to track gesture changes for the subtle animation
#     previous_gesture = "Waiting..."
#     last_change_time = 0
    
#     while ctx.state.playing:
#         if ctx.video_processor:
#             g = ctx.video_processor.current_gesture
#             c = ctx.video_processor.current_confidence
#             f = ctx.video_processor.current_fps
            
#             # Detect gesture change and timestamp it
#             if g != previous_gesture:
#                 previous_gesture = g
#                 last_change_time = time.time()
            
#             # Apply the CSS animation class if the gesture changed within the last 0.4 seconds
#             anim_class = "gesture-changed" if (time.time() - last_change_time) < 0.4 else ""
            
#             with analytics_placeholder.container():
#                 st.markdown(f"""
#                     <div class="gesture-card">
#                         <p class="gesture-title">Predicted Gesture</p>
#                         <span class="gesture-value {anim_class}">{g}</span>
#                     </div>
#                     <div class="live-card">
#                         <p class="live-label">Confidence Score</p>
#                         <p class="live-value">{c*100:.1f}%</p>
#                     </div>
#                     <div class="live-card">
#                         <p class="live-label">System FPS</p>
#                         <p class="live-value">{f}</p>
#                     </div>
#                 """, unsafe_allow_html=True)
#         time.sleep(0.1) # Sleep to free up the thread and prevent browser crashing
