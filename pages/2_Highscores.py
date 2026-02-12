import streamlit as st
import json
import os

st.set_page_config(
    page_title="Highscores",
    page_icon="🏆",
    layout="wide",
)

st.title("Highscores")
# Load highscores from JSON file
highscores_path = os.path.join("data", "highscores.json")
try:
    with open(highscores_path, "r") as f:
        highscores_data = json.load(f)

    # Support both "highscores" and legacy "scores" keys
    entries = highscores_data.get("highscores") or highscores_data.get("scores") or []

    if not entries:
        st.info("No highscores available yet. Play the quiz to set a new highscore!")
    else:
        st.subheader("Top Highscores")
        sorted_highscores = sorted(entries, key=lambda x: x.get("score", 0), reverse=True)

        for idx, entry in enumerate(sorted_highscores[:10], start=1):
            name = entry.get("name", "Anonymous")
            score = entry.get("score", 0)
            st.write(f"{idx}. **{name}** - {score} points")
except FileNotFoundError:
    st.error("Highscores file not found. Please play the quiz to create a highscores file.")