import os
import requests 

# URL-ji spletne strani za različne podatke 
podjetja_urls = {
    'trzna_kap': "https://companiesmarketcap.com/eur/",
    'prihodek': "https://companiesmarketcap.com/eur/largest-companies-by-revenue/",
    'dobicek': "https://companiesmarketcap.com/eur/most-profitable-companies/",
    'st_zaposlenih': "https://companiesmarketcap.com/eur/largest-companies-by-number-of-employees/",
    'dividende': "https://companiesmarketcap.com/eur/top-companies-by-dividend-yield/",
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

def zajemi_kategorijo(kategorija):
    """Funkcija zajeme podatke za določeno kategorijo in shrani HTML"""
    if kategorija not in podjetja_urls:
        print(f"Nepoznana kategorija: {kategorija}")
        return False
    
    url = podjetja_urls[kategorija]
    filename = f"{kategorija}.html"
    
    # Ustvari podmapo za kategorijo
    kategorija_directory = os.path.join(podjetja_directory, kategorija)
    
    print(f"Zajemam podatke za kategorijo '{kategorija}'...")
    
    return shrani_spletno_stran(url, kategorija_directory, filename)

def zajemi_vse_kategorije():
    """Funakcija zajemi podatke iz vseh kategorij in za vsako pokliče zajemi_kategorijo()"""

    uspesne_kategorije = []
    for kategorija in podjetja_urls:
        if zajemi_kategorijo(kategorija):
            uspesne_kategorije.append(kategorija)
        else:
            print(f"Napaka pri zajemanju kategorije: {kategorija}")
    
    print(f"Uspešno zajete kategorije: {uspesne_kategorije}")
    return uspesne_kategorije

def zajemi_vse_strani_kategorije(kategorija, max_strani=None):
    """Ker so podatki za določeno kategorijo navedeni na večih zaporednih stranaj,
    nam funkcija zajeme vse strani za določeno kategorijo"""
    if kategorija not in podjetja_urls:
        print(f"Nepoznana kategorija: {kategorija}")
        return False
    
    base_url = podjetja_urls[kategorija]
    uspesne_strani = []
    stran = 1  # začnemo na prvi strani
    
    # Ustvari podmapo za kategorijo
    kategorija_directory = os.path.join(podjetja_directory, kategorija)
    
    while True:
        # URL za trenutno stran
        if stran == 1:
            url = base_url
        else:
            url = f"{base_url}page/{stran}/"
        
        filename = f"stran_{stran}.html"
        
        print(f"Zajemam stran {stran} za kategorijo '{kategorija}'...")
        
        # Proba zajeti stran
        if shrani_spletno_stran(url, kategorija_directory, filename):
            uspesne_strani.append(stran)
            stran += 1
            
            #Nočemo, da nas strežnik blokira, zato dodamo povze med zahtevami
            import time 
            time.sleep(1)
            
            if max_strani and stran > max_strani:
                break
        else:
            print(f"Stran {stran} ne obstaja. Zajem za kategorijo '{kategorija}' je končan.")
            break
    
    print(f"Za kategorijo '{kategorija}' uspešno zajeto {len(uspesne_strani)} strani")
    return uspesne_strani

# Test
if __name__ == "__main__":
    # Testiraj z eno kategorijo
    print("Testiram zajem ene kategorije...")
    zajemi_kategorijo('trzna_kap')
    
    # Testiraj z vsemi kategorijami (pozor: traja nekaj časa!)
    # print("Testiram zajem vseh kategorij...")
    # zajemi_vse_kategorije()

    # Testiraj prvih 5 strani za vse kategorije
    print("\nTestiram zajem prvih 5 strani za vse kategorije...")
    for kategorija in podjetja_urls:
        print(f"\n--- Zajemam kategorijo: {kategorija} ---")
        zajemi_vse_strani_kategorije(kategorija, max_strani=5)
    
    print("\n=== ZAJEM KONČAN ===")
    print("Zajeto je bilo 5 strani × 6 kategorij = 30 strani")
    print("To predstavlja približno 500 podjetij × 6 kategorij = 3000 podatkov")
    
    # Testiraj z vsemi kategorijami in vsemi stranmi (POZOR: TRAJA DOLGO!)
    # print("Testiram zajem vseh strani za vse kategorije...")
    # for kategorija in podjetja_urls:
    #     zajemi_vse_strani_kategorije(kategorija)  # Brez max_strani = vse strani
