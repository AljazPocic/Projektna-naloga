import csv
import os
import obdelava
import pandas as pd

def zapisi_csv(fieldnames, rows, directory, filename):
    """Funkcija v CSV datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None

def shrani_podjetja_csv(podjetja, directory, filename):
    """Funkcija shrani podatke o podjetjih v CSV. Funkcija predpostavi,
    da so ključi vseh slovarjev parametra podjetja enaki in da je seznam podjetja neprazen"""
    assert podjetja and (all(p.keys() == podjetja[0].keys() for p in podjetja))
    
    fieldnames = list(podjetja[0].keys())
    zapisi_csv(fieldnames, podjetja, directory, filename)
    print(f"Shranjeno {len(podjetja)} podjetij")

def shrani_kategorijo_csv(kategorija, directory):
    """Funkcija obdela in shrani podatke ene kategorije v svojo CSV datoteko"""
    podjetja = obdelava.obdelaj_kategorijo(kategorija, directory)
    if not podjetja:
        print(f"Ni podatkov za kategorijo '{kategorija}'")
        return
    filename = f"{kategorija}.csv"
    shrani_podjetja_csv(podjetja, directory, filename)

def shrani_vse_kategorije(directory):
    """Funkcija shrani podatke vseh kategorij v posamezne CSV datoteke"""
    kategorije = ['trzna_kap', 'prihodek', 'dobicek', 'st_zaposlenih', 'dividende', 'kazalnik_p_e']
    for kategorija in kategorije:
        shrani_kategorijo_csv(kategorija, directory)
    print("Vse kategorije so bile shranjene v CSV datoteke")

def zdruzi_vse_kategorije(directory, izhodni_filename='vse_kategorije.csv'):
    """Funkcija združi vse kategorije v eno CSV datoteko po id, name, country.
    Če kateremu podjetju manjka podatek neke kategorija se mu tam zapiše NaN"""
    # imena vseh CSV datotek
    kategorije = ['trzna_kap', 'prihodek', 'dobicek', 'st_zaposlenih', 'dividende', 'kazalnik_p_e']
    dfs = []    #dsf kot DataFrames
    for kategorija in kategorije:
        path = os.path.join(directory, f"{kategorija}.csv")
        dfs.append(pd.read_csv(path))
    # združimo po id, name, country
    vsi_df = dfs[0]
    for df in dfs[1:]:
        vsi_df = vsi_df.merge(df, on=['id', 'name', 'country'], how='outer') # how='outer' ohrani vsa podjetja iz vseh kategorij

    izhod_path = os.path.join(directory, izhodni_filename)
    vsi_df.to_csv(izhod_path, index=False)

