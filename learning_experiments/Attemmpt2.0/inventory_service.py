import json
from pathlib import Path
import requests 

MY_BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = MY_BASE_DIR / "inventory.json" # Assumes json is in the same folder
DISCORD_URL_FILE = MY_BASE_DIR / "discord_webhook_url.env"


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


def new_item(new_name, new_id, new_quantity, new_location, image=None): 
    inventory = get_inventory()
    item = {
        "id": new_id,
        "name": new_name,
        "quantity": new_quantity,
        "shelf": new_location,
        "image": image 
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

            if change < 0 and item["quantity"] < 3:
                send_discord_alerts(item["name"], item["quantity"])


            found = True
            break

    if found:
        save_inventory(inventory)
        return True
    else:
        return False


def update_item(old_id, new_id, new_name, new_quantity, new_shelf, image=None):
    inventory = get_inventory()
    found = False
    for item in inventory:
        if item["id"] == old_id:
            item["id"] = new_id
            item["name"] = new_name
            item["quantity"] = new_quantity
            item["shelf"] = new_shelf
            if image: # Only update image if a new one was provided
                item["image"] = image
            found = True
            break
    if found:
        save_inventory(inventory)
        return True
    return False


#Function for sending message to discord when there is low number of componetns in storage
def send_discord_alerts(product_name, quantity):

    if not DISCORD_URL_FILE.exists():
        print("Discord webhook URL file not found.")
        return

    with open(DISCORD_URL_FILE, "r") as f:
        file_content = f.read()

        try:
            parts = file_content.split("=")
            discord_url = parts[1].strip()
        
            msg_notification = {"content": f"Remaining number of {product_name} is {quantity}!"}
            requests.post(discord_url, json=msg_notification)
            print("Discord notification sent successfully.")
        except IndexError:
            print("Invalid Discord webhook URL format in the file discord_webhook_url.env")

        