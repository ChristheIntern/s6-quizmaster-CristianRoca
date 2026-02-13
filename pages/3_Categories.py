import streamlit as st
import os
import json

st.set_page_config(
    page_title="Categories",
    page_icon="📂" ,
    layout="wide",
)
st.title("Categories Page")

if os.path.exists("data/questions.json"):
    with open("data/questions.json", "r") as f:
        questions_data = json.load(f)
    
    categories = questions_data.get("categories", {}).keys()
    
    if not categories:
        st.error("No categories found in questions.json!")

if os.path.exists("data/highscores.json"):
    with open("data/highscores.json", "r") as f:
        highscores_data = json.load(f)
    
    highscores = highscores_data.get("highscores", []) or highscores_data.get("scores", [])

    if not highscores:
        st.info("No highscores found in highscores.json!")
