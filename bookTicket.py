def bookTicket(arg, cursor):
    sql_procedura = """ EXEC dodaj_zamowienie
        @liczba_biletow=?,
        @seans_id=?,
        @imie=?, 
        @nazwisko=?, 
        @email=?, 
        @nr_tel=?, 
        @plec=?
    """
    cursor.execute(sql_procedura, arg)
    return cursor
