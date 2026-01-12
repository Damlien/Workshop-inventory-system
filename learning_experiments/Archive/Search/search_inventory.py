import json
from pathlib import Path

MY_LOCATION = Path(__file__).resolve()
MY_BASE_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = MY_LOCATION.parent.parent

FILE_PATH = PROJECT_ROOT / "Data_inventory_test/inventory.json"

if FILE_PATH.exists():
    print(f"Found the data file {FILE_PATH}")
else:
    print(f"Data file not found here: {FILE_PATH}")

with open(FILE_PATH, "r") as f:
    retrieved_data = json.load(f)
    # print(retrieved_data)
    print("\n --------------------------------------------------------------- \n")
    search_word = input("Which component are you looking for? ").lower()
    
    for item in retrieved_data:

        if search_word in item["name"].lower():
            print("-" * 50)
            print(f"FOUND ITEM: {item['name']}")
            print("-" * 50)
            print(f"Stock quantity : {item['quantity']} pieces")
            print(f"Location       : Shelf {item['shelf']}")
            print("-" * 50)
            print("")
