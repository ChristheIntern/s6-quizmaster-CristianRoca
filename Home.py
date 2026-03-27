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

st.markdown("# 🎓 QuizMaster")
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 20px;'>
    <h3>Welcome to the Ultimate Quiz Experience!</h3>
    <p>Challenge yourself with engaging quizzes across multiple categories.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Name input

init_db()

# Auth: simple register / login
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if not st.session_state.get("user_id"):
    st.markdown("### 🔐 Create Account or Login")
    reg_col, login_col = st.columns(2)
    
    with reg_col:
        st.markdown("#### 📝 New User?")
        new_user = st.text_input("Username", key="reg_user", placeholder="Choose a username")
        new_pass = st.text_input("Password", type="password", key="reg_pass", placeholder="Create a password")
        if st.button("🚀 Register", key="reg_button", use_container_width=True):
            if new_user and new_pass:
                ok = create_user(new_user, new_pass)
                if ok:
                    st.success("✅ Account created! Now please login.")
                else:
                    st.error("❌ Username already exists.")
            else:
                st.warning("⚠️ Please fill in all fields.")

    with login_col:
        st.markdown("#### 👋 Existing User?")
        login_user = st.text_input("Username", key="login_user", placeholder="Enter your username")
        login_pass = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
        if st.button("🎯 Login", key="login_button", use_container_width=True):
            if login_user and login_pass:
                uid = verify_user(login_user, login_pass)
                if uid:
                    st.session_state["user_id"] = uid
                    st.session_state["player_name"] = login_user
                    st.success("✅ Successfully logged in!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")
            else:
                st.warning("⚠️ Please enter username and password.")
    st.stop()

else:
    # User is logged in
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"### 👤 Welcome back, **{st.session_state.get('player_name')}**!")
    with col2:
        # Check if user is admin
        if database.is_admin(st.session_state.get("user_id")):
            if st.button("🛠️ Admin Panel", key="admin_btn"):
                st.switch_page("pages/4_Admin.py")
    with col3:
        if st.button("🚪 Logout", key="logout"):
            st.session_state["user_id"] = None
            st.session_state["player_name"] = None
            st.rerun()

# Category selection
st.markdown("---")
st.markdown("### 🎯 Choose Your Challenge")

if st.button("📂 Browse Categories & Start Quiz", key="categories_button", use_container_width=True):
    st.switch_page("pages/3_Categories.py")