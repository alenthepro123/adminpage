import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import hashlib

# Simulated User Authentication Database (Replace this with a real database)
USER_DB = {
    'admin@example.com': hashlib.sha256('admin123'.encode()).hexdigest(),
    'user@example.com': hashlib.sha256('user123'.encode()).hexdigest()
}

# Feedback storage (in-memory for now)
feedback_data = []

# Helper: Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Login Function
def login(email, password):
    hashed = hash_password(password)
    return USER_DB.get(email) == hashed

# Main Application
st.set_page_config(page_title="Admin Panel", page_icon="🔒", layout="wide")

# Session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = None

# Login Page
if not st.session_state.logged_in:
    st.title("🔒 Admin Panel Login")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    login_button = st.button("Login")

    if login_button:
        if login(email, password):
            st.success("Login successful! Redirecting...")
            st.session_state.logged_in = True
            st.session_state.email = email
        else:
            st.error("Invalid credentials. Please try again.")
else:
    # Admin Panel Navigation
    with st.sidebar:
        selected = option_menu(
            menu_title="Admin Panel",
            options=["Dashboard", "Feedback", "Settings", "Logout"],
            icons=["house", "envelope", "gear", "box-arrow-right"],
            menu_icon="cast",
            default_index=0
        )

    # Logout Functionality
    if selected == "Logout":
        st.session_state.clear()
        st.experimental_set_query_params()  # Ensures app refresh

    # Dashboard Section
    elif selected == "Dashboard":
        st.title("🔄 Dashboard")
        st.write(f"Welcome, **{st.session_state.email}**! Here's an overview of the system.")
        st.metric("Total Feedback Received", len(feedback_data))

    # Feedback Section
    elif selected == "Feedback":
        st.title("📝 Feedback")

        # Display feedback data
        if feedback_data:
            df = pd.DataFrame(feedback_data, columns=["Name", "Email", "Message", "Date"])
            st.table(df)
        else:
            st.info("No feedback received yet.")

        # Feedback Form
        st.subheader("Send Feedback")
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        if st.button("Submit Feedback"):
            feedback_data.append((name, email, message, pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')))
            st.success("Thank you for your feedback!")

    # Settings Section
    elif selected == "Settings":
        st.title("🔧 Settings")
        st.write("Configure your application settings.")

        app_title = st.text_input("Application Title", value="Admin Panel")
        bg_color = st.color_picker("Background Color", value="#ffffff")

        if st.button("Save Settings"):
            st.success("Settings saved successfully!")

        # Apply settings dynamically
        st.markdown(
            f"<style>body {{background-color: {bg_color};}}</style>",
            unsafe_allow_html=True
        )



