import os
import re

def preberi_datoteko(directory, filename):
    """Funkija prebere html datoteko in vrne vsebino kot niz"""
    path = os.path.join(directory, filename)
    with open(path, "r", encoding="utf-8") as dat:
        return dat.read()
    
def razdeli_na_podjetja(html_vsebina):
    """Funkcija razdeli html datoteko na posamezne bloke podjetij"""
    # Vzorec za eno vrstico tabele (eno podjetje)
    vzorec = r'<tr><td class="fav"><img.*?</span></td></tr>'
    podjetja_bloki = re.findall(vzorec, html_vsebina, re.DOTALL)
    print(f"Najdeno {len(podjetja_bloki)} podjetij v HTML")
    return podjetja_bloki

def poberi_podatke_podjetja(blok, kategorija):
    """Funkcija izlušči podatke iz bloka enega podjetja:
      name, vrednost (različno glede na kategorijo), country."""
    
    # ID (vsako podjetje ima na spletni strani svojo ID številko)
    id_vzorec = r'data-id="([0-9]+)"'
    id_najdi = re.search(id_vzorec, blok)
    id = id_najdi.group(1).strip() if id_najdi else "Ni podatka"

    # NAME (ime podjetja)  
    name_vzorec = r'<div class="company-name">(.*?)</div>'
    name_najdi = re.search(name_vzorec, blok)
    name = name_najdi.group(1).strip() if name_najdi else "Ni podatka"

    # COUNTRY (država podjetja)
    country_vzorec = r'<span class="responsive-hidden">(.*?)</span>'
    country_najdi = re.search(country_vzorec, blok)
    country = country_najdi.group(1).strip() if country_najdi else "Ni podatka"

    # VREDNOST glede na kategorijo
    if kategorija == 'kazalnik_p_e':
        vrednost_vzorec = r'<td class="td-right" data-sort="([0-9.]+)"'
        vrednost_najdi = re.search(vrednost_vzorec, blok)
        vrednost = vrednost_najdi.group(1).strip() if vrednost_najdi else "Ni podatka"
        
    elif kategorija == 'trzna_kap':
        vrednost_vzorec = r'<td class="td-right" data-sort="([0-9.]+)"><span class="currency-symbol-left">€</span>'
        vrednost_najdi = re.search(vrednost_vzorec, blok)
        vrednost = vrednost_najdi.group(1).strip() if vrednost_najdi else "Ni podatka"
        
    elif kategorija == 'st_zaposlenih':
        vrednost_vzorec = r'<td class="td-right" data-sort="([0-9]+)">([0-9,]+)</td>'
        vrednost_najdi = re.search(vrednost_vzorec, blok)
        vrednost = vrednost_najdi.group(1).strip() if vrednost_najdi else "Ni podatka"
        
    elif kategorija == 'dividende':
        vrednost_vzorec = r'</path></svg>([0-9.]+)%</span></td>'
        vrednost_najdi = re.search(vrednost_vzorec, blok, re.DOTALL)
        vrednost = vrednost_najdi.group(1).strip() if vrednost_najdi else "Ni podatka"
        
    elif kategorija == 'prihodek':
        vrednost_vzorec = r'<td class="td-right" data-sort="([0-9.]+)">€'
        vrednost_najdi = re.search(vrednost_vzorec, blok)
        vrednost = vrednost_najdi.group(1).strip() if vrednost_najdi else "Ni podatka"
    
    elif kategorija == 'dobicek':
        vrednost_vzorec = r'<td class="td-right" data-sort="([0-9.]+)">€'
        vrednost_najdi = re.search(vrednost_vzorec, blok)
        vrednost = vrednost_najdi.group(1).strip() if vrednost_najdi else "Ni podatka"
    
    else:
        vrednost = "Neznana kategorija"
    
    # slovar podatkov
    podatki = {
        "id": id,
        "name": name,
        "country": country
    }

    # v slovar dodamo podatek glede na kategorijo
    if kategorija == 'trzna_kap':
        podatki["marketcap"] = vrednost
    elif kategorija == 'prihodek':
        podatki["revenue"] = vrednost
    elif kategorija == 'dobicek':
        podatki["earnings"] = vrednost
    elif kategorija == 'st_zaposlenih':
        podatki["employees"] = vrednost
    elif kategorija == 'dividende':
        podatki["dividends"] = vrednost
    elif kategorija == 'kazalnik_p_e':
        podatki["pe_ratio"] = vrednost
    
    return podatki

def obdelaj_datoteko(kategorija, directory, filename):
    """Funkcija obdela eno HTML datoteko in vrne seznam slovarjev"""

    html_vsebina = preberi_datoteko(directory, filename)
    podjetja_bloki = razdeli_na_podjetja(html_vsebina)
    
    seznam_podjetij = []
    for blok in podjetja_bloki:
        podjetje = poberi_podatke_podjetja(blok, kategorija)
        seznam_podjetij.append(podjetje)
    
    return seznam_podjetij

def obdelaj_kategorijo(kategorija, directory):
    """Funkcija obdela vse strani za eno kategorijo."""
    kategorija_directory = os.path.join(directory, kategorija)
    vsa_podjetja = []
    
    # ali mapa obstaja
    if not os.path.exists(kategorija_directory):
        print(f"Mapa {kategorija_directory} ne obstaja!")
        return []
    
    # Poišči vse datoteke oblike stran_st.html
    datoteke = [f for f in os.listdir(kategorija_directory) if f.startswith('stran_') and f.endswith('.html')]
    datoteke.sort()  # stran_1, stran_2, stran_3...
    
    for datoteka in datoteke:
        podjetja = obdelaj_datoteko(kategorija, kategorija_directory, datoteka)
        vsa_podjetja.extend(podjetja)
    
    return vsa_podjetja

