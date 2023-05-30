def addMovieDetails(arg, cursor):
    sql_procedura_dodaj_film_szczegoly = """ EXEC dodaj_film_szczegoly 
        @tytul=?, 
        @premiera=?, 
        @opis=?,
        @recenzje=?,
        @jezyk_oryginalny=?,
        @jezyk_lektor=?,
        @jezyk_napisy=?,
        @pg_rating=?
    """
    cursor.execute(sql_procedura_dodaj_film_szczegoly, arg)
    return cursor
