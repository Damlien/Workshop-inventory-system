import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from inventory_service import get_inventory, new_item, search_item, change_stock, update_item


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Hide main window while logging in

        # --- STEP 1: LOGIN (Who are you?) ---
        self.is_admin = False
        if not self.show_login_screen():
            root.destroy()  # Exit if user cancels/closes
            return

        # If we get here, login succeeded – show main window.
        self.root.deiconify()
        self.root.title(
            f"Inventory Management Modern - "
            f"{'ADMINISTRATOR' if self.is_admin else 'Store Worker'}"
        )
        self.root.geometry("1000x600")

        # Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

        # Split view
        self.split_view = tk.PanedWindow(
            root, orient="horizontal", sashrelief="ridge", sashwidth=4
        )
        self.split_view.pack(fill="both", expand=True)

        # --- LEFT SIDE ---
        self.frame_list = tk.Frame(self.split_view, bg="#f0f0f0")
        self.split_view.add(self.frame_list, minsize=400)

        # Search
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.run_auto_search)

        lbl_search = tk.Label(
            self.frame_list,
            text="Search inventory:",
            bg="#f0f0f0",
            font=("Segoe UI", 10),
        )
        lbl_search.pack(pady=(10, 0), padx=10, anchor="w")

        entry_search = ttk.Entry(self.frame_list, textvariable=self.search_var)
        entry_search.pack(fill="x", padx=10, pady=5)

        # Table
        columns = ("id", "name", "quantity", "shelf")
        self.tree = ttk.Treeview(
            self.frame_list, columns=columns, show="headings", selectmode="browse"
        )

        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, anchor="center")

        self.tree.heading("name", text="Item name")
        self.tree.column("name", width=200)

        self.tree.heading("quantity", text="#")
        self.tree.column("quantity", width=50, anchor="center")

        # New column
        self.tree.heading("shelf", text="Location")
        self.tree.column("shelf", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.show_details)

        # --- SECURITY CHECK 1: Only admin sees “New Item” button ---
        if self.is_admin:
            btn_new = ttk.Button(
                self.frame_list,
                text="+ Register New Item",
                command=self.show_new_item_form,
            )
            btn_new.pack(fill="x", padx=10, pady=10)
        else:
            lbl_info = tk.Label(
                self.frame_list,
                text=(
                    "You are logged in as a regular user.\n"
                    "Contact an admin to create new items."
                ),
                bg="#f0f0f0",
                fg="gray",
            )
            lbl_info.pack(pady=10)

        # --- RIGHT SIDE ---
        self.frame_detail = tk.Frame(self.split_view, bg="white")
        self.split_view.add(self.frame_detail, minsize=400)

        self.detail_container = tk.Frame(self.frame_detail, bg="white")
        self.detail_container.pack(fill="both", expand=True, padx=40, pady=40)

        lbl_intro = tk.Label(
            self.detail_container,
            text="Select an item in the list to view details",
            bg="white",
            fg="gray",
            font=("Segoe UI", 14),
        )
        lbl_intro.pack(expand=True)

        self.update_list()

    # ---------------------------------------------------------
    # LOGIN LOGIC
    # ---------------------------------------------------------
    def show_login_screen(self):
        """Simple window asking who you are."""
        login_win = tk.Toplevel(self.root)
        login_win.title("Log in")
        login_win.geometry("300x200")
        login_win.resizable(False, False)

        # Make window modal (must be answered)
        login_win.grab_set()

        tk.Label(login_win, text="Choose profile", font=("Arial", 14, "bold")).pack(
            pady=20
        )

        result = tk.BooleanVar(value=False)  # Tracks if login was OK

        def choose_admin():
            # Optional: add real password check here
            password = simpledialog.askstring(
                "Password",
                "Enter admin password (hint: 1234)",
                parent=login_win,
            )
            if password == "1234":
                self.is_admin = True
                result.set(True)
                login_win.destroy()
            elif password is not None:
                messagebox.showerror("Error", "Wrong password!")

        def choose_user():
            self.is_admin = False
            result.set(True)
            login_win.destroy()

        tk.Button(
            login_win,
            text="Store worker (Regular)",
            command=choose_user,
            height=2,
            width=25,
        ).pack(pady=5)
        tk.Button(
            login_win,
            text="Administrator (Full access)",
            command=choose_admin,
            height=2,
            width=25,
        ).pack(pady=5)

        # Wait until window is closed
        self.root.wait_window(login_win)
        return result.get()

    # ---------------------------------------------------------
    # MAIN APP LOGIC
    # ---------------------------------------------------------
    def run_auto_search(self, *args):
        query = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)

        results = search_item(query)
        for item in results:
            self.tree.insert(
                "",
                "end",
                iid=str(item["id"]),
                values=(
                    item["id"],
                    item["name"],
                    item["quantity"],
                    item.get("shelf", ""),  # Shelf or empty string if missing
                ),
            )

    def update_list(self):
        self.run_auto_search()

    def show_details(self, event):
        # Ensure we have a variable for save messages
        if not hasattr(self, "save_message"):
            self.save_message = ""

        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected)
        try:
            selected_id_from_list = int(item["values"][0])
        except ValueError:
            return

        all_items = get_inventory()
        item_obj = next(
            (v for v in all_items if v["id"] == selected_id_from_list), None
        )
        if not item_obj:
            return

        # Clear right side
        for widget in self.detail_container.winfo_children():
            widget.destroy()

        # --- VARIABLES ---
        original_id = item_obj["id"]
        var_name = tk.StringVar(value=item_obj["name"])
        var_id = tk.StringVar(value=str(item_obj["id"]))
        var_shelf = tk.StringVar(value=item_obj.get("shelf", "-"))

        # --- NAME ---
        if self.is_admin:
            tk.Label(
                self.detail_container,
                text="Item name:",
                bg="white",
                fg="gray",
            ).pack(anchor="w")
            ent_name = tk.Entry(
                self.detail_container,
                textvariable=var_name,
                font=("Segoe UI", 18, "bold"),
                bg="#ffffe0",
                relief="solid",
            )
            ent_name.pack(anchor="w", fill="x", pady=(0, 20))
        else:
            lbl_title = tk.Label(
                self.detail_container,
                text=item_obj["name"],
                bg="white",
                font=("Segoe UI", 24, "bold"),
            )
            lbl_title.pack(anchor="w", pady=(0, 20))

        # --- INFO TABLE ---
        info_frame = tk.Frame(self.detail_container, bg="white")
        info_frame.pack(fill="x", pady=10)

        # ID
        tk.Label(info_frame, text="ID:", bg="white", fg="gray").grid(
            row=0, column=0, sticky="w"
        )
        if self.is_admin:
            tk.Entry(
                info_frame,
                textvariable=var_id,
                width=10,
                bg="#ffffe0",
            ).grid(row=1, column=0, sticky="w", padx=(0, 30))
        else:
            tk.Label(
                info_frame,
                text=str(item_obj["id"]),
                bg="white",
                font=("Segoe UI", 12),
            ).grid(row=1, column=0, sticky="w", padx=(0, 30))

        # Location
        tk.Label(info_frame, text="LOCATION:", bg="white", fg="gray").grid(
            row=0, column=1, sticky="w"
        )
        if self.is_admin:
            tk.Entry(
                info_frame,
                textvariable=var_shelf,
                width=15,
                bg="#ffffe0",
            ).grid(row=1, column=1, sticky="w")
        else:
            tk.Label(
                info_frame,
                text=var_shelf.get(),
                bg="white",
                font=("Segoe UI", 12),
            ).grid(row=1, column=1, sticky="w")

        # --- SAVE BUTTON AND STATUS (Admin only) ---
        if self.is_admin:
            lbl_status = tk.Label(
                info_frame,
                text="",
                bg="white",
                font=("Segoe UI", 9, "bold"),
            )
            lbl_status.grid(row=3, column=0, columnspan=2, sticky="w")

            if self.save_message:
                lbl_status.config(text=self.save_message, fg="green")
                self.save_message = ""

                def clear_text():
                    try:
                        lbl_status.config(text="")
                    except tk.TclError:
                        pass

                self.root.after(3000, clear_text)

            def save_changes():
                try:
                    new_id_int = int(var_id.get())
                except ValueError:
                    lbl_status.config(text="ID must be a number!", fg="red")
                    return

                success = update_item(
                    old_id=original_id,
                    new_id=new_id_int,
                    new_name=var_name.get(),
                    new_quantity=item_obj["quantity"],
                    new_shelf=var_shelf.get(),
                )

                if success:
                    self.save_message = "Changes saved"
                    self.update_list()

                    if original_id == new_id_int:
                        try:
                            self.tree.selection_set(str(new_id_int))
                        except Exception:
                            pass
                else:
                    lbl_status.config(
                        text="Could not save (ID already in use?)", fg="red"
                    )

            btn_save = tk.Button(
                info_frame,
                text="SAVE CHANGES",
                command=save_changes,
                bg="#4CAF50",
                fg="white",
                font=("Segoe UI", 10, "bold"),
            )
            btn_save.grid(row=2, column=0, columnspan=2, sticky="w", pady=(15, 5))

        # --- STOCK (only once) ---
        tk.Frame(self.detail_container, height=2, bg="#f0f0f0").pack(
            fill="x", pady=20
        )
        tk.Label(
            self.detail_container,
            text="STOCK",
            bg="white",
            fg="gray",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")

        stock_frame = tk.Frame(self.detail_container, bg="white")
        stock_frame.pack(pady=10, anchor="w")

        tk.Button(
            stock_frame,
            text="-",
            font=("Arial", 20),
            width=3,
            bg="#ffcccc",
            relief="flat",
            command=lambda: self.change_quantity(item_obj["id"], -1),
        ).pack(side="left", padx=10)

        tk.Label(
            stock_frame,
            text=str(item_obj["quantity"]),
            font=("Segoe UI", 40),
            bg="white",
            width=4,
        ).pack(side="left", padx=10)

        tk.Button(
            stock_frame,
            text="+",
            font=("Arial", 20),
            width=3,
            bg="#ccffcc",
            relief="flat",
            command=lambda: self.change_quantity(item_obj["id"], 1),
        ).pack(side="left", padx=10)

        # Manual change
        manual_frame = tk.Frame(self.detail_container, bg="white")
        manual_frame.pack(anchor="w", pady=10)
        var_manual = tk.IntVar(value=0)
        ttk.Entry(manual_frame, textvariable=var_manual, width=8).pack(side="left")

        def manual_change(direction):
            try:
                amount = var_manual.get()
                if amount > 0:
                    self.change_quantity(item_obj["id"], amount * direction)
            except Exception:
                pass

        tk.Button(
            manual_frame,
            text="WITHDRAW",
            bg="#ffcccc",
            command=lambda: manual_change(-1),
        ).pack(side="left", padx=5)
        tk.Button(
            manual_frame,
            text="RESTOCK",
            bg="#ccffcc",
            command=lambda: manual_change(1),
        ).pack(side="left", padx=5)

    def change_quantity(self, item_id, delta):
        change_stock(item_id, delta)
        self.update_list()
        try:
            self.tree.selection_set(str(item_id))
            self.show_details(None)
        except tk.TclError:
            pass

    def show_new_item_form(self):
        # Double-check in case someone tampers with the GUI
        if not self.is_admin:
            messagebox.showerror("Denied", "You do not have access.")
            return

        for widget in self.detail_container.winfo_children():
            widget.destroy()

        tk.Label(
            self.detail_container,
            text="Register New Item",
            bg="white",
            font=("Segoe UI", 20),
        ).pack(pady=20)
        form_frame = tk.Frame(self.detail_container, bg="white")
        form_frame.pack()

        def make_row(text, row):
            tk.Label(
                form_frame,
                text=text,
                bg="white",
                font=("Segoe UI", 10),
            ).grid(row=row, column=0, sticky="w", pady=10)
            e = ttk.Entry(form_frame, width=30)
            e.grid(row=row, column=1, padx=10, pady=10)
            return e

        e_name = make_row("Name:", 0)
        e_id = make_row("ID (Number):", 1)
        e_quantity = make_row("Initial stock:", 2)
        e_shelf = make_row("Shelf:", 3)

        def save():
            try:
                new_item(
                    e_name.get(),
                    int(e_id.get()),
                    int(e_quantity.get()),
                    e_shelf.get(),
                )
                messagebox.showinfo("Success", "Item created!")
                self.update_list()
                e_name.delete(0, "end")
                e_id.delete(0, "end")
            except ValueError:
                messagebox.showerror("Error", "ID and Quantity must be numbers.")

        ttk.Button(form_frame, text="SAVE ITEM", command=save).grid(
            row=4, column=1, sticky="e", pady=20
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
