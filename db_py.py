import sqlite3
import json

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
    # Сохраняем изенения и закрываем соединение
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

def get_teacher_list():
    connection = sqlite3.connect('course.db')
    cursor = connection.cursor()

    cursor.execute("SELECT user.id, user.login FROM user, usertype where user.userTypeID = usertype.id and user.userTypeID = 2")
    teacherlist = cursor.fetchall()
    return teacherlist

def get_student_results(teacher_id):
    """
    Получает результаты тестов для учеников, назначенных учителю.
    Args:
        teacher_id (int): ID учителя.
    Returns:
        list: Список учеников с их результатами.
    """
    try:
        connection = sqlite3.connect('course.db')
        cursor = connection.cursor()

        # Получаем список учеников, назначенных этому учителю
        cursor.execute("""
            SELECT student.id, student.login
            FROM user AS student
            JOIN teacherToStudent AS ts ON student.id = ts.idStudent
            WHERE ts.idTeacher = ?
        """, (teacher_id,))
        students = cursor.fetchall()

        results = []
        for student in students:
            student_id = student[0]
            student_name = student[1]

            # Получаем результаты тестов для ученика
            cursor.execute("""
                SELECT tr.idTest, tr.answerKey, tr.date, t.testKey
                FROM testsResults tr
                JOIN tests t ON tr.idTest = t.id
                WHERE tr.idUser = ?
                ORDER BY tr.date DESC
            """, (student_id,))
            
            test_results = cursor.fetchall()
            correct_count = 0

            # Формируем список тестов студента
            tests = []
            for test in test_results:
                test_id, answer_key, date, test_key = test
                
                answer_key = str(test[1])
                answer_list = list(answer_key)
                test_key = str(test[3])
                correct_list = list(test_key)

                for a, b in zip(answer_list, correct_list):
                    if a == b:
                        correct_count += 1
                
                tests.append({
                    'course_id': test_id,
                    'correct_count': correct_count,
                    'date': date,
                    'answer_key': answer_key
                })
                correct_count=0
            
            # Добавляем информацию о студенте в общий список
            if tests:  # Добавляем только студентов, у которых есть результаты тестов
                results.append({
                    'id': student_id,
                    'name': student_name,
                    'tests': tests
                })
        
        return results

    except sqlite3.Error as e:
        print(f"Произошла ошибка при получении результатов тестов: {e}")
        return []

    finally:
        if connection:
            connection.close()

def post_test_results(course_id, answers, timestamp, student_id):
    try:
        connection = sqlite3.connect('course.db')
        cursor = connection.cursor()

        # Получаем id теста из первого вопроса (все вопросы относятся к одному тесту)
       
        test_id = course_id

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

def assign_students(student_teacher_pairs):
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

def getStudentName(student_id):
    """
    Получает имя и фамилию ученика
    Args:
        student_id: ID ученика
    Returns:
        str: Имя и фамилия ученика или None в случае ошибки
    """
    try:
        connection = sqlite3.connect('course.db')
        cursor = connection.cursor()

        # Получаем логин (имя) ученика
        cursor.execute("""
            SELECT login 
            FROM user 
            WHERE id = ? AND userTypeID = 1
        """, (student_id,))
        
        result = cursor.fetchone()
        
        if result:
            return result[0]  # Возвращаем имя ученика
        return None
        
    except sqlite3.Error as e:
        print(f"Произошла ошибка при получении данных ученика: {e}")
        return None
        
    finally:
        if connection:
            connection.close()

def get_student_assignment_list():
    """
    Функция возвращает список студентов, которые не назначены учителям.
    Returns:
        list: Список студентов в формате [{'id': id, 'name': name}]
    """
    try:
        connection = sqlite3.connect('course.db')
        cursor = connection.cursor()

        # Получаем всех студентов
        cursor.execute("SELECT id, login FROM user WHERE userTypeID = 1")
        all_students = cursor.fetchall()

        # Получаем id студентов, которые уже назначены
        cursor.execute("SELECT idStudent FROM teacherToStudent")
        assigned_students = {row[0] for row in cursor.fetchall()}

        # Фильтруем студентов, которые не назначены
        unassigned_students = [
            {'id': student[0], 'name': student[1]} 
            for student in all_students 
            if student[0] not in assigned_students
        ]
        
        return unassigned_students

    except sqlite3.Error as e:
        print(f"Произошла ошибка при получении списка студентов: {e}")
        return []

    finally:
        if connection:
            connection.close()

def load_tests_to_db(json_file='course_tests.json'):
    """
    Загружает тесты из JSON файла в таблицу questionBase.
    Args:
        json_file (str): Путь к JSON файлу с тестами.
    Returns:
        None
    """
    try:
        # Чтение данных из JSON файла
        with open(json_file, 'r', encoding='utf-8') as file:
            tests_data = json.load(file)

        # Check if 'tests' key exists
        if not tests_data:
            print(f"Файл {json_file} пуст или имеет неверный формат.")
            return

        connection = sqlite3.connect('course.db')
        cursor = connection.cursor()

        # Вставка данных в таблицу questionBase
        for test_id, test in tests_data.items():
            for question in test['questions']:
                question_id = question['id']
                question_text = question['text']
                answers = question['answers']

                # Prepare answers based on the expected structure
                answer1 = answers[0]['text'] if len(answers) > 0 else ""
                answer2 = answers[1]['text'] if len(answers) > 1 else ""
                answer3 = answers[2]['text'] if len(answers) > 2 else ""
                answer4 = answers[3]['text'] if len(answers) > 3 else ""

                # Вставляем вопрос в таблицу
                cursor.execute("""
                    INSERT INTO questionBase (idTest, textQuest, answer1, answer2, answer3, answer4)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    question_id,  # idTest from the question
                    question_text,  # textQuest
                    answer1,  # answer1
                    answer2,  # answer2
                    answer3,  # answer3
                    answer4   # answer4
                ))

        connection.commit()
        print("Тесты успешно загружены в базу данных.")

    except sqlite3.Error as e:
        print(f"Произошла ошибка при загрузке тестов в базу данных: {e}")
    except FileNotFoundError:
        print(f"Файл {json_file} не найден.")
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON файла.")
    finally:
        if connection:
            connection.close()