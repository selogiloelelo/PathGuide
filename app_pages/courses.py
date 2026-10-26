

import streamlit as st
from theme import apply_theme, show_footer

apply_theme()


st.set_page_config(
    page_title="Explore Courses | StudentPath SA",
    page_icon="📚",
    layout="wide"
)

# ---------- STUDENTPATH SA COLOUR THEME ----------
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

    .course-category {
        display: inline-block;
        background-color: #E8E1FC;
        color: #44318F !important;
        padding: 6px 10px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .course-label {
        color: #756A96 !important;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.7px;
        margin-top: 10px;
        margin-bottom: 6px;
    }

    .course-description {
        color: #51466F !important;
        font-size: 0.92rem;
        line-height: 1.6;
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

    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid #D9CEF7;
        border-radius: 10px;
    }

    div[data-testid="stAlert"] {
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


# ---------- COURSE DATA ----------
courses = [
    {
        "name": "Civil Engineering",
        "category": "Engineering",
        "icon": "🏗️",
        "description": "Learn to plan, design and maintain infrastructure such as roads, bridges, dams and buildings.",
        "careers": [
            "Civil Engineer",
            "Structural Engineer",
            "Transport Engineer",
            "Construction Project Manager",
            "Water Resources Engineer"
        ],
        "subjects": "Mathematics and Physical Sciences",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Mechanical Engineering",
        "category": "Engineering",
        "icon": "⚙️",
        "description": "Study machines, mechanical systems, manufacturing and energy systems.",
        "careers": [
            "Mechanical Engineer",
            "Design Engineer",
            "Maintenance Engineer",
            "Manufacturing Engineer"
        ],
        "subjects": "Mathematics and Physical Sciences",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Electrical Engineering",
        "category": "Engineering",
        "icon": "⚡",
        "description": "Explore electrical power, electronic systems, control systems and related technologies.",
        "careers": [
            "Electrical Engineer",
            "Power Systems Engineer",
            "Control Systems Engineer",
            "Electronics Engineer"
        ],
        "subjects": "Mathematics and Physical Sciences",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Medicine (MBChB)",
        "category": "Health Sciences",
        "icon": "🩺",
        "description": "Study human health, disease prevention, diagnosis and medical treatment.",
        "careers": [
            "Medical Doctor",
            "Medical Researcher",
            "Clinical Academic",
            "Specialist Physician (after further training)"
        ],
        "subjects": "Mathematics, Physical Sciences and Life Sciences are commonly important for admission",
        "website": "https://www.healthcareers.co.za/"
    },
    {
        "name": "Nursing",
        "category": "Health Sciences",
        "icon": "🏥",
        "description": "Learn how to care for patients, promote health and support treatment and recovery.",
        "careers": [
            "Professional Nurse",
            "Community Health Nurse",
            "Clinical Nurse Specialist (with further qualifications)",
            "Nurse Educator (with further qualifications)"
        ],
        "subjects": "Check each university's admission requirements",
        "website": "https://www.healthcareers.co.za/"
    },
    {
        "name": "Pharmacy",
        "category": "Health Sciences",
        "icon": "💊",
        "description": "Study medicines, their safe use, effects, preparation and distribution.",
        "careers": [
            "Pharmacist",
            "Hospital Pharmacist",
            "Community Pharmacist",
            "Pharmaceutical Industry Professional"
        ],
        "subjects": "Mathematics, Physical Sciences and other required subjects",
        "website": "https://www.healthcareers.co.za/"
    },
    {
        "name": "Physiotherapy",
        "category": "Health Sciences",
        "icon": "🦴",
        "description": "Study movement, rehabilitation and ways to help people improve physical function.",
        "careers": [
            "Physiotherapist",
            "Sports Physiotherapist",
            "Rehabilitation Practitioner",
            "Private Practice Physiotherapist"
        ],
        "subjects": "Check each university's admission requirements",
        "website": "https://www.healthcareers.co.za/"
    },
    {
        "name": "Computer Science",
        "category": "Information Technology",
        "icon": "💻",
        "description": "Learn programming, algorithms, software design and the foundations of computing.",
        "careers": [
            "Software Developer",
            "Systems Analyst",
            "Application Developer",
            "Research Programmer"
        ],
        "subjects": "Mathematics is commonly required or recommended",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Information Technology",
        "category": "Information Technology",
        "icon": "🌐",
        "description": "Explore computer systems, networks, databases, cybersecurity and technical support.",
        "careers": [
            "IT Support Specialist",
            "Network Administrator",
            "Systems Administrator",
            "Cybersecurity Analyst (with relevant skills)"
        ],
        "subjects": "Requirements vary by institution and qualification",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Data Science",
        "category": "Information Technology",
        "icon": "📊",
        "description": "Use statistics, programming and data analysis to identify patterns and support decisions.",
        "careers": [
            "Data Analyst",
            "Data Scientist",
            "Business Intelligence Analyst",
            "Machine Learning Engineer (with further specialisation)"
        ],
        "subjects": "Mathematics and statistics are important",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Accounting",
        "category": "Business and Commerce",
        "icon": "📈",
        "description": "Study financial records, reporting, auditing, taxation and financial management.",
        "careers": [
            "Accountant",
            "Auditor",
            "Tax Consultant",
            "Financial Reporting Analyst"
        ],
        "subjects": "Mathematics is useful; admission requirements vary",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Business Management",
        "category": "Business and Commerce",
        "icon": "💼",
        "description": "Learn about business operations, leadership, strategy, people and organisational management.",
        "careers": [
            "Business Manager",
            "Operations Coordinator",
            "Management Consultant",
            "Entrepreneur"
        ],
        "subjects": "Check the institution's admission requirements",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Economics",
        "category": "Business and Commerce",
        "icon": "📉",
        "description": "Explore how people, businesses and governments make decisions about resources and markets.",
        "careers": [
            "Economic Analyst",
            "Policy Analyst",
            "Research Assistant",
            "Financial Analyst (with relevant additional skills)"
        ],
        "subjects": "Mathematics is beneficial and may be required",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Law (LLB)",
        "category": "Law and Humanities",
        "icon": "⚖️",
        "description": "Study legal principles, legislation, court processes and the South African legal system.",
        "careers": [
            "Attorney (after required practical training and admission)",
            "Advocate (after applicable training and admission)",
            "Legal Adviser",
            "Compliance Officer"
        ],
        "subjects": "Strong reading, writing and analytical skills are useful",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Psychology",
        "category": "Law and Humanities",
        "icon": "🧠",
        "description": "Study human behaviour, mental processes, research and psychological theory.",
        "careers": [
            "Research Assistant",
            "Human Resources Practitioner",
            "Psychology Honours Graduate (roles depend on requirements)",
            "Registered Psychologist (after further approved training and registration)"
        ],
        "subjects": "Admission requirements vary by programme",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Education",
        "category": "Education",
        "icon": "📚",
        "description": "Learn teaching methods, curriculum development, assessment and learner support.",
        "careers": [
            "School Teacher (after meeting registration requirements)",
            "Education Assistant",
            "Curriculum Developer (with relevant experience)",
            "Education Administrator"
        ],
        "subjects": "Requirements depend on the teaching phase and subjects chosen",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Agriculture",
        "category": "Agriculture and Environment",
        "icon": "🌱",
        "description": "Explore crop production, animal science, soil management and sustainable farming.",
        "careers": [
            "Agricultural Advisor",
            "Farm Manager",
            "Agricultural Research Assistant",
            "Agricultural Consultant"
        ],
        "subjects": "Requirements vary by qualification",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Environmental Science",
        "category": "Agriculture and Environment",
        "icon": "🌍",
        "description": "Study ecosystems, pollution, conservation and the environmental impact of human activities.",
        "careers": [
            "Environmental Consultant",
            "Environmental Officer",
            "Conservation Practitioner",
            "Environmental Researcher"
        ],
        "subjects": "Science and Mathematics may be required",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Architecture",
        "category": "Design and Built Environment",
        "icon": "🏛️",
        "description": "Learn to design buildings and spaces while considering function, safety and sustainability.",
        "careers": [
            "Architect (after required professional training and registration)",
            "Architectural Technologist",
            "Urban Design Assistant",
            "Building Design Professional"
        ],
        "subjects": "Check Mathematics, portfolio and other programme requirements",
        "website": "https://www.careerhelp.org.za/"
    },
    {
        "name": "Quantity Surveying",
        "category": "Design and Built Environment",
        "icon": "📐",
        "description": "Study construction costs, project budgets, contracts and the financial management of building projects.",
        "careers": [
            "Quantity Surveyor",
            "Cost Consultant",
            "Construction Estimator",
            "Contract Administrator"
        ],
        "subjects": "Mathematics is commonly important",
        "website": "https://www.careerhelp.org.za/"
    }
]


# ---------- PAGE HEADER ----------
st.title("📚 Explore Courses & Careers")

st.write(
    "Discover what you can study, what each course involves "
    "and the career paths it may open up."
)

st.info(
    "Career options depend on your qualification, experience "
    "and any required professional registration. Always confirm "
    "entry requirements with the institution."
)


# ---------- SEARCH AND FILTERS ----------
col1, col2 = st.columns([2, 1])

with col1:
    search = st.text_input(
        "Search courses or careers",
        placeholder="🔍 Try medicine, engineering, doctor..."
    ).strip().casefold()

with col2:
    categories = ["All"] + sorted(
        set(course["category"] for course in courses)
    )

    category_filter = st.selectbox(
        "Subject area",
        categories
    )


# ---------- FILTER COURSES ----------
filtered_courses = []

for course in courses:
    searchable_text = (
        course["name"] + " "
        + course["category"] + " "
        + course["description"] + " "
        + " ".join(course["careers"]) + " "
        + course["subjects"]
    ).casefold()

    matches_search = search in searchable_text

    matches_category = (
        category_filter == "All"
        or course["category"] == category_filter
    )

    if matches_search and matches_category:
        filtered_courses.append(course)


st.caption(
    f"Showing {len(filtered_courses)} of {len(courses)} courses"
)

st.divider()


# ---------- THREE-COLUMN COURSE GRID ----------
if not filtered_courses:
    st.warning("No matching courses found. Try another search.")

else:
    columns_per_row = 3

    for start in range(
        0, len(filtered_courses), columns_per_row
    ):
        row_courses = filtered_courses[
            start:start + columns_per_row
        ]

        columns = st.columns(columns_per_row, gap="medium")

        for column, course in zip(columns, row_courses):
            with column:
                with st.container(border=True):

                    st.markdown(
                        f"### {course['icon']} {course['name']}"
                    )

                    st.markdown(
                        f'<span class="course-category">'
                        f'{course["category"]}</span>',
                        unsafe_allow_html=True
                    )

                    st.write("")

                    st.markdown(
                        '<div class="course-label">'
                        'WHAT YOU WILL LEARN</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f'<div class="course-description">'
                        f'{course["description"]}</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        '<div class="course-label">'
                        'POSSIBLE CAREERS</div>',
                        unsafe_allow_html=True
                    )

                    for career in course["careers"]:
                        st.markdown(f"- {career}")

                    with st.expander(
                        "Useful subjects and entry guidance"
                    ):
                        st.write(course["subjects"])

                    st.link_button(
                        "Explore career information ↗",
                        course["website"],
                        use_container_width=True
                    )


# ---------- FOOTER ----------
st.markdown(
    """
    <div class="footer-note">
        PathGuide SA · Explore your options. Plan your future.
    </div>
    """,
    unsafe_allow_html=True
)
