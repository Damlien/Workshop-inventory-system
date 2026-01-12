import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from inventory_service import get_inventory, new_item, search_item, change_stock  # [web:5]

# --- 1. MAIN WINDOW SETUP ---
root = tk.Tk()
root.title("Inventory Management v1.0")
root.geometry("600x500")  # Slightly larger window now [web:5]

# Create a container (frame) that will hold the content.
# This is what is changed when switching "pages".
content_frame = tk.Frame(root)
content_frame.pack(fill="both", expand=True, padx=20, pady=20)  # [web:5]


# --- 2. HELPER FUNCTION TO SWITCH PAGES ---
def switch_content(new_function):
    """
    Deletes everything currently in the window and calls the new function
    to draw the new content.
    """
    for widget in content_frame.winfo_children():
        widget.destroy()
    new_function()  # [web:1]


# --- 3. PAGE: MAIN MENU ---
def show_menu():
    label = tk.Label(content_frame, text="Main Menu", font=("Arial", 20, "bold"))
    label.pack(pady=20)

    btn1 = tk.Button(
        content_frame,
        text="1. Show overview",
        command=lambda: switch_content(show_overview_page),
        height=2,
    )
    btn1.pack(fill="x", pady=5)

    btn2 = tk.Button(
        content_frame,
        text="2. Withdraw item",
        height=2,
        command=lambda: switch_content(lambda: show_transaction_page("withdraw")),
    )
    btn2.pack(fill="x", pady=5)

    btn3 = tk.Button(
        content_frame,
        text="3. Restock item",
        height=2,
        command=lambda: switch_content(lambda: show_transaction_page("restock")),
    )
    btn3.pack(fill="x", pady=5)

    btn4 = tk.Button(
        content_frame,
        text="4. Register new item",
        height=2,
        command=lambda: switch_content(show_registration_page),
    )
    btn4.pack(fill="x", pady=5)

    separator = tk.Frame(content_frame, height=2, bd=1, relief="sunken")
    separator.pack(fill="x", pady=20)

    btn5 = tk.Button(content_frame, text="Exit", command=root.destroy, bg="#ffcccc")
    btn5.pack(pady=5)


# --- 4. PAGE: OVERVIEW (TABLE) ---
def show_overview_page():
    tk.Label(content_frame, text="Inventory", font=("Arial", 16)).pack(pady=10)

    columns = ("id", "name", "quantity", "shelf")
    table = ttk.Treeview(content_frame, columns=columns, show="headings", height=15)

    table.heading("id", text="ID")
    table.heading("name", text="Name")
    table.heading("quantity", text="Quantity")
    table.heading("shelf", text="Shelf")

    table.column("id", width=50, anchor="center")
    table.column("name", width=200)
    table.column("quantity", width=80, anchor="center")
    table.column("shelf", width=80)

    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=table.yview)
    table.configure(yscroll=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    table.pack(fill="both", expand=True)

    items = get_inventory()
    for item in items:
        table.insert(
            "",
            tk.END,
            values=(
                item.get("id"),
                item.get("name"),
                item.get("quantity"),
                item.get("shelf"),
            ),
        )

    btn_back = tk.Button(
        content_frame,
        text="⬅ Back to menu",
        command=lambda: switch_content(show_menu),
    )
    btn_back.pack(pady=15)


# --- 5. PAGE: REGISTER NEW ITEM ---
def show_registration_page():
    tk.Label(content_frame, text="Register New Item", font=("Arial", 16)).pack(pady=10)

    tk.Label(content_frame, text="Name:").pack(anchor="w", padx=100)
    entry_name = tk.Entry(content_frame)
    entry_name.pack(fill="x", padx=100)

    tk.Label(content_frame, text="ID (Number):").pack(anchor="w", padx=100)
    entry_id = tk.Entry(content_frame)
    entry_id.pack(fill="x", padx=100)

    tk.Label(content_frame, text="Quantity (Number):").pack(anchor="w", padx=100)
    entry_quantity = tk.Entry(content_frame)
    entry_quantity.pack(fill="x", padx=100)

    tk.Label(content_frame, text="Shelf location:").pack(anchor="w", padx=100)
    entry_shelf = tk.Entry(content_frame)
    entry_shelf.pack(fill="x", padx=100)

    def validate_and_save():
        name = entry_name.get()
        id_text = entry_id.get()
        quantity_text = entry_quantity.get()
        shelf = entry_shelf.get()

        if not name or not id_text or not quantity_text:
            messagebox.showwarning(
                "Missing info", "You must fill in name, ID and quantity!"
            )
            return

        try:
            item_id = int(id_text)
            quantity = int(quantity_text)

            new_item(name, item_id, quantity, shelf)
            messagebox.showinfo("Success", f"{name} has been saved!")

            entry_name.delete(0, tk.END)
            entry_id.delete(0, tk.END)
            entry_quantity.delete(0, tk.END)
            entry_shelf.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "ID and Quantity must be integers!")

    btn_save = tk.Button(
        content_frame,
        text="💾 Save item",
        command=validate_and_save,
        bg="#ccffcc",
        height=2,
    )
    btn_save.pack(pady=20, fill="x", padx=100)

    btn_back = tk.Button(
        content_frame,
        text="⬅ Back to menu",
        command=lambda: switch_content(show_menu),
    )
    btn_back.pack(pady=5)


