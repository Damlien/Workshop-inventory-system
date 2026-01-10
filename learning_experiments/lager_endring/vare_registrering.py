from pathlib import Path
import json

MIN_PLASSERING = Path(__file__).resolve()
MIN_BASE_DIR = Path(__file__).resolve().parent

PROSJEKT_ROT = MIN_PLASSERING.parent.parent


FIL_STI = PROSJEKT_ROT / "Data_lagring_test/lager.json"

if FIL_STI.exists():
    print(f"Fant datafilen {FIL_STI}")
else:
    print(f"Fant ikke datafilen her: {FIL_STI}")

nytt_navn= input("Hva er navn på ny komponent?")
ny_id = int(input("Hva er id på ny komponent?"))
nytt_antall = int( input("Hva er antall av komponenten?") )
ny_lokasjon =  input("hva er lokasjonen på komponenten?") 



with open(FIL_STI, "r") as f:
    hentet_data =json.load(f)


ny_vare = {
    "id": ny_id,
    "navn": nytt_navn,
    "antall": nytt_antall,
    "hylle": ny_lokasjon
}

hentet_data.append(ny_vare)

with open(FIL_STI, "w") as f:
    json.dump(hentet_data, f, indent=4)