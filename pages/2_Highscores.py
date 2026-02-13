import streamlit as st
import json
import os

st.set_page_config(
    page_title="Highscores",
    page_icon="🏆",
    layout="wide",
)

st.title("Highscores")

# Load highscores from JSON file (support both 'highscores' and legacy 'scores')
highscores_path = os.path.join("data", "highscores.json")
entries = []
key_present = None

if os.path.exists(highscores_path):
    try:
        with open(highscores_path, "r") as f:
            highscores_data = json.load(f)

        if "highscores" in highscores_data:
            entries = highscores_data.get("highscores", [])
            key_present = "highscores"
        elif "scores" in highscores_data:
            entries = highscores_data.get("scores", [])
            key_present = "scores"
        else:
            entries = []
    except Exception:
        st.error("Failed to read highscores file. It may be corrupted.")
else:
    entries = []

if not entries:
    st.info("No highscores available yet. Play the quiz to set a new highscore!")
else:
    st.subheader("Top Highscores")
    sorted_highscores = sorted(entries, key=lambda x: x.get("score", 0), reverse=True)

    for idx, entry in enumerate(sorted_highscores[:10], start=1):
        name = entry.get("name", "Anonymous")
        score = entry.get("score", 0)
        st.write(f"{idx}. **{name}** - {score} points")

# Clear highscores button with confirmation
st.markdown("---")
st.subheader("Manage Highscores")
confirm = st.checkbox("I understand this will permanently delete all highscores.")
if st.button("Clear highscores"):
    if not confirm:
        st.warning("Please check the confirmation box to clear highscores.")
    else:
        try:
            # Default to legacy key if none detected
            out_key = key_present if key_present else "scores"
            with open(highscores_path, "w") as f:
                json.dump({out_key: []}, f, indent=4)
            st.success("Highscores cleared.")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Failed to clear highscores: {e}")