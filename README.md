Popis Projektu:
 - projekt slouží k extrahovaní výsledku voleb pro rok 2017. 
 - Z Odkazu https: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8102
 - Odkaz na Okres Frýdek-Místek. 

Knihovny:
- Knihovny použité v kodu jsou přiloženy v souboru requirements.txt. 
- Knihovny je dobré nainstalovat do nově vytvořeného virtualního prostředí. 
- Ve virtualním prostředí stačí pak do terminalu napsat pip3 install -r requirements.txt a knihovny se nainstalují. 

Spuštění projektu:
- Projekt se spouští pomocí 2 argumentů. První je url požadované stranky obce, druhý jmeno csv souboru do kterého chceme vysledky uložit.
- V našem případě arg1: "//volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8102"
		  arg2: "Vysledky_FM.csv"

- Tyto 2 argumenty stačí zapsat do konzole, spustit a počkat na vztvoření vysledného csv.
- Příklad zapisu argumentu do konzole: python Project_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8102" , "Vysledky_FM.csv"
