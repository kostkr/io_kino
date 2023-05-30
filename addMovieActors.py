def addMovieActors(arg, cursor):
    sql_procedura_dodaj_film_aktorzy = """ EXEC dodaj_film_aktorzy
        @tytul=?, 
        @premiera=?, 
        @imie_aktora=?,
        @nazwisko_aktora=?,
        @plec_aktora=?,
        @imie_rola_aktora=?,
        @nazwisko_rola_aktora=?,
        @plec_rola_aktora=?
    """
    cursor.execute(sql_procedura_dodaj_film_aktorzy, arg)
    return cursor
