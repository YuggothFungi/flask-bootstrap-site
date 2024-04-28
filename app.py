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
        if request.form.get("loginAction")=='1':
            if not request.form.get("loginName"):
                return render_template('error.html', message="Вы не ввели логин")
            session['logged_in']=True
            session['name'] = request.form.get("loginName")
            return redirect("/course1")
        
        session['logged_in'] = False
        session['name'] = None
        return redirect("/")
    return render_template('login.html', name=session.get("name"))

@app.route("/course1")
def course1():
    name = session.get("name")
    return render_template('course1.html', name=name)

@app.route("/course2")
def course2():
    name = session.get("name")
    return render_template('course2.html', name=name)

@app.route("/course3")
def course3():
    name = session.get("name")
    return render_template('course3.html', name=name)

@app.route("/course4")
def course4():
    name = session.get("name")
    return render_template('course4.html', name=name)

@app.route("/course5")
def course5():
    name = session.get("name")
    return render_template('course5.html', name=name)
    
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