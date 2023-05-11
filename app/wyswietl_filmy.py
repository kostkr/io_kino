from flask import Flask, render_template, request, redirect
import pyodbc

from bd_connection import connection

wyswietl_filmy = Flask(__name__)

@wyswietl_filmy.route("/")
def main():
    filmy = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wyswietl_filmy")
    for row in cursor.fetchall():
        filmy.append({"id": row[0], "tytul": row[1], "premiera": row[2], "dlugosc": row[3]})
    conn.close()
    return render_template("wyswietl_filmy.html", filmy = filmy)



@wyswietl_filmy.route("/a_wyswietl_filmy")
def a_wyswietl_filmy():
    filmy = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wyswietl_filmy")
    for row in cursor.fetchall():
        filmy.append({"id": row[0], "tytul": row[1], "premiera": row[2], "dlugosc": row[3]})
    conn.close()
    return render_template("a_wyswietl_filmy.html", filmy = filmy)


@wyswietl_filmy.route("/a_wyswietl_filmy/sprzedaz")
def sprzedaz():
    sprzedaz = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM raport_sprzedazy")
    for row in cursor.fetchall():
        sprzedaz.append({"id": row[0], "l_seans": row[1], "srednia_cena_za_bilet": row[2], "l_sprz_biletow": row[3], "laczny_przychod": row[4]})
    conn.close()
    return render_template("a_sprzedaz.html", sprzedaz = sprzedaz)


@wyswietl_filmy.route("/a_wyswietl_filmy/sale_lista")
def sale_lista():
    sale = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wyswietl_sale_kinowe")
    for row in cursor.fetchall():
        sale.append({"sala_id": row[0], "limit_miejsc": row[1], "wejscie_dla_niepelnosprawnych": row[2], "pracownik_id": row[3]})
    conn.close()
    return render_template("a_sale.html", sale = sale)



@wyswietl_filmy.route("/dodaj_film", methods = ['GET','POST'])
def dodaj_film():
    if request.method == 'GET':
        return render_template("dodaj_film.html", film = {})
    if request.method == 'POST':
        tytul = str(request.form["tytul"])
        premiera = str(request.form["premiera"])
        dlugosc = str(request.form["dlugosc"])
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("EXEC dodaj_film @tytul=?, @premiera=?, @dlugosc=?", tytul, premiera, dlugosc)

        wyniki=[]
        for row in cursor.fetchall():
          wyniki.append({"w": row[0]})

        conn.commit()
        conn.close()
        return render_template("wynik_dodania.html",wyniki = wyniki)


@wyswietl_filmy.route("/dodaj_seans", methods = ['GET','POST'])
def dodaj_seans():
    if request.method == 'GET':
        return render_template("dodaj_seans.html", seans = {})
    if request.method == 'POST':
        tytul = str(request.form["tytul"])
        premiera = str(request.form["premiera"])
        data_rozpoczecia = str(request.form["data_rozpoczecia"])
        data_zakonczenia = str(request.form["data_zakonczenia"])
        id_s = str(request.form["id_s"])
        cena = str(request.form["cena"])
        conn = connection()
        cursor = conn.cursor()
        q = (""" EXEC dodaj_seans
                                  @tytul=?, 
                                  @premiera=?, 
                                  @data_rozpoczecia=?,
                                  @data_zakonczenia=?,
                                  @id_sala=?,
                                  @cena=?
          """)
        cursor.execute(q, tytul, premiera, data_rozpoczecia, data_zakonczenia, id_s, cena)

        wyniki=[]
        for row in cursor.fetchall():
          wyniki.append({"w": row[0]})

        conn.commit()
        conn.close()
        return render_template("wynik_dodania.html",wyniki = wyniki)


@wyswietl_filmy.route("/dodaj_aktorow", methods = ['GET','POST'])
def dodaj_aktorow():
    if request.method == 'GET':
        return render_template("dodaj_aktorow.html", film = {})
    if request.method == 'POST':
        tytul = str(request.form["tytul"])
        premiera = str(request.form["premiera"])
        imie = str(request.form["imie"])
        nazwisko = str(request.form["nazwisko"])
        plec = str(request.form["plec"])
        imie_roli = str(request.form["imie_roli"])
        nazwisko_roli = str(request.form["nazwisko_roli"])
        plec_roli = str(request.form["plec_roli"])
        conn = connection()
        cursor = conn.cursor()
        q = (""" EXEC dodaj_film_aktorzy
                                        @tytul=?, 
                                        @premiera=?, 
                                        @imie_aktora=?,
                                        @nazwisko_aktora=?,
                                        @plec_aktora=?,
                                        @imie_rola_aktora=?,
                                        @nazwisko_rola_aktora=?,
                                        @plec_rola_aktora=?
          """)
        cursor.execute(q, tytul, premiera, imie,nazwisko,plec,imie_roli,nazwisko_roli,plec_roli)

        wyniki=[]
        for row in cursor.fetchall():
          wyniki.append({"w": row[0]})

        conn.commit()
        conn.close()
        return render_template("wynik_dodania.html",wyniki = wyniki)








