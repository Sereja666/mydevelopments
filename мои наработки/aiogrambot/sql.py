import sqlite3

from sqlite3 import Error

def sql_connection(): #соединение  с базой
    try:
        con = sqlite3.connect('mydatabase.db')
        return con
    except Error:
        print(Error)

def sql_table(con): #используя объект курсора выполняет SQL оператор create table.

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE employees(id integer PRIMARY KEY, name text, salary real, department text, position text, hireDate text)")

    con.commit() # Метод commit() сохраняет все сделанные изменения. В конце скрипта производится вызов обеих функций.

con = sql_connection()  #соединение  с базой
sql_table(con)