# --- 6. PAGE: TRANSACTION (WITHDRAW / RESTOCK) ---
def show_transaction_page(mode):
    title = "Withdraw item" if mode == "withdraw" else "Restock item"
    color = "#ffcccc" if mode == "withdraw" else "#ccffcc"

    tk.Label(content_frame, text=title, font=("Arial", 16)).pack(pady=10)

    search_frame = tk.Frame(content_frame)
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="Search: ").pack(side="left")
    entry_search = tk.Entry(search_frame)
    entry_search.pack(side="left", padx=5)

    columns = ("id", "name", "quantity", "shelf")
    table = ttk.Treeview(content_frame, columns=columns, show="headings", height=8)

    for col in columns:
        table.heading(col, text=col.capitalize())
        table.column(col, width=80)
    table.column("name", width=150)

    table.pack(pady=10)

    def run_search(event=None):
        for row in table.get_children():
            table.delete(row)

        text = entry_search.get().lower()
        results = search_item(text)

        for item in results:
            table.insert(
                "",
                tk.END,
                values=(
                    item["id"],
                    item["name"],
                    item["quantity"],
                    item.get("shelf", "-"),
                ),
            )

    btn_search = tk.Button(search_frame, text="🔍 Search", command=run_search)
    btn_search.pack(side="left")

    entry_search.bind("<Return>", run_search)

    action_frame = tk.Frame(content_frame)
    action_frame.pack(pady=20)

    tk.Label(action_frame, text="Quantity:").pack(side="left")
    entry_amount = tk.Entry(action_frame, width=5)
    entry_amount.pack(side="left", padx=5)

    def perform_action():
        selected_item = table.selection()
        if not selected_item:
            messagebox.showwarning(
                "Oops", "You must click an item in the list above!"
            )
            return

        values = table.item(selected_item)["values"]
        selected_id = values[0]
        selected_name = values[1]

        try:
            amount = int(entry_amount.get())
            change = amount * -1 if mode == "withdraw" else amount

            if change_stock(selected_id, change):
                messagebox.showinfo("Success", f"Updated {selected_name}!")
                run_search()
                entry_amount.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Something went wrong while saving.")

        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number!")

    btn_execute = tk.Button(
        action_frame, text="Execute", command=perform_action, bg=color
    )
    btn_execute.pack(side="left", padx=10)

    tk.Button(
        content_frame,
        text="Back",
        command=lambda: switch_content(show_menu),
    ).pack(side="bottom", pady=10)

    # Run an initial search with empty text so the table shows all items at start.
    run_search()


# --- START APP ---
show_menu()
root.mainloop()
 