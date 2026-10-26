
import streamlit as st


def apply_theme():
    st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background-color: #F5F2FF;
            color: #30245F;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Headings and text */
        h1, h2, h3 {
            color: #30245F !important;
        }

        p, label, .stMarkdown, .stCaption {
            color: #40375F;
        }

        /* Cards */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF !important;
            border: 1px solid #D9CEF7 !important;
            border-radius: 16px !important;
            padding: 18px !important;
            box-shadow: 0 4px 14px rgba(48, 36, 95, 0.08);
        }

        /* Text inputs */
        div[data-testid="stTextInput"] input {
            background-color: #FFFFFF !important;
            color: #30245F !important;
            border: 1px solid #B8A5EF !important;
            border-radius: 10px !important;
        }

        /* Dropdowns */
        div[data-testid="stSelectbox"] div[data-baseweb="select"] {
            background-color: #FFFFFF;
            color: #30245F;
            border-radius: 10px;
        }

        /* Buttons */
        .stButton button,
        .stLinkButton a {
            background-color: #5B43B5 !important;
            color: #FFFFFF !important;
            border: 1px solid #5B43B5 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }

        .stButton button:hover,
        .stLinkButton a:hover {
            background-color: #44318F !important;
            border-color: #44318F !important;
            color: #FFFFFF !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #E8E1FC;
        }

        [data-testid="stSidebar"] * {
            color: #30245F;
        }

        /* Information messages */
        div[data-testid="stAlert"] {
            border-radius: 10px;
        }

        /* Consistent footer */
        .footer-note {
            color: #756A96;
            text-align: center;
            padding-top: 2rem;
            font-size: 0.85rem;
        }
    </style>
    """, unsafe_allow_html=True)


def show_footer():
    st.markdown("""
    <div class="footer-note">
        PathGuide SA · Explore your options, plan your future.
    </div>
    """, unsafe_allow_html=True)
