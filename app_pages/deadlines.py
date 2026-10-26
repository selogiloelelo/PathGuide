
import streamlit as st
import calendar
from datetime import date, datetime
from urllib.parse import urlencode
from html import escape
from database import get_universities, get_bursaries


# ---------- PAGE HEADER ----------
st.title("📅 Application Deadlines")
st.caption(
    "Plan ahead by exploring university application "
    "and bursary closing dates."
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
            result = datetime.strptime(value, date_format).date()

            if result.year < 2000:
                return None

            return result
        except ValueError:
            continue

    return None


# ---------- LOAD DATABASE ----------
universities = [dict(row) for row in get_universities()]
bursaries = [dict(row) for row in get_bursaries()]


# ---------- GROUP DEADLINES BY DATE ----------
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


# ---------- URL STATE ----------
def make_url(updates):
    params = dict(st.query_params)
    params.update(updates)
    return "?" + urlencode(params)


def get_calendar_state(prefix):
    today = date.today()

    selected_value = st.query_params.get(
        f"{prefix}_date", today.isoformat()
    )

    try:
        selected = date.fromisoformat(selected_value)
    except (ValueError, TypeError):
        selected = today

    try:
        year = int(
            st.query_params.get(f"{prefix}_year", selected.year)
        )
        month = int(
            st.query_params.get(f"{prefix}_month", selected.month)
        )

        if not 1 <= month <= 12 or not 1900 <= year <= 2200:
            raise ValueError

    except (ValueError, TypeError):
        year = selected.year
        month = selected.month

    return year, month, selected


# ---------- CALENDAR DESIGN ----------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

.calendar-switch {
    display: flex;
    gap: 8px;
    margin: 12px 0 22px 0;
}

.calendar-switch a {
    flex: 1;
    text-align: center;
    padding: 12px 8px;
    border-radius: 12px;
    border: 1px solid var(--border-color, #dddddd);
    text-decoration: none !important;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-color) !important;
}

.calendar-switch a.active {
    background: #2563eb;
    color: white !important;
    border-color: #2563eb;
}

.calendar-header {
    display: grid;
    grid-template-columns: 44px minmax(0, 1fr) 44px;
    align-items: center;
    gap: 8px;
    margin-bottom: 14px;
}

.calendar-header .month-name {
    text-align: center;
    font-size: 19px;
    font-weight: 700;
}

.calendar-header .month-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 40px;
    border-radius: 12px;
    border: 1px solid var(--border-color, #dddddd);
    text-decoration: none !important;
    color: var(--text-color) !important;
    font-size: 24px;
}

.weekday-grid,
.date-grid {
    display: grid;
    grid-template-columns: repeat(7, minmax(0, 1fr));
    gap: 3px;
}

.weekday-grid {
    margin-bottom: 8px;
}

.weekday {
    text-align: center;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-color);
    opacity: 0.65;
    padding: 8px 0;
}

.date-cell {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    min-width: 0;
    min-height: 51px;
    padding: 3px 0;
    border-radius: 12px;
    text-decoration: none !important;
    color: var(--text-color) !important;
    box-sizing: border-box;
}

.date-cell .day-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    font-size: 14px;
    line-height: 1;
}

.date-cell.selected .day-number {
    background: #2563eb;
    color: white;
    font-weight: 700;
}

.date-cell.today:not(.selected) .day-number {
    border: 1px solid #2563eb;
    font-weight: 700;
}

.date-cell .deadline-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #3b82f6;
    margin-top: 2px;
}

.date-cell.selected .deadline-dot {
    background: #2563eb;
}

.date-cell:hover {
    background: var(--secondary-background-color, #f2f2f2);
}

.calendar-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    align-items: center;
    font-size: 12px;
    opacity: 0.8;
    margin: 12px 0 20px 0;
}

.legend-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #3b82f6;
    margin-right: 5px;
}

.legend-today {
    display: inline-block;
    width: 13px;
    height: 13px;
    border: 1px solid #2563eb;
    border-radius: 50%;
    vertical-align: middle;
    margin-right: 5px;
}

