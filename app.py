
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

users = {
    "admin": "1234"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            return redirect(url_for("dashboard"))
        return "Invalid login"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return "Login Successful - " + datetime.now().strftime("%d-%m-%Y")

if __name__ == "__main__":
    app.run(debug=True)
