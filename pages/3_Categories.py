import streamlit as st
import os
import json

st.set_page_config(
    page_title="Categories",
    page_icon="📂",
    layout="wide",
)

st.markdown("# 📚 Quiz Categories")
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 18px;'>Explore our exciting collection of quiz categories and challenge yourself!</p>", unsafe_allow_html=True)
st.markdown("")

if os.path.exists("data/questions.json"):
    with open("data/questions.json", "r", encoding="utf-8") as f:
        questions_data = json.load(f)
    
    categories_dict = questions_data.get("categories", {})
    categories = categories_dict.keys()
    
    if not categories:
        st.error("No categories found in questions.json!")
    else:
        # Display categories in a card layout
        st.markdown("### 🎯 Available Categories")
        
        # Create columns for category cards
        cols = st.columns(len(list(categories_dict.items())))
        
        category_emojis = {
            "Mathematics": "🔢",
            "Science": "🔬",
            "History": "📜",
            "Geography": "🌍",
            "Arts": "🎨",
            "Literature": "📖"
        }
        
        for idx, (cat, questions) in enumerate(categories_dict.items()):
            count = len(questions) if isinstance(questions, list) else 0
            emoji = category_emojis.get(cat, "❓")
            
            with cols[idx]:
                st.markdown(
                    f"""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; border-radius: 10px; text-align: center; color: white;'>
                    <h2>{emoji}</h2>
                    <h3>{cat}</h3>
                    <p style='font-size: 14px; margin: 10px 0;'>📋 {count} Question{'s' if count != 1 else ''}</p>
                    </div>""",
                    unsafe_allow_html=True
                )
        
        st.markdown("---")
        st.markdown("### ⚙️ Quiz Settings")
        
        # Category selection
        selected_category = st.selectbox(
            "Select a category:",
            list(categories_dict.keys()),
            key="category_selection"
        )
        
        # Difficulty selection
        st.markdown("**Choose your difficulty level:**")
        difficulty_cols = st.columns(3)
        
        with difficulty_cols[0]:
            easy_btn = st.button("🟢 Easy", use_container_width=True, key="diff_easy")
        with difficulty_cols[1]:
            medium_btn = st.button("🟡 Medium", use_container_width=True, key="diff_medium")
        with difficulty_cols[2]:
            hard_btn = st.button("🔴 Hard", use_container_width=True, key="diff_hard")
        
        # Handle difficulty selection
        selected_difficulty = st.session_state.get("selected_difficulty", None)
        if easy_btn:
            st.session_state["selected_difficulty"] = "easy"
            selected_difficulty = "easy"
        elif medium_btn:
            st.session_state["selected_difficulty"] = "medium"
            selected_difficulty = "medium"
        elif hard_btn:
            st.session_state["selected_difficulty"] = "hard"
            selected_difficulty = "hard"
        
        # Display selection
        if selected_difficulty:
            difficulty_emoji = "🟢" if selected_difficulty == "easy" else "🟡" if selected_difficulty == "medium" else "🔴"
            st.markdown(
                f"<div style='background-color: #e7f3ff; padding: 15px; border-radius: 10px; text-align: center;'><h4>Category: <b>{selected_category}</b> {difficulty_emoji} Difficulty: <b>{selected_difficulty.upper()}</b></h4></div>",
                unsafe_allow_html=True
            )
            
            st.markdown("")
            if st.button("🚀 Start Quiz", use_container_width=True, key="start_quiz_button"):
                st.session_state["selected_category"] = selected_category
                st.session_state["selected_difficulty"] = selected_difficulty
                st.switch_page("pages/1_Quiz.py")
        else:
            st.info("👆 Select a difficulty level to start the quiz!")
        
        st.markdown("---")
        st.markdown(
            "<p style='text-align: center; color: gray; font-size: 14px;'>💡 Choose your difficulty and start challenging yourself!</p>",
            unsafe_allow_html=True
        )