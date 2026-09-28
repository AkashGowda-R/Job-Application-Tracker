from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date


app = Flask(__name__)


# =========================
# Database Connection
# =========================

def get_db_connection():
    connection = sqlite3.connect("applications.db")
    connection.row_factory = sqlite3.Row
    return connection


# =========================
# Dashboard
# =========================

@app.route("/")
def index():

    conn = get_db_connection()

    # Search and status filter
    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "").strip()

    query = """
        SELECT *
        FROM applications
        WHERE 1=1
    """

    parameters = []

    if search:
        query += """
            AND (
                company LIKE ?
                OR job_title LIKE ?
                OR location LIKE ?
            )
        """

        parameters.extend([
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ])

    if status_filter:
        query += " AND status = ?"
        parameters.append(status_filter)

    query += " ORDER BY id DESC"

    applications = conn.execute(
        query,
        parameters
    ).fetchall()


    # Dashboard statistics
    total_applications = conn.execute(
        "SELECT COUNT(*) FROM applications"
    ).fetchone()[0]

    applied = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE status = ?",
        ("Applied",)
    ).fetchone()[0]

    interviews = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE status = ?",
        ("Interview",)
    ).fetchone()[0]

    offers = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE status = ?",
        ("Offer",)
    ).fetchone()[0]

    rejected = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE status = ?",
        ("Rejected",)
    ).fetchone()[0]

    withdrawn = conn.execute(
        "SELECT COUNT(*) FROM applications WHERE status = ?",
        ("Withdrawn",)
    ).fetchone()[0]


    # Follow-ups
    today = date.today().isoformat()

    due_applications = conn.execute(
        """
        SELECT *
        FROM applications
        WHERE follow_up_date IS NOT NULL
            AND follow_up_date != ''
            AND follow_up_date <= ?
            AND status NOT IN ('Rejected', 'Withdrawn', 'Offer')
        ORDER BY follow_up_date ASC
        """,
        (today,)
    ).fetchall()

    follow_ups_due = len(due_applications)


    # Application rates
    interview_rate = 0
    offer_rate = 0

    if total_applications > 0:
        interview_rate = round(
            (interviews / total_applications) * 100,
            1
        )

        offer_rate = round(
            (offers / total_applications) * 100,
            1
        )


    conn.close()


    return render_template(
        "index.html",
        applications=applications,
        follow_ups_due=follow_ups_due,
        total_applications=total_applications,
        due_applications=due_applications,
        today=today,
        applied=applied,
        interviews=interviews,
        offers=offers,
        rejected=rejected,
        withdrawn=withdrawn,
        interview_rate=interview_rate,
        offer_rate=offer_rate
    )


# =========================
# Add Application
# =========================

@app.route("/add", methods=["GET", "POST"])
def add_application():

    if request.method == "POST":

        company = request.form["company"]
        job_title = request.form["job_title"]
        location = request.form["location"]
        status = request.form["status"]
        priority = request.form["priority"]
        application_date = request.form["application_date"]
        follow_up_date = request.form["follow_up_date"]
        job_url = request.form["job_url"]
        notes = request.form["notes"]

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO applications
            (
                company,
                job_title,
                location,
                status,
                priority,
                application_date,
                follow_up_date,
                job_url,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company,
                job_title,
                location,
                status,
                priority,
                application_date,
                follow_up_date,
                job_url,
                notes
            )
        )

        conn.commit()
        conn.close()

        return redirect("/")


    return render_template("add_application.html")


# =========================
# Edit Application
# =========================

@app.route(
    "/application/<int:application_id>/edit",
    methods=["GET", "POST"]
)
def edit_application(application_id):

    conn = get_db_connection()

    application = conn.execute(
        """
        SELECT *
        FROM applications
        WHERE id = ?
        """,
        (application_id,)
    ).fetchone()


    # Application not found
    if application is None:
        conn.close()
        return redirect("/")


    if request.method == "POST":

        company = request.form["company"]
        job_title = request.form["job_title"]
        location = request.form["location"]
        status = request.form["status"]
        priority = request.form["priority"]
        application_date = request.form["application_date"]
        follow_up_date = request.form["follow_up_date"]
        job_url = request.form["job_url"]
        notes = request.form["notes"]

        conn.execute(
            """
            UPDATE applications
            SET
                company = ?,
                job_title = ?,
                location = ?,
                status = ?,
                priority = ?,
                application_date = ?,
                follow_up_date = ?,
                job_url = ?,
                notes = ?
            WHERE id = ?
            """,
            (
                company,
                job_title,
                location,
                status,
                priority,
                application_date,
                follow_up_date,
                job_url,
                notes,
                application_id
            )
        )

        conn.commit()
        conn.close()

        return redirect(
            f"/application/{application_id}"
        )


    conn.close()

    return render_template(
        "edit_application.html",
        application=application
    )


# =========================
# Delete Application
# =========================

@app.route(
    "/application/<int:application_id>/delete",
    methods=["POST"]
)
def delete_application(application_id):

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM applications
        WHERE id = ?
        """,
        (application_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# =========================
# Quick Change Status
# =========================

@app.route(
    "/application/<int:application_id>/status",
    methods=["POST"]
)
def update_status(application_id):

    status = request.form["status"]

    conn = get_db_connection()

    conn.execute(
        """
        UPDATE applications
        SET status = ?
        WHERE id = ?
        """,
        (status, application_id)
    )

    conn.commit()
    conn.close()

    return redirect(
        f"/application/{application_id}"
    )


# =========================
# Application Details
# =========================

@app.route("/application/<int:application_id>")
def application_details(application_id):

    conn = get_db_connection()

    application = conn.execute(
        """
        SELECT *
        FROM applications
        WHERE id = ?
        """,
        (application_id,)
    ).fetchone()

    conn.close()


    # Application not found
    if application is None:
        return redirect("/")


    return render_template(
        "application_details.html",
        application=application
    )


# =========================
# Run Application
# =========================

if __name__ == "__main__":
    app.run(debug=True)