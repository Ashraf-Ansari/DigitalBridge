import calendar
import os
import sqlite3
import time


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

def generate_file_name(name):
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    name = str(ts)+"-"+name
    return name