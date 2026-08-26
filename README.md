# AI Gym Coach 🏋️

An AI-powered fitness coaching web app that provides real-time workout guidance and feedback, combining computer vision, natural language processing, and voice feedback.

## Features

- **Real-time Pose Detection** – Tracks exercise form using computer vision
- **AI Coach** – Powered by the Groq API to analyze performance and generate personalized feedback
- **Voice Feedback** – Delivers coaching cues via text-to-speech alongside on-screen text
- **Workout Metrics** – Tracks and logs exercise data for progress monitoring
- **Web-based Interface** – Built with Streamlit, runs directly in the browser

## Tech Stack

- **Frontend/UI:** Streamlit
- **Backend:** Python
- **AI/LLM:** Groq API
- **Computer Vision:** MediaPipe / OpenCV
- **Voice:** Text-to-Speech pipeline

## Project Structure

Main App/
├── core/ # Core application logic
├── detectors/ # Pose/exercise detection modules
├── ml_models/ # Machine learning models
├── pages/ # Streamlit pages
├── services/
│ ├── auth/ # Authentication
│ └── coaching/ # AI coaching logic (LLM, TTS, voice pipeline)
├── static/ # Static assets
└── main.py # App entry point


## Setup & Installation

1. Clone the repository:
```bash
   git clone https://github.com/ashwinijain30/AI-Gym-Coach.git
   cd AI-Gym-Coach/Main App
```

2. Create a virtual environment and install dependencies:
```bash
   python -m venv venv
   venv\Scripts\Activate.ps1
   pip install -r requirements.txt
```

3. Add your API keys to a `.env` file (not tracked by git):
4. 
4. Run the app:
```bash
   streamlit run main.py
```

## Status

🚧 Actively in development — some features (like voice feedback) are still being debugged.

## Acknowledgments

Built as part of a course project, with code adapted and extended from a base GitHub repository.
