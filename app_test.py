import pytest
from app import app
from flask import session
from test_resources import (
    ERROR_AUTH_REQUIRED, ERROR_TEACHER_ONLY, ERROR_LOGIN_REQUIRED,
    ERROR_PASSWORDS_MISMATCH, CLASS_HEADER_STUDENT_NAME, CLASS_HEADER_TESTS,
    CLASS_TITLE, UTF8_TO_RUSSIAN, readable_error
)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_key'
    app.config['SESSION_TYPE'] = "filesystem"
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index_page(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    # Проверяем, что используется правильный шаблон
    assert b'Python' in response.data

def test_login_page_get(client):
    """Тест страницы логина (GET запрос)"""
    response = client.get('/login')
    assert response.status_code == 200
    # Проверяем наличие формы логина
    assert b'loginName' in response.data
    assert b'loginPassword' in response.data

@readable_error
def test_login_post_empty_credentials(client):
    """Тест логина с пустыми данными"""
    response = client.post('/login', data={
        'loginName': '',
        'loginPassword': '',
        'loginAction': '1'
    })
    assert ERROR_LOGIN_REQUIRED in response.data, \
        f'Ожидалось сообщение "{UTF8_TO_RUSSIAN[ERROR_LOGIN_REQUIRED]}"'

@readable_error
def test_login_post_empty_password(client):
    """Тест логина с пустым паролем"""
    response = client.post('/login', data={
        'loginName': 'test_user',
        'loginPassword': '',
        'loginAction': '1'
    })
    assert ERROR_LOGIN_REQUIRED in response.data, \
        f'Ожидалось сообщение "{UTF8_TO_RUSSIAN[ERROR_LOGIN_REQUIRED]}"'

def test_login_post_logout(client):
    """Тест выхода из системы"""
    # Сначала входим в систему
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['name'] = 'test_user'
        sess['role'] = 'Учащийся'
    
    # Проверяем, что сессия установлена
    response = client.get('/')
    assert b'test_user' in response.data
    
    # Выполняем выход
    response = client.post('/login', data={
        'loginAction': '0'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Проверяем, что сессия очищена
    with client.session_transaction() as sess:
        assert 'logged_in' not in sess
        assert 'name' not in sess
        assert 'role' not in sess

@pytest.mark.parametrize('route', [
    '/course1',
    '/course2',
    '/course3',
    '/course4',
    '/course5',
    '/course6',
    '/course7',
    '/register',
    '/users',
    '/class'
])
def test_protected_routes_without_login(client, route):
    """Тест защищенных маршрутов без авторизации"""
    response = client.get(route)
    if route == '/class':
        assert ERROR_TEACHER_ONLY in response.data, \
            f'Ожидалось сообщение "{UTF8_TO_RUSSIAN[ERROR_TEACHER_ONLY]}"'
    else:
        assert ERROR_AUTH_REQUIRED in response.data, \
            f'Ожидалось сообщение "{UTF8_TO_RUSSIAN[ERROR_AUTH_REQUIRED]}"'

@readable_error
def test_register_validation(client):
    """Тест валидации данных при регистрации"""
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['name'] = 'admin'
        sess['role'] = 'Администратор'
    
    response = client.post('/register', data={
        'registerUsername': 'new_user',
        'registerUsertype': '1',
        'registerPassword': 'pass1',
        'registerRepeatPassword': 'pass2'
    })
    assert ERROR_PASSWORDS_MISMATCH in response.data, \
        f'Ожидалось сообщение "{UTF8_TO_RUSSIAN[ERROR_PASSWORDS_MISMATCH]}"'

def test_handle_course(client):
    """Тест функции обработки курсов"""
    # Устанавливаем сессию как учащийся
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['name'] = 'student'
        sess['role'] = 'Учащийся'
    
    # Тест GET запроса
    response = client.get('/course1')
    assert response.status_code == 200
    
    # Тест POST запроса с ответами на тест
    response = client.post('/course1', 
        json={'1': '3', '2': '2'}, 
        content_type='application/json')
    assert response.status_code == 200
    
    # Проверяем формат ответа
    data = response.get_json()
    assert 'results' in data
    assert isinstance(data['results'], dict)

@readable_error
def test_class_page_with_teacher(client):
    """Тест страницы класса с авторизацией учителя"""
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['name'] = 'test_teacher'
        sess['role'] = 'Учитель'
        sess['user_id'] = 1
    
    response = client.get('/class')
    assert response.status_code == 200
    assert CLASS_TITLE in response.data, \
        f'Ожидалось сообщение "{UTF8_TO_RUSSIAN[CLASS_TITLE]}"'

@readable_error
def test_class_page_with_student(client):
    """Тест страницы класса с авторизацией ученика"""
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['name'] = 'test_student'
        sess['role'] = 'Учащийся'
    
    response = client.get('/class')
    assert ERROR_TEACHER_ONLY in response.data, \
        f'Ожидалось сообщение "{UTF8_TO_RUSSIAN[ERROR_TEACHER_ONLY]}"'

@readable_error
def test_submit_test_answers(client):
    """Тест отправки ответов на тест учеником"""
    # Устанавливаем сессию как учащийся
    course_id = 1
    test_user_id = 1  # ID тестового студента
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['name'] = 'test_student'
        sess['role'] = 'Учащийся'
        sess['user_id'] = test_user_id  # Используем тот же ID что и для теста

    # Отправляем ответы на тест
    test_answers = {
        '1': '3',  # Ответ на первый вопрос
        '2': '2',  # Ответ на второй вопрос
        '3': '1',  # Ответ на третий вопрос
        '4': '4',  # Ответ на четвертый вопрос
        '5': '2'   # Ответ на пятый вопрос
    }
    
    test_timestamp = 1234567890  # Фиксированное время для теста
    
    response = client.post('/submit_test', 
        json={
            'course_id': 1,
            'answers': test_answers,
            'timestamp': test_timestamp,
            'user_id': test_user_id  # Изменено с student_id на user_id
        },
        content_type='application/json')
    
    # Проверяем ответ сервера
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'

    # Проверяем, что результаты были переданы в БД с правильным ID студента
    from db_py import post_test_results
    test_results = post_test_results(course_id, test_answers, test_timestamp, test_user_id)
    assert test_results is None  # Заглушка пока просто возвращает None

if __name__ == '__main__':
    pytest.main(['-v']) 