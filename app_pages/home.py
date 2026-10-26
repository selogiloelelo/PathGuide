import streamlit as st
from theme import apply_theme, show_footer

# ---------- SHARED DESIGN ----------
apply_theme()

# ---------- NAVIGATION FUNCTION ----------
def navigate_to(destination):
    st.session_state["selected_page"] = destination


# ---------- WELCOME BANNER ----------
st.title("🎓 Welcome to PathGuide SA")

st.write(
    "Your guide to South African higher education. "
    "Explore universities, courses, bursaries and application dates "
    "to help you plan your next step."
)

st.divider()


# ---------- CLICKABLE NAVIGATION CARDS ----------
st.subheader("Explore your opportunities")
st.write("Select a card to explore that section.")

cards = [
    (
        "🏛️ Universities",
        "Explore universities and official application information.",
        "Universities"
    ),
    (
        "💰 Bursaries & Scholarships",
        "Discover funding opportunities and eligibility requirements.",
        "Bursaries & Scholarships"
    ),
    (
        "📚 Explore Courses",
        "Explore qualifications and possible career paths.",
        "Explore Courses"
    )
    
]

for start in range(0, len(cards), 2):
    columns = st.columns(2, gap="medium")

    for column, card in zip(columns, cards[start:start + 2]):
        title, description, destination = card

        with column:
            with st.container(border=True):
                st.markdown(f"### {title}")
                st.write(description)

                st.button(
                    f"Explore {destination} →",
                    key=f"home_{destination}",
                    use_container_width=True,
                    on_click=navigate_to,
                    args=(destination,)
                )


# ---------- GETTING STARTED ----------
st.divider()
st.subheader("🌱 How to get started")

st.markdown("""
1. Explore universities and the courses they offer.
2. Check admission requirements and application dates.
3. Find bursaries or scholarships you may qualify for.
4. Use official websites to verify details and apply.
""")

st.info(
    "Application dates and funding requirements can change. "
    "Always confirm details with the official university or funder."
)


# ---------- FOOTER ----------
show_footer()