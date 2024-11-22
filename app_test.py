import pytest
from app import app
from flask import session

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

def test_login_post_empty_credentials(client):
    """Тест логина с пустыми данными"""
    response = client.post('/login', data={
        'loginName': '',
        'loginPassword': '',
        'loginAction': '1'
    })
    # Проверяем сообщение "Необходимо ввести логин и пароль"
    assert b'\xd0\x9d\xd0\xb5\xd0\xbe\xd0\xb1\xd1\x85\xd0\xbe\xd0\xb4\xd0\xb8\xd0\xbc\xd0\xbe \xd0\xb2\xd0\xb2\xd0\xb5\xd1\x81\xd1\x82\xd0\xb8 \xd0\xbb\xd0\xbe\xd0\xb3\xd0\xb8\xd0\xbd \xd0\xb8 \xd0\xbf\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbb\xd1\x8c' in response.data

def test_login_post_empty_password(client):
    """Тест логина с пустым паролем"""
    response = client.post('/login', data={
        'loginName': 'test_user',
        'loginPassword': '',
        'loginAction': '1'
    })
    assert b'\xd0\x9d\xd0\xb5\xd0\xbe\xd0\xb1\xd1\x85\xd0\xbe\xd0\xb4\xd0\xb8\xd0\xbc\xd0\xbe \xd0\xb2\xd0\xb2\xd0\xb5\xd1\x81\xd1\x82\xd0\xb8 \xd0\xbb\xd0\xbe\xd0\xb3\xd0\xb8\xd0\xbd \xd0\xb8 \xd0\xbf\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbb\xd1\x8c' in response.data  # "Необходимо ввести логин и пароль" в UTF-8

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
        # Проверяем сообщение "Эта страница доступна только для учителей"
        assert b'\xd0\xad\xd1\x82\xd0\xb0 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb0 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xbd\xd0\xb0 \xd1\x82\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xba\xd0\xbe \xd0\xb4\xd0\xbb\xd1\x8f \xd1\x83\xd1\x87\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xb9' in response.data
    else:
        # Проверяем сообщение "Необходима авторизация"
        assert b'\xd0\x9d\xd0\xb5\xd0\xbe\xd0\xb1\xd1\x85\xd0\xbe\xd0\xb4\xd0\xb8\xd0\xbc\xd0\xb0 \xd0\xb0\xd0\xb2\xd1\x82\xd0\xbe\xd1\x80\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f' in response.data

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
    # Проверяем сообщение "Пароли не совпадают"
    assert b'\xd0\x9f\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbb\xd0\xb8 \xd0\xbd\xd0\xb5 \xd1\x81\xd0\xbe\xd0\xb2\xd0\xbf\xd0\xb0\xd0\xb4\xd0\xb0\xd1\x8e\xd1\x82' in response.data

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
    assert b'Python' in response.data  # Проверяем наличие контента курса
    
    # Тест POST запроса
    with pytest.raises(NotImplementedError):
        client.post('/course1', data={'test': 'data'})

def test_class_page_with_teacher(client):
    """Тест страницы класса с авторизацией учителя"""
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['name'] = 'test_teacher'
        sess['role'] = 'Учитель'
    
    response = client.get('/class')
    assert response.status_code == 200
    # Проверяем сообщение "Управление классом"
    assert b'\xd0\xa3\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xba\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81\xd0\xbe\xd0\xbc' in response.data

def test_class_page_with_student(client):
    """Тест страницы класса с авторизацией ученика"""
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['name'] = 'test_student'
        sess['role'] = 'Учащийся'
    
    response = client.get('/class')
    # Проверяем сообщение "Эта страница доступна только для учителей"
    assert b'\xd0\xad\xd1\x82\xd0\xb0 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb0 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xbd\xd0\xb0 \xd1\x82\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xba\xd0\xbe \xd0\xb4\xd0\xbb\xd1\x8f \xd1\x83\xd1\x87\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xb9' in response.data

if __name__ == '__main__':
    pytest.main(['-v']) 