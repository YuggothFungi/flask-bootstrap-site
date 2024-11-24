import sqlite3

# Создание или изменение пользователя.
# Если такой логин есть в базе, изменяем для него переданные пароль и роль пользователя,
# Если логина нет - создаем нового пользователя.
def registerUser(login, password, userTypeID):
    connection = sqlite3.connect('course.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM user WHERE login = ?", [login])
    user = cursor.fetchone()
    
    if user:
        # Обновляем данные указанного пользователя
        cursor.execute('UPDATE user SET userTypeID = ?, password = ? WHERE login = ?', (userTypeID, password, login))
        
    else:
        # Добавляем нового пользователя
        cursor.execute('INSERT INTO user (login, password, userTypeID) VALUES (?, ?, ?)', (login, password, userTypeID))

    cursor.execute("SELECT userTypeID FROM user WHERE login = ?", [login])
    usertype = cursor.fetchone()
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()
    return usertype[0]

#Авторизация пользователя
def authUser(login, password):
    connection = sqlite3.connect('course.db')
    cursor = connection.cursor()

    cursor.execute("SELECT userTypeID FROM user WHERE login=? AND password=?", (login, password))
    result = cursor.fetchone()
    connection.commit()
    connection.close()

    if result:
        return result[0]
    else:
        return None

def getUserList():
    connection = sqlite3.connect('course.db')
    cursor = connection.cursor()



    cursor.execute("SELECT login, typeName FROM user, usertype where user.userTypeID = usertype.id and user.userTypeID <> 3")
    userlist = cursor.fetchall()
    return userlist

def getStudentResults(teacherId):
    """
    Получает список учеников и их результаты тестов для конкретного учителя
    Args:
        teacherId: ID учителя
    Returns:
        list: Список учеников в формате [{'id': id, 'name': name, 'tests': [{'course_id': id, 'score': score}, ...]}]
    """
    # Заглушка с тестовыми данными
    return [
        {
            'id': 1,
            'name': 'Иванов Иван',
            'tests': [
                {'course_id': 1, 'score': 5},
                {'course_id': 2, 'score': 4}
            ]
        },
        {
            'id': 2,
            'name': 'Петров Петр',
            'tests': [
                {'course_id': 1, 'score': 3}
            ]
        },
        {
            'id': 3,
            'name': 'Сидоров Сидор',
            'tests': []
        }
    ]

def postTestResults(answers):
    """
    Заглушка для сохранения результатов теста
    Args:
        answers: словарь с ответами ученика в формате {номер_вопроса: номер_ответа}
    Returns:
        None
    """
    # TODO: Реализовать сохранение результатов в базу данных
    print(f"Результаты теста: {answers}")
    return None