@media (max-width: 480px) {
    .block-container {
        padding-left: 0.45rem;
        padding-right: 0.45rem;
    }

    .calendar-header .month-name {
        font-size: 17px;
    }

    .weekday-grid,
    .date-grid {
        gap: 1px;
    }

    .date-cell {
        min-height: 45px;
        border-radius: 9px;
    }

    .date-cell .day-number {
        width: 31px;
        height: 31px;
        font-size: 13px;
    }

    .weekday {
        font-size: 11px;
    }

    .calendar-switch a {
        font-size: 12px;
        padding: 11px 4px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------- CALENDAR RENDERER ----------
def show_calendar(prefix, title, emoji, deadline_lookup):
    today = date.today()
    year, month, selected = get_calendar_state(prefix)

    st.subheader(f"{emoji} {title}")

    # Month navigation
    previous_month = month - 1
    previous_year = year

    if previous_month == 0:
        previous_month = 12
        previous_year -= 1

    next_month = month + 1
    next_year = year

    if next_month == 13:
        next_month = 1
        next_year += 1

    # Keep the selected day where possible when changing months
    previous_day = min(
        selected.day,
        calendar.monthrange(previous_year, previous_month)[1]
    )
    next_day = min(
        selected.day,
        calendar.monthrange(next_year, next_month)[1]
    )

    previous_selected = date(
        previous_year, previous_month, previous_day
    )
    next_selected = date(
        next_year, next_month, next_day
    )

    previous_url = make_url({
        "active_calendar": prefix,
        f"{prefix}_year": previous_year,
        f"{prefix}_month": previous_month,
        f"{prefix}_date": previous_selected.isoformat(),
    })

    next_url = make_url({
        "active_calendar": prefix,
        f"{prefix}_year": next_year,
        f"{prefix}_month": next_month,
        f"{prefix}_date": next_selected.isoformat(),
    })

    month_name = calendar.month_name[month]

    st.markdown(
        f"""
        <div class="calendar-header">
            <a class="month-arrow"
               href="{escape(previous_url, quote=True)}"
               aria-label="Previous month">‹</a>
            <div class="month-name">
                {month_name} {year}
            </div>
            <a class="month-arrow"
               href="{escape(next_url, quote=True)}"
               aria-label="Next month">›</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Weekdays and dates start on Sunday
    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    weekday_html = "".join(
        f'<div class="weekday">{day}</div>'
        for day in weekdays
    )

    st.markdown(
        f'<div class="weekday-grid">{weekday_html}</div>',
        unsafe_allow_html=True
    )

    month_calendar = calendar.Calendar(firstweekday=6)
    weeks = month_calendar.monthdayscalendar(year, month)

    date_cells = []

    for week in weeks:
        for day_number in week:
            if day_number == 0:
                date_cells.append(
                    '<div class="date-cell empty"></div>'
                )
                continue

            chosen_date = date(year, month, day_number)
            date_key = chosen_date.isoformat()

            has_deadline = date_key in deadline_lookup
            is_selected = chosen_date == selected
            is_today = chosen_date == today

            classes = ["date-cell"]

            if is_selected:
                classes.append("selected")

            if is_today:
                classes.append("today")

            url = make_url({
                "active_calendar": prefix,
                f"{prefix}_year": year,
                f"{prefix}_month": month,
                f"{prefix}_date": date_key,
            })

            dot_html = (
                '<span class="deadline-dot"></span>'
                if has_deadline
                else ""
            )

            date_cells.append(
                f'<a class="{" ".join(classes)}" '
                f'href="{escape(url, quote=True)}" '
                f'aria-label="{chosen_date.strftime("%A, %d %B %Y")}" '
                f'title="{chosen_date.strftime("%d %B %Y")}'
                f'{" — Deadline recorded" if has_deadline else ""}">'
                f'<span class="day-number">{day_number}</span>'
                f'{dot_html}'
                f'</a>'
            )

    st.markdown(
        '<div class="date-grid">'
        + "".join(date_cells)
        + '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
        <div class="calendar-legend">
            <span><span class="legend-dot"></span>Deadline recorded</span>
            <span><span class="legend-today"></span>Today</span>
        </div>
    """, unsafe_allow_html=True)

    # ---------- SELECTED DATE RESULTS ----------
    st.divider()

    st.markdown(
        f"### {selected.strftime('%A, %d %B %Y')}"
    )

    matches = deadline_lookup.get(selected.isoformat(), [])

    if matches:
        st.success(
            f"{len(matches)} deadline(s) recorded for this date."
        )

        for index, item in enumerate(matches):
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
                        key=f"{prefix}_website_{index}_{selected.isoformat()}",
                        use_container_width=True
                    )
    else:
        st.info(
            "No recorded closing deadlines for this date. "
            "Check official websites for additional or "
            "programme-specific deadlines."
        )

    st.caption(
        "Deadline information may change. Always confirm "
        "dates on the relevant official website."
    )


# ---------- CALENDAR SWITCHER ----------
active_calendar = st.query_params.get(
    "active_calendar", "university"
)

if active_calendar not in ["university", "bursary"]:
    active_calendar = "university"

university_tab_url = make_url({
    "active_calendar": "university"
})

bursary_tab_url = make_url({
    "active_calendar": "bursary"
})

university_class = (
    "active" if active_calendar == "university" else ""
)

bursary_class = (
    "active" if active_calendar == "bursary" else ""
)

st.markdown(
    f"""
    <div class="calendar-switch">
        <a class="{university_class}"
           href="{escape(university_tab_url, quote=True)}">
           🎓 Universities
        </a>
        <a class="{bursary_class}"
           href="{escape(bursary_tab_url, quote=True)}">
           💰 Bursaries
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------- DISPLAY SELECTED CALENDAR ----------
if active_calendar == "university":
    show_calendar(
        "u",
        "University Application Deadlines",
        "🎓",
        university_deadlines
    )
else:
    show_calendar(
        "b",
        "Bursary & Scholarship Deadlines",
        "💰",
        bursary_deadlines
    )
