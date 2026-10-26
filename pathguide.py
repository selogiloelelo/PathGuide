
import sqlite3
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


# ---------- DATABASE LOCATION ----------
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "studentpath.db"


# ---------- DATABASE CONNECTION ----------
def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# ---------- AUTOMATIC STATUS CALCULATION ----------
def calculate_status(opening_date, closing_date):
    """Calculate an opportunity's status using its dates."""

    def parse_date(value, is_closing=False):
        if not value or not isinstance(value, str):
            return None

        value = value.strip()

        formats = [
            ("%d %B %Y, %H:%M", True),
            ("%d %B %Y %H:%M", True),
            ("%d %B %Y", False),
            ("%d %b %Y", False),
        ]

        for date_format, has_time in formats:
            try:
                parsed = datetime.strptime(value, date_format)

                # Avoid accepting obvious year-entry mistakes.
                if not 2000 <= parsed.year <= 2100:
                    return None

                # Date-only opening dates begin at midnight.
                # Date-only closing dates end at 23:59:59.
                if not has_time:
                    if is_closing:
                        parsed = parsed.replace(
                            hour=23,
                            minute=59,
                            second=59
                        )
                    else:
                        parsed = parsed.replace(
                            hour=0,
                            minute=0,
                            second=0
                        )

                return parsed

            except ValueError:
                continue

        return None

    opening = parse_date(opening_date)
    closing = parse_date(closing_date, is_closing=True)

    # Unknown or invalid dates must be verified.
    if opening is None or closing is None:
        return "VERIFY"

    # Opening date must not be later than closing date.
    if opening > closing:
        return "VERIFY"

    # Use South African local time.
    now = datetime.now(
        ZoneInfo("Africa/Johannesburg")
    ).replace(tzinfo=None)

    if now > closing:
        return "CLOSED"

    if now < opening:
        return "UPCOMING"

    return "OPEN"


# ---------- CREATE DATABASE TABLES ----------
def initialise_database():
    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS universities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                opening_date TEXT,
                closing_date TEXT,
                status TEXT DEFAULT 'VERIFY',
                website TEXT
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS bursaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                provider TEXT,
                description TEXT,
                opening_date TEXT,
                closing_date TEXT,
                eligibility TEXT,
                website TEXT,
                status TEXT DEFAULT 'VERIFY'
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS application_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                university_id INTEGER NOT NULL,
                progress TEXT NOT NULL DEFAULT 'Not started',
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_id, university_id),
                FOREIGN KEY (university_id)
                    REFERENCES universities(id)
            )
        """)

    print("PathGuide SA database is ready!")


# ---------- ADD OR UPDATE A UNIVERSITY ----------
def add_university(
    name,
    opening_date,
    closing_date,
    status,
    website
):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO universities
            (name, opening_date, closing_date, status, website)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                opening_date = excluded.opening_date,
                closing_date = excluded.closing_date,
                status = excluded.status,
                website = excluded.website
        """, (
            name,
            opening_date,
            closing_date,
            status,
            website
        ))