@wyswietl_filmy.route("/dodaj_film_szczegoly", methods = ['GET','POST'])
def dodaj_film_szczegoly():
    if request.method == 'GET':
        return render_template("dodaj_film_szczegoly.html", film = {})
    if request.method == 'POST':
        tytul = str(request.form["tytul"])
        premiera = str(request.form["premiera"])
        opis = str(request.form["opis"])
        recenzje = str(request.form["recenzje"])
        jezyk_oryginalny = str(request.form["jezyk_oryginalny"])
        jezyk_lektor = str(request.form["jezyk_lektor"])
        jezyk_napisy = str(request.form["jezyk_napisy"])
        pg_rating = str(request.form["pg_rating"])
        conn = connection()
        cursor = conn.cursor()

        cursor.execute(""" EXEC dodaj_film_szczegoly 
                                @tytul=?, 
                                @premiera=?, 
                                @opis=?,
                                @recenzje=?,
                                @jezyk_oryginalny=?,
                                @jezyk_lektor=?,
                                @jezyk_napisy=?,
                                @pg_rating=?
                                """
                          ,tytul, premiera, opis, recenzje, jezyk_oryginalny, jezyk_lektor, jezyk_napisy, pg_rating)

        wyniki=[]
        for row in cursor.fetchall():
          wyniki.append({"w": row[0]})

        conn.commit()
        conn.close()
        return render_template("wynik_dodania.html",wyniki = wyniki)



@wyswietl_filmy.route('/szczegoly/<int:id>')
def szczegoly(id):
    filmy = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wyswietl_szczegoly_filmu_po_id(?)", id)
    for row in cursor.fetchall():
        filmy.append({"tytul": row[0], "premiera": row[1], "dlugosc": row[2], "opis": row[3], "recenzje": row[4], "jezyk_oryginalny": row[5], "jezyk_lektor": row[6], "jezyk_napisy": row[7], "pg_rating": row[8]})
    conn.close()
    return render_template("wyswietl_filmy_szczegoly.html", filmy = filmy)


@wyswietl_filmy.route('/aktorzy/<int:id>')
def aktorzy(id):
    filmy = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wyswietl_aktorow_filmu_po_id(?)", id)
    for row in cursor.fetchall():
        filmy.append({"tytul": row[0], "premiera": row[1], "dlugosc": row[2], "o_imie": row[3], "o_nazwisko": row[4], "o_plec": row[5], "w_roli": row[6], "r_o_imie": row[7], "r_o_nazwisko": row[8], "r_o_plec": row[9]})
    conn.close()
    return render_template("wyswietl_aktorow.html", filmy = filmy)


@wyswietl_filmy.route('/seans/<int:id>')
def seans(id):
    seanse = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wyswietl_seanse_po_id(?)", id)
    for row in cursor.fetchall():
        seanse.append({"tytul": row[0], "premiera": row[1], "dlugosc": row[2], "data_rozpoczecia": row[3], "data_zakonczenia": row[4], "sala_id": row[5], "seans_id":row[6], "cena":row[7]})
    conn.close()
    return render_template("wyswietl_seans.html", seanse = seanse)



@wyswietl_filmy.route('/seans/sale/<int:id>')
def sale(id):
    sale = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wyswietl_sale_po_id(?)", id)
    for row in cursor.fetchall():
        sale.append({"sala_id": row[0], "limit_miejsc": row[1], "wejscie_dla_niepelnosprawnych": row[2]})
    conn.close()
    return render_template("wyswietl_sale.html", sale = sale)



@wyswietl_filmy.route('/seans/bilety/<int:id>', methods = ['GET','POST'])
def bilety(id):
    if request.method == 'GET':
      seans = []
      conn = connection()
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM wyswietl_seans_po_id(?)", id)
      for row in cursor.fetchall():
          seans.append({"tytul": row[0], "premiera": row[1], "dlugosc": row[2], "data_rozpoczecia": row[3], "data_zakonczenia": row[4], "sala_id": row[5], "seans_id":row[6], "cena":row[7]})

      cursor.execute("SELECT dbo.wolne_miejsca(?)", id)
      for row in cursor.fetchall():
          seans.append({"l": row[0]})
      conn.close()
      return render_template("kup_bilet.html", bilet = {}, seans = seans)


    if request.method == 'POST':
        imie = str(request.form["imie"])
        nazwisko = str(request.form["nazwisko"])
        email = str(request.form["email"])
        nr_tel = str(request.form["nr_tel"])
        plec = str(request.form["plec"])
        liczba_biletow = str(request.form["liczba_biletow"])
        conn = connection()
        cursor = conn.cursor()
        q = """EXEC dodaj_zamowienie 
          @liczba_biletow=?, 
          @seans_id=?, 
          @imie=?, 
          @nazwisko=?, 
          @email=?, 
          @nr_tel=?, 
          @plec=?
        """
        print(id)
        cursor.execute(q, liczba_biletow, str(id), imie, nazwisko, email, nr_tel, plec)

        wyniki=[]
        for row in cursor.fetchall():
          wyniki.append({"w": row[0],})

        conn.commit()
        conn.close()
        return render_template("wynik_dodania.html",wyniki = wyniki)




@wyswietl_filmy.route('/rezyserzy/<int:id>')
def rezyserzy(id):
    filmy = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wyswietl_szczegoly_filmu_po_id(?)", id)
    for row in cursor.fetchall():
        filmy.append({"tytul": row[0], "premiera": row[1], "dlugosc": row[2], "opis": row[3], "recenzje": row[4], "jezyk_oryginalny": row[5], "jezyk_lektor": row[6], "jezyk_napisy": row[7], "pg_rating": row[8]})
    conn.close()
    return render_template("wyswietl_filmy_szczegoly.html", filmy = filmy)






if(__name__ == "__main__"):
    wyswietl_filmy.run()
