from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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
    if request.method == "POST":
        return redirect(url_for("dashboard"))

    return render_template("certificate.html")
# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        return redirect(url_for("dashboard"))

    return render_template("upload.html")


# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():
    return render_template("profile.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    return redirect(url_for("home"))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)