import os
import requests 
import re

# URL-ji spletne strani za različne podatke 
podjetja_urls = {
    'trzna_kap': "https://companiesmarketcap.com/eur/",
    'prihodek': "https://companiesmarketcap.com/eur/by-revenue/",
    'dobicek': "https://companiesmarketcap.com/eur/most-profitable-companies/",
    'st_zaposlenih': "https://companiesmarketcap.com/eur/by-employees/",
    'dividende': "https://companiesmarketcap.com/eur/by-dividend-yield/",
    'kazalnik_p_e': "https://companiesmarketcap.com/eur/top-companies-by-pe-ratio/"
}
# mapa, v katero bomo shranili podatke
podjetja_directory = 'podatki'
# ime CSV datoteke za shranjevanje podatkov
csv_filename = 'podjetja.csv'

def pridobi_html(url):
    """Funkcija kot argument sprejme niz in poskusi vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        page_content =  response.text
    except requests.RequestException as e:
        print(f"Napaka pri pridobivanju podatkov z {url}: {e}")
        return None
    return page_content

def besedilo_v_datoteko(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)  # Da se ustvari mapa, če ne obstaja
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def shrani_spletno_stran(url, directory, filename):
    """S pomočjo prejšnjih dveh funkcij, funkcija shrani vsebino spletne strani
    iz "url" v datoteko "filename" v direktoriju "directory"."""
    html_vsebina = pridobi_html(url)
    if html_vsebina is not None:
        besedilo_v_datoteko(html_vsebina, directory, filename)
        print(f"Stran je shranjena v {directory}/{filename}")
        return True
    else:
        print(f"Napaka: Ni bilo mogoče prenesti strani {url}")
        return False
