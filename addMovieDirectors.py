def addMovieDirectors(arg, cursor):
    sql_procedura_dodaj_film_rezyserzy = """
    EXEC dodaj_film_rezyserzy 
        @tytul=?, 
        @premiera=?, 
        @imie_rezysera=?,
        @nazwisko_rezysera=?,
        @plec_rezysera=?,
        @ocena_rezysera=?
    """
    cursor.execute(sql_procedura_dodaj_film_rezyserzy, arg)
    return cursor
