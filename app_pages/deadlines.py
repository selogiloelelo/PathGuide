
import streamlit as st
import calendar
from datetime import date, datetime
from database import get_universities, get_bursaries

st.set_page_config(
    page_title="Application Deadlines | PathGuide SA",
    page_icon="📅",
    layout="wide"
)

# ---------- PAGE HEADER ----------
st.title("📅 Application Deadlines")
st.caption(
    "Plan ahead. Select a date to discover university "
    "application and bursary deadlines."
)

# ---------- DATE HELPER ----------
def parse_date(value):
    if not value or not isinstance(value, str):
        return None

    value = value.strip()

    formats = [
        "%d %B %Y, %H:%M",
        "%d %B %Y %H:%M",
        "%d %B %Y",
        "%d %b %Y",
    ]

    for date_format in formats:
        try:
            return datetime.strptime(value, date_format).date()
        except ValueError:
            continue

    return None


# ---------- LOAD DATABASE DATA ----------
universities = [
    dict(row) for row in get_universities()
]

bursaries = [
    dict(row) for row in get_bursaries()
]


# ---------- GROUP OPPORTUNITIES BY CLOSING DATE ----------
def build_deadline_lookup(items):
    lookup = {}

    for item in items:
        closing_date = parse_date(
            item.get("closing_date")
        )

        if closing_date:
            key = closing_date.isoformat()
            lookup.setdefault(key, []).append(item)

    return lookup


university_deadlines = build_deadline_lookup(universities)
bursary_deadlines = build_deadline_lookup(bursaries)


