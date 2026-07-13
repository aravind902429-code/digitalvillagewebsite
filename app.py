from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "digitalvillage123"

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return render_template("about.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mobile = request.form["mobile"]
        password = request.form["password"]

        conn = sqlite3.connect("village.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE mobile=? AND password=?",
            (mobile, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Mobile Number or Password"

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        aadhaar = request.form["aadhaar"]
        village = request.form["village"]
        password = request.form["password"]

        conn = sqlite3.connect("village.db")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users(name, mobile, email, aadhaar, village, password)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, mobile, email, aadhaar, village, password))

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------- SCHEMES ----------------
@app.route("/schemes")
def schemes():
    return render_template("schemes.html")


# ---------------- WATER ----------------
@app.route("/water")
def water():
    return render_template("water.html")


# ---------------- ELECTRICITY ----------------
@app.route("/electricity")
def electricity():
    return render_template("electricity.html")


# ---------------- COMPLAINT ----------------
@app.route("/complaint", methods=["GET", "POST"])
def complaint():
    if request.method == "POST":
        name = request.form["name"]
        mobile = request.form["mobile"]
        complaint_type = request.form["type"]
        details = request.form["details"]

        conn = sqlite3.connect("village.db")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO complaints(name, mobile, type, details)
            VALUES (?, ?, ?, ?)
        """, (name, mobile, complaint_type, details))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("complaint.html")


# ---------------- VILLAGE NEWS ----------------
@app.route("/villagenews")
def villagenews():
    return render_template("villagenews.html")


# ---------------- CONTACT ----------------
@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---------------- CERTIFICATE ----------------
@app.route("/certificate", methods=["GET", "POST"])
def certificate():
    conn = sqlite3.connect("village.db")
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mobile TEXT,
        certificate TEXT,
        reason TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    if request.method == "POST":
        name = request.form["name"]
        mobile = request.form["mobile"]
        certificate = request.form["certificate"]
        reason = request.form["reason"]

        # Check if already applied
        cur.execute(
            "SELECT * FROM certificates WHERE mobile=? AND certificate=?",
            (mobile, certificate)
        )

        if cur.fetchone():
            conn.close()
            return "You have already applied for this certificate."

        # Save application
        cur.execute("""
        INSERT INTO certificates(name, mobile, certificate, reason, status)
        VALUES (?, ?, ?, ?, ?)
        """, (name, mobile, certificate, reason, "Pending"))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    conn.close()
    return render_template("certificate.html")
# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        return redirect(url_for("dashboard"))

    return render_template("upload.html")
# ---------------- ADMIN LOGIN ----------------
@app.route("/adminlogin", methods=["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            return "Invalid Admin Username or Password"

    return render_template("adminlogin.html")
# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect(url_for("adminlogin"))

    conn = sqlite3.connect("village.db")
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM certificates ORDER BY id DESC")
        certificates = cur.fetchall()

    except sqlite3.Error:
        certificates = []

    conn.close()

    return render_template("admin.html", certificates=certificates)
# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():
    return render_template("profile.html")

# ---------------- ADMIN LOGOUT ----------------
@app.route("/adminlogout")
def adminlogout():
    session.pop("admin", None)
    return redirect(url_for("adminlogin"))
# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)