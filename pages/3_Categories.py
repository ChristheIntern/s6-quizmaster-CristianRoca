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
    
    categories_dict = questions_data.get("categories", {})
    categories = categories_dict.keys()
    
    if not categories:
        st.error("No categories found in questions.json!")
    else:
        # display each category along with number of questions
        st.subheader("Available Categories")
        for cat, questions in categories_dict.items():
            count = len(questions) if isinstance(questions, list) else 0
            st.write(f"**{cat}** — {count} question{'s' if count != 1 else ''}")