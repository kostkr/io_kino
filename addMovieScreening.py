def addMovieScreening(arg, cursor):
    sql_procedura_dodaj_seans = """ EXEC dodaj_seans
        @tytul=?, 
        @premiera=?, 
        @data_rozpoczecia=?, 
        @data_zakonczenia=?,
        @id_sala=?,
        @cena=?
    """
    cursor.execute(sql_procedura_dodaj_seans, arg)
    return cursor
