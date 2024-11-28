import sqlite3

# Создание или изменение пользователя.
# Если такой логин есть в базе, изменяем для него переданные пароль и роль пользователя,
# Если логина нет - создаем нового пользователя.
def register_user(login, password, user_type_id):
    connection = sqlite3.connect('course.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM user WHERE login = ?", [login])
    user = cursor.fetchone()
    
    if user:
        # Обновляем данные указанного пользователя
        cursor.execute('UPDATE user SET userTypeID = ?, password = ? WHERE login = ?', (user_type_id, password, login))
        
    else:
        # Добавляем нового пользователя
        cursor.execute('INSERT INTO user (login, password, userTypeID) VALUES (?, ?, ?)', (login, password, user_type_id))

    cursor.execute("SELECT userTypeID FROM user WHERE login = ?", [login])
    usertype = cursor.fetchone()
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()
    return usertype[0]

#Авторизация пользователя
def auth_user(login, password):
    try:
        connection = sqlite3.connect('course.db')
        cursor = connection.cursor()

        cursor.execute("SELECT userTypeID, id FROM user WHERE login=? AND password=?", (login, password))
        result = cursor.fetchone()
        
        return result if result else None
        
    except sqlite3.Error as e:
        print(f"Произошла ошибка при работе с базой данных: {e}")
        return None
        
    finally:
        if connection:
            connection.close()

def get_user_list():
    connection = sqlite3.connect('course.db')
    cursor = connection.cursor()



    cursor.execute("SELECT login, typeName FROM user, usertype where user.userTypeID = usertype.id and user.userTypeID <> 3")
    userlist = cursor.fetchall()
    return userlist

def get_student_results(teacher_id):
    """
    Получает список учеников и их результаты тестов для конкретного учителя
    Args:
        teacherId: ID учителя
    Returns:
        list: Список учеников в формате [{'id': id, 'name': name, 'tests': [{'course_id': id, 'score': score, 
        'date': timestamp, 'answer_key': answer}]}]
    """
    try:
        connection = sqlite3.connect('course.db')
        cursor = connection.cursor()
        
        # Получаем список студентов (userTypeID = 3 для студентов)
        cursor.execute("""
            SELECT DISTINCT u.id, u.login
            FROM user u
            JOIN testsResults tr ON u.id = tr.idUser
            WHERE u.userTypeID = 3
        """)
        students = cursor.fetchall()
        
        results = []
        for student in students:
            student_id, student_name = student
            
            # Получаем результаты тестов для каждого студента
            cursor.execute("""
                SELECT tr.idTest, tr.answerKey, tr.date, t.testKey
                FROM testsResults tr
                JOIN tests t ON tr.idTest = t.id
                WHERE tr.idUser = ?
                ORDER BY tr.date DESC
            """, (student_id,))
            
            test_results = cursor.fetchall()
            
            # Формируем список тестов студента
            tests = []
            for test in test_results:
                test_id, answer_key, date, test_key = test
                
                # Вычисляем оценку, сравнивая ключ ответов с правильным ключом
                score = 5 if answer_key == test_key else (
                    4 if abs(answer_key - test_key) == 1 else (
                    3 if abs(answer_key - test_key) == 2 else 2))
                
                tests.append({
                    'course_id': test_id,
                    'score': score,
                    'date': date,
                    'answer_key': answer_key
                })
            
            # Добавляем информацию о студенте в общий список
            if tests:  # Добавляем только студентов, у которых есть результаты тестов
                results.append({
                    'id': student_id,
                    'name': student_name,
                    'tests': tests
                })
        
        return results
        
    except sqlite3.Error as e:
        print(f"Произошла ошибка при работе с базой данных: {e}")
        return []
        
    finally:
        if connection:
            connection.close()

def post_test_results(answers, timestamp, student_id):
    """
    Заглушка для сохранения результатов теста
    Args:
        answers: словарь с ответами ученика в формате {номер_вопроса: номер_ответа}
        timestamp: время сдачи теста в тиках (миллисекунды с начала эпохи)
        student_id: идентификатор студента
    Returns:
        None
    """
    # TODO: Реализовать сохранение результатов в базу данных
    print(f"Результаты теста: {answers}")
    print(f"Время сдачи (тики): {timestamp}")
    print(f"ID студента: {student_id}")
    return None

