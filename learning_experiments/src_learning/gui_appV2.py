import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Tools for tabs and modern widgets
from inventory_service import get_inventory, new_item, search_item, change_stock, update_item

# --- MAIN SETUP ---
root = tk.Tk()
root.title("Workshop Inventory Management Pro")
root.geometry("800x600")  # Larger window for a dashboard feel

# Use a Notebook to create tabs
tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

# --- TAB 1: DASHBOARD (Overview + Actions) ---
tab_dashboard = tk.Frame(tabs)
tabs.add(tab_dashboard, text="📦 Inventory Control")

# 1. TOP: SEARCH FIELD
top_frame = tk.Frame(tab_dashboard, bg="#f0f0f0", pady=10)
top_frame.pack(fill="x")

tk.Label(top_frame, text="Search inventory:", bg="#f0f0f0", font=("Arial", 12)).pack(
    side="left", padx=10
)
entry_search = tk.Entry(top_frame, font=("Arial", 12), width=30)
entry_search.pack(side="left", padx=5)

# 2. MIDDLE: TABLE
tree_frame = tk.Frame(tab_dashboard)
tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("id", "name", "quantity", "shelf")
table = ttk.Treeview(tree_frame, columns=columns, show="headings")

# Configure columns
table.heading("id", text="ID")
table.column("id", width=60, anchor="center")
table.heading("name", text="Item name")
table.column("name", width=300, anchor="center")
table.heading("quantity", text="Quantity")
table.column("quantity", width=100, anchor="center")
table.heading("shelf", text="Shelf", anchor="center")
table.column("shelf", width=100, anchor="center")

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=table.yview)
table.configure(yscroll=scrollbar.set)

table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 3. BOTTOM: ACTION PANEL
action_frame = tk.Frame(
    tab_dashboard, bg="#e6e6e6", height=150, bd=1, relief="raised"
)
action_frame.pack(fill="x", side="bottom")

# Heading in the action panel
lbl_action_title = tk.Label(
    action_frame,
    text="Select an item in the list above to make changes",
    bg="#e6e6e6",
    font=("Arial", 10, "italic"),
)
lbl_action_title.pack(pady=10)

# Inputs and buttons
btn_frame = tk.Frame(action_frame, bg="#e6e6e6")
btn_frame.pack(pady=5)

tk.Label(btn_frame, text="Quantity:", bg="#e6e6e6").pack(side="left")
entry_quantity = tk.Entry(btn_frame, width=5, font=("Arial", 12))
entry_quantity.pack(side="left", padx=5)

# --- DASHBOARD LOGIC ---
def update_table(event=None):
    # Clear table
    for row in table.get_children():
        table.delete(row)

    # Search (empty search -> get all)
    text = entry_search.get().lower()
    items = search_item(text)

    for v in items:
        # Color rows with low stock
        tag = "normal"
        if v["quantity"] < 5:
            tag = "low_stock"

        table.insert(
            "",
            "end",
            values=(v["id"], v["name"], v["quantity"], v.get("shelf", "-")),
            tags=(tag,),
        )

# Show red text if little stock remains
table.tag_configure("low_stock", foreground="red")

def perform_transaction(action_type):
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Oops", "Select an item in the list first!")
        return

    item = table.item(selected)
    item_id = item["values"][0]
    name = item["values"][1]

    try:
        qty = int(entry_quantity.get())

        # Withdraw is minus, restock is plus
        if action_type == "withdraw":
            change = qty * -1
            confirmation = f"Withdrew {qty} pcs of {name}"
        else:
            change = qty
            confirmation = f"Restocked {qty} pcs to {name}"

        if change_stock(item_id, change):
            update_table()
            entry_quantity.delete(0, "end")

            lbl_action_title.config(text=f"Success: {confirmation}", fg="green")

            root.after(
                3000,
                lambda: lbl_action_title.config(
                    text="Select an item...", fg="black"
                ),
            )
        else:
            messagebox.showerror("Error", "Could not find the item in the system.")

    except ValueError:
        messagebox.showerror("Error", "Enter a valid number in the quantity field.")

