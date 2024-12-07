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
    try:
        connection = sqlite3.connect('course.db')
        cursor = connection.cursor()

        # Получаем id теста из первого вопроса (все вопросы относятся к одному тесту)
        first_question = min(answers.keys())
        cursor.execute("SELECT idTest FROM questionBase WHERE id = ?", (first_question,))
        test_id = cursor.fetchone()[0]

        # Формируем ключ ответов (конкатенация всех ответов в порядке возрастания номеров вопросов)
        sorted_answers = [str(answers[q]) for q in sorted(answers.keys())]
        answer_key = int(''.join(sorted_answers))

        # Сохраняем результат теста
        cursor.execute("""
            INSERT INTO testsResults (idUser, idTest, answerKey, date)
            VALUES (?, ?, ?, ?)
        """, (student_id, test_id, answer_key, timestamp))

        connection.commit()

    except sqlite3.Error as e:
        print(f"Произошла ошибка при сохранении результатов теста: {e}")
        
    finally:
        if connection:
            connection.close()

    return None

def setTeacher(student_teacher_pairs):
    """
    Присваивает учеников учителю
    Args:
        student_teacher_pairs: словарь с парами ученик-учитель в формате {student_id: teacher_id}
    Returns:
        int: 1 в случае успеха, 0 в случае ошибки
    """
    try:
        connection = sqlite3.connect('course.db')
        cursor = connection.cursor()

        # Начинаем транзакцию
        cursor.execute("BEGIN TRANSACTION")

        # Удаляем старые назначения для этих студентов
        student_ids = list(student_teacher_pairs.keys())
        cursor.execute("DELETE FROM teacherToStudent WHERE idStudent IN ({})".format(
            ','.join('?' * len(student_ids))), student_ids)

        # Добавляем новые назначения
        for student_id, teacher_id in student_teacher_pairs.items():
            cursor.execute("""
                INSERT INTO teacherToStudent (idTeacher, idStudent)
                VALUES (?, ?)
            """, (teacher_id, student_id))

        # Подтверждаем транзакцию
        connection.commit()
        return 1

    except sqlite3.Error as e:
        print(f"Произошла ошибка при назначении учеников: {e}")
        # Откатываем изменения в случае ошибки
        if connection:
            connection.rollback()
        return 0
        
    finally:
        if connection:
            connection.close()



