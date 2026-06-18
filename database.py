import sqlite3



def create_table():
    # Подключаемся к файлу базы (если файла нет — Питон сам его создаст)
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()  # Курсор — это "рука", которая вводит команды

    # SQL-команда, которая буквально рисует твою таблицу
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            task_text TEXT,
            solution TEXT,
            language TEXT,
            title TEXT
        )
    ''')

    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем файл, чтобы не висел в памяти



def add_task(date, task_text, solution, language, title):   # Функция добавления задания в БД

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO tasks (date, task_text, solution, language, title)
    VALUES (?,?,?,?,?)
    ''', (date, task_text, solution,language,title))

    conn.commit()
    conn.close()



def available_tasks():   # Функция для вывода списка дат заданий из БД пользователю
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT date, COUNT(*)
    FROM tasks
    GROUP BY date
    ORDER BY date
    ''')

    dates = cursor.fetchall()

    conn.close()

    return dates



def get_solution_by_date(date):   # Функция для вывода решения задания
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT solution, language, title
    FROM tasks 
    WHERE date = ?
    ORDER BY id
    ''', (date,))

    solutions = cursor.fetchall()

    conn.close()

    return solutions



def get_task_by_date(date):  # Функция для вывода заданий для перегенерации
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id, task_text, language, title
    FROM tasks 
    WHERE date = ?
    ORDER BY id
    ''', (date,))

    tasks = cursor.fetchall()

    conn.close()

    return tasks



def get_task_by_id(task_id):

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT task_text, language, title
    FROM tasks
    WHERE id = ?
    ''', (task_id,))

    task_text = cursor.fetchone()

    conn.close()

    return task_text