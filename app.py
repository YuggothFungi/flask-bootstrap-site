import base64
from db import getUserList, authUser
from flask import Flask, render_template, request, redirect, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Повторяет описание таблицы из БД, в которой хранятся типы ролей пользователей на сайте
USERTYPES = { 1: "Учащийся"
            , 2 : "Учитель"
            , 0 : "Администратор"
            }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_name = request.form.get("loginName")
        login_pass = request.form.get("loginPassword")
        
        if request.form.get("loginAction")=='1':
            if not login_name:
                return render_template("error.html", message="Вы не ввели логин")

            if not login_pass:
                return render_template("error.html", message="Вы не ввели пароль")
            else:
                login_pass_safe = base64.b64encode(login_pass.encode('utf-8'))

            auth_result = authUser(login_name, login_pass_safe)
            if auth_result not in USERTYPES:
                return render_template("error.html", message="Невозможно авторизоваться. Проверьте логин/пароль.")
            
            # Обработали все исключительные ситуации, теперь можно обновлять данные сессии
            session["logged_in"] = True
            session["name"] = login_name
            session["role"] = USERTYPES[auth_result]
            session.modified = True

            if auth_result > 0:
                return redirect("/course1")
            else:
                return redirect("/register")
        
        # Если в качестве loginAction пришёл 0 (завершить работу), очищаем сессию и возвращаемся на главную
        session.clear()
        return redirect("/")
    # Если страница вызывается методом GET, то просто открывается форма логина
    return render_template("login.html")

@app.route("/course1")
def course1():
    return render_template("course1.html")

@app.route("/course2")
def course2():
    return render_template("course2.html")

@app.route("/course3")
def course3():
    return render_template("course3.html")

@app.route("/course4")
def course4():
    return render_template("course4.html")

@app.route("/course5")
def course5():
    return render_template("course5.html")
    
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