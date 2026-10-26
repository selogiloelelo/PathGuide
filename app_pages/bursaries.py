
import streamlit as st
from database import get_bursaries
from theme import apply_theme, show_footer

apply_theme()

st.set_page_config(
    page_title="Bursaries | StudentPath SA",
    page_icon="💰",
    layout="wide"
)

# ---------- PAGE DESIGN ----------
st.markdown("""
<style>
    .stApp {
        background-color: #F3F0FF;
        color: #30245F;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .page-title {
        color: #30245F;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .page-description {
        color: #514477;
        font-size: 1.05rem;
        margin-bottom: 25px;
    }

    .hero {
        background: linear-gradient(120deg, #3346A8, #7664D8);
        padding: 30px;
        border-radius: 20px;
        color: white;
        margin: 20px 0 30px 0;
    }

    .hero h2 {
        color: white !important;
        font-size: 1.8rem;
    }

    .hero p {
        color: #FFFFFF !important;
        font-size: 1rem;
        margin-bottom: 0;
    }

    .section-title {
        color: #30245F;
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    .section-description {
        color: #514477;
        margin-bottom: 15px;
    }

    /* Individual bursary card */
    .bursary-card {
        background: #FFFFFF;
        border: 2px solid #D4C7F5;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 5px 16px rgba(48, 36, 95, 0.10);
        color: #30245F;
    }

    .bursary-card h3 {
        color: #30245F !important;
        font-size: 1.4rem;
        font-weight: 800;
        margin-top: 0;
        margin-bottom: 8px;
    }

    .bursary-category {
        display: inline-block;
        background: #EAE3FF;
        color: #49358C;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .bursary-description {
        color: #40375F;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 18px;
    }

    .bursary-detail {
        background: #F8F6FF;
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        color: #30245F;
        line-height: 1.5;
        overflow-wrap: anywhere;
    }

    .bursary-detail strong {
        color: #5B43B5;
    }

    .bursary-status {
        background: #FFF4D6;
        color: #694D00;
        border-radius: 8px;
        padding: 10px 12px;
        margin-top: 12px;
        margin-bottom: 15px;
        font-size: 0.9rem;
        font-weight: 600;
    }

    .stTextInput input {
        background-color: white !important;
        color: #30245F !important;
        border: 1px solid #B8A5EF !important;
        border-radius: 10px;
    }

    div[data-testid="stTextInput"] label {
        color: #30245F !important;
        font-weight: 600;
    }

    .stLinkButton a {
        background-color: #5B43B5 !important;
        color: white !important;
        border: 1px solid #5B43B5 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    .stLinkButton a:hover {
        background-color: #40318B !important;
    }

    [data-testid="stSidebar"] {
        background-color: #E8E1FC;
    }

    .footer-note {
        color: #514477;
        font-size: 0.85rem;
        text-align: center;
        padding-top: 25px;
    }
</style>
""", unsafe_allow_html=True)


# ---------- PAGE HEADER ----------
st.markdown(
    '<div class="page-title">💰 Bursaries & Scholarships</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-description">'
    'Discover funding opportunities to help make your education more affordable.'
    '</div>',
    unsafe_allow_html=True
)


# ---------- WELCOME BANNER ----------
st.markdown("""
<div class="hero">
    <h2>Your future deserves a chance. 🎓</h2>
    <p>
        Explore financial aid, discover funding opportunities, and take
        the next step towards your academic goals.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------- SEARCH ----------
st.markdown(
    '<div class="section-title">🔎 Find funding for your future</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Search by funding provider, opportunity, or field of study.'
    '</div>',
    unsafe_allow_html=True
)

search = st.text_input(
    "Search funding opportunities",
    placeholder="Try NSFAS, teaching or engineering",
    key="bursary_search"
).strip().casefold()


# ---------- LOAD DATABASE ----------
database_bursaries = get_bursaries()

bursaries = [
    {
        "name": row["name"] or "Unnamed opportunity",
        "category": row["provider"] or "Funding opportunity",
        "description": (
            row["description"]
            or "Visit the official website for more information."
        ),
        "website": row["website"] or "https://www.gov.za/",
        "eligibility": (
            row["eligibility"] or "Check the provider's requirements."
        ),
        "opening": row["opening_date"] or "Check official website",
        "closing": row["closing_date"] or "Check official website",
        "status": row["status"] or "VERIFY",
    }
    for row in database_bursaries
]


# ---------- FILTER RESULTS ----------
results = [
    bursary for bursary in bursaries
    if search in (
        bursary["name"] + " "
        + bursary["description"] + " "
        + bursary["category"] + " "
        + bursary["eligibility"]
    ).casefold()
]


# ---------- RESULTS HEADING ----------
st.markdown(
    '<div class="section-title">🎓 Available funding opportunities</div>',
    unsafe_allow_html=True
)

st.caption(f"{len(results)} funding opportunities found")


# ---------- DISPLAY EACH BURSARY AS A CARD ----------
if results:

    # Two large cards per row
    for start in range(0, len(results), 2):
        columns = st.columns(2, gap="large")

        for offset, column in enumerate(columns):
            index = start + offset

            if index >= len(results):
                break

            bursary = results[index]

            with column:
                # Card header, description and details
                st.markdown(
                    f"""
                    <div class="bursary-card">
                        <h3>💜 {bursary['name']}</h3>
                        <div class="bursary-category">
                            {bursary['category']}
                        </div>
                        <div class="bursary-description">
                            {bursary['description']}
                        </div>
                        <div class="bursary-detail">
                            <strong>👤 Who can apply?</strong><br>
                            {bursary['eligibility']}
                        </div>
                        <div class="bursary-detail">
                            <strong>📅 Opening date</strong><br>
                            {bursary['opening']}
                        </div>
                        <div class="bursary-detail">
                            <strong>⏳ Closing date</strong><br>
                            {bursary['closing']}
                        </div>
                        <div class="bursary-status">
                            Status: {bursary['status']}<br>
                            Confirm availability and dates with the provider.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.link_button(
                    "Visit official website ↗",
                    bursary["website"],
                    use_container_width=True,
                    key=f"bursary_link_{index}"
                )

else:
    st.info(
        "No matching funding opportunities found. "
        "Try a different search term."
    )


# ---------- REMINDER ----------
st.markdown("---")

st.markdown(
    '<div class="section-title">💡 Before you apply</div>',
    unsafe_allow_html=True
)

st.write(
    "Check the eligibility requirements, required documents, opening dates "
    "and closing dates on the official funding website. Information can change."
)


# ---------- FOOTER ----------
st.markdown("""
<div class="footer-note">
    PathGuide SA · Find opportunities. Plan your future.
</div>
""", unsafe_allow_html=True)
