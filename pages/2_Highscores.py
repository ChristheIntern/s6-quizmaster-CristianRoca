import streamlit as st
import database

st.set_page_config(
    page_title="Highscores",
    page_icon="🏆",
    layout="wide",
)

st.markdown("# 🏆 Hall of Fame")
st.markdown("---")

database.init_db()
entries = database.get_highscores(10)

if not entries:
    st.markdown(
        "<div style='text-align: center; padding: 50px;'><h2>📭 No highscores yet!</h2><p>Play the quiz to claim your spot in the Hall of Fame!</p></div>",
        unsafe_allow_html=True
    )
else:
    st.markdown("### 👑 Top 10 Leaderboard")
    st.markdown("")
    
    for idx, entry in enumerate(entries, start=1):
        # Medal emoji
        if idx == 1:
            medal = "🥇"
        elif idx == 2:
            medal = "🥈"
        elif idx == 3:
            medal = "🥉"
        else:
            medal = "⭐"
        
        # Color styling based on rank
        if idx == 1:
            bg_color = "#fffacd"  # Light yellow
        elif idx == 2:
            bg_color = "#e8e8e8"  # Light gray
        elif idx == 3:
            bg_color = "#ffe4c4"  # Light orange
        else:
            bg_color = "#f5f5f5"
        
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
        
        with col1:
            st.markdown(f"<div style='background-color: {bg_color}; padding: 10px; border-radius: 5px; text-align: center;'><h3>{medal} #{idx}</h3></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='background-color: {bg_color}; padding: 10px; border-radius: 5px;'><b>{entry['username']}</b></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div style='background-color: {bg_color}; padding: 10px; border-radius: 5px;'>{entry['category']}</div>", unsafe_allow_html=True)
        with col4:
            accuracy = (entry['correct_answers'] / entry['total_questions'] * 100) if entry['total_questions'] > 0 else 0
            st.markdown(f"<div style='background-color: {bg_color}; padding: 10px; border-radius: 5px;'>📊 {accuracy:.0f}% ({entry['correct_answers']}/{entry['total_questions']})</div>", unsafe_allow_html=True)
        with col5:
            st.markdown(f"<div style='background-color: {bg_color}; padding: 10px; border-radius: 5px; text-align: center;'><h4>⭐ {entry['score']}</h4></div>", unsafe_allow_html=True)

# Clear highscores button with confirmation
st.markdown("---")
st.markdown("### ⚙️ Manage Highscores")
confirm = st.checkbox("I understand this will permanently delete all highscores.")
if st.button("🗑️ Clear highscores", use_container_width=True):
    if not confirm:
        st.warning("Please check the confirmation box to clear highscores.")
    else:
        try:
            database.clear_scores()
            st.success("Highscores cleared.")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to clear highscores: {e}")