from db import getUserList, checkUserRole
from flask import Flask, render_template, request, redirect, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

USERTYPES = { 1: "Учащийся"
            , 2 : "Учитель"
            , 0 : "Администратор"
            }

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("loginAction")=='1':
            if not request.form.get("loginName"):
                return render_template('error.html', message="Вы не ввели логин")
            session['logged_in']=True
            session_name = session['name'] = request.form.get("loginName")
            session_role = checkUserRole(session_name)
            if session_role == 1:
                return redirect("/course1")
            else:
                session['role'] = USERTYPES[session_role]
                session.modified = True
                return redirect("/register")
        
        session.clear()
        return redirect("/")
    return render_template('login.html')

@app.route("/course1")
def course1():
    return render_template('course1.html')

@app.route("/course2")
def course2():
    return render_template('course2.html')

@app.route("/course3")
def course3():
    return render_template('course3.html')

@app.route("/course4")
def course4():
    return render_template('course4.html')

@app.route("/course5")
def course5():
    return render_template('course5.html')
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form.get("registerPassword") != request.form.get("registerRepeatPassword"):
            return render_template("error.html", message="Пароли не совпадают")
        reg_role = int(request.form.get("registerUsertype"))
        if reg_role not in USERTYPES:
            return render_template("error.html", message="Некорректная роль пользователя")  
              
        return redirect("/users")    
    
    return render_template("register.html", usertypes=USERTYPES)

@app.route("/users")
def users():
    users = getUserList()
    return render_template("users.html", users=users)

@app.route("/test")
def test():
    return render_template("test.html")