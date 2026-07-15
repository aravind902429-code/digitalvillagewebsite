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
@app.route("/water", methods=["GET", "POST"])
def water():

    conn = sqlite3.connect("village.db")
    cur = conn.cursor()

    # Create table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS water_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mobile TEXT,
        area TEXT,
        issue TEXT,
        description TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    if request.method == "POST":

        name = request.form["name"]
        mobile = request.form["mobile"]
        area = request.form["area"]
        issue = request.form["issue"]
        description = request.form["description"]

        cur.execute("""
        INSERT INTO water_requests
        (name, mobile, area, issue, description, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, mobile, area, issue, description, "Pending"))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    conn.close()
    return render_template("water.html")
    
# ---------------- ELECTRICITY ----------------
@app.route("/electricity", methods=["GET", "POST"])
def electricity():

    conn = sqlite3.connect("village.db")
    cur = conn.cursor()

    # Create table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS electricity_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mobile TEXT,
        area TEXT,
        issue TEXT,
        description TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    if request.method == "POST":

        name = request.form["name"]
        mobile = request.form["mobile"]
        area = request.form["area"]
        issue = request.form["issue"]
        description = request.form["description"]

        cur.execute("""
        INSERT INTO electricity_requests
        (name, mobile, area, issue, description, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, mobile, area, issue, description, "Pending"))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    conn.close()
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
        # Water Requests
        cur.execute("SELECT * FROM water_requests ORDER BY id DESC")
        water_requests = cur.fetchall()

        # Electricity Requests
        cur.execute("SELECT * FROM electricity_requests ORDER BY id DESC")
        electricity_requests = cur.fetchall()

        # Road Requests
        cur.execute("SELECT * FROM road_requests ORDER BY id DESC")
        road_requests = cur.fetchall()

        # Certificate Applications
        cur.execute("SELECT * FROM certificates ORDER BY id DESC")
        certificates = cur.fetchall()

        # Complaint Applications
        cur.execute("SELECT * FROM complaints ORDER BY id DESC")
        complaints = cur.fetchall()

    except sqlite3.Error:
        water_requests = []
        electricity_requests = []
        road_requests = []
        certificates = []
        complaints = []

    conn.close()

    return render_template(
        "admin.html",
        water_requests=water_requests,
        electricity_requests=electricity_requests,
        road_requests=road_requests,
        certificates=certificates,
        complaints=complaints
    )
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

# ---------------- ROAD ----------------
@app.route("/road", methods=["GET", "POST"])
def road():

    conn = sqlite3.connect("village.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS road_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        mobile TEXT,
        area TEXT,
        issue TEXT,
        description TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    if request.method == "POST":

        name = request.form["name"]
        mobile = request.form["mobile"]
        area = request.form["area"]
        issue = request.form["issue"]
        description = request.form["description"]

        cur.execute("""
        INSERT INTO road_requests
        (name,mobile,area,issue,description,status)
        VALUES(?,?,?,?,?,?)
        """,(name,mobile,area,issue,description,"Pending"))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    conn.close()

    return render_template("road.html")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)