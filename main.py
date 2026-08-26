import os
import time
import streamlit as st
import pandas as pd

from groq import Groq
from streamlit_webrtc import webrtc_streamer, WebRtcMode

from services.auth.login_wall import render_login_wall
from services.state.session_defaults import initial_session_defaults
from services.config.workout_config import EXERCISE_OPTIONS
from services.ui.style_loader import (
    load_css,
    inject_local_font,
    inject_webrtc_styles,
)
from services.persistence.exercise_repository import (
    init_db,
    get_users_exercises,
)
from services.vision.exercise_video_processor import VideoProcessorClass
from services.tracking.metrics import sync_metrics_update

from services.coaching.llm import LLMCoach
from services.coaching.tts import TextToSpeech
from services.coaching.voice_pipeline import (
    VoicePipeline,
    autoplay_audio,
)


def main():

    st.set_page_config(
        page_title="AI Real-time GYM Coach",
        page_icon="🏋️‍♂️",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    load_css(os.path.join(os.getcwd(), "static", "style.css"))
    inject_local_font(
        os.path.join(os.getcwd(), "static", "AdobeClean.otf"),
        "AdobeClean",
    )

    init_db()

    if not render_login_wall():
        return

    initial_session_defaults()

    # --------------------------
    # Audio Queue
    # --------------------------
    if "audio_queue" not in st.session_state:
        st.session_state.audio_queue = []

    if "coach_feedback" not in st.session_state:
        st.session_state.coach_feedback = ""

    if "voice_pipeline" not in st.session_state:

        try:

            api_key = os.environ.get("GROQ_API_KEY", "")

            if (
                not api_key
                and hasattr(st, "secrets")
                and "GROQ_API_KEY" in st.secrets
            ):
                api_key = st.secrets["GROQ_API_KEY"]

            groq_client = Groq(api_key=api_key)

            llm = LLMCoach(groq_client)

            tts = TextToSpeech()

            st.session_state.voice_pipeline = VoicePipeline(
                llm,
                tts,
            )

        except Exception as e:

            st.session_state.voice_pipeline = None
            st.error(f"Voice Pipeline Error : {e}")

    workout_started = st.session_state.get(
        "workout_started",
        False,
    )

    with st.sidebar:

        st.title("🏋️ AI Coach")

        if st.session_state.username:
            st.caption(
                f"👤 Logged in as {st.session_state.username}"
            )

        st.divider()

        st.subheader("Workout Plan")

        if not workout_started:

            exercise = st.selectbox(
                "Exercise",
                EXERCISE_OPTIONS,
            )

            sets = st.number_input(
                "Sets",
                min_value=1,
                max_value=50,
                value=3,
            )

            reps = st.number_input(
                "Reps per Set",
                min_value=1,
                max_value=50,
                value=10,
            )

            if st.button(
                "Start Workout",
                use_container_width=True,
            ):

                st.session_state.exercise_type = exercise
                st.session_state.target_sets = int(sets)
                st.session_state.reps_per_set = int(reps)

                st.session_state.reps = 0
                st.session_state.workout_started = True

                st.session_state.last_saved_sets_completed = 0
                st.session_state.set_cycle_started_at = time.time()

                if st.session_state.voice_pipeline:

                    result = (
                        st.session_state.voice_pipeline.process_event(
                            event="workout_started",
                            exercise=exercise,
                            metrics={},
                        )
                    )

                    if result:

                        audio, feedback = result

                        if audio:
                            st.session_state.audio_queue.append(audio)

                        st.session_state.coach_feedback = feedback

                st.rerun()

        else:

            exercise = st.session_state.exercise_type

            st.info(
                f"""
**Exercise :** {exercise}

**Sets :** {st.session_state.target_sets}

**Reps :** {st.session_state.reps_per_set}
"""
            )

            if st.button(
                "End Workout",
                use_container_width=True,
            ):

                st.session_state.workout_started = False

                if st.session_state.voice_pipeline:

                    result = (
                        st.session_state.voice_pipeline.process_event(
                            event="workout_completed",
                            exercise=exercise,
                            metrics={},
                        )
                    )

                    if result:

                        audio, feedback = result

                        if audio:
                            st.session_state.audio_queue.append(audio)

                        st.session_state.coach_feedback = feedback

                st.rerun()
                    # ==============================
    # MAIN PAGE
    # ==============================

    st.title("🏋️ AI Real-time GYM Coach")
    st.markdown("#### Real-time pose detection with proactive AI voice coaching")

    # --------------------------------
    # Play queued audio (ONE clip only)
    # --------------------------------
    if st.session_state.audio_queue:
        audio = st.session_state.audio_queue.pop(0)
        autoplay_audio(audio)

    # Coach Feedback
    if st.session_state.coach_feedback:
        st.success(
            f"🤖 Coach:\n\n{st.session_state.coach_feedback}"
        )

    # ==============================
    # WAITING SCREEN
    # ==============================

    if not workout_started:

        st.markdown(
            """
            <div style="
                border:4px dashed #888;
                padding:40px;
                text-align:center;
                border-radius:15px;
            ">
            <h2>👈 Configure your workout</h2>

            <p>Select Exercise → Sets → Reps</p>

            <p>Then click <b>Start Workout</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        context = webrtc_streamer(
            key="exercise-analysis",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=VideoProcessorClass,
            rtc_configuration={
                "iceServers": [
                    {
                        "urls": [
                            "stun:stun.l.google.com:19302"
                        ]
                    }
                ]
            },
            media_stream_constraints={
                "video": True,
                "audio": False,
            },
            async_processing=True,
        )

        sync_metrics_update(context)

        # --------------------------
        # Progress
        # --------------------------

        st.divider()

        st.subheader("Workout Progress")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Reps",
            st.session_state.get("reps", 0),
        )

        col2.metric(
            "Current Set",
            f"{st.session_state.get('current_set_reps',0)} / "
            f"{st.session_state.get('reps_per_set',0)}",
        )

        col3.metric(
            "Completed Sets",
            f"{st.session_state.get('sets_completed',0)} / "
            f"{st.session_state.get('target_sets',0)}",
        )

        exercise = st.session_state.get("exercise_type")

        st.divider()

        if exercise == "Squats":

            st.subheader("Squat Metrics")

            st.metric(
                "Knee Angle",
                f"{st.session_state.knee_angle}°",
            )

            st.metric(
                "Back Angle",
                f"{st.session_state.back_angle}°",
            )

            st.metric(
                "Depth",
                st.session_state.depth_status,
            )

        elif exercise == "Push-ups":

            st.subheader("Push-up Metrics")

            st.metric(
                "Elbow Angle",
                f"{st.session_state.elbow_angle}°",
            )

            st.metric(
                "Body Alignment",
                st.session_state.body_alignment,
            )

            st.metric(
                "Hip Position",
                st.session_state.hip_status,
            )

        elif exercise == "Biceps Curls (Dumbbell)":

            st.subheader("Biceps Curl Metrics")

            st.metric(
                "Elbow Angle",
                f"{st.session_state.elbow_angle}°",
            )

            st.metric(
                "Shoulder Stability",
                st.session_state.shoulder_status,
            )

            st.metric(
                "Swing Detection",
                st.session_state.swing_status,
            )

        elif exercise == "Shoulder Press":

            st.subheader("Shoulder Press Metrics")

            st.metric(
                "Elbow Angle",
                f"{st.session_state.elbow_angle}°",
            )

            st.metric(
                "Arm Extension",
                st.session_state.extension_status,
            )

            st.metric(
                "Back Arch",
                st.session_state.back_arch_status,
            )

        elif exercise == "Lunges":

            st.subheader("Lunge Metrics")

            st.metric(
                "Front Knee Angle",
                f"{st.session_state.front_knee_angle}°",
            )

            st.metric(
                "Torso Angle",
                f"{st.session_state.torso_angle}°",
            )

            st.metric(
                "Balance",
                st.session_state.balance_status,
            )

        if context.state.playing:

            time.sleep(0.25)

            st.rerun()

        inject_webrtc_styles()

    # ==============================
    # Workout History
    # ==============================

    st.divider()

    st.subheader("Workout History")

    user_id = st.session_state.get("user_id", 0)

    if isinstance(user_id, int):

        history = get_users_exercises(user_id)

        rows = []

        for row in history:

            rows.append(
                {
                    "Exercise": row["exercise_name"],
                    "Reps": row["reps"],
                    "Sets": row["sets"],
                    "Time(sec)": row["time"],
                    "Date": row["created_at"],
                }
            )

        df = pd.DataFrame(rows)

        if not df.empty:

            df["Date"] = pd.to_datetime(
                df["Date"]
            ).dt.date

            df = (
                df.groupby(
                    ["Exercise", "Date"]
                )
                .agg(
                    {
                        "Reps": "sum",
                        "Sets": "sum",
                        "Time(sec)": "sum",
                    }
                )
                .reset_index()
            )

            df.index += 1

            st.table(df)

        else:

            st.info("No workout history found.")


if __name__ == "__main__":
    main()