# ---------- CALENDAR STYLING ----------
st.markdown("""
<style>
/* Main page spacing */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Calendar headings */
.calendar-month-title {
    text-align: center;
    font-size: 1.15rem;
    font-weight: 700;
    padding: 0.45rem 0;
}

/* Weekday headings */
.calendar-weekday {
    text-align: center;
    color: var(--text-color);
    opacity: 0.7;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.35rem 0;
}

/* Date buttons */
div[data-testid="stButton"] button {
    min-height: 40px;
    padding: 0.1rem 0.05rem;
    border-radius: 12px;
    font-size: 0.82rem;
    font-weight: 500;
    white-space: normal;
    overflow-wrap: anywhere;
}

/* Tighter calendar grid */
div[data-testid="stHorizontalBlock"] {
    gap: 0.25rem;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-weight: 600;
}

/* Mobile adjustments */
@media (max-width: 600px) {
    .block-container {
        padding-top: 1rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }

    div[data-testid="stButton"] button {
        min-height: 38px;
        padding: 0;
        font-size: 0.75rem;
        border-radius: 10px;
    }

    .calendar-month-title {
        font-size: 1rem;
    }

    .calendar-weekday {
        font-size: 0.7rem;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------- CALENDAR FUNCTION ----------
def show_calendar(
    calendar_id,
    heading,
    emoji,
    deadline_lookup
):
    today = date.today()

    year_key = f"{calendar_id}_year"
    month_key = f"{calendar_id}_month"
    selected_key = f"{calendar_id}_selected_date"

    if year_key not in st.session_state:
        st.session_state[year_key] = today.year

    if month_key not in st.session_state:
        st.session_state[month_key] = today.month

    if selected_key not in st.session_state:
        st.session_state[selected_key] = today.isoformat()

    st.subheader(f"{emoji} {heading}")

    # ---------- MONTH NAVIGATION ----------
    previous, month_display, next_month = st.columns(
        [1, 4, 1]
    )

    with previous:
        if st.button(
            "‹",
            key=f"{calendar_id}_previous",
            use_container_width=True
        ):
            if st.session_state[month_key] == 1:
                st.session_state[month_key] = 12
                st.session_state[year_key] -= 1
            else:
                st.session_state[month_key] -= 1

            st.rerun()

    with month_display:
        month_name = calendar.month_name[
            st.session_state[month_key]
        ]

        st.markdown(
            f'<div class="calendar-month-title">'
            f'{month_name} {st.session_state[year_key]}'
            f'</div>',
            unsafe_allow_html=True
        )

    with next_month:
        if st.button(
            "›",
            key=f"{calendar_id}_next",
            use_container_width=True
        ):
            if st.session_state[month_key] == 12:
                st.session_state[month_key] = 1
                st.session_state[year_key] += 1
            else:
                st.session_state[month_key] += 1

            st.rerun()

    # ---------- WEEKDAY HEADINGS ----------
    weekdays = ["S", "M", "T", "W", "T", "F", "S"]

    weekday_columns = st.columns(7)

    for column, weekday in zip(
        weekday_columns, weekdays
    ):
        column.markdown(
            f'<div class="calendar-weekday">'
            f'{weekday}</div>',
            unsafe_allow_html=True
        )

    # ---------- CALENDAR DATES ----------
    month_calendar = calendar.Calendar(
        firstweekday=6
    )

    weeks = month_calendar.monthdayscalendar(
        st.session_state[year_key],
        st.session_state[month_key]
    )

    for week_index, week in enumerate(weeks):
        columns = st.columns(7)

        for day_index, day_number in enumerate(week):
            with columns[day_index]:

                if day_number == 0:
                    st.write("")
                    continue

                chosen_date = date(
                    st.session_state[year_key],
                    st.session_state[month_key],
                    day_number
                )

                date_key = chosen_date.isoformat()

                has_deadline = (
                    date_key in deadline_lookup
                )

                is_selected = (
                    st.session_state[selected_key]
                    == date_key
                )

                is_today = chosen_date == today

                # Keep the date number readable.
                # Deadline dots and today's marker are separate.
                if is_today:
                    label = f"• {day_number}"
                else:
                    label = str(day_number)

                if has_deadline:
                    label = f"● {day_number}"

                if is_today and has_deadline:
                    label = f"● {day_number} •"

                if st.button(
                    label,
                    key=f"{calendar_id}_day_{date_key}",
                    use_container_width=True,
                    type=(
                        "primary"
                        if is_selected
                        else "secondary"
                    ),
                    help=(
                        "Deadline recorded"
                        if has_deadline
                        else f"Select {chosen_date.strftime('%d %B %Y')}"
                    )
                ):
                    st.session_state[selected_key] = date_key
                    st.rerun()

    # ---------- SELECTED-DAY RESULTS ----------
    selected_date = st.session_state[selected_key]
    parsed_selected_date = date.fromisoformat(
        selected_date
    )

    st.divider()

    st.markdown(
        f"**{parsed_selected_date.strftime('%A, %d %B %Y')}**"
    )

    matches = deadline_lookup.get(
        selected_date, []
    )

    if matches:
        st.success(
            f"{len(matches)} closing deadline(s) recorded"
        )

        for item in matches:
            with st.container(border=True):
                st.markdown(
                    f"**{emoji} {item.get('name', 'Opportunity')}**"
                )

                if item.get("provider"):
                    st.caption(
                        f"Provider: {item['provider']}"
                    )

                if item.get("closing_date"):
                    st.write(
                        f"Closing date: {item['closing_date']}"
                    )

                if item.get("description"):
                    st.write(item["description"])

                if item.get("eligibility"):
                    st.caption(
                        f"Eligibility: {item['eligibility']}"
                    )

                if item.get("website"):
                    st.link_button(
                        "Visit official website ↗",
                        item["website"],
                        key=(
                            f"{calendar_id}_link_"
                            f"{item.get('id', item['name'])}"
                        ),
                        use_container_width=True
                    )

    else:
        st.info(
            "No closing deadlines are recorded for this date. "
            "Some opportunities may have unlisted or "
            "programme-specific deadlines."
        )

    st.caption(
        "● Deadline recorded · • Today. "
        "Confirm dates on official websites."
    )


# ---------- UNIVERSITY AND BURSARY TABS ----------
university_tab, bursary_tab = st.tabs([
    "🎓 Universities",
    "💰 Bursaries"
])

with university_tab:
    show_calendar(
        "university_calendar",
        "University Deadlines",
        "🎓",
        university_deadlines
    )

with bursary_tab:
    show_calendar(
        "bursary_calendar",
        "Bursary & Scholarship Deadlines",
        "💰",
        bursary_deadlines
    )
