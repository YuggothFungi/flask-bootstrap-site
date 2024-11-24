import base64
from functools import wraps
from db_py import (
    register_user, get_user_list, auth_user, 
    get_student_results, post_test_results
)
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_session import Session
from utils import generate_test_html, load_course_test
import json

app = Flask(__name__)

# Конфигурация сессий
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SECRET_KEY"] = "your_secret_key_here"
Session(app)

# Константы
USERTYPES = {
    1: "Учащийся",
    2: "Учитель", 
    3: "Администратор"
}

TEACHER_ROLE = 2
ADMIN_ROLE = 3
LOGIN_REQUIRED_MESSAGE = "Необходима авторизация для доступа к этой странице."

# Декораторы для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return render_template("base/error.html", message=LOGIN_REQUIRED_MESSAGE)
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in") or session.get("role") != "Учитель":
            return render_template("base/error.html", 
                message="Эта страница доступна только для учителей.")
        return f(*args, **kwargs)
    return decorated_function

# Общая функция для обработки маршрутов курсов
def handle_course(course_number):
    if request.method == "POST":
        # Обработка ответов на тест
        answers = request.get_json()
        test_data = load_course_test(course_number)
        results = {}
        
        for question in test_data['questions']:
            q_id = str(question['id'])
            if q_id in answers:
                results[q_id] = int(answers[q_id]) == question['correct']
        
        return jsonify({'results': results})
    
    # Генерация страницы курса
    test_html = generate_test_html(course_number)
    return render_template(
        f"courses/course{course_number}.html",
        test_html=test_html,
        course_number=course_number
    )

# Маршрут для главной страницы
@app.route("/")
def index():
    return render_template("base/index.html")

# Маршрут для авторизации
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
                return render_template("base/error.html", 
                    message="Необходимо ввести логин и пароль.")

            login_pass_safe = base64.b64encode(login_pass.encode('utf-8'))
            auth_result = auth_user(login_name, login_pass_safe)
            
            if auth_result not in USERTYPES:
                return render_template("base/error.html", 
                    message="Невозможно авторизоваться. Проверьте логин/пароль.")
            
            session["logged_in"] = True
            session["name"] = login_name
            session["role"] = USERTYPES[auth_result]
            session.modified = True

            # Перенаправление в зависимости от роли
            if auth_result == ADMIN_ROLE:  # Администратор
                return redirect(url_for('register'))
            elif auth_result == TEACHER_ROLE:  # Учитель
                return redirect(url_for('teacher_class'))
            else:  # Учащийся
                return redirect(url_for('course1'))
    
    return render_template("auth/login.html")

# Маршруты для курсов
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

# Маршрут для регистрации пользователя
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
            return render_template("base/error.html", 
                message="Все поля должны быть заполнены.")

        if reg_pass != reg_pass_confirm:
            return render_template("base/error.html", 
                message="Пароли не совпадают.")

        try:
            reg_role = int(reg_role)
            if reg_role not in USERTYPES:
                raise ValueError
        except ValueError:
            return render_template("base/error.html", 
                message="Некорректная роль пользователя.")

        reg_pass_safe = base64.b64encode(reg_pass.encode('utf-8'))
        
        if not register_user(reg_name, reg_pass_safe, reg_role):
            return render_template("base/error.html", 
                message="Не удалось зарегистировать данные пользователя.")

        return redirect(url_for('users'))    
    
    return render_template("admin/register.html", usertypes=USERTYPES)

# Маршрут для страницы списка пользователей
@app.route("/users")
@login_required
def users():
    users = get_user_list()
    return render_template("admin/users.html", users=users)

@app.route("/class")
@teacher_required
def teacher_class():
    teacher_id = session.get("user_id")
    students = get_student_results(teacher_id)
    return render_template("teacher/class.html", students=students)

@app.route("/submit_test", methods=['POST'])
@login_required
def submit_test():
    data = request.get_json()
    course_id = data.get('course_id')
    answers = data.get('answers')
    timestamp = data.get('timestamp')
    student_id = data.get('student_id')  # Получаем ID студента из запроса
    
    # Проверяем, что все необходимые данные получены
    if not all([course_id, answers, timestamp, student_id]):
        return jsonify({'status': 'error', 'message': 'Не все данные предоставлены'}), 400
    
    # Сохраняем результаты в БД через заглушку
    post_test_results(answers, timestamp, student_id)
    
    return jsonify({'status': 'success'})
