import sqlite3

try:
    connection = sqlite3.connect('database.db')
    with open('schema.sql') as f:
        script = f.read()
    connection.executescript(script)

    cur = connection.cursor()

    cur.execute("INSERT INTO badges (name, description,badge,students) VALUES (?, ? ,?,?)",
                ('First Post', 'Content for the first post',"","ashraf@gmail.com")
                )

    cur.execute("INSERT INTO badges (name, description,badge,students) VALUES (?, ? ,?,?)",
                ('second Post', 'Content for the second post',"","ashraf.ali@gmail.com")
                )
    connection.commit()
    connection.close()
except sqlite3.Error as error:
    print("Error while executing sqlite script", error)
finally:
    if connection:
        connection.close()
        print("sqlite connection is closed")
