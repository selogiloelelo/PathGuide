
import streamlit as st
import runpy
from pathlib import Path
from theme import apply_theme, show_footer

# ---------------- PAGE SETUP ----------------

st.set_page_config(
    page_title="PathGuide SA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- APPLY SHARED THEME ----------------
apply_theme()

# ---------------- PROJECT FOLDERS ----------------
BASE_DIR = Path(__file__).resolve().parent
PAGES_DIR = BASE_DIR / "app_pages"

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎓 PathGuide SA")
st.sidebar.caption("Your student opportunities hub")

pages = [
    "Home",
    "Universities",
    "Bursaries & Scholarships",
    "Explore Courses"
    
]
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Home"

page = st.sidebar.radio(
    "Navigate",
    pages,
    key="selected_page"
)

# ---------------- PAGE ROUTING ----------------
if page == "Home":
    runpy.run_path(str(PAGES_DIR / "home.py"))

elif page == "Universities":
    runpy.run_path(str(PAGES_DIR / "universities.py"))

elif page == "Bursaries & Scholarships":
    runpy.run_path(str(PAGES_DIR / "bursaries.py"))

elif page == "Explore Courses":
    courses_file = PAGES_DIR / "courses.py"

    if courses_file.exists():
        runpy.run_path(str(courses_file))
    else:
        st.title("📚 Explore Courses")
        st.write(
            "Discover courses, qualifications and study options "
            "that match your interests and career goals."
        )
        st.info("Course information will be added here.")

