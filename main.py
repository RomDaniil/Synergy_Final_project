import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame): #Создание главного окна
    def __init__(self, root): #Конструктор
        super().__init__(root)
        self.init_main() #Вызов init_main
        self.db = db #Добавление аттрибута db
        self.view_records()

    def init_main(self): #Хранение и инициализайия данных
        toolbar = tk.Frame(bg="#d7d8e0", bd=2) #Панель инструментов
        toolbar.pack(side=tk.TOP, fill=tk.X) #Расположение панели, расширение по всему окну 
        self.add_img = tk.PhotoImage(file="./img/add.png") #Изображение для кнопки добавить
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.add_img, command=self.open_dialog
        ) #Создание кнопки добавить
        btn_open_dialog.pack(side=tk.LEFT) #Расположение кнопки на главном экране

        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "tel", "email", "wages"), height=45, show="headings"
        ) #Создание таблички

        self.tree.column("ID", width=30, anchor=tk.CENTER) #Параметры колонки id
        self.tree.column("name", width=300, anchor=tk.CENTER) #Параметры колонки ФИО
        self.tree.column("tel", width=150, anchor=tk.CENTER) #Параметры колонки телефон
        self.tree.column("email", width=150, anchor=tk.CENTER) #Параметры колонки почта
        self.tree.column("wages", width=100, anchor=tk.CENTER) #Параметры колонки зарплата

        self.tree.heading("ID", text="ID") #Создание удобочиемого вида id
        self.tree.heading("name", text="ФИО") #Создание удобочиемого вида ФИО
        self.tree.heading("tel", text="Телефон") #Создание удобочиемого вида телефон
        self.tree.heading("email", text="E-mail") #Создание удобочиемого вида почта
        self.tree.heading("wages", text='Зарплата') #Создание удобочитаемого вида зарплата

        self.tree.pack(side=tk.LEFT) #Размещение на главном окне

        self.update_img = tk.PhotoImage(file="./img/update.png") #Изображение для кнопки редактировать
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        ) #Создание кнопки редактировать
        btn_edit_dialog.pack(side=tk.LEFT) #Расположение кнопки редактировать на главном окне

        self.delete_img = tk.PhotoImage(file="./img/delete.png") #Изображение для кнопки удалить
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        ) #Создание кнопки удалить
        btn_delete.pack(side=tk.LEFT) #Расположение кнопки удалить на главном окне

        self.search_img = tk.PhotoImage(file="./img/search.png") #Изображение для кнопки найти
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        ) #Создание кнопки найти
        btn_search.pack(side=tk.LEFT) #Расположение кнопки найти на главном окне

    def open_dialog(self): #Обращение к классу Child
        Child()

    def records(self, name, tel, email, wages): #Записи на главном окне
        self.db.insert_data(name, tel, email, wages)
        self.view_records() #Вызов метода view_records

    def view_records(self): #Просмотр данных из базы данных
        self.db.cursor.execute("SELECT * FROM db") #Выбор всей информации
        [self.tree.delete(i) for i in self.tree.get_children()] #Доливаем из виджета таблицы
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()] #Добавить в виджеты таблицы всю информацию из базы данных

    def open_update_dialog(self): #Вызов класса Update
        Update()

    def update_records(self, name, tel, email, wages): #Редактировать запись
        self.db.cursor.execute(
            """UPDATE db SET name=?, tel=?, email=?, wages=? WHERE id=?""",
            (name, tel, email, wages, self.tree.set(self.tree.selection()[0], "#1")),
        ) #Редактирование записи
        self.db.conn.commit()
        self.view_records() #Отрытие окна для редактирования данных

    def delete_records(self): #Удадение записи
        for selection_items in self.tree.selection(): #Цикл с помощью которого мы удаляем выделенную запись
            self.db.cursor.execute(
                "DELETE FROM db WHERE id=?", (self.tree.set(selection_items, "#1"))
            )
        self.db.conn.commit()
        self.view_records() #Вызов view_records 

    def open_search_dialog(self): #Вызов Search
        Search()

    def search_records(self, name): #Найти запись
        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM db WHERE name LIKE ?", (name,)) #Нахождение записи по любому отрывку из записи
        [self.tree.delete(i) for i in self.tree.get_children()] #Доливаем из виджета таблицы
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()] #Добавить в виджеты таблицы всю информацию из базы данных

