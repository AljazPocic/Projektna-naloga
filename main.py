import zajem
import obdelava
import shrani

# Program zajame podatke, jih obdela in ustvari 7 CSV datotek. Najbolj pomembna je vse_kategorije.csv

def main():
    print("Zajem spletne strani")
    for kategorija in zajem.podjetja_urls:
        zajem.zajemi_vse_strani_kategorije(kategorija, max_strani=100)
    print("Zajem je končan!")

    print("Obdelava podatkov in shranjevanje v CSV")
    shrani.shrani_vse_kategorije('podatki') #obdelva je že vlkjučena v shrani.py
    shrani.zdruzi_vse_kategorije('podatki')
    print("Obdelva in shranjevannje je končano!")

if __name__ == "__main__":
    main()