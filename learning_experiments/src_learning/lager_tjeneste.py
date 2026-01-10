import json
from pathlib import Path

MIN_PLASSERING = Path(__file__).resolve()
MIN_BASE_DIR = Path(__file__).resolve().parent

PROSJEKT_ROT = MIN_PLASSERING.parent.parent

FIL_STI = PROSJEKT_ROT / "Data_lagring_test/lager.json" 


def hent_lager():
    
    if not FIL_STI.exists():
        return []
    
    with open(FIL_STI, "r", encoding="utf-8") as f:
        hentet_data = json.load(f)
        return hentet_data
    
def lagre_lager(lager):
    with open(FIL_STI, "w", encoding="utf-8") as f:
        json.dump(lager, f, indent=4)

def print_tabell(vareliste):
    print(f"{'ID':<5} {'NAVN':<30} {'ANTALL':>10}   {'HYLLE':<10}")
    print("-" * 60)

    for vare in vareliste:
        print(f"{vare['id']:<5} {vare['navn']:<30} {vare['antall']:>10}   {vare['hylle']:<10}")
    
    print("-" * 60)
    print(f"Totalt: {len(vareliste)} produkter i databasen.")
    print("-" * 60)

def ny_vare(nytt_navn, ny_id, nytt_antall, ny_lokasjon):

    liste = hent_lager()


    ny_vare = {
        "id": ny_id,
        "navn": nytt_navn,
        "antall": nytt_antall,
        "hylle": ny_lokasjon
    }

    liste.append(ny_vare)

    lagre_lager(liste)


def søk_vare(søkeord):
    liste = hent_lager()
    funnet_vare = []
    
    søkeord = str(søkeord).lower()

    for vare in liste:
        navn = str(vare.get("navn", "")).lower()
        
        if søkeord in navn:
            funnet_vare.append(vare)

    return funnet_vare


def endre_beholdning(vare_id, endring):
    liste = hent_lager()

    funnet = False

    for vare in liste:
        if vare["id"] == vare_id:
            vare["antall"] += endring
            funnet = True
            break

    if funnet:
        lagre_lager(liste)  
        return True
    else:
        return False
    

def oppdater_vare(gammel_id,ny_id, nytt_navn, nytt_antall, ny_hylle):

    liste = hent_lager()

    funnet = False  

    for vare in liste:
        if vare["id"] == gammel_id:
            vare["id"] = ny_id
            vare["navn"] = nytt_navn
            vare["antall"] = nytt_antall
            vare["hylle"] = ny_hylle
            funnet = True
            break

    if funnet:
        lagre_lager(liste)
        return True
    else:
        return False