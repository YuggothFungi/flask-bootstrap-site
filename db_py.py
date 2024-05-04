import sqlite3

#Создание пользователя
def registerUser(login, password, userTypeID):
    connection = sqlite3.connect('course.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM user WHERE login = ? AND password = ?", (login, password))
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
    print(usertype[1])
    return usertype[1]

#Проверка является ли пользователя администратором
# def checkAdmin(login):
#     conn = sqlite3.connect('course.db')
#     cursor = conn.cursor()
    
#     query = f"SELECT userTypeID FROM user WHERE login = '{login}'"
#     cursor.execute(query)
    
#     userTypeID = cursor.fetchone()
    
#     conn.close()
    
#     if userTypeID := 2:
#         return print(True)
#     else:
#         return None

#Авторизация пользователя
def authUser(login, password):
    conn = sqlite3.connect('course.db')  # Подставьте имя вашей базы данных SQLite3
    cursor = conn.cursor()

    cursor.execute("SELECT id, userTypeID FROM user WHERE login=? AND password=?", (login, password))
    result = cursor.fetchone()

    if result:
        print(result)
        return result
    else:
        return None

    conn.close()

def getUserList():
    connection = sqlite3.connect('course.db')
    cursor = connection.cursor()

    cursor.execute("SELECT login, typeName FROM user, usertype where user.userTypeID = usertype.id and user.userTypeID <> 3")
    userlist = cursor.fetchall()
    return userlist

# createUser('Niveis2', '123456', 1)
