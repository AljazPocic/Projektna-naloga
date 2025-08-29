# Finančna analiza največjih podjetij na svetu

Za projektno nalogo pri predmetu _Uvod v programiranje_ sem si izbral finančno analizo največjih podjetij, ki so navedena na spletni strani [companiesmarketcap.com/eur](https://companiesmarketcap.com/eur/). Spletna stran vsebuje podatke o več kot 10000 podjetjih in njihovi tržni kapitalizaciji, dobičku, prihodku, kazalniku P/E, številu zaposlenih...
Vključena so le podjetja, ki so delniške družbe, torej tista podjetja, katerih delnice kotirajo na borzi. Zasebna podjetja niso vključena.
Za lažje razumevanje bodo finančni podatki izraženi v evrih. Privzeta valuat spletne strani je namreč ameriški dolar. 

## Kaj bom analiziral

- Največja podjetja po tržni kapitalizaciji
- Podjetja z največjim prihodkom
- Povezavo med številom zaposlenih in prihodkom
- Podjetja z najvišjim kazalnikom P/E
- Povezavo med tržno kapitalizacijo in dividendami
- Delež podjetij po državah

## Navodila za uporabo

Uporabnik programa mora odpret dokument `analiza_podjetji.ipynb`. Tam so v Jupyter Notebook-u analizirani podatki.

Po želji lahko uporabnik požene main.py, ki zajame podatke, jih obdela in shrani v CSV datoteke.

Uporabljene knjižnice: os, re, requests, csv, pandas, matplotlib.