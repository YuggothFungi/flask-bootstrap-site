from db import getUserList
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

USERTYPES = ["Учащийся", "Учитель", "Администратор"]

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/course", methods=["POST"])
def course():
    if not request.form.get("login"):
        return render_template('error.html', message="Вы не ввели логин")
    else:
        name = request.form.get("login")
        return render_template('course.html',name=name)
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form.get("usertype") not in USERTYPES:
            return render_template("error.html", message="Некорректная роль пользователя")
        return redirect("/users")
    return render_template("register.html")

@app.route("/users")
def users():
    users = getUserList()
    return render_template("users.html", users=users )