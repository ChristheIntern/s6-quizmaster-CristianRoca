import streamlit as st
import database

st.set_page_config(page_title="Admin", page_icon="🛠️", layout="wide")
st.title("🛠️ Admin Panel")

database.init_db()

if not st.session_state.get("user_id"):
    st.error("Admin access requires login. Log in on the Home page first.")
    st.stop()

# Check if user is admin
if not database.is_admin(st.session_state.get("user_id")):
    st.error("❌ Access Denied! Only admins can access this panel.")
    if st.button("🏠 Go to Home"):
        st.switch_page("Home.py")
    st.stop()

st.markdown("---")

# Create tabs for different admin functions
tab1, tab2 = st.tabs(["👥 User Management", "❓ Questions CRUD"])

with tab1:
    st.subheader("👥 All User Accounts")
    
    users = database.get_all_users()
    
    if not users:
        st.info("No users found.")
    else:
        st.markdown(f"**Total Users:** {len(users)}")
        st.markdown("---")
        
        # Display users in a nice format
        for user in users:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                admin_badge = "👑 ADMIN" if user['is_admin'] else "👤 User"
                st.markdown(f"**{user['username']}** - {admin_badge}")
            
            with col2:
                st.markdown(f"ID: {user['id']}")
            
            with col3:
                pass
            
            with col4:
                # Don't allow deleting the admin account
                if not user['is_admin'] and st.button("🗑️ Delete", key=f"delete_{user['id']}"):
                    if database.delete_user(user['id']):
                        st.success(f"✅ User '{user['username']}' deleted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete user.")
                elif user['is_admin']:
                    st.markdown("<span style='color: gray;'>Protected</span>", unsafe_allow_html=True)
            
            st.markdown("---")

with tab2:
    st.subheader("Add Question")
    with st.form("add_q"):
        category = st.text_input("Category", value="General")
        question = st.text_area("Question")
        options_raw = st.text_area("Options (one per line)")
        correct = st.number_input("Correct option index (0-based)", min_value=0, step=1, value=0)
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])
        points = st.number_input("Points", min_value=0, value=10)
        submitted = st.form_submit_button("Add question")
        if submitted:
            options = [o.strip() for o in options_raw.splitlines() if o.strip()]
            if not question or not options:
                st.error("Provide question and at least one option.")
            else:
                database.add_question(category, question, options, int(correct), difficulty, int(points))
                st.success("Question added.")

    st.markdown("---")
    st.subheader("Existing Questions")
    qs = database.get_questions()
    if not qs:
        st.info("No questions yet.")
    else:
        for q in qs:
            with st.expander(f"[{q['id']}] {q['category']} — {q['question']}"):
                st.write(f"**Difficulty:** {q['difficulty']} — **Points:** {q['points']}")
                st.write("Options:")
                for idx, opt in enumerate(q['options']):
                    st.write(f"{idx}. {opt}")
                col1, col2 = st.columns([1,1])
                if col1.button("Delete", key=f"del_{q['id']}"):
                    database.delete_question(q['id'])
                    st.rerun()
                if col2.button("Edit", key=f"edit_{q['id']}"):
                    # show simple edit form
                    new_cat = st.text_input("Category", value=q['category'], key=f"ecat_{q['id']}")
                    new_q = st.text_area("Question", value=q['question'], key=f"eq_{q['id']}")
                    new_opts = st.text_area("Options (one per line)", value="\n".join(q['options']), key=f"eopt_{q['id']}")
                    new_correct = st.number_input("Correct index", min_value=0, value=q['correct'], key=f"ec_{q['id']}")
                    new_diff = st.selectbox("Difficulty", ["easy","medium","hard"], index=["easy","medium","hard"].index(q['difficulty']) if q['difficulty'] in ["easy","medium","hard"] else 0, key=f"ed_{q['id']}")
                    new_points = st.number_input("Points", min_value=0, value=q['points'], key=f"ep_{q['id']}")
                    if st.button("Save", key=f"save_{q['id']}"):
                        new_options = [o.strip() for o in new_opts.splitlines() if o.strip()]
                        database.update_question(q['id'], new_cat, new_q, new_options, int(new_correct), new_diff, int(new_points))
                        st.success("Updated")
                        st.rerun()

st.markdown("---")
if st.button("🏠 Back to Home", use_container_width=True):
    st.switch_page("Home.py")
