from pathlib import Path

jeg_er_her = Path(__file__)

print(jeg_er_her)

full_sti = jeg_er_her.resolve()

print(full_sti)

mappen_min =full_sti.parent

print(mappen_min)


ny_sti =mappen_min /("lager.json")

print(ny_sti)

if ny_sti.exists():
    print("Fant den!")