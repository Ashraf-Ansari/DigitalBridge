import sqlite3

try:
    connection = sqlite3.connect('database.db')
    with open('schema.sql') as f:
        script = f.read()
    connection.executescript(script)
    connection.close()
except sqlite3.Error as error:
    print("Error while executing sqlite script", error)
finally:
    if connection:
        connection.close()
        print("sqlite connection is closed")
