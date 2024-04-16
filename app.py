import sys
from db import getUserList
from flask import Flask, render_template, request, redirect, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

USERTYPES = ["Учащийся", "Учитель", "Администратор"]

@app.route("/")
def index():
    return render_template('index.html', name=session.get("name"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not request.form.get("loginName"):
            return render_template('error.html', message="Вы не ввели логин")
        session["name"] = request.form.get("loginName")
        return redirect("/")
    return render_template('login.html')

@app.route("/auth", methods=["POST"])
def course():
    name = session.get("name")
    return render_template('course.html', name=name)
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form.get("registerUsertype") not in USERTYPES:
            return render_template("error.html", message="Некорректная роль пользователя")
        return redirect("/users")
    return render_template("register.html", usertypes=USERTYPES)

@app.route("/users")
def users():
    users = getUserList()
    return render_template("users.html", users=users )

@app.route("/test")
def test():
    return render_template("test.html")