#!/bin/bash 


# docker run -e "ACCEPT_EULA=Y" --platform linux/amd64 -e "SA_PASSWORD=citqus-viVcy6-najcyq" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-latest;
#   chmod +x start.sh
#   ./start.sh


source $PWD/venv/bin/activate


python3 $PWD/baza_danych/1createTables.py;
python3 $PWD/baza_danych/2create_dodaj.py;
python3 $PWD/baza_danych/3create_wyswietl.py;
python3 $PWD/baza_danych/4create_triggers.py;
python3 $PWD/baza_danych/1exec_dodaj.py;

export FLASK_APP=$PWD/app/wyswietl_filmy.py
export FLASK_DEBUG=1
python3 -m flask run


deactivate

