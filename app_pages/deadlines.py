
import streamlit as st
import calendar
from datetime import date, datetime
from database import get_universities, get_bursaries

st.title("📅 Application Deadline Calendars")
st.write(
    "Explore university application and bursary deadlines. "
    "Select any date to see opportunities closing that day."
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


# ---------- PREPARE DEADLINES ----------
universities = [dict(row) for row in get_universities()]
bursaries = [dict(row) for row in get_bursaries()]


def build_deadline_lookup(items):
    lookup = {}

    for item in items:
        closing_date = parse_date(item.get("closing_date"))

        if closing_date:
            key = closing_date.isoformat()
            lookup.setdefault(key, []).append(item)

    return lookup


university_deadlines = build_deadline_lookup(universities)
bursary_deadlines = build_deadline_lookup(bursaries)


# ---------- CALENDAR FUNCTION ----------
def show_calendar(calendar_id, heading, emoji, deadline_lookup):
    st.subheader(f"{emoji} {heading}")

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

    # Month navigation
    previous, month_display, next_month = st.columns([1, 3, 1])

    with previous:
        if st.button(
            "◀",
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
            f"<div style='text-align:center;font-weight:bold;"
            f"padding-top:8px'>"
            f"{month_name} {st.session_state[year_key]}"
            f"</div>",
            unsafe_allow_html=True
        )

    with next_month:
        if st.button(
            "▶",
            key=f"{calendar_id}_next",
            use_container_width=True
        ):
            if st.session_state[month_key] == 12:
                st.session_state[month_key] = 1
                st.session_state[year_key] += 1
            else:
                st.session_state[month_key] += 1
            st.rerun()

    # Weekday headings
    weekdays = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
    weekday_columns = st.columns(7)

    for column, weekday in zip(weekday_columns, weekdays):
        column.markdown(
            f"<div style='text-align:center;font-size:12px;"
            f"color:gray'>{weekday}</div>",
            unsafe_allow_html=True
        )

    weeks = calendar.monthcalendar(
        st.session_state[year_key],
        st.session_state[month_key]
    )

    # Draw calendar dates
    for week in weeks:
        columns = st.columns(7)

        for column, day_number in zip(columns, week):
            with column:
                if day_number == 0:
                    st.write(" ")
                    continue

                chosen_date = date(
                    st.session_state[year_key],
                    st.session_state[month_key],
                    day_number
                )

                date_key = chosen_date.isoformat()
                has_deadline = date_key in deadline_lookup
                is_selected = (
                    st.session_state[selected_key] == date_key
                )

                label = str(day_number)

                if has_deadline:
                    label = f"🔵 {day_number}"

                if chosen_date == today:
                    label = f"• {day_number}"

                if st.button(
                    label,
                    key=f"{calendar_id}_day_{date_key}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    st.session_state[selected_key] = date_key
                    st.rerun()

    # Results below this calendar
    selected_date = st.session_state[selected_key]
    parsed_selected_date = date.fromisoformat(selected_date)

    st.markdown("---")
    st.markdown(
        f"**Closing on {parsed_selected_date.strftime('%d %b %Y')}**"
    )

    matches = deadline_lookup.get(selected_date, [])

    if matches:
        st.success(f"{len(matches)} deadline(s) found.")

        for item in matches:
            with st.container(border=True):
                st.markdown(f"**{emoji} {item['name']}**")

                if item.get("provider"):
                    st.caption(f"Provider: {item['provider']}")

                st.caption(
                    f"Closing date: {item.get('closing_date', 'Not available')}"
                )

                if item.get("website"):
                    st.link_button(
                        "Official website",
                        item["website"],
                        key=f"{calendar_id}_link_{item['name']}"
                    )
    else:
        st.info("No recorded deadlines for this date.")

    st.caption(
        "🔵 Dates with recorded deadlines. "
        "Confirm dates on official websites."
    )


# ---------- DISPLAY BOTH CALENDARS SIDE BY SIDE ----------
# ---------- COMPACT CALENDAR LAYOUT ----------

# ---------- MOBILE-FRIENDLY CALENDAR LAYOUT ----------
st.markdown("""
<style>
.block-container {
    padding-top: 1.25rem;
    padding-left: 0.75rem;
    padding-right: 0.75rem;
}

/* Compact, comfortable date buttons */
div[data-testid="stButton"] button {
    min-height: 38px;
    padding: 0.15rem 0;
    font-size: 0.85rem;
    border-radius: 8px;
}

/* Reduce gaps between calendar columns */
div[data-testid="stHorizontalBlock"] {
    gap: 0.3rem;
}

/* Keep calendar headings neat */
h3 {
    font-size: 1.1rem;
}
</style>
""", unsafe_allow_html=True)

# Tabs keep the calendars from being squeezed together
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
        "Bursary Deadlines",
        "💰",
        bursary_deadlines
    )
