import streamlit as st

# Page configuration

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Home")
st.write(
    """
    Welcome to the Home page! This is where you can find an overview of the application and its features.
    
    Use the sidebar to navigate through different sections of the app. Each section provides specific functionalities and insights.
    
    Feel free to explore and make the most out of this application!
    """
)

# Name input

st.text_input("Your name", placeholder="Enter your name here", key="name_input")
if st.session_state.get("name_input"):
    st.write(f"Hello, {st.session_state['name_input']}! Please select a category.")

# Category selection

st.write("Select a category to explore:")
categories = ["Mathematics", "Science", "History"]
selected_category = st.selectbox("Choose a category", categories, key="category_select")
if selected_category:
    st.write(f"You have selected: {selected_category}")

# Starting quiz

if st.button("Start Quiz", key="start_quiz_button"):
    if selected_category and st.session_state.get("name_input"):
        # Save the selected category to session state
        st.session_state["selected_category"] = selected_category
        st.session_state["player_name"] = st.session_state["name_input"]
        st.switch_page("pages/1_Quiz.py")
    else:
        st.warning("Please enter your name and select a category before starting the quiz.")