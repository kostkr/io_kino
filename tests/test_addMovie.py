import sys, pytest
import datetime
sys.path.append('../')
from io_kino.bd_connection import connection
from io_kino.addMovie import addMovie

def test_addMovie():
    conn = connection()
    cursor = conn.cursor()

    arg1 = (
    "colasion1",
    "1999-12-19",
    "03:31:10",
    );addMovie(arg1, cursor)

    arg2 = (
    "colasion2",
    "1997-12-19",
    "03:45:10",
    );addMovie(arg2, cursor)
    
    query = 'SELECT tytul, premiera, dlugosc FROM filmy WHERE tytul = ? AND premiera = ? AND dlugosc = ?'
    cursor.execute(query, arg1)

    row = cursor.fetchall()
    assert row[0][0] == arg1[0] and row[0][1].strftime('%Y-%m-%d') == arg1[1] and row[0][2].strftime('%H:%M:%S') == arg1[2]

    cursor.execute(query, arg2)

    row = cursor.fetchall()
    assert row[0][0] == arg2[0] and row[0][1].strftime('%Y-%m-%d') == arg2[1] and row[0][2].strftime('%H:%M:%S') == arg2[2]
     
    cursor.close()
    conn.close()
