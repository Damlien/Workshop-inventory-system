from pathlib import Path
import json

MY_LOCATION = Path(__file__).resolve()
MY_BASE_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = MY_LOCATION.parent.parent

FILE_PATH = PROJECT_ROOT / "Data_inventory_test/inventory.json"

if FILE_PATH.exists():
    print(f"Found the data file {FILE_PATH}")
else:
    print(f"Data file not found here: {FILE_PATH}")

new_id = int(input("What is the ID of the new component? "))
new_name = input("What is the name of the new component? ")
new_quantity = int(input("What is the quantity of the component? "))
new_location = input("What is the location of the component? ")

with open(FILE_PATH, "r") as f:
    retrieved_data = json.load(f)

new_item = {
    "id": new_id,
    "name": new_name,
    "quantity": new_quantity,
    "shelf": new_location
}

retrieved_data.append(new_item)

with open(FILE_PATH, "w") as f:
    json.dump(retrieved_data, f, indent=4)
