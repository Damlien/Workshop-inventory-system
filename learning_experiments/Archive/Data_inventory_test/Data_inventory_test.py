import json
from pathlib import Path

components = [  # format {"id": , "name": , "quantity": , "shelf": }
    {"id": 1, "name": "resistor 10kΩ", "quantity": 100, "shelf": "1"},
    {"id": 2, "name": "Arduino Nano", "quantity": 8, "shelf": "2"},
    {"id": 3, "name": "capacitor", "quantity": 20, "shelf": "3"},
    {"id": 4, "name": "nmos", "quantity": 20, "shelf": "4"}
]

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "inventory.json"

# Write the data to a JSON file
with open(FILE_PATH, "w") as f:
    json.dump(components, f, indent=4)

# Read the data back from the file
with open(FILE_PATH, "r") as f:
    retrieved_data = json.load(f)
    print(retrieved_data)
