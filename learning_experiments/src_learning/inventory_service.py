import json
from pathlib import Path

MY_LOCATION = Path(__file__).resolve()
MY_BASE_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = MY_LOCATION.parent.parent

FILE_PATH = PROJECT_ROOT / "Data_inventory_test/inventory.json"


def get_inventory():
    if not FILE_PATH.exists():
        return []
    
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        retrieved_data = json.load(f)
        return retrieved_data


def save_inventory(inventory):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=4)


def print_table(item_list):
    print(f"{'ID':<5} {'NAME':<30} {'QUANTITY':>10}   {'SHELF':<10}")
    print("-" * 60)

    for item in item_list:
        print(f"{item['id']:<5} {item['name']:<30} {item['quantity']:>10}   {item['shelf']:<10}")
    
    print("-" * 60)
    print(f"Total: {len(item_list)} products in the database.")
    print("-" * 60)


def new_item(new_name, new_id, new_quantity, new_location):
    inventory = get_inventory()

    item = {
        "id": new_id,
        "name": new_name,
        "quantity": new_quantity,
        "shelf": new_location
    }

    inventory.append(item)
    save_inventory(inventory)


def search_item(keyword):
    inventory = get_inventory()
    found_items = []
    
    keyword = str(keyword).lower()

    for item in inventory:
        name = str(item.get("name", "")).lower()
        if keyword in name:
            found_items.append(item)

    return found_items


def change_stock(item_id, change):
    inventory = get_inventory()
    found = False

    for item in inventory:
        if item["id"] == item_id:
            item["quantity"] += change
            found = True
            break

    if found:
        save_inventory(inventory)
        return True
    else:
        return False


def update_item(old_id, new_id, new_name, new_quantity, new_shelf):
    inventory = get_inventory()
    found = False

    for item in inventory:
        if item["id"] == old_id:
            item["id"] = new_id
            item["name"] = new_name
            item["quantity"] = new_quantity
            item["shelf"] = new_shelf
            found = True
            break

    if found:
        save_inventory(inventory)
        return True
    else:
        return False
