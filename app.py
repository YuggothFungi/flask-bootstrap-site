import base64
from functools import wraps
from db_py import registerUser, getUserList, authUser
from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Константы
USERTYPES = {
    1: "Учащийся",
    2: "Учитель", 
    3: "Администратор"
}

ADMIN_ROLE = 3
LOGIN_REQUIRED_MESSAGE = "Необходима авторизация для доступа к этой странице."

# Декоратор для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return render_template("error.html", message=LOGIN_REQUIRED_MESSAGE)
        return f(*args, **kwargs)
    return decorated_function

def handle_course(course_number):
    """Общая функция для обработки всех курсов"""
    if request.method == "POST":
        # Тут должно быть описание действий на странице, после прохождения теста
        raise NotImplementedError
    return render_template(f"course{course_number}.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_name = request.form.get("loginName")
        login_pass = request.form.get("loginPassword")
        login_action = request.form.get("loginAction")
        
        if login_action == '0':
            session.clear()
            return redirect(url_for('index'))
            
        if login_action == '1':
            if not login_name or not login_pass:
                return render_template("error.html", 
                    message="Необходимо ввести логин и пароль.")

            login_pass_safe = base64.b64encode(login_pass.encode('utf-8'))
            auth_result = authUser(login_name, login_pass_safe)
            
            if auth_result not in USERTYPES:
                return render_template("error.html", 
                    message="Невозможно авторизоваться. Проверьте логин/пароль.")
            
            session["logged_in"] = True
            session["name"] = login_name
            session["role"] = USERTYPES[auth_result]
            session.modified = True

            return redirect(url_for('register' if auth_result == ADMIN_ROLE else 'course1'))
    
    return render_template("login.html")

# Маршруты для курсов с использованием общей функции
@app.route("/course1", methods=["GET", "POST"])
@login_required
def course1():
    return handle_course(1)

@app.route("/course2", methods=["GET", "POST"])
@login_required
def course2():
    return handle_course(2)

@app.route("/course3", methods=["GET", "POST"])
@login_required
def course3():
    return handle_course(3)

@app.route("/course4", methods=["GET", "POST"])
@login_required
def course4():
    return handle_course(4)

@app.route("/course5", methods=["GET", "POST"])
@login_required
def course5():
    return handle_course(5)

@app.route("/course6", methods=["GET", "POST"])
@login_required
def course6():
    return handle_course(6)

@app.route("/course7", methods=["GET", "POST"])
@login_required
def course7():
    return handle_course(7)

# ... аналогично для остальных курсов

@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":
        reg_name = request.form.get("registerUsername")
        reg_role = request.form.get("registerUsertype")
        reg_pass = request.form.get("registerPassword")
        reg_pass_confirm = request.form.get("registerRepeatPassword")

        # Валидация данных
        if not all([reg_name, reg_role, reg_pass, reg_pass_confirm]):
            return render_template("error.html", 
                message="Все поля должны быть заполнены.")

        if reg_pass != reg_pass_confirm:
            return render_template("error.html", 
                message="Пароли не совпадают.")

        try:
            reg_role = int(reg_role)
            if reg_role not in USERTYPES:
                raise ValueError
        except ValueError:
            return render_template("error.html", 
                message="Некорректная роль пользователя.")

        reg_pass_safe = base64.b64encode(reg_pass.encode('utf-8'))
        
        if not registerUser(reg_name, reg_pass_safe, reg_role):
            return render_template("error.html", 
                message="Не удалось зарегистировать данные пользователя.")

        return redirect(url_for('users'))    
    
    return render_template("register.html", usertypes=USERTYPES)

@app.route("/users")
@login_required
def users():
    users = getUserList()
    return render_template("users.html", users=users)
