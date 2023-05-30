def addMovie(arg, cursor):
    sql_procedura_dodaj_film = """ EXEC dodaj_film 
        @tytul=?, 
        @premiera=?, 
        @dlugosc=?
    """
    cursor.execute(sql_procedura_dodaj_film, arg)
    return cursor
