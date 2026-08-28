# 🏋️ AI Real-time GYM Coach

A real-time AI-powered fitness coaching application that uses computer vision, exercise-specific form analysis, LLM-based coaching, and voice feedback to act like a virtual gym trainer.

## 🚀 Live Demo

[Open the AI Real-time GYM Coach](https://ai-gym-coach-ashwini.streamlit.app/)

## 📌 Overview

AI Real-time GYM Coach analyzes a user's workout through a webcam and provides real-time feedback on exercise performance.

The application combines:

- Computer Vision for real-time pose detection
- MediaPipe and OpenCV for body landmark and movement analysis
- Rule-based exercise detectors for form checking and repetition tracking
- Groq API for AI-generated coaching feedback
- gTTS for voice feedback
- Streamlit and WebRTC for the interactive web interface
- SQLite for workout history and persistence

## ✨ Features

### 🧍 Real-Time Pose Detection

The application processes webcam video and analyzes body movement using MediaPipe and OpenCV.

### 🏋️ Supported Exercises

- Squats
- Push-ups
- Biceps Curls (Dumbbell)
- Shoulder Press
- Lunges

### 🔢 Rep and Set Tracking

The application tracks:

- Total repetitions
- Current set progress
- Completed sets
- Workout duration/history

### ⚠️ Exercise Form Analysis

Different exercises use different metrics to evaluate form.

Examples include:

- Squats: knee angle, back angle, and depth
- Push-ups: elbow angle, body alignment, and hip position
- Biceps curls: elbow angle, shoulder stability, and swing detection
- Shoulder press: elbow angle, arm extension, and back arch
- Lunges: front knee angle, torso angle, and balance

### 🤖 AI Coaching

The application integrates the Groq API to generate contextual coaching feedback based on workout events and performance.

### 🔊 Voice Coaching

The coaching feedback can be converted into speech using gTTS, providing an interactive trainer-like experience.

### 🔐 User Login and Workout History

The application includes a login system and stores workout information using SQLite.

### 🎥 Real-Time WebRTC Video

WebRTC is used to stream webcam video to the Streamlit application for real-time exercise analysis.

## 🏗️ System Architecture

```text
User
  │
  ▼
Webcam Video
  │
  ▼
Streamlit + WebRTC
  │
  ▼
MediaPipe / OpenCV
  │
  ▼
Body Landmark & Movement Analysis
  │
  ▼
Exercise Detector
  │
  ├── Rep Counting
  ├── Set Tracking
  └── Form Analysis
  │
  ▼
Workout Metrics
  │
  ▼
AI Coaching Layer
  │
  ├── Groq API
  └── gTTS
  │
  ▼
Voice + On-Screen Feedback
  │
  ▼
SQLite Workout History
```

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Web Framework | Streamlit |
| Real-Time Video | streamlit-webrtc |
| Computer Vision | MediaPipe, OpenCV |
| Data Processing | Pandas |
| AI / LLM | Groq API |
| Text-to-Speech | gTTS |
| Database | SQLite |
| Styling | CSS |
| Configuration | python-dotenv |

## 📂 Project Structure

```text
AI-Gym-Coach/
│
├── .streamlit/
│   └── config.toml
│
├── core/
│   └── Base exercise logic
│
├── detectors/
│   ├── squat.py
│   ├── pushup.py
│   ├── biceps_curl.py
│   ├── shoulder_press.py
│   └── lunges.py
│
├── ml_models/
│
├── pages/
│
├── services/
│   ├── auth/
│   ├── coaching/
│   ├── config/
│   ├── persistence/
│   ├── state/
│   ├── tracking/
│   ├── ui/
│   └── vision/
│
├── static/
│   ├── style.css
│   └── AdobeClean.otf
│
├── tutorial-info/
│
├── data.db
├── main.py
├── packages.txt
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/ashwinijain30/AI-Gym-Coach.git
cd AI-Gym-Coach
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Setup

The application uses the Groq API for AI coaching.

Create a `.env` file locally:

```env
GROQ_API_KEY=your_api_key_here
```

Never commit the `.env` file or your API key to GitHub.

For Streamlit Cloud deployment, add the key through the application's **Secrets** settings instead of putting it in the repository.

## ▶️ Run Locally

From the project root:

```bash
streamlit run main.py
```

The application will normally be available at:

```text
http://localhost:8501
```

## 🎮 How to Use

1. Open the application.
2. Enter a unique username.
3. Select an exercise.
4. Select the number of sets.
5. Select repetitions per set.
6. Click **Start Workout**.
7. Allow webcam access when requested.
8. Perform the selected exercise in front of the camera.
9. Monitor repetitions, sets, and form metrics.
10. Receive AI coaching and voice feedback.
11. End the workout to save the session/history.

## 📊 Workout Metrics

The application displays exercise-specific metrics and workout progress.

### Squats

- Knee Angle
- Back Angle
- Depth

### Push-ups

- Elbow Angle
- Body Alignment
- Hip Position

### Biceps Curls

- Elbow Angle
- Shoulder Stability
- Swing Detection

### Shoulder Press

- Elbow Angle
- Arm Extension
- Back Arch

### Lunges

- Front Knee Angle
- Torso Angle
- Balance

## ☁️ Deployment

The application is deployed using Streamlit Community Cloud.

Deployment configuration:

```text
Repository: ashwinijain30/AI-Gym-Coach
Branch: main
Entry point: main.py
```

The Groq API key should be configured as a Streamlit secret:

```toml
GROQ_API_KEY = "your_api_key_here"
```

## 🔒 Security

- Do not upload `.env` files containing API keys.
- Do not hard-code API keys in Python files.
- Use Streamlit Secrets for cloud deployment.
- Do not expose private credentials in the GitHub repository.

## 🔮 Future Improvements

- Personalized workout plans
- More exercise detectors
- Advanced workout analytics
- Fatigue detection
- Improved posture scoring
- More robust multi-user support
- Mobile-friendly experience
- Cloud database integration
- More natural and personalized AI coaching

## ⚠️ Disclaimer

This application is intended for educational and fitness-assistance purposes. It is not a substitute for a certified personal trainer, physiotherapist, or medical professional. Users should exercise safely and stop if they experience pain, dizziness, or discomfort.

## 👩‍💻 Author

**Ashwini Jain**

GitHub: https://github.com/ashwinijain30

## ⭐ Project

If you find this project useful, consider giving the repository a star and sharing feedback.
