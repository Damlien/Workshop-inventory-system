import json
from pathlib import Path

MIN_PLASSERING = Path(__file__).resolve()
MIN_BASE_DIR = Path(__file__).resolve().parent

PROSJEKT_ROT = MIN_PLASSERING.parent.parent


FIL_STI = PROSJEKT_ROT / "Data_lagring_test/lager.json" 

if FIL_STI.exists():
    print(f"Fant datafilen {FIL_STI}")
else:
    print(f"Fant ikke datafilen her: {FIL_STI}")

with open(FIL_STI, "r") as f:
    hentet_data = json.load(f)
    #print(hentet_data)
    print("\n --------------------------------------------------------------- \n")
    sokeord = input("Hvilken komponent skal du ha?").lower()
    
    for i in hentet_data:

        if sokeord in i["navn"].lower():
            print("-" * 50)
            print(f"FUNNET VARE: {i['navn']}") 
            print("-" * 50)
            print(f"Lagerbeholdning : {i['antall']} stykker")
            print(f"Lokasjon        : Hylle {i['hyll']}")
            print("-" * 50)
            print("") 