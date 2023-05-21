import pyodbc
import json

def connection():
    # Opening JSON file
    f = open('config.json')
    data = json.load(f)

    server   = data["server"]
    database = data["database"]
    username = data["username"]
    password = data["password"]
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';UID='+username+';PWD='+ password)

    f.close()
    return conn