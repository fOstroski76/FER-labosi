#!/bin/bash

# define the input arguments for each run

echo "[BASH] Pokrećem PasswordManager testove..."
echo "[BASH] Test 1 - pokretanje programa i spremanje/prikaz lozinke: "



args1="start"
args2="init MaStErPasS"
args3="put MaStErPasS www.adresa.hr N3kaSifra"
args4="get MaStErPasS www.adresa.hr"



# loop through each set of arguments and run the program
for args in "$args1" "$args2" ; do
    python3 PasswordManager.py $args
done

echo " "
echo " "
echo " "
echo " "
echo "[BASH] Kreiram master password : MaStErPasS"
echo "[BASH] Kreiram par adresa-lozinka: www.adresa.hr - N3kaSifra "

for args in  "$args3" "$args4"; do
    python3 PasswordManager.py $args
done

echo " "
echo " "
echo " "
echo " "
echo "[BASH] Test 2 - izmjena postojeće lozinke + dodavanje novog para"
echo " "
echo "[BASH] Kreiram par adresa-lozinka: www.sunce.hr - Ljeto "



args5="put MaStErPasS www.sunce.hr Ljeto"
args6="get MaStErPasS www.sunce.hr"
args7="put MaStErPasS www.sunce.hr Zima"
args8="get MaStErPasS www.sunce.hr"

for args in "$args5" "$args6" ; do
    python3 PasswordManager.py $args
done

echo " "
echo " "
echo " "
echo " "
echo "[BASH] Mijenjam lozinku od www.sunce.hr na Zima"

for args in "$args7" "$args8" ; do
    python3 PasswordManager.py $args
done

echo " "
echo " "
echo " "
echo " "
echo "[BASH] Test 3 - pokušaj >put< i >get< naredbe sa krivim master passwordom"
echo " "
echo "[BASH] Krivi master password će biti: kriviMasterPass"
echo "[BASH] Pokušavam: put kriviMasterPass www.fer.hr faks123"

args9="put kriviMasterPass www.fer.hr faks123"
args10="get kriviMasterPass www.adresa.hr"

for args in "$args9"; do
    python3 PasswordManager.py $args
done


echo " "
echo " "
echo " "
echo " "
echo "[BASH] Pokušavam: get kriviMasterPass www.adresa.hr"

for args in "$args10"; do
    python3 PasswordManager.py $args
done

echo " "
echo " "
echo " "
echo " "
echo "[BASH] Test 3 - Unos neispravnih inputa - program dojavljuje neispravni input"
echo " "
echo "[BASH] Pokušavam: init MaStErPasS www.adresa_nesmije_biti_u_naredbi.hr "

args11="init MaStErPasS www.adresa_nesmije_biti_u_naredbi.hr"

for args in "$args11"; do
    python3 PasswordManager.py $args
done

echo " "
echo "[BASH] Pokušavam: get MaStErPasS www.adresa_koju_zelim.hr neocekivana_sifra ovdje "

args12="get MaStErPasS www.adresa_koju_zelim.hr neocekivana_sifra ovdje"

for args in "$args12"; do
    python3 PasswordManager.py $args
done

echo " "
echo "[BASH] Pokušavam: start get init put help potpuno_kriva_naredba"

args13="start get init put help potpuno_kriva_naredba"

for args in "$args13"; do
    python3 PasswordManager.py $args
done