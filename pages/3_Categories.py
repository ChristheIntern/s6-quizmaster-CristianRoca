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
    with open("data/questions.json", "r") as f:
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
        st.markdown(
            "<p style='text-align: center; color: gray; font-size: 14px;'>💡 Go back to Home and select a category to start your quiz!</p>",
            unsafe_allow_html=True
        )