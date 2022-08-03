import calendar;
import sqlite3
import time;
import os

from flask import Flask, render_template, request

app = Flask(__name__)

sqlite_insert_blob_query = """INSERT INTO badges (name, description,badge,students) VALUES (?, ? ,?,?)"""
image_basepath = "static/images/"
allData = 'select * from badges'
def delete_file(filepath):

    if os.path.isfile(filepath):
        os.remove(filepath)
        print("File has been deleted")
    else:
        print("File does not exist")

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/data')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM badges').fetchall()
    print(posts)
    conn.close()
    return render_template('file_upload_form.html')

@app.route('/')
def upload():
    con = get_db_connection()
    result = con.execute(allData).fetchall()
    print("length",len(result))
    con.close()
    return render_template("file_upload_form.html")
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")



# def generate_file_name(name):
#     gmt = time.gmtime()
#     ts = calendar.timegm(gmt)
#     if name==None:
#
#     name = str(name)
#
#     new_name = str(ts)+"-"+name.replace(" ","").replace("-","")
#     return new_name

@app.route('/addBadge', methods=['POST'])
def success():
    print("inside success method")
    if request.method == 'POST':
        file = request.files['file']
        description = request.form['description']
        name = request.form['name']
        students = request.form['students']
        print("A",file.filename)
        if file.filename=="":
            print("empty")
        else:
            file_path = image_basepath+file.filename
            print(file, description, name, students,file_path)
            file.save(file_path)
            file_data = convertToBinaryData(file_path)
            con = get_db_connection()
            con.execute(sqlite_insert_blob_query,(name,description,file_data,students))
            con.commit()
            con.close()
            # delete_file(file_path)
        return render_template("success.html")

@app.route('/detection')
def detection():
    dir = os.walk(image_basepath)
    print("dir",dir)
    file_list = []

    for path, subdirs, files in dir:
        for file in files:
            print(path,file)
            temp = path + file
            print(temp)
            file_list.append(temp)
    print("all files ",file_list)
    return render_template('showpictures.html', filenames=file_list)

@app.route('/showpictures')
def showpictures():
    con = get_db_connection()
    result = con.execute(allData).fetchall()
    print("length", len(result))
    file_list = []
    for i in result:
        file_list.append(i[3])
        print(i[1],i[4])
    print()
    print()
    print()
    return render_template('showpictures.html', filenames=file_list)

@app.route('/badge/verify', methods=['GET'])
def search():
    args = request.args
    args = args.to_dict();
    print(args)
    name = args.get("name")
    email = args.get("email")
    con = get_db_connection()
    result = con.execute(allData).fetchall()
    print("length", len(result))
    finalResult = []
    for i in result:
        if name==i[1]:
            emails = str(i[4]).split(",")
            for j in emails:
                if j==email:
                    finalResult.append(i)
    print(finalResult)
    return render_template("success.html")


if __name__ == '__main__':
    app.run(debug=True)