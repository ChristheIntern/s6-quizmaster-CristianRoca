import streamlit as st
from database import init_db, create_user, verify_user
import database

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

init_db()

# Auth: simple register / login
with st.expander("Account"):
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    reg_col, login_col = st.columns(2)
    with reg_col:
        st.subheader("Register")
        new_user = st.text_input("New username", key="reg_user")
        new_pass = st.text_input("New password", type="password", key="reg_pass")
        if st.button("Register", key="reg_button"):
            if new_user and new_pass:
                ok = create_user(new_user, new_pass)
                if ok:
                    st.success("User created. Please login.")
                else:
                    st.error("Username already exists.")

    with login_col:
        st.subheader("Login")
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", key="login_button"):
            if login_user and login_pass:
                uid = verify_user(login_user, login_pass)
                if uid:
                    st.session_state["user_id"] = uid
                    st.session_state["player_name"] = login_user
                    st.success("Logged in.")
                else:
                    st.error("Invalid credentials.")

    if st.session_state.get("user_id"):
        st.write(f"Logged in as: {st.session_state.get('player_name')}")
        if st.button("Logout", key="logout"):
            st.session_state["user_id"] = None
            st.session_state["player_name"] = None
            st.experimental_rerun()

# Name input (fallback if not logged in)
st.text_input("Your name", placeholder="Enter your name here", key="name_input")
if st.session_state.get("name_input") and not st.session_state.get("player_name"):
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