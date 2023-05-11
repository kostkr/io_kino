import pyodbc

def connection():
    server = 'localhost'
    database = ''
    username = 'sa'
    password = 'citqus-viVcy6-najcyq'
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';UID='+username+';PWD='+ password)
    return conn

