from inventory_service import get_inventory, save_inventory, print_table, new_item, search_item, change_stock

def main_menu():
    print("\n" + "=" * 30)
    print("  INVENTORY MANAGEMENT V1.0  ")
    print("=" * 30)

    while True:
        print("\n--- Main Menu ---")
        print("1. View overview")
        print("2. Withdraw component")
        print("3. Restock component")
        print("4. Register new item")
        print("5. Exit")

        choice = input("What would you like to do? ")

        if choice == "1":
            print_table(get_inventory())

        elif choice == "2":
            print("\n --Withdraw item--")
            search_word = input("Which component do you want to withdraw? ").lower()
            
            results = search_item(search_word)

            if len(results) == 0:
                print("No results found")
            else:
                print(f"Found {len(results)} result(s)")
                print_table(results)

                try:
                    item_id = int(input("Enter the ID of the item you want to withdraw: "))
                    change = int(input("How many would you like to withdraw? "))

                    withdrawal_amount = change * (-1)

                    if change_stock(item_id, withdrawal_amount):
                        print("Inventory updated")
                    else:
                        print("ID not found. Cancelled.")
                except ValueError:
                    print("Invalid value")

        elif choice == "3":
            print("\n --Restock item--")
            
            search_word = input("Which component do you want to restock? ").lower()
            
            results = search_item(search_word)

            if len(results) == 0:
                print("No results found")
            else:
                print(f"Found {len(results)} result(s)")
                print_table(results)

                try:
                    item_id = int(input("Enter the ID of the item to restock: "))
                    change = int(input("How many are you adding? "))

                    restock_amount = change

                    if change_stock(item_id, restock_amount):
                        print("Inventory updated")
                    else:
                        print("ID not found. Cancelled.")
                except ValueError:
                    print("Invalid value")

        elif choice == "4":
            print("\n --New Item--")

            new_name = input("What is the name of the new component? ")
            new_id = int(input("What is the ID of the new component? "))
            new_quantity = int(input("What is the quantity of the component? "))
            new_location = input("What is the location of the component? ")

            new_item(new_name, new_id, new_quantity, new_location)
            print("Saved")

        elif choice == "5":
            break


main_menu()
