# Quiz Page
import streamlit as st
import json
import os

st.set_page_config(
    page_title="Quiz",
    page_icon="📝",
    layout="wide",
)

st.title("Quiz Page")

# Get the selected category from session state
selected_category = st.session_state.get("selected_category", None)
player_name = st.session_state.get("player_name", "Player")

if not selected_category:
    st.error("No category selected! Please go back to the home page and select a category.")
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()

st.write(f"Welcome, **{player_name}**!")
st.write(f"Category: **{selected_category}**")

# Load questions from JSON file in data folder
try:
    questions_path = os.path.join("data", "questions.json")
    with open(questions_path, "r") as f:
        questions_data = json.load(f)
    
    # Get questions for the selected category
    category_questions = questions_data["categories"].get(selected_category, [])
    
    if not category_questions:
        st.error(f"No questions found for category: {selected_category}")
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
        
        st.subheader(f"Question {current_q_index + 1} of {len(category_questions)}")
        st.write(f"**Difficulty:** {question['difficulty'].capitalize()}")
        st.write(f"**Points:** {question['points']}")
        
        st.write("---")
        st.write(f"### {question['question']}")
        
        # Display options as radio buttons
        answer = st.radio(
            "Select your answer:",
            options=range(len(question["options"])),
            format_func=lambda x: question["options"][x],
            key=f"question_{question['id']}"
        )
        
        col1, col2 = st.columns([1, 5])
        
        with col1:
            if st.button("Submit Answer"):
                # Check if answer is correct
                is_correct = answer == question["correct"]
                
                if is_correct:
                    st.session_state.score += question["points"]
                    st.success(f"Correct! +{question['points']} points")
                else:
                    st.error(f"Wrong! The correct answer was: {question['options'][question['correct']]}")
                
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
        
        with col2:
            st.write(f"**Current Score:** {st.session_state.score}")
    
    else:
        # Quiz completed
        st.success("🎉 Quiz Completed!")
        st.write(f"### Final Score: {st.session_state.score}")
        st.write(f"**Questions Answered:** {len(st.session_state.answers)}")
        
        correct_answers = sum(1 for ans in st.session_state.answers if ans["is_correct"])
        st.write(f"**Correct Answers:** {correct_answers}/{len(st.session_state.answers)}")
        
        # Save highscore
        if st.button("Save Score & Return Home"):
            # Load existing highscores
            highscores_path = os.path.join("data", "highscores.json")
            try:
                with open(highscores_path, "r") as f:
                    content = f.read().strip()
                    highscores = json.loads(content) if content else {"scores": []}
            except (FileNotFoundError, json.JSONDecodeError):
                highscores = {"scores": []}
            
            # Add new score
            highscores["scores"].append({
                "name": player_name,
                "category": selected_category,
                "score": st.session_state.score,
                "total_questions": len(st.session_state.answers),
                "correct_answers": correct_answers
            })
            
            # Save highscores
            with open(highscores_path, "w") as f:
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