# ---------- GET UNIVERSITIES WITH AUTOMATIC STATUS ----------
def get_universities():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT * FROM universities
            ORDER BY name
        """).fetchall()

    universities = []

    for row in rows:
        university = dict(row)

        university["status"] = calculate_status(
            university["opening_date"],
            university["closing_date"]
        )

        universities.append(university)

    return universities


# ---------- UNIVERSITY DATA ----------
def seed_universities():
    universities = [
        (
            "University of Johannesburg (UJ)",
            "1 April 2026",
            "31 October 2026, 12:00",
            "VERIFY",
            "https://www.uj.ac.za/admission-aid/undergraduate/"
        ),
        (
            "University of Fort Hare (UFH)",
            "1 May 2026",
            "31 October 2026",
            "VERIFY",
            "https://www.ufh.ac.za/apply/apply-undergraduate"
        ),
        (
            "University of Mpumalanga (UMP)",
            "1 June 2026",
            "30 November 2026",
            "VERIFY",
            "https://www.ump.ac.za/Study-with-us/Application-Process/Online-Applications"
        ),
        (
            "University of Cape Town (UCT)",
            "1 April 2026",
            "31 July 2026",
            "CLOSED",
            "https://uct.ac.za/students/applications-apply-undergraduate-qualifications/application-procedure"
        ),
        (
            "University of the Free State (UFS)",
            "1 April 2026",
            "30 September 2026",
            "CLOSED",
            "https://www.ufs.ac.za/prospective/study-at-ufs/undergraduate/prospectus"
        ),
        (
            "University of Pretoria (UP)",
            "1 April 2026",
            "30 June 2026",
            "CLOSED",
            "https://www.up.ac.za/"
        ),
        (
            "Stellenbosch University",
            "1 April 2026",
            "31 July 2026",
            "CLOSED",
            "https://www.sun.ac.za/"
        ),
        (
            "University of the Witwatersrand (Wits)",
            "1 March 2026",
            "30 September 2026",
            "CLOSED",
            "https://www.wits.ac.za/"
        ),
        (
            "North-West University (NWU)",
            "Check official website",
            "Check official website",
            "VERIFY",
            "https://www.nwu.ac.za/"
        ),
        (
            "University of KwaZulu-Natal (UKZN)",
            "1 March 2026",
            "Check official website",
            "VERIFY",
            "https://www.ukzn.ac.za/"
        ),
        (
            "University of the Western Cape (UWC)",
            "1 April 2026",
            "Check official website",
            "VERIFY",
            "https://www.uwc.ac.za/"
        ),
        (
            "Nelson Mandela University",
            "Check official website",
            "Check official website",
            "VERIFY",
            "https://www.mandela.ac.za/"
        ),
        (
            "University of Limpopo (UL)",
            "Check official website",
            "Check official website",
            "VERIFY",
            "https://www.ul.ac.za/"
        ),
        (
            "University of Venda (UNIVEN)",
            "Check official website",
            "Check official website",
            "VERIFY",
            "https://www.univen.ac.za/"
        ),
        (
            "Walter Sisulu University (WSU)",
            "Check official website",
            "Check official website",
            "VERIFY",
            "https://www.wsu.ac.za/"
        ),
        (
            "Vaal University of Technology (VUT)",
            "1 April 2026",
            "30 September 2026",
            "CLOSED",
            "https://www.vut.ac.za/"
        ),
        (
            "Sefako Makgatho Health Science University (SMU)",
            "1 April 206",
            "31 July 2026",
            "CLOSED",
            "https://www.smu.ac.za/"
        )
    ]

    with get_connection() as connection:
        connection.executemany("""
            INSERT INTO universities
            (name, opening_date, closing_date, status, website)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                opening_date = excluded.opening_date,
                closing_date = excluded.closing_date,
                status = excluded.status,
                website = excluded.website
        """, universities)

    print("University data updated!")


# ---------- ADD OR UPDATE A BURSARY ----------
def add_bursary(
    name,
    provider,
    description,
    opening_date,
    closing_date,
    eligibility,
    website,
    status="VERIFY"
):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO bursaries
            (
                name, provider, description,
                opening_date, closing_date,
                eligibility, website, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                provider = excluded.provider,
                description = excluded.description,
                opening_date = excluded.opening_date,
                closing_date = excluded.closing_date,
                eligibility = excluded.eligibility,
                website = excluded.website,
                status = excluded.status
        """, (
            name,
            provider,
            description,
            opening_date,
            closing_date,
            eligibility,
            website,
            status
        ))


# ---------- GET BURSARIES WITH AUTOMATIC STATUS ----------
def get_bursaries():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT * FROM bursaries
            ORDER BY name
        """).fetchall()

    bursaries = []

    for row in rows:
        bursary = dict(row)

        bursary["status"] = calculate_status(
            bursary["opening_date"],
            bursary["closing_date"]
        )

        bursaries.append(bursary)

    return bursaries


# ---------- BURSARY DATA ----------
def seed_bursaries():
    bursaries = [
        (
            "NSFAS",
            "Government financial aid",
            "Financial assistance for eligible students at public universities and TVET colleges.",
            "18 September 2026",
            "31 October 2026",
            "Eligibility and household income requirements apply. Check the official website.",
            "https://www.nsfas.org.za/",
            "OPEN"
        ),
        (
            "Funza Lushaka",
            "Teaching",
            "Financial assistance for eligible students pursuing approved teaching qualifications.",
            "Check official website",
            "31 January 2027 (new applicants; verify)",
            "Applicants must meet the programme's age, academic and qualification requirements. Returning bursars may have different deadlines.",
            "https://www.funzalushaka.doe.gov.za/",
            "VERIFY"
        ),
        (
            "Sasol Bursaries",
            "Engineering and science",
            "Bursary opportunities may be available for selected engineering, science and related qualifications.",
            "Check official website",
            "Check official website",
            "Requirements vary by opportunity, qualification and academic year.",
            "https://www.sasol.com/",
            "VERIFY"
        ),
        (
            "National Skills Fund",
            "Skills development",
            "Explore funding information and opportunities listed by the National Skills Fund.",
            "Check official website",
            "Check official website",
            "Available programmes and eligibility requirements vary. Confirm current opportunities with the official fund.",
            "https://nsf.org.za/bursaries-and-scholarships/",
            "VERIFY"
        )
    ]

    for bursary in bursaries:
        add_bursary(*bursary)

    print("Bursary data updated!")


# ---------- APPLICATION PROGRESS FUNCTIONS ----------
def save_application_progress(
    student_id,
    university_id,
    progress
):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO application_progress
            (student_id, university_id, progress)
            VALUES (?, ?, ?)
            ON CONFLICT(student_id, university_id)
            DO UPDATE SET
                progress = excluded.progress,
                updated_at = CURRENT_TIMESTAMP
        """, (
            student_id,
            university_id,
            progress
        ))


def get_application_progress(student_id, university_id):
    with get_connection() as connection:
        result = connection.execute("""
            SELECT progress
            FROM application_progress
            WHERE student_id = ? AND university_id = ?
        """, (
            student_id,
            university_id
        )).fetchone()

        return result["progress"] if result else "Not started"


# ---------- RUN DATABASE SETUP ----------
if __name__ == "__main__":
    initialise_database()
    seed_universities()
    seed_bursaries()
