import pyodbc
import json

def connection():
    # Opening JSON config file
    f = open('config.json')
    data = json.load(f)

    server   = data["server"]
    database = data["database"]
    username = data["username"]
    password = data["password"]
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';UID='+username+';PWD='+ password)
    # ON WINDOWS
    # conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';UID='+username+';PWD='+ password, Trusted_Connection='Yes')

    f.close()
    return conn