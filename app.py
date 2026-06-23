
from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
from datetime import datetime
try:
    from weasyprint import HTML
    WEASY = True
except:
    WEASY = False

APP_NAME = "Jagdamba Inspection Software"
DB = "inspection_software.db"

app = Flask(__name__)

def db():
    return sqlite3.connect(DB)

def init_db():
    con = db(); cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS party_master(id INTEGER PRIMARY KEY AUTOINCREMENT, party_name TEXT, address TEXT, gst_no TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS inspector_master(id INTEGER PRIMARY KEY AUTOINCREMENT, inspector_name TEXT, designation TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS reports(id INTEGER PRIMARY KEY AUTOINCREMENT, party TEXT, inspector TEXT, insp_date TEXT)")
    cur.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES('admin','admin123','admin')")
    con.commit(); con.close()

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u,p = request.form["u"], request.form["p"]
        con=db(); cur=con.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))
        ok = cur.fetchone(); con.close()
        if ok: return redirect(url_for("dashboard"))
    return render_template("login.html", app=APP_NAME)

@app.route("/dashboard")
def dashboard():
    con=db(); cur=con.cursor()
    cur.execute("SELECT COUNT(*) FROM party_master"); parties=cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM inspector_master"); inspectors=cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM reports"); reports=cur.fetchone()[0]
    con.close()
    return render_template("dashboard.html", parties=parties, inspectors=inspectors, reports=reports, app=APP_NAME)

@app.route("/party", methods=["GET","POST"])
def party():
    if request.method=="POST":
        con=db(); cur=con.cursor()
        cur.execute("INSERT INTO party_master(party_name,address,gst_no) VALUES(?,?,?)",
                    (request.form["party"],request.form["addr"],request.form["gst"]))
        con.commit(); con.close()
    con=db(); cur=con.cursor()
    cur.execute("SELECT * FROM party_master"); rows=cur.fetchall(); con.close()
    return render_template("party_master.html", rows=rows, app=APP_NAME)

@app.route("/inspector", methods=["GET","POST"])
def inspector():
    if request.method=="POST":
        con=db(); cur=con.cursor()
        cur.execute("INSERT INTO inspector_master(inspector_name,designation) VALUES(?,?)",
                    (request.form["name"],request.form["desig"]))
        con.commit(); con.close()
    con=db(); cur=con.cursor()
    cur.execute("SELECT * FROM inspector_master"); rows=cur.fetchall(); con.close()
    return render_template("inspector_master.html", rows=rows, app=APP_NAME)

@app.route("/report", methods=["GET","POST"])
def report():
    con=db(); cur=con.cursor()
    cur.execute("SELECT party_name FROM party_master"); parties=[r[0] for r in cur.fetchall()]
    cur.execute("SELECT inspector_name FROM inspector_master"); inspectors=[r[0] for r in cur.fetchall()]
    if request.method=="POST":
        cur.execute("INSERT INTO reports(party, inspector, insp_date) VALUES(?,?,?)",
                    (request.form["party"], request.form["inspector"], request.form["date"]))
        con.commit()
    con.close()
    return render_template("report.html", parties=parties, inspectors=inspectors, app=APP_NAME)

@app.route("/pdf")
def pdf():
    html = render_template("pdf.html", party="Sample Party", inspector="MR. JAYDIP CHAUHAN",
                           date=datetime.now().strftime("%d/%m/%Y"), app=APP_NAME)
    if WEASY:
        pdf = HTML(string=html, base_url=".").write_pdf()
        resp = make_response(pdf)
        resp.headers["Content-Type"]="application/pdf"
        resp.headers["Content-Disposition"]="attachment; filename=Inspection_Report.pdf"
        return resp
    return html

if __name__=="__main__":
    init_db()
    app.run(debug=True)
