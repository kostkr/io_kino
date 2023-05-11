import pyodbc

from bd_connection import connection
conn = connection()
cursor = conn.cursor()




drop = """
    DROP TRIGGER IF EXISTS Tr_INSERT_filmy
    DROP TRIGGER IF EXISTS Tr_INSERT_f_szczegoly
    DROP TRIGGER IF EXISTS Tr_INSERT_seans
    DROP TRIGGER IF EXISTS Tr_INSERT_zamowienie
    DROP TRIGGER IF EXISTS Tr_INSERT_nr_tel
    DROP TRIGGER IF EXISTS Tr_INSERT_email
    DROP TRIGGER IF EXISTS Tr_INSERT_osoba
    DROP TRIGGER IF EXISTS Tr_INSERT_plec
    SET IMPLICIT_TRANSACTIONS OFF;
"""
cursor.execute(drop)

film = """
    CREATE TRIGGER Tr_INSERT_filmy ON filmy
    INSTEAD OF INSERT
    AS
    BEGIN
        SET NOCOUNT ON;
        
        DECLARE @tytul NVARCHAR(50)
        SELECT @tytul = I.tytul
        FROM Inserted I

        DECLARE @premiera DATE
        SELECT @premiera = I.premiera
        FROM Inserted I

        DECLARE @dlugosc TIME
        SELECT @dlugosc = I.dlugosc
        FROM Inserted I

        IF (SELECT film_id FROM filmy WHERE tytul=@tytul AND premiera=@premiera) IS NOT NULL
            SELECT 'PODANY FILM JUZ ISTNIEJE W BAZIE DANYCH'
        ELSE 
        BEGIN
            INSERT INTO filmy VALUES (@tytul, @premiera, @dlugosc);
            SELECT 'FILM ZOSTAL POPRAWNIE DODANY DO BAZY DANYCH'
        END
    END
"""
cursor.execute(film)



film_szczegoly = """
    CREATE TRIGGER Tr_INSERT_f_szczegoly ON filmy_szczegoly
    INSTEAD OF INSERT
    AS
    BEGIN
        SET NOCOUNT ON;
        
        DECLARE @id_f INT
        SELECT @id_f = I.film_id
        FROM Inserted I

        DECLARE @opis NVARCHAR(1000)
        SELECT @opis = I.opis
        FROM Inserted I

        DECLARE @recenzje float
        SELECT @recenzje = I.recenzje
        FROM Inserted I

        DECLARE @jezyk_oryginalny NVARCHAR(20)
        SELECT @jezyk_oryginalny = I.jezyk_oryginalny
        FROM Inserted I

        DECLARE @jezyk_lektor NVARCHAR(20)
        SELECT @jezyk_lektor = I.jezyk_lektor
        FROM Inserted I

        DECLARE @jezyk_napisy NVARCHAR(20)
        SELECT @jezyk_napisy = I.jezyk_napisy
        FROM Inserted I

        DECLARE @pg_rating INT
        SELECT @pg_rating = I.pg_rating
        FROM Inserted I

        IF EXISTS (
            SELECT 
                1
            FROM 
                filmy_szczegoly 
            WHERE 
                opis=@opis AND 
                recenzje=@recenzje AND 
                jezyk_oryginalny=@jezyk_oryginalny AND 
                jezyk_lektor=@jezyk_lektor AND 
                jezyk_napisy=@jezyk_napisy AND pg_rating=@pg_rating
            ) 
        BEGIN
            RAISERROR ('JUZ ISTNIEJE' ,16,1)
            --ROLLBACK TRANSACTION
        END 
        ELSE IF EXISTS(
            SELECT
                1
            FROM
                INSERTED
            WHERE
                jezyk_lektor LIKE '%[0-9]%' 
                OR jezyk_napisy LIKE '%[0-9]%' 
                OR jezyk_oryginalny LIKE '%[0-9]%' 
                OR pg_rating LIKE '%[A-Za-z]%'
        )    
        BEGIN
            RAISERROR ('NIEPOPRAWNE DANE - ZAWIERA CYFRE LUB LITERE' ,16,1)
            --ROLLBACK TRANSACTION
        END
        ELSE
        BEGIN
            INSERT INTO filmy_szczegoly VALUES
                (@id_f, @opis, @recenzje, @jezyk_oryginalny, @jezyk_lektor, @jezyk_napisy, @pg_rating)
            SELECT 'SZCZEGOLY FILMU ZOSTALY DODANE PRAWIDLOWO'
        END

    END
"""
cursor.execute(film_szczegoly)



