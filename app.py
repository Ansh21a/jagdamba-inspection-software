from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_NAME = "inspection_software.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/party-master", methods=["GET", "POST"])
def party_master():
    conn = get_db_connection()
    if request.method == "POST":
        name = request.form["party_name"]
        conn.execute("INSERT INTO party (name) VALUES (?)", (name,))
        conn.commit()
    parties = conn.execute("SELECT * FROM party").fetchall()
    conn.close()
    return render_template("party_master.html", parties=parties)

@app.route("/inspector-master", methods=["GET", "POST"])
def inspector_master():
    conn = get_db_connection()
    if request.method == "POST":
        name = request.form["inspector_name"]
        conn.execute("INSERT INTO inspector (name) VALUES (?)", (name,))
        conn.commit()
    inspectors = conn.execute("SELECT * FROM inspector").fetchall()
    conn.close()
    return render_template("inspector_master.html", inspectors=inspectors)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
