# Сообщения об ошибках
ERROR_AUTH_REQUIRED = b'\xd0\x9d\xd0\xb5\xd0\xbe\xd0\xb1\xd1\x85\xd0\xbe\xd0\xb4\xd0\xb8\xd0\xbc\xd0\xb0 \xd0\xb0\xd0\xb2\xd1\x82\xd0\xbe\xd1\x80\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f'  # "Необходима авторизация"
ERROR_TEACHER_ONLY = b'\xd0\xad\xd1\x82\xd0\xb0 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb0 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xbd\xd0\xb0 \xd1\x82\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xba\xd0\xbe \xd0\xb4\xd0\xbb\xd1\x8f \xd1\x83\xd1\x87\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xb9'  # "Эта страница доступна только для учителей"
ERROR_LOGIN_REQUIRED = b'\xd0\x9d\xd0\xb5\xd0\xbe\xd0\xb1\xd1\x85\xd0\xbe\xd0\xb4\xd0\xb8\xd0\xbc\xd0\xbe \xd0\xb2\xd0\xb2\xd0\xb5\xd1\x81\xd1\x82\xd0\xb8 \xd0\xbb\xd0\xbe\xd0\xb3\xd0\xb8\xd0\xbd \xd0\xb8 \xd0\xbf\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbb\xd1\x8c'  # "Необходимо ввести логин и пароль"
ERROR_PASSWORDS_MISMATCH = b'\xd0\x9f\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbb\xd0\xb8 \xd0\xbd\xd0\xb5 \xd1\x81\xd0\xbe\xd0\xb2\xd0\xbf\xd0\xb0\xd0\xb4\xd0\xb0\xd1\x8e\xd1\x82'  # "Пароли не совпадают"

# Заголовки таблицы класса
CLASS_HEADER_STUDENT_NAME = b'\xd0\x98\xd0\xbc\xd1\x8f \xd1\x83\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0'  # "Имя ученика"
CLASS_HEADER_TESTS = b'\xd0\x9f\xd1\x80\xd0\xbe\xd0\xb9\xd0\xb4\xd0\xb5\xd0\xbd\xd0\xbd\xd1\x8b\xd0\xb5 \xd1\x82\xd0\xb5\xd1\x81\xd1\x82\xd1\x8b'  # "Пройденные тесты"

# Тестовые данные студентов
STUDENT_NAME_IVANOV = b'\xd0\x98\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xbe\xd0\xb2 \xd0\x98\xd0\xb2\xd0\xb0\xd0\xbd'  # "Иванов Иван"
STUDENT_NAME_PETROV = b'\xd0\x9f\xd0\xb5\xd1\x82\xd1\x80\xd0\xbe\xd0\xb2 \xd0\x9f\xd0\xb5\xd1\x82\xd1\x80'  # "Петров Петр"

# Сообщения на странице класса
CLASS_NO_STUDENTS = b'\xd0\xa3 \xd0\xb2\xd0\xb0\xd1\x81 \xd0\xbf\xd0\xbe\xd0\xba\xd0\xb0 \xd0\xbd\xd0\xb5\xd1\x82 \xd1\x83\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xba\xd0\xbe\xd0\xb2 \xd0\xb2 \xd0\xba\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81\xd0\xb5'  # "У вас пока нет учеников в классе"
CLASS_TITLE = b'\xd0\xa3\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xba\xd0\xbb\xd0\xb0\xd1\x81\xd1\x81\xd0\xbe\xd0\xbc'  # "Управление классом"

# Кнопки
BUTTON_DETAILS = b'\xd0\x9f\xd0\xbe\xd0\xb4\xd1\x80\xd0\xbe\xd0\xb1\xd0\xbd\xd0\xb5\xd0\xb5'  # "Подробнее"

# Словарь для замены UTF-8 на русский текст
UTF8_TO_RUSSIAN = {
    ERROR_AUTH_REQUIRED: "Необходима авторизация",
    ERROR_TEACHER_ONLY: "Эта страница доступна только для учителей",
    ERROR_LOGIN_REQUIRED: "Необходимо ввести логин и пароль",
    ERROR_PASSWORDS_MISMATCH: "Пароли не совпадают",
    CLASS_HEADER_STUDENT_NAME: "Имя ученика",
    CLASS_HEADER_TESTS: "Пройденные тесты",
    STUDENT_NAME_IVANOV: "Иванов Иван",
    STUDENT_NAME_PETROV: "Петров Петр",
    CLASS_NO_STUDENTS: "У вас пока нет учеников в классе",
    CLASS_TITLE: "Управление классом",
    BUTTON_DETAILS: "Подробнее"
}

from functools import wraps

def readable_error(func):
    """Декоратор для замены UTF-8 строк на читаемый текст в сообщениях об ошибках"""
    @wraps(func)  # Сохраняем метаданные оригинальной функции
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError as e:
            error_msg = str(e)
            for utf8, russian in UTF8_TO_RUSSIAN.items():
                error_msg = error_msg.replace(str(utf8), f'"{russian}"')
            raise AssertionError(error_msg)
    return wrapper
 