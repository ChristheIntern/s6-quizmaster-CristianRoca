# Quiz Page
import streamlit as st
import json
import os
import database

st.set_page_config(
    page_title="Quiz",
    page_icon="📝",
    layout="wide",
)

st.markdown("# 🎯 Quiz Master Challenge")
st.markdown("---")

# Get the selected category from session state
selected_category = st.session_state.get("selected_category", None)
selected_difficulty = st.session_state.get("selected_difficulty", None)
player_name = st.session_state.get("player_name") or st.session_state.get("name_input", "Player")

if not selected_category:
    st.error("❌ No category selected! Please go back to the home page and select a category.")
    if st.button("🏠 Go to Home"):
        st.switch_page("Home.py")
    st.stop()

if not selected_difficulty:
    st.error("❌ No difficulty selected! Please select a difficulty level.")
    if st.button("📂 Go to Categories"):
        st.switch_page("pages/3_Categories.py")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"### 👤 Player: **{player_name}**")
with col2:
    st.markdown(f"### 📚 Category: **{selected_category}**")
with col3:
    difficulty_emoji = "🟢" if selected_difficulty == "easy" else "🟡" if selected_difficulty == "medium" else "🔴"
    st.markdown(f"### {difficulty_emoji} Difficulty: **{selected_difficulty.capitalize()}**")
with col4:
    pass

# Load questions from JSON file in data folder
try:
    questions_path = os.path.join("data", "questions.json")
    with open(questions_path, "r", encoding="utf-8") as f:
        questions_data = json.load(f)
    
    # Get questions for the selected category
    all_category_questions = questions_data["categories"].get(selected_category, [])
    
    # Filter questions by selected difficulty
    category_questions = [q for q in all_category_questions if q['difficulty'] == selected_difficulty]
    
    if not category_questions:
        st.error(f"No {selected_difficulty} questions found for category: {selected_category}")
        if st.button("📂 Go to Categories"):
            st.switch_page("pages/3_Categories.py")
        st.stop()
    
    # Initialize quiz state
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    
    # Display current question
    current_q_index = st.session_state.current_question
    
    if current_q_index < len(category_questions):
        question = category_questions[current_q_index]
        
        # Progress bar and stats
        progress = current_q_index / len(category_questions)
        st.progress(progress)
        
        # Header with question number and metadata
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Question", f"{current_q_index + 1}/{len(category_questions)}")
        with col2:
            difficulty_emoji = "🟢" if question['difficulty'] == "easy" else "🟡" if question['difficulty'] == "medium" else "🔴"
            st.metric("Difficulty", f"{difficulty_emoji} {question['difficulty'].capitalize()}")
        with col3:
            st.metric("Points", question['points'])
        with col4:
            st.metric("Current Score", st.session_state.score)
        
        st.markdown("---")
        
        # Question display with styling
        st.markdown(
            f"<div style='background-color: #f0f4ff; padding: 20px; border-radius: 10px; border-left: 5px solid #0066cc;'><h3>{question['question']}</h3></div>",
            unsafe_allow_html=True
        )
        
        st.markdown("### 💡 Select your answer:")
        # Display options as radio buttons
        answer = st.radio(
            "Options:",
            options=range(len(question["options"])),
            format_func=lambda x: f"{'ABCD'[x]}. {question['options'][x]}",
            key=f"question_{question['id']}",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("✅ Submit Answer", use_container_width=True, key="submit_btn"):
            # Check if answer is correct
            is_correct = answer == question["correct"]
            
            if is_correct:
                st.session_state.score += question["points"]
                st.success(f"🎉 Correct! +{question['points']} points")
            else:
                st.error(f"❌ Wrong! The correct answer was: {question['options'][question['correct']]}")
            
            # Save answer
            st.session_state.answers.append({
                "question_id": question["id"],
                "selected": answer,
                "correct": question["correct"],
                "is_correct": is_correct
            })
            
            # Move to next question
            st.session_state.current_question += 1
            st.rerun()
    
    else:
        # Quiz completed
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; padding: 30px;'><h1>🎊 QUIZ COMPLETED! 🎊</h1></div>",
            unsafe_allow_html=True
        )
        st.markdown("---")
        
        correct_answers = sum(1 for ans in st.session_state.answers if ans["is_correct"])
        percentage = (correct_answers / len(st.session_state.answers) * 100) if st.session_state.answers else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Final Score", st.session_state.score)
        with col2:
            st.metric("✅ Correct Answers", f"{correct_answers}/{len(st.session_state.answers)}")
        with col3:
            st.metric("📈 Accuracy", f"{percentage:.1f}%")
        
        st.markdown("---")
        
        # Performance message
        if percentage == 100:
            st.balloons()
            st.success("🏆 **PERFECT SCORE!** You're a quiz master!")
        elif percentage >= 80:
            st.info("⭐ **EXCELLENT!** Outstanding performance!")
        elif percentage >= 60:
            st.info("👍 **GOOD JOB!** Keep practicing!")
        else:
            st.warning("📚 **KEEP LEARNING!** Try again to improve!")
        
        st.markdown("---")
        
        # Save highscore
        if st.button("💾 Save Score & Return Home", use_container_width=True):
            # Load existing highscores
            highscores_path = os.path.join("data", "highscores.json")
            try:
                with open(highscores_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    highscores = json.loads(content) if content else {"scores": []}
            except (FileNotFoundError, json.JSONDecodeError):
                highscores = {"scores": []}
            
            # Add new score: save in DB if logged in, otherwise fallback to file
            if st.session_state.get("user_id"):
                database.add_score(st.session_state.get("user_id"), selected_category, st.session_state.score, len(st.session_state.answers), correct_answers)
            else:
                highscores["scores"].append({
                    "name": player_name,
                    "category": selected_category,
                    "score": st.session_state.score,
                    "total_questions": len(st.session_state.answers),
                    "correct_answers": correct_answers
                })
                # Save highscores to file
                with open(highscores_path, "w", encoding="utf-8") as f:
                    json.dump(highscores, f, indent=4)

            # Reset quiz state
            del st.session_state.current_question
            del st.session_state.score
            del st.session_state.answers

            st.switch_page("Home.py")

except FileNotFoundError:
    st.error("Questions file not found! Please make sure 'data/questions.json' exists.")
except json.JSONDecodeError:
    st.error("Error reading questions file! Please check the JSON format.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