class Child(tk.Toplevel): #Дочернее окно
    def __init__(self): #Конструктор
        super().__init__(root)
        self.init_child() #Вызов init_child
        self.view = app

    def init_child(self): #Прописываем дочернее окно
        self.title("Добавить") #
        self.geometry("400x220") #Размеры
        self.resizable(False, False) #Ограничение размеров 

        self.grab_set() #Перехват событий 
        self.focus_set() #Захват фокуса

        label_name = tk.Label(self, text="ФИО:") #Поле для ФИО
        label_name.place(x=50, y=50) #Расположение надписи
        label_select = tk.Label(self, text="Телефон:") #Поле для телефона
        label_select.place(x=50, y=80) #Расположение надписи
        label_sum = tk.Label(self, text="E-mail:") #Поле для почты
        label_sum.place(x=50, y=110) #Расположение надписи
        label_wages = tk.Label(self, text="Зарплата:") #Поле для зарплаты
        label_wages.place(x=50, y=140) #Расположение зарплаты

        self.entry_name = ttk.Entry(self) #Создание поля для ввода имени
        self.entry_name.place(x=200, y=50) #Расположение поля 
        self.entry_email = ttk.Entry(self) #Создание поля для ввода почты
        self.entry_email.place(x=200, y=80) #Расположение поля 
        self.entry_tel = ttk.Entry(self) #Создание поля для ввода телефона
        self.entry_tel.place(x=200, y=110) #Расположение поля 
        self.entry_wages = ttk.Entry(self) #Создание поля для ввода зарплаты
        self.entry_wages.place(x=200, y=140) #Расположение поля 

        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy) #Кнопка для закрытия окна
        self.btn_cancel.place(x=220, y=170) #Расположение окна

        self.btn_ok = ttk.Button(self, text="Добавить") #Кнопка для добавления
        self.btn_ok.place(x=220, y=170)

        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_wages.get()
            ),
        ) #Отслеживание нажатия, связывание базы данных


class Update(Child): #Класс для редактирования записи
    def __init__(self): #Инициализатор
        super().__init__()
        self.init_edit() #Вызов init_edit
        self.view = app
        self.db = db #Добавление аттрибута db
        self.default_data() #Вызов default_data

    def init_edit(self): #Созжание дочернего окна для редактирования 
        self.title("Редактирование контакта") #Название окна
        btn_edit = ttk.Button(self, text="Редактировать") #Кнопка редактировать
        btn_edit.place(x=205, y=170) #Кнопка редактировать
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_wages.get()
            ),
        ) #Отслеживание нажития левой кнопки мыши 
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+") #Отслеживание нажития левой кнопки мыши 
        self.btn_ok.destroy() #Закрыть

    def default_data(self):
        self.db.cursor.execute(
            "SELECT * FROM db WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),
        ) #Выбор всей выделенной информации
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_wages.insert(0, row[4])

class Search(tk.Toplevel): #Класс для поиска
    def __init__(self): #Инициализатор
        super().__init__()
        self.init_search() #Запуск init_search
        self.view = app

    def init_search(self): #дочернее окно поиск
        self.title("Поиск контакта") #Название окна
        self.geometry("300x100") #Размеры окна
        self.resizable(False, False) #Ограничение размеров

        label_search = tk.Label(self, text="Имя:") #Надпись Имя:
        label_search.place(x=50, y=20) #Расположение надписи

        self.entry_search = ttk.Entry(self) #Текстовое поле для ввода
        self.entry_search.place(x=100, y=20, width=150) #Расположение поля

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy) #кнопка закрыть
        btn_cancel.place(x=185, y=50) #Расположение кнопки закрыть

        search_btn = ttk.Button(self, text="Найти") #Создание кнопки найти
        search_btn.place(x=105, y=50) #Расположение кнопки 
        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        ) #Отлеживание нажатия левой кнопки мыши
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+") #Отлеживание нажатия левой кнопки мыши


class DB: #База данных
    def __init__(self): #Инициализатор
        self.conn = sqlite3.connect("db.db") #Соединение с базой данных
        self.cursor = self.conn.cursor() #Создание обьекта cursor
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT,
                wages INTEGER
            )"""
        ) #Запрос на создание таблицы
        self.conn.commit()

    def insert_data(self, name, tel, email, wages):
        self.cursor.execute(
            """INSERT INTO db(name, tel, email, wages) VALUES(?, ?, ?, ?)""", (name, tel, email, wages)
        ) #Метод для добавления данных
        self.conn.commit()


if __name__ == "__main__": #Цикл программы
    root = tk.Tk() #root - главное окно
    db = DB() #Добавление аттрибута db
    app = Main(root) 
    app.pack()
    root.title("Список сотрудников") #Название окна
    root.geometry("760x480") #Размеры окна
    root.resizable(False, False) #Ограничение расширения окна
    root.mainloop() #Завершение кода
