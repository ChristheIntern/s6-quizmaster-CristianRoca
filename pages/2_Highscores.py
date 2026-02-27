import streamlit as st
import database

st.set_page_config(
    page_title="Highscores",
    page_icon="🏆",
    layout="wide",
)

st.title("Highscores")

database.init_db()
entries = database.get_highscores(10)

if not entries:
    st.info("No highscores available yet. Play the quiz to set a new highscore!")
else:
    st.subheader("Top Highscores")
    for idx, entry in enumerate(entries, start=1):
        st.write(f"{idx}. **{entry['username']}** — {entry['score']} points — {entry['category']} ({entry['correct_answers']}/{entry['total_questions']}) — {entry['timestamp']}")

# Clear highscores button with confirmation
st.markdown("---")
st.subheader("Manage Highscores")
confirm = st.checkbox("I understand this will permanently delete all highscores.")
if st.button("Clear highscores"):
    if not confirm:
        st.warning("Please check the confirmation box to clear highscores.")
    else:
        try:
            database.clear_scores()
            st.success("Highscores cleared.")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Failed to clear highscores: {e}")