def edit_selected_item():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Oops", "Select an item in the list first!")
        return

    item = table.item(selected)
    values = item["values"]

    old_id = values[0]
    current_name = values[1]
    current_quantity = values[2]
    current_shelf = values[3]

    edit_window = tk.Toplevel(root)
    edit_window.title(f"Edit: {current_name}")
    edit_window.geometry("300x350")

    tk.Label(edit_window, text="Name:").pack(anchor="w", padx=20, pady=(10, 0))
    e_name = tk.Entry(edit_window)
    e_name.pack(fill="x", padx=20)
    e_name.insert(0, current_name)

    tk.Label(edit_window, text="ID:").pack(anchor="w", padx=20, pady=(10, 0))
    e_id = tk.Entry(edit_window)
    e_id.pack(fill="x", padx=20)
    e_id.insert(0, old_id)

    tk.Label(edit_window, text="Quantity:").pack(anchor="w", padx=20, pady=(10, 0))
    e_quantity = tk.Entry(edit_window)
    e_quantity.pack(fill="x", padx=20)
    e_quantity.insert(0, current_quantity)

    tk.Label(edit_window, text="Shelf:").pack(anchor="w", padx=20, pady=(10, 0))
    e_shelf = tk.Entry(edit_window)
    e_shelf.pack(fill="x", padx=20)
    e_shelf.insert(0, current_shelf)

    def save_changes():
        try:
            new_name = e_name.get()
            new_id = int(e_id.get())
            new_quantity = int(e_quantity.get())
            new_shelf = e_shelf.get()

            if update_item(old_id, new_id, new_name, new_quantity, new_shelf):
                messagebox.showinfo("Success", "Item has been updated!")
                edit_window.destroy()
                update_table()
            else:
                messagebox.showerror("Error", "Could not update the item.")
        except ValueError:
            messagebox.showerror("Error", "ID and Quantity must be numbers.")

    tk.Button(
        edit_window,
        text="Save changes",
        command=save_changes,
        bg="#ccffcc",
        height=2,
    ).pack(pady=20, fill="x", padx=20)

# Buttons
btn_withdraw = tk.Button(
    btn_frame,
    text="WITHDRAW",
    bg="#ffcccc",
    width=15,
    command=lambda: perform_transaction("withdraw"),
)
btn_withdraw.pack(side="left", padx=20)

btn_restock = tk.Button(
    btn_frame,
    text="RESTOCK",
    bg="#ccffcc",
    width=15,
    command=lambda: perform_transaction("restock"),
)
btn_restock.pack(side="left", padx=20)

btn_edit = tk.Button(
    btn_frame,
    text="EDIT",
    bg="#ffffcc",
    width=15,
    command=edit_selected_item,
)
btn_edit.pack(side="left", padx=20)

# Bind Enter key to search
entry_search.bind("<Return>", update_table)

# Update label when clicking in table
def on_click(event):
    selected = table.selection()
    if selected:
        item = table.item(selected)
        name = item["values"][1]
        lbl_action_title.config(
            text=f"Selected item: {name} - What would you like to do?",
            fg="blue",
        )

table.bind("<<TreeviewSelect>>", on_click)

# --- TAB 2: REGISTRATION ---
tab_reg = tk.Frame(tabs)
tabs.add(tab_reg, text="New Item")

tk.Label(tab_reg, text="Register new component", font=("Arial", 16)).pack(pady=20)

reg_frame = tk.Frame(tab_reg)
reg_frame.pack()

tk.Label(reg_frame, text="Name:").grid(row=0, column=0, sticky="e", pady=5)
e_name_reg = tk.Entry(reg_frame)
e_name_reg.grid(row=0, column=1, pady=5)

tk.Label(reg_frame, text="ID:").grid(row=1, column=0, sticky="e", pady=5)
e_id_reg = tk.Entry(reg_frame)
e_id_reg.grid(row=1, column=1, pady=5)

tk.Label(reg_frame, text="Quantity:").grid(row=2, column=0, sticky="e", pady=5)
e_quantity_reg = tk.Entry(reg_frame)
e_quantity_reg.grid(row=2, column=1, pady=5)

tk.Label(reg_frame, text="Shelf:").grid(row=3, column=0, sticky="e", pady=5)
e_shelf_reg = tk.Entry(reg_frame)
e_shelf_reg.grid(row=3, column=1, pady=5)

def save_new():
    try:
        new_item(
            e_name_reg.get(),
            int(e_id_reg.get()),
            int(e_quantity_reg.get()),
            e_shelf_reg.get(),
        )
        messagebox.showinfo("Success", "Item saved!")
        e_name_reg.delete(0, "end")
        e_id_reg.delete(0, "end")
        e_quantity_reg.delete(0, "end")
        e_shelf_reg.delete(0, "end")
        update_table()
    except ValueError:
        messagebox.showerror("Error", "Check that ID and Quantity are numbers.")

tk.Button(tab_reg, text="Save Item", bg="#ccffcc", command=save_new).pack(pady=20)

# --- START ---
update_table()
root.mainloop()