seans = """
    CREATE TRIGGER Tr_INSERT_seans ON seanse_filmowe 
    INSTEAD OF INSERT
    AS
    BEGIN
        SET NOCOUNT ON;
        
        DECLARE @id_f INT
        SELECT @id_f = I.film_id
        FROM Inserted I

        DECLARE @data_rozpoczecia DATETIME
        SELECT @data_rozpoczecia = I.data_rozpoczecia
        FROM Inserted I

        DECLARE @data_zakonczenia DATETIME
        SELECT @data_zakonczenia = I.data_zakonczenia
        FROM Inserted I

        DECLARE @id_sala INT
        SELECT @id_sala = I.sala_id
        FROM Inserted I

        DECLARE @cena MONEY
        SELECT @cena = I.cena
        FROM Inserted I

        IF NOT EXISTS(  
            SELECT 
                * 
            FROM 
                seanse_filmowe 
            WHERE 
                data_rozpoczecia=@data_rozpoczecia AND 
                data_zakonczenia=@data_zakonczenia AND 
                sala_id=@id_sala AND film_id=@id_f
            ) 
            BEGIN

                IF @data_zakonczenia > @data_rozpoczecia
                BEGIN

                    DECLARE @dlugosc_f TIME;
                    SET @dlugosc_f = (SELECT dlugosc FROM filmy WHERE film_id=@id_f)
                    DECLARE @dlugosc_seansu INT
                    DECLARE @dlugosc_filmu INT
                    SET @dlugosc_seansu = (SELECT DATEDIFF ( minute , @data_rozpoczecia , @data_zakonczenia ) )
                    SET @dlugosc_filmu = (SELECT DATEDIFF ( minute , '00:00:00', @dlugosc_f ) )
                    IF (@dlugosc_seansu >= @dlugosc_filmu) --w minutach
                    BEGIN

                        IF NOT EXISTS (SELECT 
                                data_rozpoczecia, 
                                data_zakonczenia 
                            FROM 
                                seanse_filmowe 
                            WHERE 
                                sala_id = @id_sala AND 
                                @data_rozpoczecia <= data_zakonczenia AND 
                                @data_zakonczenia >= data_rozpoczecia)
                        BEGIN

                            INSERT INTO seanse_filmowe VALUES (
                                @id_f, 
                                @data_rozpoczecia, 
                                @data_zakonczenia, 
                                @id_sala,
                                @cena
                            )
                            SELECT 'SEANS ZOSTAL DODANY PRAWIDLOWO'

                        END
                        ELSE
                            SELECT 'BLAD - NA PODANYM PRZEDZIALE CZASU SEANSU SALA ZOSTALA JUZ ZAREZERWOWANA'

                    END
                    ELSE
                        SELECT 'BLAD - CZAS TRWANIA SEANSU JEST MNIEJSZY NIZ CZAS TRWANIA FILMU'


                END
                ELSE
                    SELECT 'BLAD - DATA ZAKONCZENIA JEST PRZED DATA ROZPOCZECIA'

            END
        ELSE 
            SELECT 'JUZ ISTNIEJE'

    END
"""
cursor.execute(seans)


nr_tel = """
    CREATE TRIGGER Tr_INSERT_nr_tel ON wlasciciel_nr_tel
    INSTEAD OF INSERT
    AS
    BEGIN
        SET NOCOUNT ON;

        IF EXISTS (
            SELECT 
                1
            FROM 
                INSERTED
            WHERE 
                (LEN(nr_tel) >= 10 OR LEN(nr_tel) <=8 OR nr_tel LIKE '%[^0-9]%')
        )
        BEGIN
            RAISERROR ('NIEPOPRAWNY NR TEL' ,16,1)
        END 
        ELSE    
        BEGIN
            INSERT INTO 
                wlasciciel_nr_tel 
            SELECT 
                I.osoba_id, 
                I.nr_tel
            FROM 
                INSERTED I
        END    
    END
"""
cursor.execute(nr_tel)


email = """
    CREATE TRIGGER Tr_INSERT_email ON wlasciciel_adresu_email
    INSTEAD OF INSERT
    AS
    BEGIN
        SET NOCOUNT ON;

        IF EXISTS (
            SELECT 
                1
            FROM 
                INSERTED
            WHERE 
                (email NOT LIKE '%_@%_.__%')
        )
        BEGIN
            RAISERROR ('NIEPOPRAWNY ADRES EMAIL' ,16,1)
        END 
        ELSE    
        BEGIN
            INSERT INTO 
                wlasciciel_adresu_email
            SELECT 
                I.osoba_id, 
                I.email
            FROM 
                INSERTED I
        END    
    END
"""
cursor.execute(email)


osoba = """
    CREATE TRIGGER Tr_INSERT_osoba ON osoba
    INSTEAD OF INSERT
    AS
    BEGIN
        SET NOCOUNT ON;

        IF EXISTS (
            SELECT 
                1
            FROM 
                INSERTED
            WHERE 
                (imie  LIKE '%[0-9]%')
        )
        BEGIN
            RAISERROR ('NIEPOPRAWNE IMIE' ,16,1)
        END 

        IF EXISTS (
            SELECT 
                1
            FROM 
                INSERTED
            WHERE 
                (nazwisko LIKE '%[0-9]%')
        )
        BEGIN
            RAISERROR ('NIEPOPRAWNE NAZWISKO' ,16,1)
        END 


        ELSE    
        BEGIN
            INSERT INTO 
                osoba
            SELECT 
                I.imie, 
                I.nazwisko
            FROM 
                INSERTED I
        END    
    END
"""
cursor.execute(osoba)

plec = """
    CREATE TRIGGER Tr_INSERT_plec ON plec
    INSTEAD OF INSERT
    AS
    BEGIN
        SET NOCOUNT ON;

        IF EXISTS (
            SELECT 
                1
            FROM 
                INSERTED
            WHERE 
                (plec  LIKE '%[0-9]%')
        )
        BEGIN
            RAISERROR ('NIEPOPRAWNA PLEC' ,16,1)
        END 

        ELSE    
        BEGIN
            INSERT INTO 
                plec
            SELECT 
                I.plec
            FROM 
                INSERTED I
        END    
    END
"""
cursor.execute(plec)










cursor.commit()
cursor.close()
conn.close()
