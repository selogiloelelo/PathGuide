
import streamlit as st
from database import get_universities

# ---------- PAGE SETUP ----------
st.set_page_config(
    page_title="Universities & Deadlines | StudentPath SA",
    page_icon="🎓",
    layout="wide"
)

# ---------- COLOURS AND CARD DESIGN ----------
st.markdown("""
<style>
    .stApp {
        background-color: #F5F2FF;
        color: #30245F;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #30245F !important;
    }

    p, label, .stMarkdown, .stCaption {
        color: #40375F;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D9CEF7 !important;
        border-radius: 16px !important;
        padding: 18px !important;
        box-shadow: 0 4px 14px rgba(48, 36, 95, 0.08);
    }

    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #30245F !important;
        border: 1px solid #B8A5EF !important;
        border-radius: 10px !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #FFFFFF;
        color: #30245F;
        border-radius: 10px;
    }

    .stLinkButton a {
        background-color: #5B43B5 !important;
        color: #FFFFFF !important;
        border: 1px solid #5B43B5 !important;
        border-radius: 9px !important;
        font-weight: 600 !important;
    }

    .stLinkButton a:hover {
        background-color: #44318F !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] {
        background-color: #E8E1FC;
    }

    [data-testid="stSidebar"] * {
        color: #30245F;
    }

    .footer-note {
        color: #756A96;
        text-align: center;
        padding-top: 2rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- PAGE HEADING ----------
st.title("🎓 Universities & Application Dates")
st.write(
    "Explore South African universities, check their application "
    "dates and visit their official websites for the latest information."
)

st.caption(
    "Application dates and availability can change. "
    "Always confirm details with the university."
)

# ---------- UNIVERSITY DATA ----------
database_universities = get_universities()

universities = [
    {
        "name": row["name"],
        "opening": row["opening_date"] or "Check official website",
        "closing": row["closing_date"] or "Check official website",
        "status": (row["status"] or "VERIFY").upper(),
        "website": row["website"] or "https://www.gov.za/"
    }
    for row in database_universities
]

# ---------- SEARCH AND FILTERS ----------
search_col, filter_col = st.columns([2, 1])

with search_col:
    search = st.text_input(
        "Search universities",
        placeholder="🔍 Type a university name..."
    ).strip().casefold()

with filter_col:
    status_filter = st.selectbox(
        "Filter by application availability",
        ["All", "OPEN", "CLOSED", "VERIFY"]
    )

filtered = [
    university for university in universities
    if search in university["name"].casefold()
    and (
        status_filter == "All"
        or university["status"] == status_filter
    )
]

# ---------- UNIVERSITY CARDS ----------
if not filtered:
    st.warning(
        "No universities found. Try another search or filter."
    )

else:
    st.caption(f"{len(filtered)} university/universities found")

    for start in range(0, len(filtered), 3):
        row_universities = filtered[start:start + 3]
        columns = st.columns(3, gap="medium")

        for column, university in zip(columns, row_universities):
            with column:
                with st.container(border=True):
                    st.markdown(f"### 🎓 {university['name']}")

                    st.divider()

                    st.markdown("**📅 Opening date**")
                    st.write(university["opening"])

                    st.markdown("**⏳ Closing date**")
                    st.write(university["closing"])

                    status = university["status"]

                    if status == "OPEN":
                        st.success("Listed as open")
                    elif status == "CLOSED":
                        st.warning("Listed as closed")
                    else:
                        st.info("Availability needs verification")

                    st.link_button(
                        "Visit official website ↗",
                        university["website"],
                        use_container_width=True
                    )

# ---------- FOOTER ----------
st.markdown("""
<div class="footer-note">
    PathGuide SA · Explore your options, plan your future.
</div>
""", unsafe_allow_html=True)
